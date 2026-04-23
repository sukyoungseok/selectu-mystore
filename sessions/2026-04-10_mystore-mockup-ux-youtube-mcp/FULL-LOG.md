# FULL-LOG — 마이스토어 목업 UX 개선 및 YouTube MCP 설치

**날짜:** 2026-04-10

---

## Phase 1: 목업 재개 및 상하이 데이터 반영

이전 세션에서 생성한 course-only.html(방콕 4박5일 가상 데이터)을 재오픈함. 수경님이 @june_fairytale의 인스타그램 게시글(상하이 3박4일 여행코스)을 제공하며 데이터 반영을 요청함.

Playwright로 해당 게시글에 접근하여 캡션 전문을 파싱함. 로그인 팝업 처리 후 snapshot으로 캡션 텍스트 추출 성공. 추출 결과:
- DAY 1: 공항 도착 → 상하이 디즈니랜드 → 토이스토리 호텔
- DAY 2: 우캉멘션 → 프랑스조계지 → 예원 → 황푸강 유람선
- DAY 3: 우전 수향마을 (야경투어)
- DAY 4: 동방명주 → 귀국
- MRT 연계: 디즈니랜드 5% 쿠폰, 황푸강 유람선, 수향마을 투어

A/B/C 3가지 스타일 모두 상하이 데이터로 업데이트 완료.

---

## Phase 2: 목업 UX 1차 개선 (상품 섹션 부킹카드화)

수경님 피드백: "세 개 다 구려, 상품이 눈에 안 띈다"

문제 진단: 상품이 코스 하단에 텍스트 나열 수준으로 별도 섹션 분리됨. 예약 버튼 없음, 가격 작음.

1차 개선: 상품 섹션을 부킹카드 스타일로 전환. 아이콘+상품명+가격+예약하기 버튼 구조. A/B/C 스타일별 색상 적용.

---

## Phase 3: 목업 UX 2차 개선 (타임라인 + 인라인 상품)

수경님 피드백: "코스 중간에 상품 링크가 바로 눈에 띄게 해야지. 코스 흐름이 없잖아."

문제 진단: 1차 개선에서도 상품은 여전히 코스 뒤에 분리된 섹션으로 존재. 코스 자체도 타임라인 흐름 없이 카드 나열.

2차 개선 방향 확정:
- 세로 타임라인(vertical line + dot) 구조로 코스 흐름 표현
- 관련 스팟 바로 아래 인라인 예약 카드 배치 (공항 도착 → 항공권, 디즈니 → 입장권 등)
- A/B/C 3가지 스타일 모두 동일한 타임라인+인라인 구조 적용

전체 HTML 재작성 후 브라우저 오픈 완료.

---

## Phase 4: YouTube MCP 탐색 및 설치

수경님이 나고야 여행 브이로그(sookoh 수코 채널, 3박4일) 영상 링크를 제공하며 코스 추출 요청.

시도:
- WebFetch로 YouTube 설명란 접근 → 광고 내용만 존재, 일정 정보 없음
- Playwright로 description 파싱 → 동일
- 챕터/타임스탬프 확인 → 없음

결론: 순수 브이로그 형식이라 영상 자체의 자막 추출이 필요함.

Smithery(https://smithery.ai/servers?q=youtube)에서 YouTube MCP 108개 탐색. 주요 후보:
- sfiorini/youtube-mcp (8.4k 설치, 자막+타임스탬프)
- samson-art/transcriptor-mcp (3.77k, Whisper fallback 포함)
- alex2zimmermann-ux/yt-transcript-mcp (479)

sfiorini/youtube-mcp 선택 및 설치 완료.
설치 명령: npx -y @smithery/cli install sfiorini/youtube-mcp --client claude
Claude 재시작 후 활성화 예정.
