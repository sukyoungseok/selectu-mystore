# 마이스토어 목업 캐러셀 개편 — 전체 로그

- 날짜: 2026-04-16
- 프로젝트 경로: `/Users/sukyoung-seok/mystore-mockup/`
- 주요 파일: `index.html`, `card-option2-dev.html`, `card-candidates.html`, `design-options.html`, `course-options.html`, `textblock-options.html`

---

## Phase 1. 문제 정의

- 세션 재개 시점에 기존 `index.html`의 코스 카드가 정보 포화 상태였음. 사진 스트립 + 제목 + 총경비 박스 + 항목 스와이프 + 버튼 2개가 동시에 노출돼 중복과 혼란 발생함.
- 쿠폰 배너/프로필 카드/텍스트 블록 등 인접 요소들도 비율·톤 미세 조정이 필요했음.
- TripSignal이 별도 프로젝트로 공개 운영 중이었고, 태욱님 작업물로서 `/api/prices/{city}` 데이터에 접근 가능한 상태였음. 기존 index는 하드코딩된 경비를 사용하고 있었음.
- 필수템 탭은 이모지와 배경색으로만 구성됨. 링크 탭은 이미 microlink 기반 OG 이미지 자동 로딩이 동작 중이었음.

## Phase 2. 디자인 탐색

- 코스 섹션 대체안을 라운드 단위로 반복 제시함. v1 5안(심플/2타일/타임라인/풀히어로/메타그리드), v2 5안(폴라로이드/보딩패스/스토리/히트맵/다이어리), 조합 2안을 거쳐 전부 반려됨.
- 수경님이 직접 작성한 `card-candidates.html`의 Option 02(선택 질문형)에서 출발점을 얻음. 히어로 + "어디부터 볼까요?" + 2버튼(일정표/총경비) + 우측 정렬 가격 캡션 구조임.
- 캡션 표기를 V1~V6 중 V5(구분선+우측정렬)로 1차 선택 후 V1+V5 머지 M1~M4에서 M2(좌 라벨 2줄 + 우 26px 숫자)로 최종 확정함.
- 국기 표시는 V1~V5 중 V1(제목 옆 원형 뱃지)로 회귀. 국가명 태그 방식은 한글로 전환했다가 최종 반려함.
- 크리에이터 한마디 블록은 V1~V6 중 V3 말풍선(아바타+꼬리)를 선택. 배경색 `#FFF5E8`, 테두리 `#FFD9AE`로 다른 흰 카드와 구분함.

## Phase 3. 메인 index.html 통합

- `course-teaser` 블록을 `trip-carousel-wrap` + `trip-card` 4장 구조로 교체함. 각 카드는 오사카·도쿄·방콕·타이베이 여행지를 담고 동일 M2 캡션 템플릿을 사용함.
- 오사카 카드만 `openCourse()` / `openExpensePanel()` 핸들러를 연결함. 나머지 3장은 플레이스홀더임.
- 제목에서 "3박 4일"을 분리하여 `tc-badges` 두 개(기간, 시즌)로 이전함. 시즌은 "26년 5월 여행" 포맷으로 시즌 느낌을 전달함.
- 코스 패널 상단 부제 `3박 4일 · 장소 6곳` 도 `26년 5월 여행`으로 교체함.
- 국기 원형 뱃지 크기를 34→46px로 확대해 제목 컬럼 높이와 비율을 맞춤.
- 섹션 주제명 태그는 한국어 카테고리명으로 전환하고 "✎ 섹션 제목" 편집 힌트는 향후 편집 기능 미정이라는 이유로 제거함.
- 크리에이터 한마디는 말풍선 구조로 리팩토링함. 제목은 "💌 셀렉트유의 한 마디" → "오사카 여행 꿀팁!"로 톤 변경.

## Phase 4. TripSignal 실시간 가격 연동

- Next.js 청크 역분석으로 `/api/prices/{id}` 엔드포인트와 `Mq` 도시 목록(osaka id 확인)을 도출함.
- `loadBudget()` 을 osaka + duration 3 기준으로 개편. 최저가 조합(항공+숙소)을 향후 6개월 범위에서 탐색함.
- AbortController 8초 타임아웃, `!res.ok`, `json.data.flights/hotels` 가드 추가함.
- 메인 카드 `#ct-budget-amount` 와 경비 패널 `#exp-flight`, `#exp-hotel`, `#exp-total` 에 실시간 값 바인딩함.
- EXTRA_COSTS(교통·마이리얼트립·식비)는 고정값 유지함. 총 예상 경비는 TripSignal 합산 + EXTRA_COSTS로 계산함.

## Phase 5. 경비 패널 재편 & 투어티켓 분리

- 식비 항목을 숙소 아래로 이동, 교통 항목을 제거함(투어티켓 그룹 내 라피트/지하철 중복).
- 마이리얼트립 구매 단일 항목을 4개 개별 상품 카드로 분할함(이심·하루카스·라피트·지하철 2일권). 각 카드에 예약 바로가기 버튼을 연결함.
- 그룹 헤더는 "🎫 투어 티켓"만 노출. "셀렉트유가 직접 구매 · 4개" 서브카피는 제거함.

## Phase 6. PC 캐러셀 & 필수템 OG

- PC에서 가로 스크롤이 직관적이지 않다는 피드백으로 화살표 버튼을 추가함. 초기에는 히어로 이미지 위 오버레이였으나 위치가 이상하다는 이슈로 도트 좌우 페이지네이션(`‹ • • • • ›`)으로 수정함.
- 모바일에서는 `@media (hover: none)` 으로 화살표를 숨기고 터치 스와이프를 유지함.
- 필수템 탭의 `pc-img` 에 `data-og-url` 을 추가하고, 별도 함수 `loadProductOg()` 로 microlink `embed=image.url` 를 호출해 backgroundImage를 세팅함. 이미지 로드 실패 시 이모지 fallback을 유지함.

## Phase 7. 배포

- 당일 총 3회 프로덕션 배포 수행: 캐러셀 1차 / 화살표 재배치 / 필수템 OG 자동화.
- 배포는 `git push origin main` + `vercel deploy --prod --yes` 조합으로 alias `mystore-mockup.vercel.app` 을 유지함.
- 현재 배포 URL: `https://mystore-mockup.vercel.app/` (최신 deployment: `mystore-mockup-9fmut5z1b-...`).

## Phase 8. 세션 아카이빙

- 기존 `/Users/sukyoung-seok/sessions/` 의 mystore 관련 3개 세션(2026-04-10, 04-13 x2)을 프로젝트 내부 `/Users/sukyoung-seok/mystore-mockup/sessions/` 로 이관함.
- 이번 세션을 동일 경로에 `2026-04-16_mystore-mockup-carousel-deploy/` 폴더로 저장함.
- DECISION-DOC.md, MEETING-NOTES.md, FULL-LOG.md 3종 파일 생성. SESSION-INDEX.md도 프로젝트 내부에 구축함.
