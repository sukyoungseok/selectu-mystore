import gspread

gc = gspread.oauth()  # 브라우저 열림 → 구글 로그인 후 허용 클릭
ws = gc.open_by_key('1XiTZD-ywUAgW-lJXFa0R0KoZMjW_m-2ytAhl7iwTbC8').worksheet('설문지 응답 시트1')

reels_data = {
    "hwung_travel":   {"avg": 106404, "ratio": "44.4%"},
    "iamsleyle":      {"avg": 55644,  "ratio": "11.1%"},
    "azzapi_":        {"avg": 98044,  "ratio": "44.4%"},
    "balbal_trip":    {"avg": 20030,  "ratio": "0.0%"},
    "ssalb_travel":   {"avg": 62842,  "ratio": "22.2%"},
    "today.brighten": {"avg": 10898,  "ratio": "0.0%"},
    "dadahe_b":       {"avg": 14073,  "ratio": "11.1%"},
    "travel_baek":    {"avg": 562333, "ratio": "77.8%"},
    "daero._.nana":   {"avg": 42667,  "ratio": "11.1%"},
}
followers = {
    "ttoodiii":6528,"mozzi_orzl_":5874,"hwung_travel":30000,"iamsleyle":13000,
    "azzapi_":14000,"trip_db_":8937,"balbal_trip":20000,"ssalb_travel":13000,
    "bbaekkom_okasan":2255,"today.brighten":60000,"heying.pu":1684,
    "everymoment_writer":7231,"dadahe_b":18000,"arang.travel":7238,
    "puwoo_travel":1426,"travel_baek":146000,"trip_heesutory":5100,
    "mangottaeng0":767,"aeriiiiiunni":7412,"mingreen_travel":85,
    "daero._.nana":86000,"sihanmom_trip":3901,"ryong_trip":240,
}
nicknames = {
    "ttoodiii":"혜키","mozzi_orzl_":"아리","hwung_travel":"훵","iamsleyle":"젤리",
    "azzapi_":"어짜피","trip_db_":"트립디비","balbal_trip":"정발발","ssalb_travel":"쌀비",
    "bbaekkom_okasan":"빼꼼오카상","today.brighten":"늘찬맘","heying.pu":"허잉",
    "everymoment_writer":"모든순간의지은이","dadahe_b":"다다헤","arang.travel":"아랑",
    "puwoo_travel":"푸우","travel_baek":"백자매","trip_heesutory":"희수",
    "mangottaeng0":"망고땡","aeriiiiiunni":"애리언니","mingreen_travel":"밍그린",
    "daero._.nana":"대로와나나","sihanmom_trip":"시남매여행","ryong_trip":"애룡",
}

all_ids = ws.col_values(3)
updates = []

for i, uid in enumerate(all_ids):
    uid = uid.strip()
    row = i + 1
    if row == 1 or not uid:
        continue
    if uid in nicknames:
        updates.append({"range": f"F{row}", "values": [[nicknames[uid]]]})
    if uid in followers:
        updates.append({"range": f"G{row}", "values": [[followers[uid]]]})
    if uid in reels_data:
        updates.append({"range": f"H{row}", "values": [[reels_data[uid]["avg"]]]})
        updates.append({"range": f"I{row}", "values": [[reels_data[uid]["ratio"]]]})

ws.batch_update(updates)
print(f"✅ 완료! {len(updates)}개 셀 업데이트됨")
