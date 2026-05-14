# 채널 페이지 템플릿화 — 설계 문서

작성일: 2026-05-14
대상: 마이스토어 크리에이터 채널 페이지

## 배경

`channel-pages-final/done/` 에 크리에이터 채널 페이지 13개가 단일 HTML(인라인 CSS/JS) 형태로 쌓여 있다. 13개 모두 동일한 골격을 공유한다:

- `head`(GA4) → 인라인 CSS(~200줄, 99% 동일) → `body`(프로필 카드 → 쿠폰 배너 → 트립카드 캐러셀 → 링크/필수템 탭 → 경비·일정·쿠폰 패널) → `script`(데이터 + 함수 ~15개)
- JS 함수 로직은 100% 동일, CSS는 `:root` 색상 토큰과 배경이미지 클래스만 다름

문제: 디자인을 한 번 수정하면 여러 파일을 반복해서 손봐야 한다. 신규 크리에이터 페이지가 계속 늘어날수록 이 반복 작업 부담이 커진다.

## 목표

신규 크리에이터 페이지를 만들 때 **데이터만 채우면 완성본 HTML이 생성되는** 템플릿 체계를 만든다.

- 디자인(CSS·레이아웃·JS)은 셸 한 곳에만 존재 — 수정은 한 번, 재빌드로 전체 반영
- 크리에이터마다 바뀌는 것은 **삽입 링크 + 여행 코스/경비 텍스트 + 기본 정보(이름·이미지 등)** 로 한정
- 결과물은 기존과 동일한 독립 HTML — Vercel 배포 방식 변화 없음

## 범위

- 신규 페이지부터만 적용. 기존 13개는 손대지 않으며 별도 체계로 공존한다.
- 일정표·경비 텍스트는 Claude가 크리에이터 영상·게시물·수경님 메모를 요약해 작성한다.
- 이미지·프로필·링크 등 단순 정보는 수경님이 데이터 파일에 직접 입력한다.

## 파일 구조

```
channel-pages-final/
  done/                       완성본 (기존 13개 + 신규 빌드 결과물)
    부산맛나.html              기존 13개는 손대지 않음
    ...
  _template/                  새 템플릿 체계
    shell.html                공유 셸: CSS·JS·HTML 구조 한 벌, 슬롯만 비어있음
    build.js                  빌드 스크립트 (Node 기본 기능만, 설치 패키지 없음)
    data/
      _EXAMPLE.js             작성 가이드 + 예시 (부산맛나 데이터로 채워둠)
      {크리에이터}.js          크리에이터별 데이터 파일 (신규마다 1개)
```

- 셸은 단 하나. CSS/JS/구조 수정은 여기서 한 번만.
- 데이터 파일은 크리에이터당 1개. 디자인과 완전히 분리.
- 빌드 결과물은 `done/`에 독립 HTML로 떨어진다.
- `build.js`는 Node 기본 기능만 사용 — `npm install` 불필요.

## 데이터 파일 스키마

`data/{크리에이터}.js` 한 파일. 수경님이 채우는 구역과 Claude가 채우는 구역을 주석으로 구분한다.

```js
module.exports = {

  // ══════════ 수경님이 채우는 구역 ══════════
  creator: {
    name: "부산맛나",
    tagline: "부산 찐맛집 · 여행 전문탐방 크리에이터",
    email: "ttt0831@naver.com",
    profileImg: "../assets/profiles/부산맛나.jpg",
    heroImg: "../assets/images/busanmatna-hero.jpg",
  },
  theme: "ember",   // 프리셋 이름만 선택 (생략 시 기본값)

  sns: [
    { type:"instagram", url:"https://..." },
    { type:"email", url:"mailto:..." },
  ],

  coupon: {
    showcaseUrl:"https://www.myrealtrip.com/coupons",
    kicker:"부산맛나 팔로워 전용", title:"선착순 할인 쿠폰팩",
    amount:"99,000", count:"8종",
    cards: [ {label,title,desc,expire,remain,url,color}, ... ]
  },

  textblock: { title:"🍜 ...", body:"..." },

  links: [   // 추천 콘텐츠 — 썸네일형/OG카드형 둘 다 지원
    { style:"thumb", icon:"🇯🇵", badges:["경비 총정리"], title:"...", sub:"...", url:"..." },
    { style:"og", img:"https://...", title:"...", url:"..." },
  ],

  products: [  // 필수템 탭 상품 목록
    { name:"...", price:"₩235,843", tag:"강추", icon:"⭐",
      bg:"#FEF3C7", tagColor:"#E07A38", tagBg:"#FDE8CE", city:"삿포로",
      url:"https://myrealt.rip/...", img:"https://..." },
  ],

  // ══════════ Claude가 채우는 구역 (영상·메모 요약) ══════════
  trips: [   // 도시 1개면 1개, 다중 도시면 여러 개 — 트립카드가 개수만큼 생성됨
    {
      city:"sapporo", flag:"🇯🇵",
      badges:["5박 6일","인당 123만원"], title:"삿포로 가성비 코스",
      cardImg:"../assets/images/busanmatna-card1.jpg",
      costFrom:"85만~",
      days: [ {day,date,dayCost,stops:[{time,place,lat,lng,pinColor,pinLabel,desc,cost,product}]} ],
      expense: { title,food,foodNote,defaultFlight,defaultHotel,defaultTotal,
                 flightNote,flightUrl,hotelName,hotelNote,hotelUrl,tours:[...],toursLabel,finePrint }
    },
  ],
};
```

핵심:
- `trips[]` 배열이 단일/다중 도시를 자동 처리. 1개면 트립카드 1장, 2개면 2장. `days`는 기존 `CITY_DAYS`, `expense`는 기존 `CITY_EXPENSE`와 동일 구조.
- `links`는 썸네일형(`thumb`)·OG카드형(`og`) 둘 다 `style` 필드로 지원.
- 수경님 구역은 영상 보고 옮기면 되는 단순 정보, Claude 구역은 요약·구조화가 필요한 부분.

## 색상 프리셋

`build.js` 안에 미리 디자인된 색 조합을 5~6개 정의한다. 데이터 파일에서는 이름만 선택한다.

```js
const THEMES = {
  ember:  { amber:"#C83020", sage:"#E05848", accent:"#7A0A0A" },
  ocean:  { amber:"#1D6FB8", sage:"#3E9BD6", accent:"#0A3A5C" },
  forest: { amber:"#2E7D4F", sage:"#5BA877", accent:"#14502E" },
  // ... 검증된 조합 5~6개
};
// theme 생략 시 기본 프리셋(ember) 사용
```

자유 입력이 아니라 검증된 프리셋만 제공하므로 디자인 일관성이 깨지지 않는다.

## 셸과 빌드 스크립트

### shell.html

부산맛나 페이지 구조를 베이스로, 변하는 부분만 슬롯/반복구역으로 표시한다.

```html
<title>{{NAME}} · 마이스토어</title>
<div class="profile-avatar"><img src="{{PROFILE_IMG}}" alt="{{NAME}}"/></div>
...
<div class="trip-carousel"><!--{{TRIP_CARDS}}--></div>
...
<script>
const products = {{PRODUCTS}};
const CREATOR = {{CREATOR}};
const CITY_DAYS = {{CITY_DAYS}};
const CITY_EXPENSE = {{CITY_EXPENSE}};
// 함수 ~15개는 셸에 그대로 고정 (전 페이지 100% 동일)
</script>
```

- CSS는 셸에 완전 고정.
- 배경 이미지는 지금 방식 그대로 유지한다. 빌드가 기존과 똑같은 형태의 CSS 한 줄(`.hero-cover{...}`, `.tc-hero.{city}{...}`)을 자동 생성해 셸의 전용 슬롯에 끼운다. 디자인 코드 접근 방식은 바꾸지 않는다.

### build.js

`node build.js 부산맛나` 실행 시:

1. `shell.html` + `data/부산맛나.js` 읽기
2. 색상 프리셋 적용 — `theme` 이름으로 `THEMES`에서 토큰 조회, `:root` 슬롯 주입
3. 배경 이미지 CSS 생성 — `heroImg` 및 각 `trips[].cardImg`로 CSS 한 줄씩 생성해 슬롯 주입
4. 반복구역 렌더링 — `sns[]`→SNS 아이콘, `trips[]`→트립카드, `links[]`→링크 항목, `coupon.cards[]`→쿠폰 카드
5. `<script>` 안에 `products` / `CREATOR` / `CITY_DAYS` / `CITY_EXPENSE` 주입 — `CITY_DAYS`·`CITY_EXPENSE`는 `trips[]`에서 `city`를 키로 자동 조립
6. `done/부산맛나.html` 완성본 출력

- 의존 패키지 없음 — Node 기본 문자열 치환만 사용.
- 빌드는 Claude가 실행. 수경님은 데이터 파일만 작성.

## 새 크리에이터 추가 워크플로우

크리에이터 "김여행" 추가 예시:

1. 수경님 — `data/_EXAMPLE.js`를 복사해 `data/김여행.js` 생성, 수경님 구역 채우기 (이름·태그라인·이메일·이미지 경로·테마 프리셋·SNS·쿠폰·말풍선·추천 링크·필수템 상품)
2. 수경님 — 김여행 크리에이터의 영상 URL 또는 정리한 메모를 Claude에게 전달
3. Claude — 영상·메모를 요약해 `trips[]` 구역(트립카드·일정표·경비) 작성
4. Claude — `node build.js 김여행` 실행 → `done/김여행.html` 생성
5. 수경님 — 브라우저로 결과 확인, OK면 배포 요청 (배포는 명시적 요청 시에만)

### 유지보수

- 디자인 변경 시 `shell.html` 한 곳만 수정 → `node build.js` 전체 재빌드 → 모든 신규 페이지 일괄 반영.
- 기존 13개는 영향 없음.

## 검증 방법

- `_EXAMPLE.js`(부산맛나 데이터)로 빌드한 결과물이 기존 `done/부산맛나.html`과 시각적으로 동일한지 브라우저에서 비교한다. (구조·코드는 다를 수 있으나 화면 출력은 일치해야 함)
- 단일 도시(트립카드 1장)·다중 도시(트립카드 2장) 두 경우 모두 빌드가 정상 동작하는지 확인한다.
- 일정표 패널, 경비 패널, 쿠폰 패널, 탭 전환, 캐러셀 화살표/dots가 모두 동작하는지 확인한다.

## 비고

- 기존 13개 페이지 마이그레이션은 범위 밖. 추후 필요 시 별도 작업으로 진행한다.
- `_template/` 폴더는 Vercel 배포 대상이 아니므로 필요 시 `.vercelignore` 등록을 검토한다.
