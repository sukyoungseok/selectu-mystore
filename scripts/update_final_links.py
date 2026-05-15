import gspread

SHEET_KEY = '1XiTZD-ywUAgW-lJXFa0R0KoZMjW_m-2ytAhl7iwTbC8'

# 행 번호 → [기존 프로필링크, 주요 콘텐츠 링크]
# 구글시트 컬럼: I = 기존 프로필링크, J = 주요 콘텐츠 링크

updates_data = {
    # ── 인스타 (구글폼 우선진행) ─────────────────────────────────────
    # 프로필링크: 신청 현황 프로필링크 컬럼
    # 주요 콘텐츠: 신청 현황 콘텐츠링크 컬럼
    3:  ["",                                            # travel_baek (백자매) - 프로필링크 없음
         "https://www.notion.so/4-6-21efefd43b9080b0a7c7fdf8dfacfed9"],

    4:  ["https://link.inpock.co.kr/seunga_travel_",   # sing.______ (씽아)
         "https://www.instagram.com/reel/DNS2SIzyQvc/"],

    5:  ["https://inpk.link/daeronana",                # daero._.nana (대로와나나)
         "https://outstanding-handspring-fda.notion.site/2026-3294502db4e480748db8f569ce0e1de3"],

    6:  ["https://link.inpock.co.kr/bright.today",     # today.brighten (늘찬맘)
         "https://www.instagram.com/reel/DW8-FOMD58s/"],

    7:  ["https://litt.ly/jayna",                      # life.traveler.jayna (제이나)
         "https://www.instagram.com/reel/DOZunqaksxa/"],

    8:  ["https://link.inpock.co.kr/hwung_travel",     # hwung_travel (훵)
         "https://www.instagram.com/reel/DTscruhAWHj/"],

    9:  ["https://litt.ly/hyemingway",                 # hyemingway0707 (혜밍웨이)
         "https://www.instagram.com/reel/DXZzWMbDA7n/"],

    10: ["https://link.inpock.co.kr/uely_",            # uely_ (유블리)
         "https://www.instagram.com/reel/C7UHO8Wh1bm/"],

    11: ["https://www.threads.com/@busan_matna_",      # busan_matna_ (부산맛나)
         "https://www.instagram.com/reel/DSCL2k-EpkW/"],

    # ── 인스타 (탭핑 컨택완료) ────────────────────────────────────────
    # 프로필링크: 미수집 (탭핑 크롤링 미포함)
    # 주요 콘텐츠: wiki 탭핑 대상 리스트에서 가져온 것만 채움
    12: ["", ""],   # hongdadak - 데이터 없음
    13: ["", ""],   # jae9un.jpg - 데이터 없음
    14: ["", "https://www.instagram.com/reel/DGLG5Z5p6kv/"],  # min_pic._
    15: ["", ""],   # henriuniverse - 데이터 없음
    16: ["", ""],   # juuuyomi_ - 데이터 없음
    17: ["", ""],   # yeseulio - 데이터 없음

    # ── 유튜브 (구글폼 우선진행) ─────────────────────────────────────
    # 프로필링크: 채널 URL
    # 주요 콘텐츠: 신청 현황 콘텐츠링크
    19: ["https://www.youtube.com/@review__channel",   # zoey._.vely (별별리뷰)
         "https://youtu.be/GJJgZGgGtrU"],

    20: ["https://www.youtube.com/@mingoose_world",    # mingoose_world (밍구스월드)
         "https://youtu.be/FKgIPxElr4Y"],

    21: ["https://www.youtube.com/@seulsup_",          # seulsup_ (슬숲)
         "https://youtu.be/yS41wcflt2c"],

    # ── 유튜브 (탭핑 컨택완료) ───────────────────────────────────────
    22: ["https://www.youtube.com/@파파트래블",         # 파파트래블
         "https://youtu.be/ALHO2k3VJxU | https://youtu.be/prPgRKLOtqo | https://youtu.be/TSWBclf1QBs"],
}

gc = gspread.oauth()
ws = gc.open_by_key(SHEET_KEY).worksheet('최종 리스트')

# 초록색 배경 제거 (데이터 행 전체 흰 배경으로 초기화)
white = {'backgroundColor': {'red': 1.0, 'green': 1.0, 'blue': 1.0}}
ws.format('A3:M22', white)
print("🎨 초록색 배경 제거 완료")

batch = []
for row, (profile, content) in updates_data.items():
    if profile:
        batch.append({"range": f"I{row}", "values": [[profile]]})
    if content:
        batch.append({"range": f"J{row}", "values": [[content]]})

if batch:
    ws.batch_update(batch)
    filled = sum(1 for r, (p, c) in updates_data.items() if p or c)
    print(f"✅ 완료! {len(batch)}개 셀 업데이트 ({filled}개 행)")
else:
    print("⚠️ 업데이트할 내용 없음")

# 결과 요약
print("\n📋 채움 현황:")
labels = {
    3:"백자매", 4:"씽아", 5:"대로와나나", 6:"늘찬맘", 7:"제이나",
    8:"훵", 9:"혜밍웨이", 10:"유블리", 11:"부산맛나",
    12:"홍다닥", 13:"재구언", 14:"민픽._", 15:"헨리", 16:"주영이랑", 17:"예슬리오",
    19:"별별리뷰", 20:"밍구스월드", 21:"슬숲", 22:"파파트래블"
}
for row, (p, c) in updates_data.items():
    name = labels.get(row, f"Row{row}")
    p_status = "✅" if p else "⬜"
    c_status = "✅" if c else "⬜"
    print(f"  {name:12s} 프로필:{p_status} 콘텐츠:{c_status}")
