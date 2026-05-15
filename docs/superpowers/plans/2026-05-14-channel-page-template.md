# 채널 페이지 템플릿화 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 신규 크리에이터 채널 페이지를 데이터 파일만 채우면 완성본 HTML이 생성되는 셸+빌드 스크립트 체계를 만든다.

**Architecture:** 공유 셸(`shell.html`)에 디자인(CSS·JS·구조)을 고정하고, 크리에이터별 데이터(`data/{이름}.js`)를 빌드 스크립트(`build.js`)가 셸에 주입해 `done/{이름}.html` 완성본을 생성한다. 결과물은 기존 13개 페이지와 동일한 독립 HTML이다.

**Tech Stack:** 순수 Node.js(설치 패키지 없음, 빌드는 문자열 치환), Node 내장 테스트 러너(`node:test`/`node:assert`), 인라인 HTML/CSS/JS.

**참고 문서:** `docs/superpowers/specs/2026-05-14-channel-page-template-design.md`

**소스 기준 파일:**
- 구조·CSS 기준: `channel-pages-final/done/부산맛나.html` (단일 도시, 가장 단순한 407줄)
- 스크립트·다중도시 기준: `channel-pages-final/done/파파트래블.html` (다중 도시, 트립카드 2장)

---

## File Structure

| 파일 | 역할 |
|------|------|
| `channel-pages-final/_template/shell.html` | 공유 셸. CSS·JS·HTML 구조 한 벌. 변하는 부분은 슬롯(`{{...}}`, `<!--{{...}}-->`)으로 비워둠 |
| `channel-pages-final/_template/build.js` | 빌드 스크립트. `buildPage(data)` 순수 함수 + CLI 진입점 |
| `channel-pages-final/_template/build.test.js` | `node:test` 기반 빌드 검증 테스트 |
| `channel-pages-final/_template/data/_EXAMPLE.js` | 예시 데이터 파일. 부산맛나 데이터를 신규 스키마로 작성. 작성 가이드 겸 빌드 테스트 입력 |
| `channel-pages-final/_template/data/{크리에이터}.js` | (이후 신규마다 추가) 크리에이터별 데이터 파일 |
| `channel-pages-final/done/{크리에이터}.html` | 빌드 산출물 |

### 셸 슬롯 목록 (Task 1에서 확정, 이후 Task에서 참조)

**단순 텍스트 슬롯** (`html.split(key).join(value)`로 전체 치환):
- `{{NAME}}` — 제목, 프로필 h2, img alt, 푸터
- `{{TAGLINE}}` — 프로필 소개 문구
- `{{EMAIL}}` — SNS 이메일 href, 푸터 메일
- `{{PROFILE_IMG}}` — 프로필 아바타 + 말풍선 아바타 img src
- `{{HERO_IMG}}` — CSS `.hero-cover` 배경
- `{{C_AMBER}}` `{{C_SAGE}}` `{{C_ACCENT}}` — CSS `:root` 색상 토큰
- `{{COUPON_URL}}` — 쿠폰 쇼케이스 배너 href
- `{{COUPON_KICKER}}` `{{COUPON_TITLE}}` `{{COUPON_AMOUNT}}` `{{COUPON_COUNT}}` — 쿠폰 배너 텍스트
- `{{TEXTBLOCK_TITLE}}` `{{TEXTBLOCK_BODY}}` — 링크탭 말풍선

**반복 구역 슬롯** (생성된 HTML로 치환):
- `<!--{{SNS_PILLS}}-->` — SNS 아이콘들
- `/*{{BG_CSS}}*/` — 트립카드 배경 이미지 CSS 규칙들
- `<!--{{TRIP_CARDS}}-->` — 트립카드들
- `<!--{{TRIP_DOTS}}-->` — 캐러셀 dot들
- `<!--{{LINK_SECTIONS}}-->` — 링크 섹션들
- `<!--{{COUPON_CARDS}}-->` — 쿠폰 패널 카드들

**스크립트 데이터 슬롯** (JSON으로 치환):
- `{{CREATOR_JSON}}` `{{PRODUCTS_JSON}}` `{{CITY_DAYS_JSON}}` `{{CITY_EXPENSE_JSON}}` `{{TRIP_KEYS_JSON}}`

---

## Task 1: 디렉토리 구조 + 셸 HTML 생성

**Files:**
- Create: `channel-pages-final/_template/shell.html`

셸은 `부산맛나.html`을 복사한 뒤 아래 변환을 정확히 적용한다. `부산맛나.html`은 단일 도시 페이지라 스크립트가 단순하므로, `<script>` 블록만 다중 도시 지원 버전(`파파트래블.html` 기준)으로 교체한다.

- [ ] **Step 1: 디렉토리 생성 및 셸 베이스 복사**

```bash
mkdir -p channel-pages-final/_template/data
cp channel-pages-final/done/부산맛나.html channel-pages-final/_template/shell.html
```

- [ ] **Step 2: CSS 영역 변환**

`shell.html`의 `<style>` 안에서 아래를 수정한다.

1. `:root` 줄의 색상 토큰을 슬롯으로:
   - `--amber:#C83020` → `--amber:{{C_AMBER}}`
   - `--sage:#E05848` → `--sage:{{C_SAGE}}`
   - `--accent:#7A0A0A` → `--accent:{{C_ACCENT}}`
2. `.hero-cover` 규칙의 배경 URL을 슬롯으로:
   - `background:url('../assets/images/busanmatna-hero.jpg')` → `background:url('{{HERO_IMG}}')`
3. `.tc-hero.busanmatna-sapporo{background:url('../assets/images/busanmatna-card1.jpg') center/cover no-repeat}` 줄 **전체를** 다음으로 교체:
   - `/*{{BG_CSS}}*/`
4. 트립 화살표 CSS를 추가한다. `.trip-dot.on{...}` 규칙 바로 다음 줄에 아래 3줄을 삽입:

```css
.trip-arrow{width:28px;height:28px;border-radius:50%;background:#fff;border:1px solid var(--border);display:flex;align-items:center;justify-content:center;font-size:14px;color:var(--text);font-weight:800;cursor:pointer;padding:0;padding-bottom:2px;box-shadow:0 2px 6px rgba(0,0,0,.06);transition:opacity .2s,transform .15s}
.trip-arrow:hover{transform:scale(1.08);background:#fff3e8;color:var(--amber)}
.trip-arrow:disabled{opacity:.3;pointer-events:none}
.trip-arrow{display:none}
```

(마지막 `.trip-arrow{display:none}`은 의도적으로 화살표를 숨김 — 메모리 `feedback_trip_carousel_arrows` 참조. 나중에 이 한 줄만 지우면 화살표가 보임.)

- [ ] **Step 3: `<head>`·프로필·쿠폰 배너 영역 변환**

1. `<title>부산맛나 · 마이스토어</title>` → `<title>{{NAME}} · 마이스토어</title>`
2. `<div class="profile-avatar"><img src="../assets/profiles/부산맛나.jpg" alt="부산맛나"/></div>` → `<div class="profile-avatar"><img src="{{PROFILE_IMG}}" alt="{{NAME}}"/></div>`
3. `<h2>부산맛나</h2>` → `<h2>{{NAME}}</h2>`
4. `<p>부산 찐맛집 · 여행 전문탐방 크리에이터</p>` → `<p>{{TAGLINE}}</p>`
5. `<div class="sns-pills">` 의 **자식 `<a>` 들 전체를** 다음 한 줄로 교체 (`<div class="sns-pills">`와 닫는 `</div>`는 유지):
   - `<!--{{SNS_PILLS}}-->`
6. `<a class="coupon-showcase" href="https://www.myrealtrip.com/coupons" target="_blank">` → `<a class="coupon-showcase" href="{{COUPON_URL}}" target="_blank">`
7. `<div class="cs-kicker">부산맛나 팔로워 전용</div>` → `<div class="cs-kicker">{{COUPON_KICKER}}</div>`
8. `<div class="cs-title">선착순 할인 쿠폰팩</div>` → `<div class="cs-title">{{COUPON_TITLE}}</div>`
9. `<span class="cs-amt">99,000</span>` → `<span class="cs-amt">{{COUPON_AMOUNT}}</span>`
10. `<span class="cs-stamp-num">8종</span>` → `<span class="cs-stamp-num">{{COUPON_COUNT}}</span>`

- [ ] **Step 4: 트립 캐러셀 영역 변환**

1. `<div class="trip-carousel">` → `<div class="trip-carousel" id="trip-carousel">`
2. `<div class="trip-carousel" id="trip-carousel">` 의 **자식 `.trip-card` 전체를** 다음 한 줄로 교체:
   - `<!--{{TRIP_CARDS}}-->`
3. `<div class="trip-nav"><div class="trip-dots"><span class="trip-dot on"></span></div></div>` 줄 **전체를** 다음으로 교체:

```html
<div class="trip-nav"><button class="trip-arrow" id="trip-prev" aria-label="이전" onclick="tripScroll(-1)">‹</button><div class="trip-dots" id="trip-dots"><!--{{TRIP_DOTS}}--></div><button class="trip-arrow" id="trip-next" aria-label="다음" onclick="tripScroll(1)">›</button></div>
```

- [ ] **Step 5: 링크탭·푸터·쿠폰 패널 영역 변환**

1. `ls-tb-avatar` 안의 `<img src="../assets/profiles/부산맛나.jpg" ...>` 의 src를 `{{PROFILE_IMG}}` 로 교체
2. `<div class="ls-tb-title">🍜 부산 찐맛집부터 해외 여행 전문탐방까지</div>` → `<div class="ls-tb-title">{{TEXTBLOCK_TITLE}}</div>`
3. `ls-tb-bubble` 안에서 `ls-tb-title` div 다음의 본문 텍스트("부산의 찐 맛집을 탐방하며…완전 정복!")를 `{{TEXTBLOCK_BODY}}` 로 교체
4. `<div class="links-section">` 부터 그 닫는 `</div>` 까지 (h3 + ls-thumb 포함한 블록 전체)와 바로 뒤 `<div class="links-section-pb"></div>` 를 **합쳐서** 다음으로 교체:
   - `<!--{{LINK_SECTIONS}}--><div class="links-section-pb"></div>`
5. `bio-footer`: `<a class="bio-footer-mail" href="mailto:ttt0831@naver.com">ttt0831@naver.com</a>` → `<a class="bio-footer-mail" href="mailto:{{EMAIL}}">{{EMAIL}}</a>`
6. `<div class="bio-footer-meta">© 2026 부산맛나 · myrealtrip</div>` → `<div class="bio-footer-meta">© 2026 {{NAME}} · myrealtrip</div>`
7. `coupon-panel`: `<div class="sheet-sub">부산맛나 통해 예약하면 받을 수 있는 혜택</div>` → `<div class="sheet-sub">{{NAME}} 통해 예약하면 받을 수 있는 혜택</div>`
8. `coupon-sheet` 안의 두 개 `<div class="coupon-card">...</div>` 를 **합쳐서** 다음 한 줄로 교체:
   - `<!--{{COUPON_CARDS}}-->`

- [ ] **Step 6: `<script>` 블록 전체 교체**

`부산맛나.html`의 `<script>...</script>` 블록(단일 도시용)을 `파파트래블.html`의 `<script>...</script>` 블록(다중 도시용, 487~644줄)으로 통째로 교체한 뒤, 아래 변경을 적용한다.

1. `const CREATOR={name:"파파트래블",...};` → `const CREATOR={{CREATOR_JSON}};`
2. `const products=[ ... ];` (490~504줄) → `const products={{PRODUCTS_JSON}};`
3. `const CITY_DAYS={ ... };` (506~569줄) → `const CITY_DAYS={{CITY_DAYS_JSON}};`
4. `const CITY_EXPENSE={ ... };` (571~617줄) → `const CITY_EXPENSE={{CITY_EXPENSE_JSON}};`
5. `let currentExpenseCity="hongkong";` 와 `const TRIP_KEYS=["hongkong","ishigaki"];let currentTripIdx=0;` 두 줄을 다음으로 교체:
   - `const TRIP_KEYS={{TRIP_KEYS_JSON}};let currentTripIdx=0;let currentExpenseCity=TRIP_KEYS[0];`
6. `let currentDay=1;let currentCourseCity="hongkong";` → `let currentDay=1;let currentCourseCity=TRIP_KEYS[0];`
7. `openCourse` 함수에서:
   - `city=city||"hongkong";` → `city=city||TRIP_KEYS[0];`
   - `document.querySelector(".panel-title").textContent=city==="ishigaki"?"이시가키 추천 코스":"홍콩 추천 코스";` → `document.getElementById("course-panel-title").textContent=(CITY_EXPENSE[city]&&CITY_EXPENSE[city].title)||"추천 코스";`
8. `openExpensePanel` 함수에서:
   - `city=city||"gochang";` → `city=city||TRIP_KEYS[0];`
   - 하드코딩된 `<span class="exp-live-tag">파파 추천</span>` 2곳을 모두 `<span class="exp-live-tag">${CREATOR.name} 추천</span>` 로 교체

(`부산맛나.html`의 course-panel은 `<div class="panel-title" id="course-panel-title">` 처럼 id가 이미 있으므로 7번 변경이 동작한다. 셸의 course-panel 영역은 부산맛나 원본 그대로 두면 된다.)

- [ ] **Step 7: 셸 검증**

```bash
cd channel-pages-final/_template
grep -c '부산맛나\|파파트래블\|busanmatna\|hongkong\|ishigaki' shell.html
```

Expected: `0` (크리에이터 고유 데이터가 모두 슬롯으로 치환됨)

```bash
grep -o '{{[A-Z_]*}}\|<!--{{[A-Z_]*}}-->\|/\*{{BG_CSS}}\*/' shell.html | sort -u
```

Expected: 위 "셸 슬롯 목록"의 모든 슬롯이 출력됨 (`{{NAME}}` `{{TAGLINE}}` `{{EMAIL}}` `{{PROFILE_IMG}}` `{{HERO_IMG}}` `{{C_AMBER}}` `{{C_SAGE}}` `{{C_ACCENT}}` `{{COUPON_URL}}` `{{COUPON_KICKER}}` `{{COUPON_TITLE}}` `{{COUPON_AMOUNT}}` `{{COUPON_COUNT}}` `{{TEXTBLOCK_TITLE}}` `{{TEXTBLOCK_BODY}}` `{{CREATOR_JSON}}` `{{PRODUCTS_JSON}}` `{{CITY_DAYS_JSON}}` `{{CITY_EXPENSE_JSON}}` `{{TRIP_KEYS_JSON}}` 및 `<!--{{SNS_PILLS}}-->` `<!--{{TRIP_CARDS}}-->` `<!--{{TRIP_DOTS}}-->` `<!--{{LINK_SECTIONS}}-->` `<!--{{COUPON_CARDS}}-->` `/*{{BG_CSS}}*/`)

- [ ] **Step 8: 커밋**

```bash
git add channel-pages-final/_template/shell.html
git commit -m "feat: 채널 페이지 공유 셸 템플릿 추가"
```

---

## Task 2: 예시 데이터 파일 `_EXAMPLE.js` 생성

**Files:**
- Create: `channel-pages-final/_template/data/_EXAMPLE.js`

`부산맛나.html`의 데이터를 신규 스키마로 옮긴다. 큰 데이터 블록(`products`, `days`, `expense`)은 `부산맛나.html`에서 그대로 복사한다.

- [ ] **Step 1: `_EXAMPLE.js` 작성**

아래 내용으로 파일을 만든다. `products` 배열은 `부산맛나.html` 353~362줄의 객체 10개를 그대로 복사해 넣는다. `trips[0].days` 는 `부산맛나.html`의 `CITY_DAYS["sapporo"]` 배열(371~389줄)을 그대로 복사한다. `trips[0].expense` 는 `CITY_EXPENSE["sapporo"]` 객체(390줄)를 그대로 복사한다.

```js
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
      { label:"마이리얼트립 파트너 혜택", title:"첫 예약 3,000원 할인",
        desc:"5만원 이상 결제 시 · 1회 사용 가능", expire:"유효기간: 2026.06.30까지",
        remain:"잔여 47장", url:"https://www.myrealtrip.com/coupons", color:"var(--amber)" },
      { label:"재방문 감사 쿠폰", title:"2번째 예약 5% 할인",
        desc:"최대 1만원 · 부산맛나 전용", expire:"유효기간: 2026.07.31까지",
        remain:"잔여 23장", url:"https://www.myrealtrip.com/coupons", color:"var(--sage)" },
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
      ],
    },
  ],

  // 필수템 탭 상품 목록 — 부산맛나.html 353~362줄의 객체 10개를 그대로 복사
  products: [
    /* 부산맛나.html 353~362줄 products 배열 객체 10개 복사 */
  ],

  // ══════════ Claude가 채우는 구역 (영상·메모 요약) ══════════
  trips: [
    {
      city: "sapporo",
      flag: "🇯🇵",
      badges: ["5박 6일", "인당 123만원"],
      title: "삿포로 가성비 코스",
      cardImg: "../assets/images/busanmatna-card1.jpg",
      costFrom: "85만~",
      // 부산맛나.html CITY_DAYS["sapporo"] 배열(371~389줄)을 그대로 복사
      days: [
        /* CITY_DAYS["sapporo"] 복사 */
      ],
      // 부산맛나.html CITY_EXPENSE["sapporo"] 객체(390줄)를 그대로 복사
      expense: {
        /* CITY_EXPENSE["sapporo"] 복사 */
      },
    },
  ],
};
```

- [ ] **Step 2: 데이터 파일 로드 검증**

```bash
cd channel-pages-final/_template
node -e "const d=require('./data/_EXAMPLE.js'); console.log(d.creator.name, d.trips.length, d.products.length, d.trips[0].days.length, Object.keys(d.trips[0].expense).length)"
```

Expected: `부산맛나 1 10 3 14` (이름, 트립 1개, 상품 10개, 일정 3일치, 경비 객체 키 14개)

- [ ] **Step 3: 커밋**

```bash
git add channel-pages-final/_template/data/_EXAMPLE.js
git commit -m "feat: 채널 페이지 예시 데이터 파일 추가 (부산맛나)"
```

---

## Task 3: `build.js` 골격 + 단순 슬롯 + 색상 프리셋 + 배경 CSS

**Files:**
- Create: `channel-pages-final/_template/build.js`
- Create: `channel-pages-final/_template/build.test.js`

- [ ] **Step 1: 실패하는 테스트 작성**

`build.test.js`:

```js
const { test } = require('node:test');
const assert = require('node:assert');
const { buildPage } = require('./build.js');
const data = require('./data/_EXAMPLE.js');

test('단순 슬롯: 크리에이터 이름·태그라인이 치환된다', () => {
  const html = buildPage(data);
  assert.ok(html.includes('<title>부산맛나 · 마이스토어</title>'));
  assert.ok(html.includes('<h2>부산맛나</h2>'));
  assert.ok(html.includes('<p>부산 찐맛집 · 여행 전문탐방 크리에이터</p>'));
  assert.ok(!html.includes('{{NAME}}'));
  assert.ok(!html.includes('{{TAGLINE}}'));
});

test('색상 프리셋: theme 이름이 토큰 값으로 치환된다', () => {
  const html = buildPage(data);
  assert.ok(html.includes('--amber:#C83020'));
  assert.ok(html.includes('--sage:#E05848'));
  assert.ok(html.includes('--accent:#7A0A0A'));
  assert.ok(!html.includes('{{C_AMBER}}'));
});

test('배경 CSS: 트립별 .tc-hero 규칙이 생성된다', () => {
  const html = buildPage(data);
  assert.ok(html.includes(".tc-hero.sapporo{background:url('../assets/images/busanmatna-card1.jpg') center/cover no-repeat}"));
  assert.ok(html.includes("background:url('../assets/images/busanmatna-hero.jpg')"));
  assert.ok(!html.includes('/*{{BG_CSS}}*/'));
});
```

- [ ] **Step 2: 테스트 실패 확인**

Run: `cd channel-pages-final/_template && node --test`
Expected: FAIL — `Cannot find module './build.js'`

- [ ] **Step 3: `build.js` 작성 (골격 + 단순 슬롯 + 프리셋 + 배경 CSS)**

```js
const fs = require('fs');
const path = require('path');

const THEMES = {
  ember:  { amber:'#C83020', sage:'#E05848', accent:'#7A0A0A' },
  ocean:  { amber:'#1D6FB8', sage:'#3E9BD6', accent:'#0A3A5C' },
  forest: { amber:'#2E7D4F', sage:'#5BA877', accent:'#14502E' },
  grape:  { amber:'#7C3AED', sage:'#A78BDA', accent:'#4C1D95' },
  rose:   { amber:'#D6336C', sage:'#E885A8', accent:'#8C1D40' },
  slate:  { amber:'#475569', sage:'#7B8A9E', accent:'#1E293B' },
};

function esc(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function renderBgCss(trips) {
  return trips
    .map(t => `.tc-hero.${t.city}{background:url('${t.cardImg}') center/cover no-repeat}`)
    .join('\n');
}

function buildPage(data) {
  let html = fs.readFileSync(path.join(__dirname, 'shell.html'), 'utf8');
  const theme = THEMES[data.theme] || THEMES.ember;

  const repl = {
    '{{NAME}}': data.creator.name,
    '{{TAGLINE}}': data.creator.tagline,
    '{{EMAIL}}': data.creator.email,
    '{{PROFILE_IMG}}': data.creator.profileImg,
    '{{HERO_IMG}}': data.creator.heroImg,
    '{{C_AMBER}}': theme.amber,
    '{{C_SAGE}}': theme.sage,
    '{{C_ACCENT}}': theme.accent,
    '{{COUPON_URL}}': data.coupon.showcaseUrl,
    '{{COUPON_KICKER}}': data.coupon.kicker,
    '{{COUPON_TITLE}}': data.coupon.title,
    '{{COUPON_AMOUNT}}': data.coupon.amount,
    '{{COUPON_COUNT}}': data.coupon.count,
    '{{TEXTBLOCK_TITLE}}': data.textblock.title,
    '{{TEXTBLOCK_BODY}}': data.textblock.body,
    '/*{{BG_CSS}}*/': renderBgCss(data.trips),
  };

  for (const [k, v] of Object.entries(repl)) {
    html = html.split(k).join(v);
  }
  return html;
}

module.exports = { buildPage, THEMES };
```

- [ ] **Step 4: 테스트 통과 확인**

Run: `cd channel-pages-final/_template && node --test`
Expected: PASS — 3 tests passed

- [ ] **Step 5: 커밋**

```bash
git add channel-pages-final/_template/build.js channel-pages-final/_template/build.test.js
git commit -m "feat: 빌드 스크립트 골격 - 단순 슬롯·색상 프리셋·배경 CSS"
```

---

## Task 4: `build.js` 반복 구역 렌더링 (SNS·트립카드·dots·링크섹션·쿠폰카드)

**Files:**
- Modify: `channel-pages-final/_template/build.js`
- Modify: `channel-pages-final/_template/build.test.js`

- [ ] **Step 1: 실패하는 테스트 추가**

`build.test.js` 끝에 추가:

```js
test('SNS pills: 인스타·이메일 아이콘이 생성된다', () => {
  const html = buildPage(data);
  assert.ok(html.includes('href="https://www.instagram.com/busan_matna_/"'));
  assert.ok(html.includes('../assets/icons/insta.png'));
  assert.ok(html.includes('href="mailto:ttt0831@naver.com" title="이메일 문의">✉️</a>'));
  assert.ok(!html.includes('<!--{{SNS_PILLS}}-->'));
});

test('트립카드: 카드와 dot이 트립 개수만큼 생성된다', () => {
  const html = buildPage(data);
  assert.ok(html.includes('<div class="tc-hero sapporo">'));
  assert.ok(html.includes('<div class="tc-title">삿포로 가성비 코스</div>'));
  assert.ok(html.includes("onclick=\"openCourse('sapporo')\""));
  assert.ok(html.includes("onclick=\"openExpensePanel('sapporo')\""));
  assert.ok(html.includes('<span class="tc-c-num">85만~</span>'));
  assert.ok(html.includes('<span class="tc-badge">5박 6일</span>'));
  assert.ok(html.includes('<span class="trip-dot on"></span>'));
  assert.ok(!html.includes('<!--{{TRIP_CARDS}}-->'));
  assert.ok(!html.includes('<!--{{TRIP_DOTS}}-->'));
});

test('링크 섹션: h3 제목과 thumb 항목이 생성된다', () => {
  const html = buildPage(data);
  assert.ok(html.includes('<h3>📸 추천 콘텐츠</h3>'));
  assert.ok(html.includes('class="ls-thumb" href="https://www.instagram.com/reel/DSCL2k-EpkW/"'));
  assert.ok(html.includes('<span class="ls-badge hot">경비 총정리</span>'));
  assert.ok(html.includes('<div class="ls-thumb-title">삿포로 5박6일 인당 123만원</div>'));
  assert.ok(!html.includes('<!--{{LINK_SECTIONS}}-->'));
});

test('쿠폰 카드: 쿠폰 패널 카드가 생성된다', () => {
  const html = buildPage(data);
  assert.ok(html.includes('<div class="cc-title">첫 예약 3,000원 할인</div>'));
  assert.ok(html.includes('<div class="cc-title">2번째 예약 5% 할인</div>'));
  assert.ok(html.includes('<div class="cc-stripe" style="background:var(--amber)"></div>'));
  assert.ok(!html.includes('<!--{{COUPON_CARDS}}-->'));
});
```

- [ ] **Step 2: 테스트 실패 확인**

Run: `cd channel-pages-final/_template && node --test`
Expected: FAIL — 새 테스트 4개가 `<!--{{...}}-->` 슬롯이 남아있어 실패

- [ ] **Step 3: 렌더링 함수 추가 및 `buildPage` 확장**

`build.js`의 `esc` 함수 아래에 렌더링 함수들을 추가한다:

```js
const SNS_ICONS = {
  instagram: '../assets/icons/insta.png',
  youtube:   '../assets/icons/youtube.png',
  tiktok:    '../assets/icons/tiktok-logo.png',
  threads:   '../assets/icons/threads-logo.png',
  blog:      '../assets/icons/blog.png',
};

function renderSnsPills(sns) {
  return sns.map(s => {
    if (s.type === 'email') {
      return `<a class="sns-icon" href="${s.url}" title="이메일 문의">✉️</a>`;
    }
    const icon = SNS_ICONS[s.type] || SNS_ICONS.instagram;
    const label = s.type.charAt(0).toUpperCase() + s.type.slice(1);
    return `<a class="sns-icon" href="${s.url}" target="_blank" aria-label="${label}"><img src="${icon}" alt="${label}"/></a>`;
  }).join('\n            ');
}

function renderTripCards(trips) {
  return trips.map(t => {
    const badges = t.badges.map(b => `<span class="tc-badge">${esc(b)}</span>`).join('');
    return `<div class="trip-card">
          <div class="tc-hero ${t.city}">
            <div class="tc-hero-content">
              <div class="tc-flag">${t.flag}</div>
              <div class="tc-title-col">
                <div class="tc-badges">${badges}</div>
                <div class="tc-title">${esc(t.title)}</div>
              </div>
            </div>
          </div>
          <div class="tc-body">
            <div class="tc-ask">어디부터 볼까요?</div>
            <div class="tc-choice">
              <button class="plan" onclick="openCourse('${t.city}')">
                <div><strong>일정표 보기</strong><span>DAY별 동선 확인</span></div>
                <div class="tc-arr">›</div>
              </button>
              <button class="cost" onclick="openExpensePanel('${t.city}')">
                <div class="tc-c-row1"><strong>상세 경비 보기</strong><div class="tc-c-price"><span class="tc-c-num">${esc(t.costFrom)}</span><span class="tc-arr" style="margin-left:0">›</span></div></div>
                <div class="tc-c-row2"><span class="tc-c-badge">🔥 인기</span><span class="tc-c-sub">항공·숙소·투어 한 번에</span></div>
              </button>
            </div>
          </div>
        </div>`;
  }).join('\n        ');
}

function renderTripDots(trips) {
  return trips.map((t, i) => `<span class="trip-dot${i === 0 ? ' on' : ''}"></span>`).join('');
}

function renderLinkSections(sections) {
  return sections.map(sec => {
    const items = sec.items.map(it => {
      const badges = (it.badges || [])
        .map(b => `<span class="ls-badge ${b.style || 'hot'}">${esc(b.text)}</span>`)
        .join('');
      if (it.type === 'og') {
        return `<a class="ls-og" href="${it.url}" target="_blank">
          <img src="${it.img}" style="width:100%;height:150px;object-fit:cover;display:block"/>
          <div class="ls-og-body">
            ${badges ? `<div class="ls-badges">${badges}</div>` : ''}
            <div class="ls-og-title">${esc(it.title)}</div>
            <div class="ls-og-domain">${esc(it.domain || '')}</div>
          </div>
        </a>`;
      }
      return `<a class="ls-thumb" href="${it.url}" target="_blank">
          <div class="ls-thumb-icon">${it.icon || ''}</div>
          <div class="ls-thumb-body">
            ${badges ? `<div class="ls-badges">${badges}</div>` : ''}
            <div class="ls-thumb-title">${esc(it.title)}</div>
            ${it.sub ? `<div class="ls-thumb-sub">${esc(it.sub)}</div>` : ''}
          </div>
          <div class="ls-thumb-arrow">›</div>
        </a>`;
    }).join('\n        ');
    return `<div class="links-section">
        <h3>${esc(sec.heading)}</h3>
        ${items}
      </div>`;
  }).join('\n      ');
}

function renderCouponCards(cards) {
  return cards.map(c =>
    `<div class="coupon-card"><div class="cc-stripe" style="background:${c.color}"></div><div class="cc-body"><div class="cc-label" style="color:${c.color}">${esc(c.label)}</div><div class="cc-title">${esc(c.title)}</div><div class="cc-desc">${esc(c.desc)}</div><div class="cc-footer"><div class="cc-expire">${esc(c.expire)}</div><div class="cc-remain">${esc(c.remain)}</div></div></div><button class="cc-btn" style="background:${c.color}" onclick="window.open('${c.url}','_blank')">받기</button></div>`
  ).join('\n      ');
}
```

그리고 `buildPage`의 `repl` 객체에 아래 항목을 추가한다 (`'/*{{BG_CSS}}*/'` 줄 다음):

```js
    '<!--{{SNS_PILLS}}-->': renderSnsPills(data.sns),
    '<!--{{TRIP_CARDS}}-->': renderTripCards(data.trips),
    '<!--{{TRIP_DOTS}}-->': renderTripDots(data.trips),
    '<!--{{LINK_SECTIONS}}-->': renderLinkSections(data.linkSections),
    '<!--{{COUPON_CARDS}}-->': renderCouponCards(data.coupon.cards),
```

- [ ] **Step 4: 테스트 통과 확인**

Run: `cd channel-pages-final/_template && node --test`
Expected: PASS — 7 tests passed

- [ ] **Step 5: 커밋**

```bash
git add channel-pages-final/_template/build.js channel-pages-final/_template/build.test.js
git commit -m "feat: 빌드 스크립트 반복 구역 렌더링 - SNS·트립카드·링크·쿠폰"
```

---

## Task 5: `build.js` 스크립트 데이터 주입 + CLI 진입점

**Files:**
- Modify: `channel-pages-final/_template/build.js`
- Modify: `channel-pages-final/_template/build.test.js`

- [ ] **Step 1: 실패하는 테스트 추가**

`build.test.js` 끝에 추가:

```js
test('스크립트 데이터: CREATOR·CITY_DAYS·CITY_EXPENSE·TRIP_KEYS가 주입된다', () => {
  const html = buildPage(data);
  assert.ok(html.includes('const CREATOR={"name":"부산맛나","email":"ttt0831@naver.com","couponUrl":"https://www.myrealtrip.com/coupons"};'));
  assert.ok(html.includes('const TRIP_KEYS=["sapporo"];'));
  assert.ok(html.includes('"sapporo":'));            // CITY_DAYS / CITY_EXPENSE 키
  assert.ok(html.includes('"삿포로 3박 4일 총경비"')); // CITY_EXPENSE 내용
  assert.ok(!html.includes('{{CREATOR_JSON}}'));
  assert.ok(!html.includes('{{PRODUCTS_JSON}}'));
  assert.ok(!html.includes('{{CITY_DAYS_JSON}}'));
  assert.ok(!html.includes('{{CITY_EXPENSE_JSON}}'));
  assert.ok(!html.includes('{{TRIP_KEYS_JSON}}'));
});

test('최종 산출물: 미치환 슬롯이 하나도 없다', () => {
  const html = buildPage(data);
  assert.ok(!/\{\{[A-Z_]+\}\}/.test(html), '치환 안 된 {{슬롯}} 발견');
  assert.ok(!html.includes('<!--{{'), '치환 안 된 <!--{{슬롯}}--> 발견');
  assert.ok(!html.includes('/*{{'), '치환 안 된 /*{{슬롯}}*/ 발견');
});
```

- [ ] **Step 2: 테스트 실패 확인**

Run: `cd channel-pages-final/_template && node --test`
Expected: FAIL — 새 테스트 2개가 `{{CREATOR_JSON}}` 등 슬롯이 남아 실패

- [ ] **Step 3: `buildPage`에 스크립트 데이터 주입 추가**

`buildPage` 함수에서 `const theme = ...` 줄 다음에 아래를 추가한다:

```js
  const cityDays = Object.fromEntries(data.trips.map(t => [t.city, t.days]));
  const cityExpense = Object.fromEntries(data.trips.map(t => [t.city, t.expense]));
  const tripKeys = data.trips.map(t => t.city);
  const creator = {
    name: data.creator.name,
    email: data.creator.email,
    couponUrl: data.coupon.showcaseUrl,
  };
```

그리고 `repl` 객체에 아래 항목을 추가한다 (`'<!--{{COUPON_CARDS}}-->'` 줄 다음):

```js
    '{{CREATOR_JSON}}': JSON.stringify(creator),
    '{{PRODUCTS_JSON}}': JSON.stringify(data.products),
    '{{CITY_DAYS_JSON}}': JSON.stringify(cityDays),
    '{{CITY_EXPENSE_JSON}}': JSON.stringify(cityExpense),
    '{{TRIP_KEYS_JSON}}': JSON.stringify(tripKeys),
```

- [ ] **Step 4: 테스트 통과 확인**

Run: `cd channel-pages-final/_template && node --test`
Expected: PASS — 9 tests passed

- [ ] **Step 5: CLI 진입점 추가**

`build.js` 맨 아래 `module.exports = ...` 줄 **바로 앞**에 추가한다:

```js
if (require.main === module) {
  const name = process.argv[2];
  if (!name) {
    console.error('사용법: node build.js <크리에이터명>');
    process.exit(1);
  }
  let data;
  try {
    data = require(path.join(__dirname, 'data', name + '.js'));
  } catch (e) {
    console.error(`데이터 파일을 찾을 수 없습니다: data/${name}.js`);
    process.exit(1);
  }
  const out = buildPage(data);
  const dest = path.join(__dirname, '..', 'done', name + '.html');
  fs.writeFileSync(dest, out, 'utf8');
  console.log('생성 완료:', dest);
}
```

- [ ] **Step 6: CLI 동작 확인 (산출물은 임시 이름으로)**

Run:
```bash
cd channel-pages-final/_template
node -e "const {buildPage}=require('./build.js');require('fs').writeFileSync('../done/_EXAMPLE.html',buildPage(require('./data/_EXAMPLE.js')))"
ls -la ../done/_EXAMPLE.html
```
Expected: `_EXAMPLE.html` 파일이 생성됨 (CLI는 `done/{이름}.html`에 쓰므로, `부산맛나.html` 덮어쓰기를 피하려고 검증은 `_EXAMPLE.html`로 함)

- [ ] **Step 7: 커밋**

```bash
git add channel-pages-final/_template/build.js channel-pages-final/_template/build.test.js
git commit -m "feat: 빌드 스크립트 스크립트 데이터 주입 + CLI 진입점"
```

---

## Task 6: 전체 검증 — 단일·다중 도시 빌드 + 브라우저 확인

**Files:**
- Create: `channel-pages-final/_template/data/_EXAMPLE2.js` (다중 도시 스모크 테스트용, 검증 후 삭제)

- [ ] **Step 1: 단일 도시 산출물 브라우저 비교**

Task 5 Step 6에서 만든 `channel-pages-final/done/_EXAMPLE.html`을 브라우저로 연다. 같은 폴더의 `부산맛나.html`과 나란히 비교한다. 확인 항목:
- 프로필 카드(이름·이미지·SNS 아이콘)가 정상 표시
- 쿠폰 배너 텍스트·금액 정상
- 트립카드 1장, 제목·뱃지·"85만~" 정상. 화살표는 보이지 않아야 함(`display:none`)
- 링크 탭: "📸 추천 콘텐츠" 섹션 + thumb 항목 1개
- 일정표 버튼 클릭 → course-panel 열림, 지도·DAY 탭·동선 정상
- 경비 버튼 클릭 → expense-panel 열림, 항공·호텔·식비·투어·총경비 정상
- 쿠폰 배너 클릭 → 쿠폰 링크로 이동 / 쿠폰 패널 카드 2개 정상
- 필수템 탭 → 상품 10개 그리드, 검색 동작

기존 `부산맛나.html`과 **시각적으로 동일**해야 한다 (클래스명·코드는 다를 수 있음 — 예: `tc-hero busanmatna-sapporo` → `tc-hero sapporo`).

- [ ] **Step 2: 다중 도시 스모크 테스트 데이터 작성**

`channel-pages-final/_template/data/_EXAMPLE2.js`를 만든다. `_EXAMPLE.js`를 복사하되 `trips` 배열에 두 번째 트립을 추가한다 (도시 키만 다르면 됨 — 빌드가 트립 2개를 처리하는지만 확인):

```js
// 다중 도시 빌드 스모크 테스트용 — 검증 후 삭제
const base = require('./_EXAMPLE.js');
module.exports = {
  ...base,
  trips: [
    base.trips[0],
    {
      ...base.trips[0],
      city: 'otaru',
      flag: '🏔️',
      title: '오타루 당일치기 코스',
      cardImg: '../assets/images/busanmatna-card1.jpg',
      costFrom: '40만~',
    },
  ],
};
```

- [ ] **Step 3: 다중 도시 빌드 실행 및 확인**

Run:
```bash
cd channel-pages-final/_template
node -e "const {buildPage}=require('./build.js');const h=buildPage(require('./data/_EXAMPLE2.js'));require('fs').writeFileSync('../done/_EXAMPLE2.html',h);console.log('cards:',(h.match(/class=\"trip-card\"/g)||[]).length,'dots:',(h.match(/class=\"trip-dot/g)||[]).length,'TRIP_KEYS:',h.includes('[\"sapporo\",\"otaru\"]'))"
```
Expected: `cards: 2 dots: 2 TRIP_KEYS: true`

- [ ] **Step 4: 다중 도시 산출물 브라우저 확인**

`channel-pages-final/done/_EXAMPLE2.html`을 브라우저로 연다. 확인 항목:
- 트립카드 2장이 캐러셀에 표시되고 가로 스크롤(스와이프) 동작
- dot 2개, 스크롤 시 활성 dot 전환
- 두 번째 카드의 일정표·경비 버튼 클릭 → 각각 `otaru` 도시로 패널 열림
- 첫 번째 카드 동작도 정상 (`sapporo`)

- [ ] **Step 5: 검증용 임시 파일 삭제**

```bash
rm channel-pages-final/done/_EXAMPLE.html channel-pages-final/done/_EXAMPLE2.html channel-pages-final/_template/data/_EXAMPLE2.js
```

- [ ] **Step 6: 전체 테스트 재실행**

Run: `cd channel-pages-final/_template && node --test`
Expected: PASS — 9 tests passed

- [ ] **Step 7: 커밋**

```bash
git add channel-pages-final/_template/
git commit -m "feat: 채널 페이지 템플릿 체계 검증 완료"
```

---

## 완료 후 신규 크리에이터 추가 방법

1. `channel-pages-final/_template/data/_EXAMPLE.js`를 `data/{크리에이터명}.js`로 복사
2. 수경님 구역(creator·theme·sns·coupon·textblock·linkSections·products) 채우기
3. Claude가 영상·메모를 요약해 `trips[]` 구역(트립카드·일정표·경비) 작성
4. `cd channel-pages-final/_template && node build.js {크리에이터명}` 실행
5. `channel-pages-final/done/{크리에이터명}.html` 브라우저 확인 후 배포 요청

디자인 수정 시: `shell.html` 한 곳만 고치고 각 크리에이터 데이터로 재빌드.

---

## Self-Review

**1. Spec coverage:**
- 파일 구조 → Task 1·2·3 (`_template/`, `shell.html`, `build.js`, `data/`)
- 데이터 파일 스키마 → Task 2 (`_EXAMPLE.js`가 스키마 전체 구현)
- 색상 프리셋 → Task 3 (`THEMES` 6종, `theme` 이름 선택)
- 셸·빌드 동작 6단계 → Task 3(읽기·프리셋·배경CSS)·Task 4(반복구역)·Task 5(스크립트주입·CLI출력)
- 트립 화살표 HTML/JS 포함+CSS 숨김 → Task 1 Step 2·4·6
- linkSections 2단 구조, thumb/og 2종 → Task 2 스키마 + Task 4 `renderLinkSections`
- 단일/다중 도시 자동 처리 → Task 6 Step 2~4 검증
- 검증 방법(브라우저 비교, 패널 동작) → Task 6
- dest-bundle 제외 → 스키마·렌더링에서 의도적으로 미포함 (스펙 비고 일치)

**2. Placeholder scan:** "부산맛나.html 353~362줄 복사" 류는 플레이스홀더가 아니라 정확한 출처 지정(대용량 데이터 블록의 원본이 레포에 존재). 그 외 TBD/TODO 없음.

**3. Type consistency:**
- 슬롯 이름: Task 1 "셸 슬롯 목록"에서 정의 → Task 3·4·5 `repl` 키와 일치 확인 완료
- `buildPage(data)` 시그니처: Task 3에서 정의 → Task 4·5에서 동일 함수 확장, `module.exports = { buildPage, THEMES }` 일관
- 데이터 키: `_EXAMPLE.js`(Task 2)의 `creator`/`theme`/`sns`/`coupon`/`textblock`/`linkSections`/`products`/`trips` → `build.js`(Task 3~5)에서 동일 키로 참조
- 렌더링 함수명(`renderBgCss`·`renderSnsPills`·`renderTripCards`·`renderTripDots`·`renderLinkSections`·`renderCouponCards`): Task 3·4에서 정의·호출 일치
