import csv
import gspread

SHEET_KEY = '1XiTZD-ywUAgW-lJXFa0R0KoZMjW_m-2ytAhl7iwTbC8'
BIO_CSV = '/Users/sukyoung-seok/mystore-mockup/bio_links_new.csv'

# 바이오링크 로드
bio_links = {}
with open(BIO_CSV, encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        bio_links[row['id']] = row['bio_link'].split('?')[0]  # 트래킹 파라미터 제거

# 인스타 탭핑 데이터
insta_tapping = [
    # [아이디, 크리에이터명, 팔로워, 평균조회수, 5만+비율]
    ["holiday__zip",        "휴가집",   1652,  "",      ""],
    ["freehan_is",          "프리한",   485,   "",      ""],
    ["soodori_travel",      "수돌이",   928,   "",      ""],
    ["jinnie_j__",          "지니J",    18,    "",      ""],
    ["sing.______",         "씽아",     85000, 580250,  "58.3%"],
    ["jh__appy_",           "제삐",     5474,  "",      ""],
    ["life.traveler.jayna", "제이나",   58000, 31700,   "25.0%"],
    ["itsotravel",          "여기잇쏘", 1078,  "",      ""],
    ["busan_matna_",        "부산맛나", 10000, 238226,  "41.7%"],
    ["ggami_travel",        "까미",     1854,  "",      ""],
    ["hyemingway0707",      "혜밍웨이", 25000, 256440,  "25.0%"],
    ["tk__natasha",         "타샤",     8448,  "",      ""],
    ["tulney_",             "튤니",     13000, 155808,  "16.7%"],
    ["dorossi_life",        "도로씨",   2135,  "",      ""],
    ["urang.trip",          "",         "",    "",      ""],
    ["choojangtrip",        "츄장",     1419,  "",      ""],
    ["seoli_o3o",           "설이",     5402,  "",      ""],
    ["uely_",               "유블리",   11000, 198902,  "33.3%"],
    ["undefined_uhfc",      "킥애스",   "",    "",      ""],
]

# 유튜브 탭핑 데이터
youtube_tapping = [
    # [아이디, 채널명, 구독자, 평균조회수, 유튜브URL]
    ["mingoose_world", "밍구스월드",    9650,  32175, "https://www.youtube.com/@mingoose_world"],
    ["seulsup_",       "슬숲",         4220,  7515,  "https://www.youtube.com/@seulsup_"],
    ["zoey._.vely",    "별별리뷰",     20100, 28820, "https://www.youtube.com/@review__channel"],
    ["Blossooo",       "연차여행연구소", 38,   851,   "https://www.youtube.com/@연차여행연구소"],
    ["@uzique_.",      "유지크",       3090,  3693,  "https://www.youtube.com/@uzique"],
    ["@골때리는",       "골때리는여행",  733,   2001,  "https://www.youtube.com/@골때리는"],
]

gc = gspread.oauth()
spreadsheet = gc.open_by_key(SHEET_KEY)

# 탭 이미 있으면 삭제 후 재생성
existing = [ws.title for ws in spreadsheet.worksheets()]
if '탭핑 현황' in existing:
    spreadsheet.del_worksheet(spreadsheet.worksheet('탭핑 현황'))
    print("기존 '탭핑 현황' 탭 삭제")

ws = spreadsheet.add_worksheet(title='탭핑 현황', rows=60, cols=10)
print("✅ '탭핑 현황' 탭 생성")

# 헤더
headers = [
    '채널유형', '아이디', '크리에이터명',
    '팔로워/구독자', '평균조회수', '5만+비율',
    '프로필링크', '컨택상태', '우선순위', '메모'
]

rows = [headers]

# 인스타 섹션
rows.append(['[인스타 탭핑]', '', '', '', '', '', '', '', '', ''])
for d in insta_tapping:
    uid = d[0]
    link = bio_links.get(uid, '')
    rows.append([
        '인스타',
        uid,
        d[1],       # 크리에이터명
        d[2],       # 팔로워
        d[3],       # 평균조회수
        d[4],       # 5만+비율
        link,       # 프로필링크
        '미컨택',   # 컨택상태
        '',         # 우선순위
        '',         # 메모
    ])

# 유튜브 섹션
rows.append(['[유튜브 탭핑]', '', '', '', '', '', '', '', '', ''])
for d in youtube_tapping:
    rows.append([
        '유튜브',
        d[0],   # 아이디
        d[1],   # 채널명
        d[2],   # 구독자
        d[3],   # 평균조회수
        '-',    # 5만+비율 (유튜브 해당없음)
        d[4],   # 유튜브 URL
        '미컨택',
        '',
        '',
    ])

ws.update('A1', rows)

# 헤더 볼드 처리
ws.format('A1:J1', {
    'textFormat': {'bold': True},
    'backgroundColor': {'red': 0.2, 'green': 0.2, 'blue': 0.2},
    'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}},
})

# 섹션 구분 행 색상
ws.format('A2:J2', {'backgroundColor': {'red': 0.9, 'green': 0.95, 'blue': 1.0}})
ws.format(f'A{2+len(insta_tapping)+1}:J{2+len(insta_tapping)+1}',
          {'backgroundColor': {'red': 1.0, 'green': 0.95, 'blue': 0.9}})

print(f"✅ 데이터 입력 완료!")
print(f"   인스타 탭핑: {len(insta_tapping)}개")
print(f"   유튜브 탭핑: {len(youtube_tapping)}개")
print(f"   총 {len(insta_tapping)+len(youtube_tapping)}개 행")
