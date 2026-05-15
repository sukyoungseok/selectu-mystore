import gspread

SHEET_KEY = '1XiTZD-ywUAgW-lJXFa0R0KoZMjW_m-2ytAhl7iwTbC8'
WORKSHEET_GID = 1133625298

# YouTube MCP로 수집한 채널 분석 데이터
# 폼에서 입력한 ID → 채널 정보
youtube_data = {
    "mingoose_world": {
        "name": "밍구스월드",
        "subscribers": 9650,
        "avg_views": 32175,   # 총조회수 7,496,619 / 영상수 233
        "ratio": "-",         # 유튜브 (릴스 비율 해당없음)
        "profile_link": "https://www.youtube.com/@mingoose_world",
    },
    "seulsup_": {
        "name": "슬숲",
        "subscribers": 4220,
        "avg_views": 7515,    # 526,040 / 70
        "ratio": "-",
        "profile_link": "https://www.youtube.com/@seulsup_",
    },
    "zoey._.vely": {
        "name": "별별리뷰",
        "subscribers": 20100,
        "avg_views": 28820,   # 14,236,981 / 494
        "ratio": "-",
        "profile_link": "https://www.youtube.com/@review__channel",
    },
    "Blossooo": {
        "name": "연차여행연구소",
        "subscribers": 38,
        "avg_views": 851,     # 12,765 / 15
        "ratio": "-",
        "profile_link": "https://www.youtube.com/@연차여행연구소",
    },
    "@uzique_.": {
        "name": "유지크",
        "subscribers": 3090,
        "avg_views": 3693,    # 1,026,525 / 278
        "ratio": "-",
        "profile_link": "https://www.youtube.com/@uzique",
    },
    "@골때리는": {
        "name": "골때리는여행",
        "subscribers": 733,
        "avg_views": 2001,    # 456,337 / 228
        "ratio": "-",
        "profile_link": "https://www.youtube.com/@골때리는",
    },
}

gc = gspread.oauth()
ws = gc.open_by_key(SHEET_KEY).get_worksheet_by_id(WORKSHEET_GID)

headers = ws.row_values(1)

def find_col(keyword):
    for i, h in enumerate(headers):
        if keyword in h:
            return i + 1
    return None

col_id       = find_col("인스타") or find_col("ID") or find_col("계정") or 3
col_name     = find_col("크리에이터") or find_col("닉네임") or find_col("이름") or 6
col_subs     = find_col("팔로워") or 7
col_avg      = find_col("평균") or find_col("조회") or 8
col_ratio    = find_col("비율") or find_col("5만") or 9
col_bio      = find_col("프로필 링크") or find_col("프로필링크") or 10

print(f"📋 컬럼 구조 확인")
print(f"  ID: {col_id} | 이름: {col_name} | 구독자: {col_subs} | 평균조회수: {col_avg} | 비율: {col_ratio} | 링크: {col_bio}\n")

all_ids = ws.col_values(col_id)
updates = []
matched = []
not_found = []

for uid, d in youtube_data.items():
    found = False
    for i, cell_val in enumerate(all_ids):
        if cell_val.strip() == uid:
            row = i + 1
            found = True
            matched.append(uid)
            updates.append({"range": f"{chr(64+col_name)}{row}",  "values": [[d["name"]]]})
            updates.append({"range": f"{chr(64+col_subs)}{row}",  "values": [[d["subscribers"]]]})
            updates.append({"range": f"{chr(64+col_avg)}{row}",   "values": [[d["avg_views"]]]})
            updates.append({"range": f"{chr(64+col_ratio)}{row}", "values": [[d["ratio"]]]})
            updates.append({"range": f"{chr(64+col_bio)}{row}",   "values": [[d["profile_link"]]]})
            break
    if not found:
        not_found.append(uid)

if updates:
    ws.batch_update(updates)
    print(f"✅ 완료! {len(updates)}개 셀 업데이트")
    print(f"   매칭 ({len(matched)}개): {matched}")
else:
    print("⚠️  업데이트할 내용 없음")

if not_found:
    print(f"\n⚠️  시트에서 못 찾은 ID ({len(not_found)}개): {not_found}")
    print("   → 시트의 C열 값과 다를 수 있음 (대소문자, @기호 등 확인)")
