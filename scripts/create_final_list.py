import gspread

SHEET_KEY = '1XiTZD-ywUAgW-lJXFa0R0KoZMjW_m-2ytAhl7iwTbC8'

# ────────────────────────────────────────────────────────────────
# 최종 진행 크리에이터 리스트
# 기준: 신청 현황 "우선 진행" + 컨택 현황 "컨택 완료"
# 컬럼: 채널유형, 아이디, 크리에이터명, 팔로워/구독자, 평균조회수,
#        5만+비율, 모집경로, 마케팅파트너ID, 마이스토어링크, 컨택상태, 메모
# ────────────────────────────────────────────────────────────────

# ── 인스타 (신청 현황 우선 진행) ─────────────────────────────────
insta_form = [
    # [아이디, 크리에이터명, 팔로워, 평균조회수, 5만+비율, 마케팅파트너ID, 메모]
    ["travel_baek",        "백자매",     146000, 562333, "77.8%", "127477", "누적 릴스 조회수 1.6억+ 메가 크리에이터"],
    ["sing.______",        "씽아",        85000, 580250, "58.3%", "139085", ""],
    ["daero._.nana",       "대로와나나",   86000,  42667, "11.1%", "105524", "MRT 공식 파트너 여행 전문가"],
    ["today.brighten",     "늘찬맘",       60000,  10898,  "0.0%", "137783", "아이와 다낭·베트남 가족 여행"],
    ["life.traveler.jayna","제이나",        58000,  31700, "25.0%", "103270", ""],
    ["hwung_travel",       "훵",           30000, 106404, "44.4%", "104720", "나고야·일본 근교 여행"],
    ["hyemingway0707",     "혜밍웨이",     25000, 256440, "25.0%", "",       ""],
    ["uely_",              "유블리",       11000, 198902, "33.3%", "107232", ""],
    ["busan_matna_",       "부산맛나",     10000, 238226, "41.7%", "132437", ""],
]

# ── 인스타 (컨택 현황 컨택 완료 - 탭핑) ──────────────────────────
insta_tapping = [
    # [아이디, 크리에이터명, 팔로워, 평균조회수, 5만+비율, 마케팅파트너ID, 메모]
    ["hongdadak",      "홍다닥",    104000, 1375416, "41.7%", "", "맛집·여행 트래블로그, 릴스 최고 1348만뷰"],
    ["jae9un.jpg",     "재구언",     28000,  143916, "66.7%", "", "테마파크 인플루언서, 5만+비율 66.7%"],
    ["min_pic._",      "민픽._",     21000,  276078, "33.3%", "", "205일 유럽 장기여행, 릴스 최고 132만뷰"],
    ["henriuniverse",  "헨리",       15000,  246500, "66.7%", "", "5만+비율 66.7%, 릴스 최고 160만뷰"],
    ["juuuyomi_",      "주영이랑",   14000,   73945, "41.7%", "", ""],
    ["yeseulio",       "예슬리오",    4004,       "", "",      "", "일반채널, 조회수 데이터 없음"],
]

# ── 유튜브 (신청 현황 우선 진행) ─────────────────────────────────
youtube_form = [
    # [아이디, 크리에이터명, 구독자, 평균조회수, 마케팅파트너ID, 채널URL, 메모]
    ["zoey._.vely",    "별별리뷰",   20100, 28820, "",       "https://www.youtube.com/@review__channel", "다낭·호이안 당일치기 여행"],
    ["mingoose_world", "밍구스월드",  9650, 32175, "103060", "https://www.youtube.com/@mingoose_world",  "발리 한달살기 전문"],
    ["seulsup_",       "슬숲",        4220,  7515, "",       "https://www.youtube.com/@seulsup_",        "발리 우붓 여행 브이로그"],
]

# ── 유튜브 (컨택 현황 컨택 완료 - 탭핑) ──────────────────────────
youtube_tapping = [
    # [아이디, 크리에이터명, 구독자, 평균조회수, 마케팅파트너ID, 채널URL, 메모]
    ["파파트래블", "파파트래블", 368000, 280000, "", "https://www.youtube.com/@파파트래블", "컨택 완료, 관련 영상 3개 공유"],
]

# ────────────────────────────────────────────────────────────────

gc = gspread.oauth()
spreadsheet = gc.open_by_key(SHEET_KEY)

existing = [ws.title for ws in spreadsheet.worksheets()]
if '최종 리스트' in existing:
    spreadsheet.del_worksheet(spreadsheet.worksheet('최종 리스트'))
    print("기존 '최종 리스트' 탭 삭제")

ws = spreadsheet.add_worksheet(title='최종 리스트', rows=60, cols=11)
print("✅ '최종 리스트' 탭 생성")

headers = [
    '채널유형', '아이디', '크리에이터명', '팔로워/구독자', '평균조회수',
    '5만+비율', '모집경로', '마케팅파트너ID', '마이스토어링크', '컨택상태', '메모'
]

rows = [headers]

# ── 인스타 섹션 ──
rows.append(['[인스타그램]', '', '', '', '', '', '', '', '', '', ''])

for d in insta_form:
    rows.append([
        '인스타', d[0], d[1], d[2], d[3], d[4],
        '구글폼', d[5], '', '진행 확정', d[6]
    ])

for d in insta_tapping:
    rows.append([
        '인스타', d[0], d[1],
        d[2] if d[2] else '', d[3] if d[3] else '',
        d[4], '인스타탭핑', d[5], '', '컨택 완료', d[6]
    ])

# ── 유튜브 섹션 ──
rows.append(['[유튜브]', '', '', '', '', '', '', '', '', '', ''])

for d in youtube_form:
    rows.append([
        '유튜브', d[0], d[1], d[2], d[3], '-',
        '구글폼', d[4], d[5], '진행 확정', d[6]
    ])

for d in youtube_tapping:
    rows.append([
        '유튜브', d[0], d[1], d[2], d[3], '-',
        '유튜브탭핑', d[4], d[5], '컨택 완료', d[6]
    ])

ws.update('A1', rows)

# 헤더 스타일
ws.format('A1:K1', {
    'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}},
    'backgroundColor': {'red': 0.13, 'green': 0.13, 'blue': 0.13},
})

# 섹션 구분 행
insta_section_row = 2
youtube_section_row = 2 + len(insta_form) + len(insta_tapping) + 1

ws.format(f'A{insta_section_row}:K{insta_section_row}', {
    'backgroundColor': {'red': 0.88, 'green': 0.93, 'blue': 1.0},
    'textFormat': {'bold': True},
})
ws.format(f'A{youtube_section_row}:K{youtube_section_row}', {
    'backgroundColor': {'red': 1.0, 'green': 0.93, 'blue': 0.87},
    'textFormat': {'bold': True},
})

# 진행 확정 행 연두색
all_rows = ws.get_all_values()
green_ranges = []
for i, row in enumerate(all_rows[2:], start=3):
    if row and row[9] == '진행 확정':
        green_ranges.append(f'A{i}:K{i}')

for r in green_ranges:
    ws.format(r, {'backgroundColor': {'red': 0.9, 'green': 1.0, 'blue': 0.9}})

total = len(insta_form) + len(insta_tapping) + len(youtube_form) + len(youtube_tapping)
print(f"✅ 최종 리스트 완성!")
print(f"   인스타 (구글폼 우선진행): {len(insta_form)}명")
print(f"   인스타 (탭핑 컨택완료):   {len(insta_tapping)}명")
print(f"   유튜브 (구글폼 우선진행): {len(youtube_form)}명")
print(f"   유튜브 (탭핑 컨택완료):   {len(youtube_tapping)}명")
print(f"   ─────────────────────────")
print(f"   총계: {total}명")
