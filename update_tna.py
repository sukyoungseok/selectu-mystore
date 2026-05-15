#!/usr/bin/env python3
import re, os

BASE = "/Users/sukyoung-seok/mystore-mockup/channel-pages-final"

def remove_reservation_section(content):
    """Remove 🛒 영상 속 예약 링크 section"""
    return re.sub(
        r'\n\s*<h3 style="margin-top:20px">🛒 영상 속 예약 링크</h3>.*?(?=\n\s*</div>\n\s*<div class="links-section-pb">)',
        '',
        content,
        flags=re.DOTALL
    )

def update_file(filename, transforms):
    path = os.path.join(BASE, filename)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    for old, new in transforms:
        if old not in content:
            print(f"  WARNING: pattern not found in {filename}: {repr(old[:80])}")
        content = content.replace(old, new)
    if content == original:
        print(f"  WARNING: no changes made to {filename}")
    else:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  OK: {filename}")

# ─────────────────────────────────────────────
# 1. 민픽.html - 이탈리아: remove section only
# ─────────────────────────────────────────────
path = os.path.join(BASE, "민픽.html")
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()
c2 = remove_reservation_section(c)
if c2 == c:
    print("WARNING: no change in 민픽.html")
else:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c2)
    print("OK: 민픽.html")

# ─────────────────────────────────────────────
# 2. 혜밍웨이.html - 독일: remove section only
# ─────────────────────────────────────────────
path = os.path.join(BASE, "혜밍웨이.html")
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()
c2 = remove_reservation_section(c)
if c2 == c:
    print("WARNING: no change in 혜밍웨이.html")
else:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c2)
    print("OK: 혜밍웨이.html")

# ─────────────────────────────────────────────
# 3. 제이나.html - 보홀: remove section + replace products
# ─────────────────────────────────────────────
BOHOL_PRODUCTS = """const products=[
  {name:"보홀 조인/단독 픽업 샌딩",price:"₩17,913",tag:"공항",icon:"🚗",bg:"#DBEAFE",tagColor:"#1D4ED8",tagBg:"#DBEAFE",url:"https://www.myrealtrip.com/experiences/3441379"},
  {name:"보홀 한바다 호핑 (발리카삭 거북이 & 나팔링)",price:"₩312,596",tag:"인기",icon:"🐬",bg:"#E8FDF4",tagColor:"#1A8A5A",tagBg:"#C8F0DC",url:"https://www.myrealtrip.com/experiences/3712862"},
  {name:"보홀 프리미엄 디프리호핑 (DJ공연·발리카삭·버진아일랜드)",price:"₩290,954",tag:"강추",icon:"⭐",bg:"#FEF3C7",tagColor:"#E07A38",tagBg:"#FDE8CE",url:"https://www.myrealtrip.com/experiences/4149387"},
  {name:"보홀 팡라오 공항 ↔ 팡라오섬 이동 서비스",price:"₩12,238",tag:"교통",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",url:"https://www.myrealtrip.com/experiences/5542495"},
  {name:"보홀션 입국팩 (BS리조트·알로나비치 도보5분)",price:"₩76,588",tag:"숙박",icon:"🏖️",bg:"#FEF0E8",tagColor:"#D47038",tagBg:"#FDD8B8",url:"https://www.myrealtrip.com/experiences/4480031"},
  {name:"보홀 반딧불 투어 (핫스팟 보트탑승)",price:"₩52,722",tag:"투어",icon:"✨",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",url:"https://www.myrealtrip.com/experiences/3471571"},
  {name:"보홀 발리카삭 버진아일랜드 호핑투어 (픽업드랍 포함)",price:"₩130,622",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",url:"https://www.myrealtrip.com/experiences/3456817"},
  {name:"보홀 스타인 핵심 데이 육상 투어 (로복강·초코릿힐·안경원숭이)",price:"₩216,251",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",url:"https://www.myrealtrip.com/experiences/3441501"},
  {name:"보홀 나팔링 & 히낙다난동굴 스노클링",price:"₩118,475",tag:"수중",icon:"🤿",bg:"#E8F4FD",tagColor:"#1E6FA8",tagBg:"#C8E4F8",url:"https://www.myrealtrip.com/experiences/3441399"},
  {name:"보홀 나팔링 체험프리다이빙 강습 투어 (정어리 수중스냅)",price:"₩134,413",tag:"수중",icon:"🤿",bg:"#E8F4FD",tagColor:"#1E6FA8",tagBg:"#C8E4F8",url:"https://www.myrealtrip.com/experiences/3880714"},
];"""

OLD_JAINA_PRODUCTS = """const products=[
  {name:"보홀 헤난 리조트 알로나비치",price:"₩220,000~/박",tag:"제이나 강추",icon:"🏖️",bg:"#FEF0E8",tagColor:"#D47038",tagBg:"#FDD8B8",sold:"4,218",url:"https://www.myrealtrip.com"},
  {name:"마델린 나팔링 스노클링",price:"₩49,000~",tag:"인기",icon:"🤿",bg:"#E8F4FD",tagColor:"#1E6FA8",tagBg:"#C8E4F8",sold:"3,821",url:"https://www.myrealtrip.com"},
  {name:"발리카삭 호핑투어",price:"₩59,000~",tag:"추천",icon:"🐬",bg:"#E8FDF4",tagColor:"#1A8A5A",tagBg:"#C8F0DC",sold:"2,954",url:"https://www.myrealtrip.com"},
  {name:"필리핀 이심 (10일, 무제한)",price:"₩15,000",tag:"필수",icon:"📱",bg:"#FFF0F3",tagColor:"#BE185D",tagBg:"#FCE7F3",sold:"18,432",url:"https://www.myrealtrip.com"}
];"""

path = os.path.join(BASE, "제이나.html")
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()
c = remove_reservation_section(c)
c = c.replace(OLD_JAINA_PRODUCTS, BOHOL_PRODUCTS)
with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print("OK: 제이나.html")

# ─────────────────────────────────────────────
# 4. 훵.html - 나고야
# ─────────────────────────────────────────────
NAGOYA_PRODUCTS = """const products=[
  {name:"나고야 메이테츠 공항철도 편도티켓",price:"₩9,618",tag:"교통",icon:"🚂",bg:"#DBEAFE",tagColor:"#1D4ED8",tagBg:"#DBEAFE",url:"https://www.myrealtrip.com/experiences/5869313"},
  {name:"시라카와고 & 다카야마 버스투어 (한국인가이드)",price:"₩174,030",tag:"강추",icon:"⭐",bg:"#FEF3C7",tagColor:"#E07A38",tagBg:"#FDE8CE",url:"https://www.myrealtrip.com/experiences/3425907"},
  {name:"나고야 시라카와고 히다 다카야마 버스투어 DSLR 촬영",price:"₩170,036",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",url:"https://www.myrealtrip.com/experiences/4913938"},
  {name:"나고야 출발 1일 시라카와고 히다 다카야마 버스투어 (아이트립)",price:"₩148,230",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",url:"https://www.myrealtrip.com/experiences/4982593"},
  {name:"미슐랭 별3개 시라카와고 버스투어 (한국인가이드)",price:"₩178,977",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",url:"https://www.myrealtrip.com/experiences/3424821"},
  {name:"나고야 다카야마 시라카와고 버스투어 엔데이트립",price:"₩150,283",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",url:"https://www.myrealtrip.com/experiences/3412124"},
  {name:"유투어버스 나고야 다카야마N시라카와고 버스 투어",price:"₩132,294",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",url:"https://www.myrealtrip.com/experiences/3862816"},
  {name:"알펜루트 설벽산책과 세계유산 시라카와고 1일투어",price:"₩885,774",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",url:"https://www.myrealtrip.com/experiences/3425906"},
  {name:"나고야항 수족관 입장권",price:"₩45,023",tag:"입장권",icon:"🎫",bg:"#FEF3C7",tagColor:"#E07A38",tagBg:"#FDE8CE",url:"https://www.myrealtrip.com/experiences/5541726"},
  {name:"포뮬러 F1 일본 스즈카 그랑프리 2026 (3일권)",price:"₩523,537",tag:"입장권",icon:"🏎️",bg:"#FEF3C7",tagColor:"#E07A38",tagBg:"#FDE8CE",url:"https://www.myrealtrip.com/experiences/5809205"},
];"""

OLD_NAGOYA_PRODUCTS = """const products=[
  {name:"나고야 메이테츠 공항철도 편도티켓",price:"상세보기",tag:"교통",icon:"🚂",bg:"#DBEAFE",tagColor:"#1D4ED8",tagBg:"#DBEAFE",url:"https://www.myrealtrip.com/experiences/5869313"},
  {name:"시라카와고 & 다카야마 버스투어 (한국인가이드)",price:"상세보기",tag:"강추",icon:"⭐",bg:"#FEF3C7",tagColor:"#E07A38",tagBg:"#FDE8CE",url:"https://www.myrealtrip.com/experiences/3425907"},
  {name:"나고야 시라카와고 히다 다카야마 버스투어 DSLR 촬영",price:"상세보기",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",url:"https://www.myrealtrip.com/experiences/4913938"},
  {name:"나고야 출발 시라카와고 히다 다카야마 버스투어 (아이트립)",price:"상세보기",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",url:"https://www.myrealtrip.com/experiences/4982593"},
  {name:"미슐랭 별3개 시라카와고 버스투어 (한국인가이드)",price:"상세보기",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",url:"https://www.myrealtrip.com/experiences/3424821"},
  {name:"나고야항 수족관 입장권",price:"상세보기",tag:"입장권",icon:"🎫",bg:"#FEF3C7",tagColor:"#E07A38",tagBg:"#FDE8CE",url:"https://www.myrealtrip.com/experiences/5541726"},
];"""

OLD_NAGOYA_EXPENSE = """const CITY_EXPENSE={nagoya:{title:"✈️ 나고야 4박 5일 총경비",food:420000,foodNote:"미소카츠·히츠마부시·하브스 포함",defaultFlight:204000,defaultHotel:380000,defaultTotal:1234000,tours:[{emoji:"🌲",name:"지브리파크 입장권",note:"사전 온라인 예매 · 오픈런 불필요",price:45000,url:"https://www.myrealtrip.com"},{emoji:"🏔️",name:"시라카와고+다카야마 버스투어",note:"합장촌·전통 거리 당일치기",price:78000,url:"https://www.myrealtrip.com"},{emoji:"📱",name:"일본 이심 (5일, 2GB/일)",note:"도착 즉시 사용 · 한국서 미리 설치",price:15000,url:"https://www.myrealtrip.com"}],finePrint:"✈️항공·🏨숙소는 최저가 기준 · 식비는 평균값"}};"""

NEW_NAGOYA_EXPENSE = """const CITY_EXPENSE={nagoya:{title:"✈️ 나고야 4박 5일 총경비",food:420000,foodNote:"미소카츠·히츠마부시·하브스 포함",defaultFlight:204000,defaultHotel:380000,defaultTotal:1232671,tours:[{emoji:"🚂",name:"나고야 메이테츠 공항철도 편도티켓",note:"공항↔나고야역 직결 교통 (편도)",price:9618,url:"https://www.myrealtrip.com/experiences/5869313"},{emoji:"🏔️",name:"시라카와고 & 다카야마 버스투어 (한국인가이드)",note:"세계문화유산 합장촌 당일치기",price:174030,url:"https://www.myrealtrip.com/experiences/3425907"},{emoji:"🐟",name:"나고야항 수족관 입장권",note:"상어·범고래·벨루가 등 국내 최대 규모",price:45023,url:"https://www.myrealtrip.com/experiences/5541726"}],finePrint:"✈️항공·🏨숙소는 최저가 기준 · 식비는 평균값"}};"""

# D2 product: update URL and price
OLD_D2 = 'cost:"₩78,000",product:{name:"시라카와고+다카야마 버스투어",price:"₩78,000",tagBg:"#DBEAFE",tagColor:"#1D4ED8",tag:"강추",bg:"#DBEAFE",icon:"🏔️",url:"https://www.myrealtrip.com"}'
NEW_D2 = 'cost:"₩174,030",product:{name:"시라카와고+다카야마 버스투어",price:"₩174,030",tagBg:"#DBEAFE",tagColor:"#1D4ED8",tag:"강추",bg:"#DBEAFE",icon:"🏔️",url:"https://www.myrealtrip.com/experiences/3425907"}'

path = os.path.join(BASE, "훵.html")
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()
c = remove_reservation_section(c)
transforms = [
    (OLD_NAGOYA_PRODUCTS, NAGOYA_PRODUCTS),
    (OLD_NAGOYA_EXPENSE, NEW_NAGOYA_EXPENSE),
    (OLD_D2, NEW_D2),
]
for old, new in transforms:
    if old not in c:
        print(f"  WARNING not found in 훵.html: {repr(old[:60])}")
    c = c.replace(old, new)
with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print("OK: 훵.html")

# ─────────────────────────────────────────────
# 5. 늘찬맘.html - 다낭
# ─────────────────────────────────────────────
DANANG_PRODUCTS = """const products=[
  {name:"다낭 VIP 패스트트랙 (입출국)",price:"₩63,709",tag:"편의",icon:"✈️",bg:"#DCFCE7",tagColor:"#15803D",tagBg:"#DCFCE7",url:"https://www.myrealtrip.com/experiences/3520268"},
  {name:"바나힐 입장권 + eSIM 50% 할인",price:"₩191,846",tag:"입장권",icon:"🎫",bg:"#FEF3C7",tagColor:"#E07A38",tagBg:"#FDE8CE",url:"https://www.myrealtrip.com/offers/63983"},
  {name:"다낭 공항 단독 픽업&샌딩",price:"₩16,263",tag:"공항",icon:"🚗",bg:"#DBEAFE",tagColor:"#1D4ED8",tagBg:"#DBEAFE",url:"https://www.myrealtrip.com/experiences/3550628"},
  {name:"바나힐 + 단독 왕복차량 투어",price:"₩258,968",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",url:"https://www.myrealtrip.com/experiences/5009871"},
  {name:"다낭 공항 CIP 라운지 3시간",price:"₩104,405",tag:"편의",icon:"✈️",bg:"#DCFCE7",tagColor:"#15803D",tagBg:"#DCFCE7",url:"https://www.myrealtrip.com/experiences/5009870"},
  {name:"다낭 바나힐&호이안 퍼펙트 원데이 투어",price:"₩387,548",tag:"강추",icon:"🌟",bg:"#FEF3C7",tagColor:"#E07A38",tagBg:"#FDE8CE",url:"https://www.myrealtrip.com/experiences/3520244"},
  {name:"남호이안 빈원더스 입장권",price:"₩141,760",tag:"입장권",icon:"🎫",bg:"#FEF3C7",tagColor:"#E07A38",tagBg:"#FDE8CE",url:"https://www.myrealtrip.com/experiences/5812485"},
  {name:"다낭 야간 공항 픽업 (시내/호이안)",price:"₩20,818",tag:"공항",icon:"🚗",bg:"#DBEAFE",tagColor:"#1D4ED8",tagBg:"#DBEAFE",url:"https://www.myrealtrip.com/experiences/3881289"},
  {name:"다낭국제공항 패스트트랙 (빠른입국·출국)",price:"₩44,434",tag:"편의",icon:"✈️",bg:"#DCFCE7",tagColor:"#15803D",tagBg:"#DCFCE7",url:"https://www.myrealtrip.com/experiences/4901394"},
  {name:"다낭·호이안 짐 보관·배송",price:"₩25,906",tag:"편의",icon:"🧳",bg:"#DCFCE7",tagColor:"#15803D",tagBg:"#DCFCE7",url:"https://www.myrealtrip.com/experiences/3885470"},
];"""

OLD_DANANG_PRODUCTS = """const products=[
  {name:"다낭 VIP 패스트트랙 (입출국)",price:"상세보기",tag:"편의",icon:"✈️",bg:"#DCFCE7",tagColor:"#15803D",tagBg:"#DCFCE7",url:"https://www.myrealtrip.com/experiences/3520268"},
  {name:"바나힐 입장권 + eSIM 50% 할인",price:"상세보기",tag:"입장권",icon:"🎫",bg:"#FEF3C7",tagColor:"#E07A38",tagBg:"#FDE8CE",url:"https://www.myrealtrip.com/offers/63983"},
  {name:"다낭 공항 단독 픽업&샌딩",price:"상세보기",tag:"공항",icon:"🚗",bg:"#DBEAFE",tagColor:"#1D4ED8",tagBg:"#DBEAFE",url:"https://www.myrealtrip.com/experiences/3550628"},
  {name:"바나힐 + 단독 왕복차량 투어",price:"상세보기",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",url:"https://www.myrealtrip.com/experiences/5009871"},
  {name:"다낭 공항 CIP 라운지 3시간",price:"상세보기",tag:"편의",icon:"✈️",bg:"#DCFCE7",tagColor:"#15803D",tagBg:"#DCFCE7",url:"https://www.myrealtrip.com/experiences/5009870"},
  {name:"다낭 바나힐&호이안 퍼펙트 원데이 투어",price:"상세보기",tag:"강추",icon:"🌟",bg:"#FEF3C7",tagColor:"#E07A38",tagBg:"#FDE8CE",url:"https://www.myrealtrip.com/experiences/3520244"},
  {name:"남호이안 빈원더스 입장권",price:"상세보기",tag:"입장권",icon:"🎫",bg:"#FEF3C7",tagColor:"#E07A38",tagBg:"#FDE8CE",url:"https://www.myrealtrip.com/experiences/5812485"},
  {name:"다낭 야간 공항 픽업 (시내/호이안)",price:"상세보기",tag:"공항",icon:"🚗",bg:"#DBEAFE",tagColor:"#1D4ED8",tagBg:"#DBEAFE",url:"https://www.myrealtrip.com/experiences/3881289"},
];"""

OLD_DANANG_EXPENSE = """const CITY_EXPENSE={danang:{title:"✈️ 다낭 4박 5일 총경비",food:280000,foodNote:"쌀국수·분짜·현지 맛집 포함",defaultFlight:298520,defaultHotel:480000,defaultTotal:1478520,tours:[{emoji:"🎫",name:"바나힐 입장권 + eSIM 50% 할인",note:"바나힐 입장권 + eSIM 번들 특가",price:79000,url:"https://www.myrealtrip.com/offers/63983"},{emoji:"🌟",name:"다낭 바나힐&호이안 퍼펙트 원데이 투어",note:"바나힐+호이안 하루에 완성",price:45000,url:"https://www.myrealtrip.com/experiences/3520244"},{emoji:"✈️",name:"다낭 VIP 패스트트랙 (입출국)",note:"입출국 전용 패스트트랙",price:63000,url:"https://www.myrealtrip.com/experiences/3520268"},{emoji:"🚗",name:"다낭 공항 단독 픽업&샌딩",note:"공항 단독 픽업·샌딩",price:35000,url:"https://www.myrealtrip.com/experiences/3550628"}],finePrint:"✈️항공·🏨숙소는 최저가 기준 · 식비는 평균값"}};"""

NEW_DANANG_EXPENSE = """const CITY_EXPENSE={danang:{title:"✈️ 다낭 4박 5일 총경비",food:280000,foodNote:"쌀국수·분짜·현지 맛집 포함",defaultFlight:298520,defaultHotel:480000,defaultTotal:1472098,tours:[{emoji:"✈️",name:"다낭 VIP 패스트트랙 (입출국)",note:"입출국 전용 패스트트랙",price:63709,url:"https://www.myrealtrip.com/experiences/3520268"},{emoji:"🎫",name:"바나힐 입장권 + eSIM 50% 할인",note:"바나힐 입장권 + eSIM 번들 특가",price:191846,url:"https://www.myrealtrip.com/offers/63983"},{emoji:"🚗",name:"다낭 공항 단독 픽업&샌딩",note:"공항 단독 픽업·샌딩",price:16263,url:"https://www.myrealtrip.com/experiences/3550628"},{emoji:"🎡",name:"남호이안 빈원더스 입장권",note:"빈원더스 테마파크 입장권",price:141760,url:"https://www.myrealtrip.com/experiences/5812485"}],finePrint:"✈️항공·🏨숙소는 최저가 기준 · 식비는 평균값"}};"""

path = os.path.join(BASE, "늘찬맘.html")
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()
c = remove_reservation_section(c)
for old, new in [(OLD_DANANG_PRODUCTS, DANANG_PRODUCTS), (OLD_DANANG_EXPENSE, NEW_DANANG_EXPENSE)]:
    if old not in c:
        print(f"  WARNING not found in 늘찬맘.html: {repr(old[:60])}")
    c = c.replace(old, new)
with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print("OK: 늘찬맘.html")

# ─────────────────────────────────────────────
# 6 & 7. Bali products (shared)
# ─────────────────────────────────────────────
BALI_PRODUCTS = """const products=[
  {name:"바투르산 지프투어 선라이즈 (사진천재 와얀)",price:"₩215,199",tag:"강추",icon:"⭐",bg:"#FEF3C7",tagColor:"#E07A38",tagBg:"#FDE8CE",url:"https://www.myrealtrip.com/experiences/3735536"},
  {name:"발리 응우라라이 공항 픽업&샌딩",price:"₩21,262",tag:"공항",icon:"🚗",bg:"#DBEAFE",tagColor:"#1D4ED8",tagBg:"#DBEAFE",url:"https://www.myrealtrip.com/experiences/5542504"},
  {name:"발리 바투르산 선라이즈 지프투어 (아퐁투어)",price:"₩179,358",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",url:"https://www.myrealtrip.com/experiences/3650240"},
  {name:"발리 남부 맞춤 택시투어 (공항드랍 무료)",price:"₩80,483",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",url:"https://www.myrealtrip.com/experiences/3886810"},
  {name:"발리 프라이빗 택시 맞춤 투어 (남부/동부/우붓)",price:"₩104,153",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",url:"https://www.myrealtrip.com/experiences/5541608"},
  {name:"발리 공항 픽업/샌딩 단독차량 (비오비투어)",price:"₩19,972",tag:"공항",icon:"🚗",bg:"#DBEAFE",tagColor:"#1D4ED8",tagBg:"#DBEAFE",url:"https://www.myrealtrip.com/experiences/5685003"},
  {name:"내 맘대로 짜는 발리 남부 투어 (인생샷 스팟)",price:"₩103,706",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",url:"https://www.myrealtrip.com/experiences/4780599"},
  {name:"발리 프라이빗 자유여행 맞춤 투어 (트립인발리)",price:"₩101,671",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",url:"https://www.myrealtrip.com/experiences/4206886"},
  {name:"렘푸양 사원(천국의문) 발리 동부 투어 (사진천재 와얀)",price:"₩236,887",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",url:"https://www.myrealtrip.com/experiences/3735545"},
  {name:"인도네시아 이심 (eSIM/로밍)",price:"₩30,986",tag:"필수",icon:"📱",bg:"#DCFCE7",tagColor:"#15803D",tagBg:"#DCFCE7",url:"https://www.myrealtrip.com/experiences/4743451"},
];"""

OLD_BALI_PRODUCTS = """const products=[
  {name:"바투르산 지프투어 선라이즈 (사진천재 와얀)",price:"상세보기",tag:"강추",icon:"⭐",bg:"#FEF3C7",tagColor:"#E07A38",tagBg:"#FDE8CE",url:"https://www.myrealtrip.com/experiences/3735536"},
  {name:"발리 응우라라이 공항 픽업&샌딩",price:"상세보기",tag:"공항",icon:"🚗",bg:"#DBEAFE",tagColor:"#1D4ED8",tagBg:"#DBEAFE",url:"https://www.myrealtrip.com/experiences/5542504"},
  {name:"발리 바투르산 선라이즈 지프투어 (아퐁투어)",price:"상세보기",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",url:"https://www.myrealtrip.com/experiences/3650240"},
  {name:"발리 남부 맞춤 택시투어 (공항드랍 무료)",price:"상세보기",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",url:"https://www.myrealtrip.com/experiences/3886810"},
  {name:"발리 프라이빗 택시 맞춤 투어 (남부/동부/우붓)",price:"상세보기",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",url:"https://www.myrealtrip.com/experiences/5541608"},
  {name:"발리 공항 픽업/샌딩 단독차량 (비오비투어)",price:"상세보기",tag:"공항",icon:"🚗",bg:"#DBEAFE",tagColor:"#1D4ED8",tagBg:"#DBEAFE",url:"https://www.myrealtrip.com/experiences/5685003"},
  {name:"렘푸양 사원(천국의문) 발리 동부 투어",price:"상세보기",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",url:"https://www.myrealtrip.com/experiences/3735545"},
  {name:"인도네시아 이심 (eSIM/로밍)",price:"상세보기",tag:"필수",icon:"📱",bg:"#DCFCE7",tagColor:"#15803D",tagBg:"#DCFCE7",url:"https://www.myrealtrip.com/experiences/4743451"}
];"""

# 밍구스월드 CITY_EXPENSE
OLD_MINGS_EXPENSE = """const CITY_EXPENSE={"bali":{title:"발리 4박 5일 총경비",food:180000,foodNote:"나시고렝·씨푸드·카페 식비 4박",defaultFlight:569700,defaultHotel:180000,defaultTotal:1129700,flightNote:"인천-발리 직항 기준",flightUrl:"https://www.myrealtrip.com/offers?keyword=발리+항공",hotelName:"꾸따/세미냑 리조트",hotelNote:"꾸따 지역 3박 1인 기준",hotelUrl:"",tours:[{emoji:"🌅",name:"울루와뚜 케차크댄스+선셋",note:"절벽 사원 야외 공연",price:35000,url:"https://www.myrealtrip.com/offers?keyword=울루와뚜+케차크"},{emoji:"🚵",name:"발리 ATV+래프팅 콤보",note:"정글 ATV+아융강 래프팅",price:89000,url:"https://www.myrealtrip.com/offers?keyword=발리+ATV"},{emoji:"📱",name:"인도네시아 이심 15일",note:"LTE 무제한 데이터",price:15000,url:""}],toursLabel:"🎫 밍구스 추천 액티비티",finePrint:"· 4박 5일 1인 평균값 · 항공 유류세 포함"}};"""
NEW_MINGS_EXPENSE = """const CITY_EXPENSE={"bali":{title:"발리 4박 5일 총경비",food:180000,foodNote:"나시고렝·씨푸드·카페 식비 4박",defaultFlight:569700,defaultHotel:180000,defaultTotal:1197147,flightNote:"인천-발리 직항 기준",flightUrl:"https://www.myrealtrip.com/offers?keyword=발리+항공",hotelName:"꾸따/세미냑 리조트",hotelNote:"꾸따 지역 3박 1인 기준",hotelUrl:"",tours:[{emoji:"⭐",name:"바투르산 지프투어 선라이즈 (사진천재 와얀)",note:"화산 일출 지프 드라이브",price:215199,url:"https://www.myrealtrip.com/experiences/3735536"},{emoji:"🚗",name:"발리 응우라라이 공항 픽업&샌딩",note:"공항 ↔ 꾸따/세미냑 단독 차량",price:21262,url:"https://www.myrealtrip.com/experiences/5542504"},{emoji:"📱",name:"인도네시아 이심 (eSIM/로밍)",note:"LTE 무제한 데이터",price:30986,url:"https://www.myrealtrip.com/experiences/4743451"}],toursLabel:"🎫 밍구스 추천 액티비티",finePrint:"· 4박 5일 1인 평균값 · 항공 유류세 포함"}};"""

path = os.path.join(BASE, "밍구스월드.html")
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()
c = remove_reservation_section(c)
for old, new in [(OLD_BALI_PRODUCTS, BALI_PRODUCTS), (OLD_MINGS_EXPENSE, NEW_MINGS_EXPENSE)]:
    if old not in c:
        print(f"  WARNING not found in 밍구스월드.html: {repr(old[:60])}")
    c = c.replace(old, new)
with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print("OK: 밍구스월드.html")

# 슬숲 CITY_EXPENSE
OLD_SEUL_EXPENSE = """const CITY_EXPENSE={"bali":{title:"발리 우붓·짱구 4박 5일 총경비",food:160000,foodNote:"나시고렝·와룽·카페 식비 4박",defaultFlight:569700,defaultHotel:200000,defaultTotal:1129700,flightNote:"인천-발리 직항 기준",flightUrl:"https://www.myrealtrip.com/offers?keyword=발리+항공",hotelName:"우붓 논밭뷰 빌라",hotelNote:"우붓 빌라 3박 1인 기준",hotelUrl:"",tours:[{emoji:"🏄",name:"꾸따 서핑 레슨",note:"초보 OK · 보드+강사 포함",price:35000,url:"https://www.myrealtrip.com/offers?keyword=발리+서핑"},{emoji:"🍳",name:"우붓 전통 요리 클래스",note:"시장투어+요리 실습 포함",price:55000,url:"https://www.myrealtrip.com/offers?keyword=발리+요리클래스"},{emoji:"📱",name:"인도네시아 이심 10일",note:"LTE 무제한 데이터",price:13000,url:""}],toursLabel:"🎫 슬숲 힐링 추천",finePrint:"· 4박 5일 1인 평균값 · 항공 유류세 포함"}};"""
NEW_SEUL_EXPENSE = """const CITY_EXPENSE={"bali":{title:"발리 우붓·짱구 4박 5일 총경비",food:160000,foodNote:"나시고렝·와룽·카페 식비 4박",defaultFlight:569700,defaultHotel:200000,defaultTotal:1197147,flightNote:"인천-발리 직항 기준",flightUrl:"https://www.myrealtrip.com/offers?keyword=발리+항공",hotelName:"우붓 논밭뷰 빌라",hotelNote:"우붓 빌라 3박 1인 기준",hotelUrl:"",tours:[{emoji:"⭐",name:"바투르산 지프투어 선라이즈 (사진천재 와얀)",note:"화산 일출 지프 드라이브",price:215199,url:"https://www.myrealtrip.com/experiences/3735536"},{emoji:"🚗",name:"발리 응우라라이 공항 픽업&샌딩",note:"공항 ↔ 우붓/짱구 단독 차량",price:21262,url:"https://www.myrealtrip.com/experiences/5542504"},{emoji:"📱",name:"인도네시아 이심 (eSIM/로밍)",note:"LTE 무제한 데이터",price:30986,url:"https://www.myrealtrip.com/experiences/4743451"}],toursLabel:"🎫 슬숲 힐링 추천",finePrint:"· 4박 5일 1인 평균값 · 항공 유류세 포함"}};"""

path = os.path.join(BASE, "슬숲.html")
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()
c = remove_reservation_section(c)
for old, new in [(OLD_BALI_PRODUCTS, BALI_PRODUCTS), (OLD_SEUL_EXPENSE, NEW_SEUL_EXPENSE)]:
    if old not in c:
        print(f"  WARNING not found in 슬숲.html: {repr(old[:60])}")
    c = c.replace(old, new)
with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print("OK: 슬숲.html")

# ─────────────────────────────────────────────
# 8. 부산맛나.html - 삿포로
# ─────────────────────────────────────────────
SAPPORO_PRODUCTS = """const products=[
  {name:"삿포로 비에이 후라노 버스투어 DSLR 촬영 (인디고트래블)",price:"₩235,843",tag:"강추",icon:"⭐",bg:"#FEF3C7",tagColor:"#E07A38",tagBg:"#FDE8CE",url:"https://www.myrealtrip.com/experiences/3417852"},
  {name:"북해도 비에이 후라노 삿포로 버스투어 (라쿠투어)",price:"₩158,009",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",url:"https://www.myrealtrip.com/experiences/3153598"},
  {name:"삿포로 비에이 후라노 버스투어 엔데이트립",price:"₩170,120",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",url:"https://www.myrealtrip.com/experiences/3412145"},
  {name:"비에이 후라노 버스투어 여행 한 그릇",price:"₩154,390",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",url:"https://www.myrealtrip.com/experiences/3425917"},
  {name:"흰그림자투어 비에이 후라노 버스투어",price:"₩191,731",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",url:"https://www.myrealtrip.com/experiences/3412046"},
  {name:"엔데이트립 비에이 아사히야마 동물원 버스투어",price:"₩288,837",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",url:"https://www.myrealtrip.com/experiences/3412141"},
  {name:"삿포로 TV 타워 입장권",price:"₩18,923",tag:"입장권",icon:"🎫",bg:"#FEF3C7",tagColor:"#E07A38",tagBg:"#FDE8CE",url:"https://www.myrealtrip.com/offers/29036"},
  {name:"JR홋카이도 삿포로-노보리베츠 에리어패스 4일권",price:"₩190,002",tag:"교통",icon:"🚂",bg:"#DBEAFE",tagColor:"#1D4ED8",tagBg:"#DBEAFE",url:"https://www.myrealtrip.com/offers/123042"},
  {name:"노보리베츠 온천마을 도야호 버스투어",price:"₩159,495",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",url:"https://www.myrealtrip.com/experiences/3555399"},
  {name:"마이재팬 비에이 후라노 버스투어",price:"₩211,283",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",url:"https://www.myrealtrip.com/experiences/3880715"},
];"""

OLD_SAPPORO_PRODUCTS = """const products=[
  {name:"삿포로 비에이 후라노 버스투어 DSLR 촬영 (인디고트래블)",price:"상세보기",tag:"강추",icon:"⭐",bg:"#FEF3C7",tagColor:"#E07A38",tagBg:"#FDE8CE",url:"https://www.myrealtrip.com/experiences/3417852"},
  {name:"북해도 비에이 후라노 삿포로 버스투어 (라쿠투어)",price:"상세보기",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",url:"https://www.myrealtrip.com/experiences/3153598"},
  {name:"삿포로 비에이 후라노 버스투어 엔데이트립",price:"상세보기",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",url:"https://www.myrealtrip.com/experiences/3412145"},
  {name:"비에이 후라노 버스투어 여행 한 그릇",price:"상세보기",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",url:"https://www.myrealtrip.com/experiences/3425917"},
  {name:"흰그림자투어 비에이 후라노 버스투어",price:"상세보기",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",url:"https://www.myrealtrip.com/experiences/3412046"},
  {name:"삿포로 TV 타워 입장권",price:"상세보기",tag:"입장권",icon:"🎫",bg:"#FEF3C7",tagColor:"#E07A38",tagBg:"#FDE8CE",url:"https://www.myrealtrip.com/offers/29036"},
  {name:"JR홋카이도 삿포로-노보리베츠 에리어패스 4일권",price:"상세보기",tag:"교통",icon:"🚂",bg:"#DBEAFE",tagColor:"#1D4ED8",tagBg:"#DBEAFE",url:"https://www.myrealtrip.com/offers/123042"},
  {name:"노보리베츠 온천마을 도야호 버스투어",price:"상세보기",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",url:"https://www.myrealtrip.com/experiences/3555399"}
];"""

OLD_SAPPORO_EXPENSE = """const CITY_EXPENSE={"sapporo":{title:"삿포로 3박 4일 총경비",food:200000,foodNote:"라멘·초밥·스프카레 홋카이도 식비 3박",defaultFlight:254200,defaultHotel:160000,defaultTotal:714200,flightNote:"인천-삿포로 직항 기준",flightUrl:"https://www.myrealtrip.com/offers?keyword=삿포로+항공",hotelName:"삿포로역 인근 호텔",hotelNote:"삿포로 시내 2박 1인 기준",hotelUrl:"",tours:[{emoji:"⛵",name:"오타루 당일치기 투어",note:"오타루 운하·회전초밥 코스",price:45000,url:"https://www.myrealtrip.com/offers?keyword=오타루+투어"},{emoji:"🚌",name:"삿포로 반나절 버스 투어",note:"주요 명소 순환 투어",price:79000,url:"https://www.myrealtrip.com/offers?keyword=삿포로+버스투어"},{emoji:"📱",name:"일본 이심 7일",note:"LTE 무제한 데이터",price:13000,url:""}],toursLabel:"🎫 부산맛나 추천 코스",finePrint:"· 3박 4일 1인 평균값 · 항공 유류세 포함"}};"""
NEW_SAPPORO_EXPENSE = """const CITY_EXPENSE={"sapporo":{title:"삿포로 3박 4일 총경비",food:200000,foodNote:"라멘·초밥·스프카레 홋카이도 식비 3박",defaultFlight:254200,defaultHotel:160000,defaultTotal:1058968,flightNote:"인천-삿포로 직항 기준",flightUrl:"https://www.myrealtrip.com/offers?keyword=삿포로+항공",hotelName:"삿포로역 인근 호텔",hotelNote:"삿포로 시내 2박 1인 기준",hotelUrl:"",tours:[{emoji:"⭐",name:"삿포로 비에이 후라노 버스투어 DSLR 촬영 (인디고트래블)",note:"DSLR 사진촬영 포함 버스투어",price:235843,url:"https://www.myrealtrip.com/experiences/3417852"},{emoji:"🗼",name:"삿포로 TV 타워 입장권",note:"오도리공원 전망 · 즉시확정",price:18923,url:"https://www.myrealtrip.com/offers/29036"},{emoji:"🚂",name:"JR홋카이도 삿포로-노보리베츠 에리어패스 4일권",note:"노보리베츠 온천 왕복 포함",price:190002,url:"https://www.myrealtrip.com/offers/123042"}],toursLabel:"🎫 부산맛나 추천 코스",finePrint:"· 3박 4일 1인 평균값 · 항공 유류세 포함"}};"""

path = os.path.join(BASE, "부산맛나.html")
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()
c = remove_reservation_section(c)
for old, new in [(OLD_SAPPORO_PRODUCTS, SAPPORO_PRODUCTS), (OLD_SAPPORO_EXPENSE, NEW_SAPPORO_EXPENSE)]:
    if old not in c:
        print(f"  WARNING not found in 부산맛나.html: {repr(old[:60])}")
    c = c.replace(old, new)
with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print("OK: 부산맛나.html")

print("\n=== ALL DONE ===")
