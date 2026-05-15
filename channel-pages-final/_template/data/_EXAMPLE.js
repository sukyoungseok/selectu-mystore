// 채널 페이지 데이터 파일 — 작성 가이드 겸 예시 (부산맛나 기준)
// 새 크리에이터: 이 파일을 data/{크리에이터명}.js 로 복사한 뒤 채우세요.
module.exports = {

  // ══════════ 수경님이 채우는 구역 ══════════
  creator: {
    name: "부산맛나",
    tagline: "부산 찐맛집 · 여행 전문탐방 크리에이터",
    email: "ttt0831@naver.com",
    profileImg: "../assets/profiles/부산맛나.jpg",
    heroImg: "../assets/images/busanmatna-hero.jpg",
  },

  // 색상 프리셋 이름. 선택지: ember, ocean, forest, grape, rose, slate (생략 시 ember)
  theme: "ember",

  // SNS 아이콘. type: instagram | youtube | tiktok | threads | blog | email
  sns: [
    { type: "instagram", url: "https://www.instagram.com/busan_matna_/" },
    { type: "email", url: "mailto:ttt0831@naver.com" },
  ],

  coupon: {
    showcaseUrl: "https://www.myrealtrip.com/coupons",
    kicker: "부산맛나 팔로워 전용",
    title: "선착순 할인 쿠폰팩",
    amount: "99,000",
    count: "8종",
    cards: [
      { label: "마이리얼트립 파트너 혜택", title: "첫 예약 3,000원 할인",
        desc: "5만원 이상 결제 시 · 1회 사용 가능", expire: "유효기간: 2026.06.30까지",
        remain: "잔여 47장", url: "https://www.myrealtrip.com/coupons", color: "var(--amber)" },
      { label: "재방문 감사 쿠폰", title: "2번째 예약 5% 할인",
        desc: "최대 1만원 · 부산맛나 전용", expire: "유효기간: 2026.07.31까지",
        remain: "잔여 23장", url: "https://www.myrealtrip.com/coupons", color: "var(--sage)" },
    ],
  },

  textblock: {
    title: "🍜 부산 찐맛집부터 해외 여행 전문탐방까지",
    body: "부산의 찐 맛집을 탐방하며 해외 여행도 빠삭하게 정리하는 부산맛나님. 삿포로 5박6일 인당 123만원 코스 — 료칸부터 스프카레, 징기스칸까지 완전 정복!",
  },

  // 추천 콘텐츠 — 섹션(h3 제목) → 항목들. 항목 type: thumb | og
  linkSections: [
    {
      heading: "📸 추천 콘텐츠",
      items: [
        { type:"thumb", icon:"🇯🇵", badges:[{text:"경비 총정리",style:"hot"}],
          title:"삿포로 5박6일 인당 123만원",
          sub:"료칸·스프카레·징기스칸·버스투어 완전 정복",
          url:"https://www.instagram.com/reel/DSCL2k-EpkW/" },
        // og 타입 예시 (큰 썸네일 카드 — 유튜브 영상 등):
        // { type:"og", img:"https://img.youtube.com/vi/{영상ID}/maxresdefault.jpg",
        //   badges:[{text:"🔥 13만 조회수",style:"hot"}], title:"영상 제목",
        //   domain:"youtube.com · 채널명", url:"https://youtu.be/{영상ID}" },
      ],
    },
  ],

  // 필수템 탭 상품 목록 — 부산맛나.html 353~362줄의 객체 10개를 그대로 복사
  products: [
    {name:"삿포로 비에이 후라노 버스투어 DSLR 촬영 (인디고트래블)",price:"₩235,843",tag:"강추",icon:"⭐",bg:"#FEF3C7",tagColor:"#E07A38",tagBg:"#FDE8CE",city:"삿포로",url:"https://myrealt.rip/ZIqQ4e",img:"https://dry7pvlp22cox.cloudfront.net/mrt-images-prod/2024/06/27/tJqk/NLTULKHS59.jpg"},
    {name:"북해도 비에이 후라노 삿포로 버스투어 (라쿠투어)",price:"₩158,009",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",city:"삿포로",url:"https://myrealt.rip/ZIqR5e",img:"https://dry7pvlp22cox.cloudfront.net/mrt-images-prod/2026/04/02/tKek/1Pja6ZDD0s.jpg"},
    {name:"삿포로 비에이 후라노 버스투어 엔데이트립",price:"₩170,120",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",city:"삿포로",url:"https://myrealt.rip/ZIqS52",img:"https://dry7pvlp22cox.cloudfront.net/mrt-images-prod/2026/03/25/vGlm/88JOVAO63O.png"},
    {name:"비에이 후라노 버스투어 여행 한 그릇",price:"₩154,390",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",city:"삿포로",url:"https://myrealt.rip/ZIqTb7",img:"https://dry7pvlp22cox.cloudfront.net/mrt-images-prod/2026/04/06/sX3v/g8FYjQcYDd.jpg"},
    {name:"흰그림자투어 비에이 후라노 버스투어",price:"₩191,731",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",city:"삿포로",url:"https://myrealt.rip/ZIqU73",img:"https://dry7pvlp22cox.cloudfront.net/mrt-images-prod/2026/04/07/azXa/cq47C67XYo.jpg"},
    {name:"엔데이트립 비에이 아사히야마 동물원 버스투어",price:"₩288,837",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",city:"삿포로",url:"https://myrealt.rip/ZIqV3f",img:"https://dry7pvlp22cox.cloudfront.net/mrt-images-prod/2024/06/25/4wlw/UHu3AZHGRS.jpg"},
    {name:"삿포로 TV 타워 입장권",price:"₩18,923",tag:"입장권",icon:"🎫",bg:"#FEF3C7",tagColor:"#E07A38",tagBg:"#FDE8CE",city:"삿포로",url:"https://myrealt.rip/ZIqWb9",img:"https://d2ur7st6jjikze.cloudfront.net/offer_photos/29036/181471_medium_1567648199.jpg?1567648199"},
    {name:"JR홋카이도 삿포로-노보리베츠 에리어패스 4일권",price:"₩190,002",tag:"교통",icon:"🚂",bg:"#DBEAFE",tagColor:"#1D4ED8",tagBg:"#DBEAFE",city:"삿포로",url:"https://myrealt.rip/ZIqX03",img:"https://d2ur7st6jjikze.cloudfront.net/offer_photos/123042/817671_medium_1684321472.jpg?1684321472"},
    {name:"노보리베츠 온천마을 도야호 버스투어",price:"₩159,495",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",city:"삿포로",url:"https://myrealt.rip/ZIqY61",img:"https://dry7pvlp22cox.cloudfront.net/mrt-images-prod/2026/03/16/7mso/Yd4bYcbac4.jpeg"},
    {name:"마이재팬 비에이 후라노 버스투어",price:"₩211,283",tag:"투어",icon:"🚌",bg:"#EDE9FE",tagColor:"#7C3AED",tagBg:"#EDE9FE",city:"삿포로",url:"https://myrealt.rip/ZIqZ65",img:"https://dry7pvlp22cox.cloudfront.net/mrt-images-prod/2026/04/13/Q5HY/KO9gVqvSjs.jpg"},
  ],

  // ══════════ Claude가 채우는 구역 (영상·메모 요약) ══════════
  trips: [
    {
      city: "sapporo",
      flag: "🇯🇵",
      // 참고: badges는 크리에이터 전체 여행 기간, days/expense는 하이라이트 압축본 (3박 4일)
      badges: ["5박 6일", "인당 123만원"],
      title: "삿포로 가성비 코스",
      cardImg: "../assets/images/busanmatna-card1.jpg",
      costFrom: "85만~",
      // 부산맛나.html CITY_DAYS["sapporo"] 배열(371~389줄)을 그대로 복사
      days: [
        {day:1,date:"D1 · 출발 → 삿포로",dayCost:"항공+이심",stops:[
          {time:"09:00 출발",place:"인천국제공항",lat:37.4602,lng:126.4407,pinColor:"amber",pinLabel:"D1",desc:"삿포로 직항 약 3시간. 가깝고 짧아서 부담 없는 여행 ✈️",cost:"왕복 ₩300,000~",product:{name:"인천-삿포로 왕복 항공권",price:"₩300,000~",tag:"필수",tagBg:"#EDE9FE",tagColor:"#6D28D9",bg:"#EDE9FE",icon:"✈️",city:"삿포로",url:"https://myrealt.rip/ZJow18"}},
          {time:"12:00 도착",place:"신치토세 공항 → 삿포로역",lat:42.7772,lng:141.6929,pinColor:"amber",pinLabel:"D1",desc:"쾌속열차로 36분이면 삿포로역. 이심 미리 개통하면 이동 완벽 대응 📱",cost:"열차 ₩8,000~",product:{name:"일본 이심 (7일, 무제한)",price:"₩13,000",tag:"필수",tagBg:"#FCE7F3",tagColor:"#BE185D",bg:"#FFF0F3",icon:"📱",url:"https://myrealt.rip/ZJozbe"}},
          {time:"저녁",place:"스스키노 라멘 골목",lat:43.0558,lng:141.3548,pinColor:"amber",pinLabel:"D1",desc:"삿포로 미소라멘 꼭 드세요! 스스키노 라멘 골목에서 진한 버터콘 라멘 추천 🍜",cost:"라멘 ₩12,000~",product:null},
        ]},
        {day:2,date:"D2 · 오타루 당일치기",dayCost:"오타루+초밥 약 ₩7만",stops:[
          {time:"09:00",place:"삿포로역 → 오타루 (JR 25분)",lat:43.1908,lng:140.9942,pinColor:"sage",pinLabel:"D2",desc:"JR 쾌속으로 25분. 오타루 시내 걸어다닐 수 있어서 렌트 불필요 🚃",cost:"왕복 ₩9,000~",product:null},
          {time:"오전",place:"오타루 운하 & 창고거리",lat:43.1967,lng:140.9947,pinColor:"sage",pinLabel:"D2",desc:"붉은 벽돌 창고와 운하 반영이 최고 포토스팟. 아침 일찍 가면 사람 없어요 📸",cost:"무료",product:null},
          {time:"점심",place:"오타루 회전초밥 (마사즈시)",lat:43.1925,lng:140.9942,pinColor:"sage",pinLabel:"D2",desc:"홋카이도 신선 해산물 회전초밥. 연어·성게·게 등 1접시 200~500엔. 줄 서도 가치 있어요 🍣",cost:"1인 ₩25,000~",product:null},
          {time:"오후",place:"오타루 오르골당 & 유리공예",lat:43.1940,lng:140.9936,pinColor:"sage",pinLabel:"D2",desc:"100년 역사 오르골 박물관. 미니 오르골이 기념품으로 인기. 체험 제작도 가능 🎵",cost:"₩15,000~",product:null},
        ]},
        {day:3,date:"D3 · 삿포로 맛집 + 귀국",dayCost:"맥주+스프카레 약 ₩5만",stops:[
          {time:"오전",place:"삿포로 맥주박물관",lat:43.0686,lng:141.3744,pinColor:"blush",pinLabel:"D3",desc:"무료 관람 + 유료 시음. 클래식·블랙라벨 등 삿포로 맥주 3종 시음 추천 🍺",cost:"시음 ₩8,000~",product:null},
          {time:"점심",place:"삿포로 스프카레 (스아게+)",lat:43.0680,lng:141.3510,pinColor:"blush",pinLabel:"D3",desc:"삿포로 소울푸드! 닭다리+큰 채소가 통째로 들어간 진한 카레. 본점 추천 🍛",cost:"₩15,000~",product:null},
          {time:"오후",place:"오도리공원 & TV타워",lat:43.0609,lng:141.3556,pinColor:"blush",pinLabel:"D3",desc:"삿포로 한복판 1.5km 공원. 겨울엔 눈 축제 장소! TV타워 전망대에서 파노라마 🗼",cost:"전망대 ₩5,000~",product:null},
          {time:"18:00",place:"신치토세 공항 → 귀국",lat:42.7772,lng:141.6929,pinColor:"blush",pinLabel:"D3",desc:"공항 면세점 로이스 생초콜릿·시로이코이비토 쿠키 필수 구매! 귀국 선물 1티어 🍫",cost:"",product:null},
        ]},
      ],
      // 부산맛나.html CITY_EXPENSE["sapporo"] 객체(390줄)를 그대로 복사
      expense: {title:"삿포로 3박 4일 총경비",food:200000,foodNote:"라멘·초밥·스프카레 홋카이도 식비 3박",defaultFlight:254200,defaultHotel:160000,defaultTotal:1058968,flightNote:"인천-삿포로 직항 기준",flightUrl:"https://myrealt.rip/ZJow18",hotelName:"삿포로역 인근 호텔",hotelNote:"삿포로 시내 2박 1인 기준",hotelUrl:"https://myrealt.rip/ZJpCd0",tours:[{emoji:"⭐",name:"삿포로 비에이 후라노 버스투어 DSLR 촬영 (인디고트래블)",note:"DSLR 사진촬영 포함 버스투어",price:235843,url:"https://myrealt.rip/ZIqQ4e",img:"https://dry7pvlp22cox.cloudfront.net/mrt-images-prod/2024/06/27/tJqk/NLTULKHS59.jpg"},{emoji:"🗼",name:"삿포로 TV 타워 입장권",note:"오도리공원 전망 · 즉시확정",price:18923,url:"https://myrealt.rip/ZIqWb9",img:"https://d2ur7st6jjikze.cloudfront.net/offer_photos/29036/181471_medium_1567648199.jpg?1567648199"},{emoji:"🚂",name:"JR홋카이도 삿포로-노보리베츠 에리어패스 4일권",note:"노보리베츠 온천 왕복 포함",price:190002,url:"https://myrealt.rip/ZIqX03",img:"https://dry7pvlp22cox.cloudfront.net/offer_photos/123042/817671_medium_1684321472.jpg?1684321472"}],toursLabel:"🎫 부산맛나 추천 코스",finePrint:"· 3박 4일 1인 평균값 · 항공 유류세 포함"},
    },
  ],
};
