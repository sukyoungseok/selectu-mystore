# FULL-LOG — 마이스토어 아키텍처 Supabase+Vercel 가이드 분석

**날짜:** 2026-04-13

---

## Phase 1: 세션 복원 및 PDF 이어 읽기

이전 세션(2026-04-10) 컨텍스트 컴팩션으로 인해 PDF 분석이 중단된 상태였음. 이전 세션에서 pages 1~5까지 읽었고, 이번 세션에서 pages 6~11(05~09챕터 및 마지막 요약 페이지)을 이어서 읽음.

추가로 확인한 챕터 내용:

05챕터(환경변수 설정): .env.local 파일에 NEXT_PUBLIC_SUPABASE_URL, NEXT_PUBLIC_SUPABASE_ANON_KEY, SLACK_WEBHOOK_URL, NEXT_PUBLIC_SITE_URL 4개 변수 관리. SLACK_WEBHOOK_URL은 서버 전용(NEXT_PUBLIC_ 없이 입력)으로 설정하여 외부 노출 차단. .gitignore에 .env.local 추가 필수 강조.

06챕터(핵심 API Route 코드): app/api/contact/route.ts에서 POST 요청 수신 → supabase.from('contacts').insert() → Slack Webhook fetch(환경변수 있을 때만 조건부 실행) 3단계 구조. 프론트엔드에서 /api/contact로 POST 요청 후 성공 시 alert 및 폼 초기화.

07챕터(Claude 프롬프트 템플릿): 역할 + 기술 스택 + 생성할 파일 목록 + 디자인 요구사항을 한 번에 정의한 Claude 프롬프트를 Claude Code에 붙여넣어 전체 코드를 한 번에 생성하는 방법 소개. "Claude Code로 실행하면 파일 직접 생성, npm run dev로 바로 로컬 확인 가능"이라고 안내함.

08챕터(커스텀 도메인 + Analytics): Vercel 대시보드에서 커스텀 도메인 추가 → DNS CNAME 설정 → SSL 자동 발급. Vercel Analytics(npm install @vercel/analytics)로 페이지뷰/방문자 수/국가/디바이스 실시간 확인. 데이터 조회는 Supabase 콘솔 Table Editor에서 CSV 다운로드 또는 Slack 채널 DM으로 실시간 확인.

09챕터(배포 전 체크리스트): 9개 항목 점검 목록 + 5개 트러블슈팅 케이스(500 에러, Slack 알림 미수신, INSERT 실패, 빌드 실패, 모바일 레이아웃 깨짐) 원인-해결 표.

마지막 요약 페이지: "HTML 파일이 아닌 실제 DB가 달린 링크페이지. 문의 오면 Slack 알림, 데이터는 Supabase에 자동 저장. Claude로 30분 안에 완성됩니다." 4단계 요약(GitHub 레포 → Supabase 셋업 → Vercel 연동 → Claude로 코드 생성 + push).

---

## Phase 2: 마이스토어 적용 가능 여부 분석

가이드 전체 내용 파악 후 마이스토어와의 비교 분석을 진행함.

**겹치는 구조 (참고할 것):**

Supabase DB + Next.js API Route 연동 패턴은 마이스토어의 크리에이터 데이터 저장, 상품 클릭 로그 기록 등 다수 엔드포인트에 그대로 적용 가능함.

RLS 보안 정책(INSERT-only 공개, SELECT는 콘솔에서만)을 크리에이터별 데이터 격리에 응용 가능함. 크리에이터 A가 크리에이터 B의 코스를 수정하지 못하도록 제한하는 용도로 동일 패턴 활용.

Slack Webhook 조건부 알림(환경변수 있을 때만 실행)은 크리에이터 신규 가입 알림 및 상품 클릭 일보 자동 발송에 활용 가능함.

.env.local + .gitignore 관리 방식은 마이스토어 개발 시 동일하게 적용. 마이스토어 추가 환경변수: MyLink API key, MRT 내부 API 인증 키.

**제외할 부분:**

Vercel 배포, Vercel Analytics, 커스텀 도메인 CNAME → MRT 내부 Jenkins 배포 및 MRT 도메인 체계(예: mystore.myrealtrip.com) 사용 예정이므로 참고 불필요.

**복잡도 차이 확인:**

가이드의 서비스는 contacts 테이블 1개(5컬럼)의 단순 링크+문의 폼임. 마이스토어는 creators, stores, courses, spots, products, click_logs 6개 테이블 + 크리에이터 관리 인터페이스가 필요한 고복잡도 서비스임. DB 스키마는 별도 설계 세션 필요.

---

## Phase 3: 결론 정리 및 다음 스텝 확인

분석 결론: 가이드는 아키텍처 패턴 레퍼런스로 유용하나, 마이스토어 구현에는 대폭 확장이 필요함. 참고할 요소 5개(API Route 패턴, RLS, Slack Webhook, 환경변수 관리, Claude 프롬프트 방식)와 제외할 요소 4개(Vercel 배포, Analytics, 도메인, 환경변수 설정)를 명확히 분리함.

다음 스텝으로 youtube-mcp 활성화 후 나고야 영상 코스 추출, 마이스토어 DB 스키마 설계, 목업 최종 스타일 결정이 대기 중임을 확인함.
