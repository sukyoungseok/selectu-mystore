import csv
import urllib.parse
import gspread

SHEET_KEY = '1XiTZD-ywUAgW-lJXFa0R0KoZMjW_m-2ytAhl7iwTbC8'
WORKSHEET_GID = 1133625298
BIO_CSV = '/Users/sukyoung-seok/mystore-mockup/bio_links_new.csv'

STRIP_PARAMS = {"utm_source", "utm_medium", "utm_content", "fbclid", "xmt"}

def clean_url(url):
    if not url:
        return ""
    parsed = urllib.parse.urlparse(url)
    qs = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
    clean_qs = {k: v for k, v in qs.items() if k not in STRIP_PARAMS}
    new_query = urllib.parse.urlencode(clean_qs, doseq=True)
    return urllib.parse.urlunparse(parsed._replace(query=new_query))

# CSV에서 바이오링크 로드
bio_links = {}
with open(BIO_CSV, encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        bio_links[row["id"]] = clean_url(row["bio_link"])

# 계산된 신규 인플루언서 데이터
new_data = {
    "holiday__zip":        {"name": "휴가집",   "followers": 1652,  "avg": None,   "ratio": None},
    "freehan_is":          {"name": "프리한",   "followers": 485,   "avg": None,   "ratio": None},
    "soodori_travel":      {"name": "수돌이",   "followers": 928,   "avg": None,   "ratio": None},
    "jinnie_j__":          {"name": "지니J",    "followers": 18,    "avg": None,   "ratio": None},
    "sing.______":         {"name": "씽아",     "followers": 85000, "avg": 580250, "ratio": "58.3%"},
    "jh__appy_":           {"name": "제삐",     "followers": 5474,  "avg": None,   "ratio": None},
    "life.traveler.jayna": {"name": "제이나",   "followers": 58000, "avg": 31700,  "ratio": "25.0%"},
    "itsotravel":          {"name": "여기잇쏘", "followers": 1078,  "avg": None,   "ratio": None},
    "busan_matna_":        {"name": "부산맛나", "followers": 10000, "avg": 238226, "ratio": "41.7%"},
    "ggami_travel":        {"name": "까미",     "followers": 1854,  "avg": None,   "ratio": None},
    "hyemingway0707":      {"name": "혜밍웨이", "followers": 25000, "avg": 256440, "ratio": "25.0%"},
    "tk__natasha":         {"name": "타샤",     "followers": 8448,  "avg": None,   "ratio": None},
    "tulney_":             {"name": "튤니",     "followers": 13000, "avg": 155808, "ratio": "16.7%"},
    "dorossi_life":        {"name": "도로씨",   "followers": 2135,  "avg": None,   "ratio": None},
    "choojangtrip":        {"name": "츄장",     "followers": 1419,  "avg": None,   "ratio": None},
    "seoli_o3o":           {"name": "설이",     "followers": 5402,  "avg": None,   "ratio": None},
    "uely_":               {"name": "유블리",   "followers": 11000, "avg": 198902, "ratio": "33.3%"},
    "undefined_uhfc":      {"name": "킥애스",   "followers": None,  "avg": None,   "ratio": None},
    # urang.trip → 바이오링크 없음, 팔로워 N/A → 스킵
}

# 바이오링크 병합
for uid in new_data:
    new_data[uid]["bio_link"] = bio_links.get(uid, "")

print("🔗 바이오링크 정리 완료:")
for uid, d in new_data.items():
    print(f"  {uid}: {d['bio_link'] or '없음'}")

gc = gspread.oauth()
spreadsheet = gc.open_by_key(SHEET_KEY)
ws = spreadsheet.get_worksheet_by_id(WORKSHEET_GID)

# 헤더 확인
headers = ws.row_values(1)
print("📋 헤더:", headers)
print(f"총 {len(headers)}개 컬럼\n")

# 컬럼 인덱스 찾기 (1-based)
def find_col(keyword):
    for i, h in enumerate(headers):
        if keyword in h:
            return i + 1  # gspread는 1-based
    return None

col_id       = find_col("인스타") or find_col("ID") or find_col("계정") or 3
col_name     = find_col("닉네임") or find_col("이름") or 6
col_followers= find_col("팔로워") or 7
col_avg      = find_col("평균") or find_col("조회") or 8
col_ratio    = find_col("비율") or find_col("5만") or 9
col_bio      = find_col("프로필 링크") or find_col("프로필링크") or find_col("바이오") or 10

print(f"ID 컬럼: {col_id} ({headers[col_id-1] if col_id <= len(headers) else '?'})")
print(f"닉네임 컬럼: {col_name}")
print(f"팔로워 컬럼: {col_followers}")
print(f"평균조회수 컬럼: {col_avg}")
print(f"5만+ 비율 컬럼: {col_ratio}")
print(f"바이오링크 컬럼: {col_bio}\n")

# 현재 ID 컬럼 전체 읽기
all_ids = ws.col_values(col_id)
updates = []
matched = []
not_found = []

for uid, d in new_data.items():
    found = False
    for i, cell_val in enumerate(all_ids):
        if cell_val.strip() == uid:
            row = i + 1
            found = True
            matched.append(uid)
            if d["name"]:
                updates.append({"range": f"{chr(64+col_name)}{row}",      "values": [[d["name"]]]})
            if d["followers"]:
                updates.append({"range": f"{chr(64+col_followers)}{row}", "values": [[d["followers"]]]})
            if d["avg"]:
                updates.append({"range": f"{chr(64+col_avg)}{row}",       "values": [[d["avg"]]]})
            if d["ratio"]:
                updates.append({"range": f"{chr(64+col_ratio)}{row}",     "values": [[d["ratio"]]]})
            if d.get("bio_link"):
                updates.append({"range": f"{chr(64+col_bio)}{row}",       "values": [[d["bio_link"]]]})
            break
    if not found:
        not_found.append(uid)

if updates:
    ws.batch_update(updates)
    print(f"✅ 업데이트 완료! {len(updates)}개 셀 수정")
    print(f"   매칭된 계정 ({len(matched)}개): {matched}")
else:
    print("⚠️  업데이트할 내용 없음")

if not_found:
    print(f"\n⚠️  시트에서 못 찾은 계정 ({len(not_found)}개): {not_found}")
    print("   → 해당 계정은 시트에 행이 없어서 스킵됨")
