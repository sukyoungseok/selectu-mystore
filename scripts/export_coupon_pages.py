"""
export_coupon_pages.py

쿠폰페이지 베리에이션 — 크리에이터별 7개 프레임을 3배율 JPG로 내보낸다.

파일 구조에서 크리에이터 세트를 자동 탐색한다:
  최상위 프레임 중 "마스터세트", "템플릿 원본" 을 제외한 프레임 = 크리에이터 세트
  그 안의 자식 프레임(MO-1 ... OG-tag) 7개를 내보냄

사용법:
  FIGMA_TOKEN=xxx python3 scripts/export_coupon_pages.py

토큰 발급:
  Figma → Settings → Security → Personal access tokens → Generate new token
  (scope 는 File content 읽기 권한이면 충분)

출력:
  쿠폰페이지 자동화/exports/{닉네임}/MO-1.jpg ... OG-tag.jpg

필요:
  pip install requests
"""

import os
import sys
import time
import unicodedata
from pathlib import Path

import requests

# ─────────────────────────────────────────────
# 설정
# ─────────────────────────────────────────────
FILE_KEY    = "HHHwWdq7CyVAiOlZ2oHEcq"          # 마케팅파트너 마이스토어 베리에이션
SKIP_FRAMES = {"마스터세트", "템플릿 원본"}        # 크리에이터 세트가 아닌 프레임
FORMAT      = "jpg"
SCALE       = 3
EXPORT_DIR  = Path(__file__).parent.parent / "쿠폰페이지 자동화" / "exports"
BASE        = "https://api.figma.com/v1"


def nfc(s: str) -> str:
    """유니코드 NFC 정규화 (macOS 파일명 NFD 대응)"""
    return unicodedata.normalize("NFC", s or "")


def get_token() -> str:
    """FIGMA_TOKEN 환경변수 우선, 없으면 ~/.config/figma/token 파일에서 읽음"""
    tok = os.environ.get("FIGMA_TOKEN", "").strip()
    if tok:
        return tok
    token_file = Path.home() / ".config" / "figma" / "token"
    if token_file.exists():
        return token_file.read_text(encoding="utf-8").strip()
    return ""


def headers() -> dict:
    tok = get_token()
    if not tok:
        print("❌ Figma 토큰이 없습니다.")
        print("   환경변수 FIGMA_TOKEN 또는 ~/.config/figma/token 파일에 저장하세요.")
        print("   토큰 발급: Figma → Settings → Security → Personal access tokens")
        sys.exit(1)
    return {"X-Figma-Token": tok}


def get_creator_frames():
    """파일 구조에서 [(닉네임, [(자식이름, id), ...]), ...] 수집"""
    r = requests.get(f"{BASE}/files/{FILE_KEY}?depth=3", headers=headers())
    r.raise_for_status()
    doc = r.json()["document"]

    sets = []
    for page in doc.get("children", []):
        for node in page.get("children", []):
            if node.get("type") != "FRAME":
                continue
            name = nfc(node["name"])
            if name in SKIP_FRAMES:
                continue
            children = [
                (nfc(c["name"]), c["id"])
                for c in node.get("children", [])
                if c.get("type") == "FRAME"
            ]
            if children:
                sets.append((name, children))
    return sets


def export_images(node_ids):
    """node id 목록 → {id: 렌더 URL}"""
    url_map = {}
    BATCH = 30
    for i in range(0, len(node_ids), BATCH):
        batch = node_ids[i:i + BATCH]
        r = requests.get(
            f"{BASE}/images/{FILE_KEY}",
            params={"ids": ",".join(batch), "format": FORMAT, "scale": SCALE},
            headers=headers(),
        )
        r.raise_for_status()
        data = r.json()
        if data.get("err"):
            print(f"⚠️  렌더 오류: {data['err']}")
        url_map.update(data.get("images", {}))
        if i + BATCH < len(node_ids):
            time.sleep(1)
    return url_map


def main():
    print("📄 파일 구조 조회 중...")
    sets = get_creator_frames()
    if not sets:
        print("⚠️  크리에이터 세트를 찾지 못했습니다. (최상위 프레임 이름 확인)")
        return
    print(f"   → {len(sets)}세트: {', '.join(n for n, _ in sets)}")

    all_ids = [cid for _, children in sets for _, cid in children]
    print(f"🖼  {len(all_ids)}개 프레임 {SCALE}배율 {FORMAT.upper()} 렌더 요청 중...")
    url_map = export_images(all_ids)

    print(f"⬇️  저장 → {EXPORT_DIR}/")
    ok, fail = 0, 0
    for nickname, children in sets:
        for childname, cid in children:
            img_url = url_map.get(cid)
            dest = EXPORT_DIR / nickname / f"{childname}.{FORMAT}"
            if not img_url:
                print(f"  ⚠️  {nickname}/{childname} 렌더 URL 없음")
                fail += 1
                continue
            ir = requests.get(img_url)
            ir.raise_for_status()
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(ir.content)
            print(f"  ✅ {nickname}/{childname}.{FORMAT}")
            ok += 1

    print(f"\n🎉 완료 — 성공 {ok} / 실패 {fail}")
    print(f"   {EXPORT_DIR}")


if __name__ == "__main__":
    main()
