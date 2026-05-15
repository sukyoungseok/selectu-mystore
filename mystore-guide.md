# 마이스토어 채널 페이지 제작 가이드

파파트래블 제작 경험 기반으로 정리한 제작 기준 및 작업 순서.

---

## 작업 순서

### STEP 1. 크리에이터 채널 분석
- 주력 여행지 파악 (도시 1~3개)
- 인기 영상에서 상품 연결 가능한 콘텐츠 선별
- 추천 코스로 묶을 수 있는 일정 구조 확인
- 구독자 수, SNS 계정, 프로필 이미지 수집

### STEP 2. 기본 정보 세팅
- CREATOR 객체: 채널명, 구독자 수, 소개글, SNS 링크
- 히어로 이미지, 프로필 사진 경로 설정
- 쿠폰팩 랜딩 링크 (없으면 비워둠)

### STEP 3. 여행지 선정 + 코스 초안
- 도시별 3박 4일 기준 일정 구조 작성
- 각 stop: 장소명, 시간대, 지도 좌표, 비용
- 이 단계에서 상품이 필요한 stop 미리 표시해두기

### STEP 4. 상품 링크 확보 (수기 작업)
- MRT에서 상품 검색 후 MyLink로 단축 URL 생성
- 상품 유형별 분류:
  - 예약 상품 (`experiences.myrealtrip.com`) → OG 이미지 수집 가능
  - 항공권 / 렌트카 검색 페이지 → OG 이미지 없음, 이모지 사용
- 가격은 반드시 **원화(KRW) 기준**으로 확인

### STEP 5. 코스 데이터 작성 (CITY_DAYS)
- 각 stop의 `desc` 필드는 **2줄 이내** (50~70자 기준)
- 상품 삽입 시 해당 stop에 `product` 또는 `products[]` 추가
- URL은 STEP 4에서 확보한 MyLink URL 사용

### STEP 6. 3곳 데이터 통일 (핵심)
아래 세 곳의 **URL · 가격 · 상품명**이 반드시 일치해야 함:

| 위치 | 역할 |
|------|------|
| `products[]` | 필수템 탭 카드 |
| `CITY_DAYS` 코스 인라인 | 일정표 내 상품 카드 |
| `CITY_EXPENSE.tours[]` | 경비 패널 예약 링크 모음 |

> 코스 인라인과 products[]의 URL이 다르면 썸네일 매칭이 안 됨 → 반드시 동일 URL 사용

### STEP 7. OG 이미지 수집
- Playwright로 각 상품 페이지 접속 → `meta[property="og:image"]` 추출
- `experiences.myrealtrip.com/products/` 페이지만 이미지 있음
- `offers` 페이지(`myrealtrip.com/offers/`)도 이미지 있음
- 항공권/렌트카/액티비티 검색 페이지 → 기본 로고 반환 → 이모지 유지
- 수집한 URL을 `products[]`의 `img` 필드에 삽입

### STEP 8. 총경비 계산 + 카드 숫자 업데이트
- `CITY_EXPENSE.defaultTotal` = 항공 + 숙박 + 식비 합산
- 해외 상품 가격은 KRW 환산가로 입력
- 목적지 카드 `tc-c-num` 숫자도 defaultTotal과 맞게 업데이트 (예: 95만~)
- 호텔이 2개 선택지이면 `hotels[]` 배열 사용, 단일이면 `hotelName/hotelUrl` 사용

### STEP 9. 최종 검증 (브라우저)
순서대로 확인:
1. 필수템 탭 → 전체 상품 카드, 썸네일, 가격 확인
2. 홍콩/이시가키 코스 패널 → 각 DAY별 상품 카드, 썸네일
3. 경비 패널 → 항공·호텔·식비·투어 가격, 예약 바로가기 버튼

---

## 제작 기준 (레슨런)

### 1. URL 일관성
코스 인라인과 products[]에 동일한 MyLink URL 사용.
URL이 다르면 imgMap 매칭이 안 돼 썸네일이 이모지로 표시됨.

### 2. 가격은 처음부터 KRW
HKD, JPY 등 현지 통화로 입력하면 나중에 전부 재작업 필요.
MRT 상품 상세 페이지의 원화 가격을 처음부터 입력.

### 3. 코스 설명은 2줄 이내
desc 필드 기준 50~70자. 길게 써도 나중에 줄여야 함.

### 4. 필수템 = 코스 등장 상품 전부
코스 데이터 작성 시 예약 가능 상품 목록을 먼저 확정하고,
그 목록이 곧 필수템 탭 구성이 됨.

### 5. 호텔 복수 선택지
"A 또는 B 호텔" 케이스는 `hotels[]` 배열로 처리.
단일 호텔은 기존 `hotelName/hotelUrl` 필드 사용.

### 6. sold 뱃지 제거
실제 판매량 데이터 없으면 " sold"만 표시돼 지저분.
renderProducts에서 pc-sold 제거한 버전 유지.

### 7. OG 이미지 수집 가능 범위
| URL 패턴 | 이미지 여부 |
|----------|------------|
| `experiences.myrealtrip.com/products/` | ✅ CDN 이미지 |
| `myrealtrip.com/offers/` | ✅ CDN 이미지 |
| `flights.myrealtrip.com` | ❌ 기본 로고 |
| `myrealtrip.com/rentalcars` | ❌ 기본 로고 |

---

## 참고: 크리에이터 유형별 구조

| 유형 | 구조 추천 |
|------|----------|
| 단일 여행지 전문 | 도시 1개, 코스 탭 1개 |
| 다수 여행지 커버 | 도시 2~3개, 슬라이드 카드 + 코스 탭 분리 |
| 국내 여행 | CITY_DAYS 구조 동일, 항공 항목 제거 |
| 맛집/일상 크리에이터 | 코스 탭 없이 링크 탭 + 필수템 탭만 운영 |

---

## GA4 트래킹 설정

### 기본 정보
| 항목 | 값 |
|------|-----|
| GA4 속성명 | 마이스토어 |
| 측정 ID | G-Q5HGL54Q9S |
| 스트림 URL | https://mystore-mrt.vercel.app |
| 스트림 ID | 14839109198 |
| 설정일 | 2026-05-08 |

### 적용 파일
`channel-pages-final/done/` 및 `channel-pages-final/` 하위 전체 채널 페이지,
`creator-intro.html`, `mockup.html`, `coupon/` 하위 HTML 파일에 적용.
새 채널 페이지 추가 시 `<head>` 바로 아래에 아래 스크립트 삽입 필요:

```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-Q5HGL54Q9S"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-Q5HGL54Q9S');
</script>
```

### 데이터 확인 방법
analytics.google.com → 보고서 → 참여 → 페이지 및 화면
→ 페이지 경로(예: `/홍다닥`, `/부산맛나`)별 일별 방문자 수 확인 가능

> 설치 후 48시간 이내에는 "데이터 수집 비활성화" 경고가 뜰 수 있으나 정상.
