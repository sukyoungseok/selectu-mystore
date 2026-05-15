import gspread

SHEET_KEY = '1XiTZD-ywUAgW-lJXFa0R0KoZMjW_m-2ytAhl7iwTbC8'

# 위키 페이지 기준 유튜버 목록 (구독자 수 YouTube API 실측값)
# [채널명, 채널URL, 구독자, 대상콘텐츠URL, 조회수, 여행지, MRT연관]
youtube_contacts = [
    ["하미마미",   "https://www.youtube.com/@hamimommy",  2790000, "https://www.youtube.com/watch?v=8ugF5pZClYw",   323740, "LA",             "✅ 갈렙투어 언급"],
    ["파파트래블", "https://www.youtube.com/@파파트래블",  368000, "https://www.youtube.com/watch?v=qzCBqrv9ojE",   280000, "일본",           "❌"],
    ["아재여행",   "https://www.youtube.com/@ajaetravel",  256000, "https://www.youtube.com/watch?v=IVJO6FNhF1k",   147107, "스페인·포르투갈","❌"],
    ["수코",       "https://www.youtube.com/@sookohaseyo", 206000, "https://www.youtube.com/watch?v=oTiR5EQ6ekM",   470000, "홍콩",           "❌"],
    ["돈캣PL·EX", "https://www.youtube.com/@doncatplex",  184000, "https://www.youtube.com/watch?v=KOvnAEts7A8", 1129714, "오사카(USJ)",    "❌"],
    ["나나제인",   "https://www.youtube.com/@nanajane",    152000, "https://www.youtube.com/watch?v=rUgDThvioJo",    38179, "상하이",         "✅ 직접 언급"],
    ["살란다",     "https://www.youtube.com/@살란다",      110000, "https://www.youtube.com/watch?v=7c5cThEY5mw",   785785, "오사카",         "❌"],
    ["산보노트",   "https://www.youtube.com/@sanbonote",   98600, "https://www.youtube.com/watch?v=grM-GAjIXYg",    75948, "타이베이",       "✅ 파트너스 활성화"],
    ["히제이HEEJ", "https://www.youtube.com/@heej",        64500, "https://www.youtube.com/watch?v=8AKLbMhAPGI",    46735, "미야자키",       "❌"],
    ["나드리",     "https://www.youtube.com/@나-드리",       7340, "https://www.youtube.com/watch?v=5qY9eX3ZY_8",   477244, "도쿄",           "❌"],
]

# 위키 페이지 기준 인스타그래머 목록
# [계정ID, 팔로워, 대상콘텐츠URL, 주요여행지, 컨택상태]
insta_contacts = [
    ["heeah_travel",   220000, "https://www.instagram.com/reel/DPqknVLEvTe/", "마카오",     ""],
    ["__ririmom",      123000, "https://www.instagram.com/reel/DK5t6Yazj-1/", "오키나와",   ""],
    ["ji_bbling",      102000, "https://www.instagram.com/reel/C8wxZ7xJP9K/", "런던",       ""],
    ["travel_dongri",   79000, "https://www.instagram.com/reel/DUNpFMqjysx/", "충칭",       ""],
    ["june_fairytale",  61000, "https://www.instagram.com/reel/DNAuebzziBo/", "시드니",     ""],
    ["leesutravel",     50000, "https://www.instagram.com/reel/DQ39AGfk2N4/", "대마도",     ""],
    ["gaule._.e",       30000, "https://www.instagram.com/p/DWgf743CRON/",    "치앙마이",   ""],
    ["da0_joy",         23000, "https://www.instagram.com/reel/C11nivpy13L/", "다낭",       ""],
    ["min_pic._",       20000, "https://www.instagram.com/reel/DGLG5Z5p6kv/", "이탈리아",  ""],
    ["ya._____.js",     17000, "https://www.instagram.com/reel/DV8S_WYkxDL/", "기타큐슈",  ""],
    ["홍다닥",              "", "",                                              "",           ""],
    ["주영",                "", "",                                              "",           ""],
    ["예슬리오",            "", "",                                              "",           ""],
    ["헨리",                "", "",                                              "",           ""],
]

gc = gspread.oauth()
spreadsheet = gc.open_by_key(SHEET_KEY)

# 탭 이미 있으면 삭제 후 재생성
existing = [ws.title for ws in spreadsheet.worksheets()]
if '컨택 현황' in existing:
    spreadsheet.del_worksheet(spreadsheet.worksheet('컨택 현황'))
    print("기존 '컨택 현황' 탭 삭제")

ws = spreadsheet.add_worksheet(title='컨택 현황', rows=80, cols=11)
print("✅ '컨택 현황' 탭 생성")

headers = [
    '유형', '채널/계정ID', '채널명', '팔로워/구독자',
    '대상 콘텐츠', '영상조회수', '주요여행지',
    'MRT연관', '목업페이지', '컨택상태', '메모'
]

rows = [headers]

# 유튜브 섹션
rows.append(['[유튜브 컨택 대상]', '', '', '', '', '', '', '', '', '', ''])
for d in youtube_contacts:
    rows.append([
        '유튜브',
        d[1],        # 채널URL
        d[0],        # 채널명
        d[2],        # 구독자 수
        d[3],        # 대상 콘텐츠 URL
        d[4],        # 조회수
        d[5],        # 여행지
        d[6],        # MRT연관
        '',          # 목업페이지
        '미컨택',
        '',
    ])

# 인스타 섹션
rows.append(['[인스타 컨택 대상]', '', '', '', '', '', '', '', '', '', ''])
for d in insta_contacts:
    rows.append([
        '인스타',
        d[0],        # 계정ID
        '',          # 채널명 (닉네임, 추후 입력)
        d[1] if d[1] else '',  # 팔로워
        d[2],        # 대상 콘텐츠 URL
        '-',         # 영상조회수 (인스타는 해당없음)
        d[3],        # 여행지
        '-',         # MRT연관
        '',          # 목업페이지
        d[4] if d[4] else '미컨택',
        '',
    ])

ws.update('A1', rows)

# 헤더 스타일
ws.format('A1:K1', {
    'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}},
    'backgroundColor': {'red': 0.2, 'green': 0.2, 'blue': 0.2},
})

# 섹션 구분 행
youtube_section_row = 2
insta_section_row = 2 + len(youtube_contacts) + 1
ws.format(f'A{youtube_section_row}:K{youtube_section_row}',
          {'backgroundColor': {'red': 0.9, 'green': 0.95, 'blue': 1.0},
           'textFormat': {'bold': True}})
ws.format(f'A{insta_section_row}:K{insta_section_row}',
          {'backgroundColor': {'red': 1.0, 'green': 0.95, 'blue': 0.9},
           'textFormat': {'bold': True}})

print(f"✅ 데이터 입력 완료!")
print(f"   유튜브 컨택 대상: {len(youtube_contacts)}개")
print(f"   인스타 컨택 대상: {len(insta_contacts)}개")
print(f"   총 {len(youtube_contacts)+len(insta_contacts)}개")
