"""
sheets_to_creators.py

Google Sheets (구글폼 응답 시트)에서 크리에이터 데이터를 읽어
figma_create_variations.js의 CREATORS 배열을 자동 생성한다.

사용법:
  python3 scripts/sheets_to_creators.py
  → CREATORS 배열을 출력 (콘솔), 클립보드에도 복사

필요:
  pip install gspread google-auth pyperclip

시트 형식 (구글폼 응답 예시):
  A: 타임스탬프
  B: 닉네임
  C: 프로필 사진 URL  (또는 Google Drive 파일 ID)
  D: 상태 (완료/대기 등, 선택)
"""

import json
import sys
import os

# ─────────────────────────────────────────────
# 설정
# ─────────────────────────────────────────────
SHEET_ID = "YOUR_GOOGLE_SHEET_ID"   # ← 스프레드시트 ID로 교체
SHEET_NAME = "폼 응답 1"             # ← 시트 탭 이름으로 교체

NICKNAME_COL  = 1   # B열 (0-indexed: 1)
PHOTO_URL_COL = 2   # C열
STATUS_COL    = 3   # D열 (-1이면 상태 컬럼 없음)

# 상태 필터: None이면 전체, "완료" 이면 완료만
STATUS_FILTER = None

# 프로필 URL이 Google Drive 파일 ID인 경우 True
PHOTO_IS_DRIVE_ID = False

# Vercel 기준 프로필 경로 (PHOTO_IS_DRIVE_ID=False일 때 base URL)
PROFILE_BASE_URL = "https://mystore-mrt.vercel.app/assets/profiles"


def gdrive_url(file_id: str) -> str:
    return f"https://drive.google.com/uc?export=download&id={file_id}"


def get_creators():
    try:
        import gspread
        from google.oauth2.service_account import Credentials
    except ImportError:
        print("❌ 패키지 없음: pip install gspread google-auth")
        sys.exit(1)

    # 서비스 계정 키 파일 경로
    key_file = os.path.expanduser("~/.config/gcloud/mystore-service-account.json")
    if not os.path.exists(key_file):
        print(f"❌ 서비스 계정 키 없음: {key_file}")
        print("   GCP 콘솔 → IAM → 서비스 계정 → JSON 키 다운로드 후 위 경로에 저장")
        sys.exit(1)

    creds = Credentials.from_service_account_file(
        key_file,
        scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"],
    )
    gc = gspread.authorize(creds)
    sheet = gc.open_by_key(SHEET_ID).worksheet(SHEET_NAME)
    rows = sheet.get_all_values()[1:]  # 헤더 제외

    creators = []
    for row in rows:
        if len(row) <= NICKNAME_COL:
            continue
        nickname = row[NICKNAME_COL].strip()
        if not nickname:
            continue

        # 상태 필터
        if STATUS_FILTER and STATUS_COL >= 0 and len(row) > STATUS_COL:
            if row[STATUS_COL].strip() != STATUS_FILTER:
                continue

        # 프로필 URL
        if len(row) > PHOTO_URL_COL and row[PHOTO_URL_COL].strip():
            raw = row[PHOTO_URL_COL].strip()
            photo_url = gdrive_url(raw) if PHOTO_IS_DRIVE_ID else raw
        else:
            # 없으면 Vercel 로컬 경로 fallback
            photo_url = f"{PROFILE_BASE_URL}/{nickname}.jpg"

        creators.append({"nickname": nickname, "profileUrl": photo_url})

    return creators


def format_js_array(creators: list) -> str:
    lines = ["const CREATORS = ["]
    for c in creators:
        lines.append(f'  {{ nickname: "{c["nickname"]}", profileUrl: "{c["profileUrl"]}" }},')
    lines.append("];")
    return "\n".join(lines)


if __name__ == "__main__":
    creators = get_creators()
    js_array = format_js_array(creators)
    print(js_array)
    print(f"\n// 총 {len(creators)}명")

    # 클립보드 복사 (pyperclip 있을 때만)
    try:
        import pyperclip
        pyperclip.copy(js_array)
        print("// ✅ 클립보드에 복사됨")
    except ImportError:
        pass
