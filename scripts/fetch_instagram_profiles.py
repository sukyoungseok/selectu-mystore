"""
fetch_instagram_profiles.py

구글폼 응답 시트의 인스타그램 URL/핸들에서 크리에이터 프로필 사진을 긁어
assets/profiles/{닉네임}.jpg 로 저장한다.

저장된 파일은 Vercel 배포 후
  https://mystore-mrt.vercel.app/assets/profiles/{닉네임}.jpg
로 서빙되며, sheets_to_creators.py 의 PROFILE_BASE_URL fallback이 이 경로를
그대로 쓰기 때문에 별도 연결 작업 없이 figma_create_variations.js 까지 이어진다.

파이프라인 위치:
  [이 스크립트] 인스타 → assets/profiles/*.jpg
    → sheets_to_creators.py  (CREATORS 배열 생성, profileUrl = Vercel 경로)
    → figma_create_variations.js  (createImageAsync로 프로필 슬롯 교체)

사용법:
  # (1) 구글폼 응답 시트에서 읽기 — 운영 기본값
  python3 scripts/fetch_instagram_profiles.py

  # (2) 로컬 파일에서 읽기 — 시트 셋업 전 빠른 테스트용
  #     파일은 한 줄에 "닉네임,인스타URL" 형식 (# 으로 시작하는 줄은 주석)
  python3 scripts/fetch_instagram_profiles.py --file test_creators.txt

  # 공통 옵션
  python3 scripts/fetch_instagram_profiles.py --dry-run   # 다운로드 없이 URL만 확인

필요:
  pip install gspread google-auth requests   # --file 모드만 쓸 거면 requests 만 있어도 됨

시트 형식 (구글폼 응답 예시):
  A: 타임스탬프
  B: 닉네임
  C: 인스타그램 URL 또는 핸들 (@handle / instagram.com/handle / 직접 이미지 URL)
  D: 상태 (선택)

--file 형식 예시 (test_creators.txt):
  # 닉네임,인스타URL
  파덕츄,https://www.instagram.com/padduckchu/
  훵,@hwung_travel

주의 — 인스타그램 프로필 페이지는 로그인 월이 뜰 때가 있어 og:image 추출이
실패할 수 있다. 실패한 크리에이터는 마지막에 목록으로 출력되니 수동으로
assets/profiles/{닉네임}.jpg 를 채우면 된다.
"""

import argparse
import html
import os
import re
import sys
import time
from pathlib import Path

import requests

# ─────────────────────────────────────────────
# 설정 — sheets_to_creators.py 와 동일하게 맞춰둘 것
# ─────────────────────────────────────────────
SHEET_ID   = "YOUR_GOOGLE_SHEET_ID"   # ← 스프레드시트 ID로 교체
SHEET_NAME = "폼 응답 1"               # ← 시트 탭 이름으로 교체

NICKNAME_COL  = 1   # B열
INSTA_COL     = 2   # C열 (인스타 URL/핸들 또는 직접 이미지 URL)
STATUS_COL    = 3   # D열 (-1이면 상태 컬럼 없음)
STATUS_FILTER = None  # None이면 전체, "완료"면 완료만

PROFILE_DIR = Path(__file__).parent.parent / "assets" / "profiles"

# 인스타 OG 메타가 로그인 월에 막히지 않도록 봇 UA 사용 (이 레포 채널페이지 작업에서 검증된 방식)
BOT_UA = "Twitterbot/1.0"
# 실제 이미지 바이트를 받을 때 / web API 호출용 일반 브라우저 UA
DL_UA  = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36")
# 인스타 웹 클라이언트 공개 App ID — web_profile_info API 호출에 필요
IG_APP_ID = "936619743392459"

OG_IMAGE_RE = re.compile(
    r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']',
    re.IGNORECASE,
)


# ─────────────────────────────────────────────
# 시트 읽기
# ─────────────────────────────────────────────
def get_rows():
    try:
        import gspread
        from google.oauth2.service_account import Credentials
    except ImportError:
        print("❌ 패키지 없음: pip install gspread google-auth")
        sys.exit(1)

    key_file = os.path.expanduser("~/.config/gcloud/mystore-service-account.json")
    if not os.path.exists(key_file):
        print(f"❌ 서비스 계정 키 없음: {key_file}")
        print("   GCP 콘솔 → IAM → 서비스 계정 → JSON 키 다운로드 후 위 경로에 저장")
        sys.exit(1)

    creds = Credentials.from_service_account_file(
        key_file,
        scopes=["https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive"],
    )
    gc = gspread.authorize(creds)
    sheet = gc.open_by_key(SHEET_ID).worksheet(SHEET_NAME)
    return sheet.get_all_values()[1:]  # 헤더 제외


def parse_creators(rows):
    """시트 행 → [(닉네임, 인스타값), ...]"""
    creators = []
    for row in rows:
        if len(row) <= max(NICKNAME_COL, INSTA_COL):
            continue
        nickname = row[NICKNAME_COL].strip()
        insta    = row[INSTA_COL].strip()
        if not nickname or not insta:
            continue
        if STATUS_FILTER and STATUS_COL >= 0 and len(row) > STATUS_COL:
            if row[STATUS_COL].strip() != STATUS_FILTER:
                continue
        creators.append((nickname, insta))
    return creators


def load_from_file(path: str):
    """로컬 파일에서 [(닉네임, 인스타값), ...] 읽기. 한 줄에 '닉네임,인스타URL'."""
    p = Path(path)
    if not p.exists():
        print(f"❌ 파일 없음: {path}")
        sys.exit(1)
    creators = []
    for ln in p.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("#"):
            continue
        if "," not in ln:
            print(f"⚠️  형식 무시 (콤마 없음): {ln}")
            continue
        nickname, insta = ln.split(",", 1)
        nickname, insta = nickname.strip(), insta.strip()
        if nickname and insta:
            creators.append((nickname, insta))
    return creators


# ─────────────────────────────────────────────
# 인스타 → 프로필 이미지 URL
# ─────────────────────────────────────────────
def extract_handle(value: str) -> str:
    """@handle / instagram.com/handle / 전체 URL → 핸들 문자열"""
    v = value.strip()
    if v.startswith("@"):
        v = v[1:]
    if "instagram.com" in v:
        m = re.search(r"instagram\.com/([^/?#]+)", v)
        if m:
            v = m.group(1)
    return v.strip("/")


def from_web_profile_api(handle: str) -> str | None:
    """
    인스타 web_profile_info API → profile_pic_url_hd (320x320).
    og:image(100x100)보다 고해상도라 1순위로 시도. 실패 시 None.
    """
    try:
        r = requests.get(
            f"https://www.instagram.com/api/v1/users/web_profile_info/?username={handle}",
            headers={"User-Agent": DL_UA, "X-IG-App-ID": IG_APP_ID},
            timeout=15,
        )
        if r.status_code != 200:
            return None
        user = r.json().get("data", {}).get("user") or {}
        return user.get("profile_pic_url_hd") or user.get("profile_pic_url")
    except (requests.RequestException, ValueError):
        return None


def from_og_image(handle: str) -> str | None:
    """프로필 페이지 og:image(100x100) — web API가 막혔을 때의 fallback."""
    try:
        r = requests.get(
            f"https://www.instagram.com/{handle}/",
            headers={"User-Agent": BOT_UA}, timeout=15,
        )
        r.raise_for_status()
    except requests.RequestException:
        return None
    m = OG_IMAGE_RE.search(r.text)
    return html.unescape(m.group(1)) if m else None


def resolve_image_url(insta_value: str) -> tuple[str | None, str]:
    """
    insta_value → (이미지 URL, 출처라벨). 실패 시 (None, 사유).
    1순위: web_profile_info API (320x320)
    2순위: og:image 스크랩 (100x100)
    """
    # 이미 직접 이미지 URL인 경우
    if re.search(r"\.(jpg|jpeg|png|webp)(\?|$)", insta_value, re.IGNORECASE):
        return insta_value, "직접URL"

    handle = extract_handle(insta_value)

    url = from_web_profile_api(handle)
    if url:
        return url, "API 320px"

    url = from_og_image(handle)
    if url:
        return url, "og:image 100px"

    return None, "추출 실패 (로그인 월/비공개/핸들 오타 가능)"


# ─────────────────────────────────────────────
# 다운로드
# ─────────────────────────────────────────────
def download(img_url: str, dest: Path) -> bool:
    try:
        r = requests.get(img_url, headers={"User-Agent": DL_UA}, timeout=20)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"     └ 이미지 다운로드 실패: {e}")
        return False
    if not r.content or len(r.content) < 1024:
        print("     └ 이미지가 비었거나 너무 작음 (차단 가능성)")
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(r.content)
    return True


# ─────────────────────────────────────────────
# 메인
# ─────────────────────────────────────────────
def run(dry_run: bool, file_path: str | None, with_handle: bool):
    if file_path:
        creators = load_from_file(file_path)
    else:
        creators = parse_creators(get_rows())
    if not creators:
        print("⚠️  처리할 크리에이터가 없어요. 시트/컬럼 설정을 확인하세요.")
        return

    mode_label = " (파일명에 핸들 포함)" if with_handle else ""
    print(f"🔍 {len(creators)}명 프로필 사진 수집 시작{mode_label}\n")
    ok, failed = [], []

    for nickname, insta in creators:
        print(f"• {nickname}  ({insta})")
        img_url, source = resolve_image_url(insta)
        if not img_url:
            print(f"     └ ❌ {source}")
            failed.append(nickname)
            continue

        if dry_run:
            print(f"     └ (dry-run) [{source}] {img_url}")
            ok.append(nickname)
            continue

        # --with-handle: {닉네임}__{핸들}.jpg, 그 외: {닉네임}.jpg
        if with_handle:
            handle = extract_handle(insta)
            dest = PROFILE_DIR / f"{nickname}__{handle}.jpg"
        else:
            dest = PROFILE_DIR / f"{nickname}.jpg"

        if download(img_url, dest):
            print(f"     └ ✅ 저장: {dest.relative_to(PROFILE_DIR.parent.parent)}  [{source}]")
            ok.append(nickname)
        else:
            failed.append(nickname)

        time.sleep(1)  # rate limit 여유

    print(f"\n🎉 완료 — 성공 {len(ok)} / 실패 {len(failed)}")
    if failed:
        fmt = "{닉네임}__{핸들}.jpg" if with_handle else "{닉네임}.jpg"
        print(f"\n⚠️  아래 크리에이터는 수동으로 assets/profiles/{fmt} 를 채워주세요:")
        for n in failed:
            print(f"   - {n}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="다운로드 없이 추출되는 이미지 URL만 출력")
    ap.add_argument("--file", default=None,
                    help="시트 대신 로컬 파일에서 읽기 (한 줄에 '닉네임,인스타URL')")
    ap.add_argument("--with-handle", action="store_true",
                    help="저장 파일명에 인스타 핸들 포함 ({닉네임}__{핸들}.jpg) — 쿠폰페이지 자동화 플러그인용")
    args = ap.parse_args()
    run(args.dry_run, args.file, args.with_handle)
