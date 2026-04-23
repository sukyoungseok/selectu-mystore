# 마이스토어 아키텍처 — Supabase+Vercel 가이드 분석 - 회의록

- **날짜:** 2026-04-13
- **참석:** 마케팅파트너팀
- **주제:** 외부 링크인바이오 구현 가이드 분석 및 마이스토어 아키텍처 참고점 정리

---

## 안건

growbeat.company가 제작한 Supabase+Vercel 기반 링크인바이오 구현 가이드(11페이지 PDF) 전체를 검토하고, 마이스토어 개발에 참고할 요소와 제외할 요소를 분리함.

---

## 주요 논의

### 1. 가이드 전체 내용 파악 (01~09챕터)

PDF 11페이지 전체를 순서대로 분석함. 주요 챕터별 내용:

01~02챕터: Next.js 14 + Supabase + Vercel 스택 소개 및 선택 이유 (무료, 15분 셋업, 자동 배포)

03~04챕터: GitHub 레포 생성 → Vercel 연동 → Supabase contacts 테이블 생성 + RLS 정책 설정

05챕터: .env.local 환경변수 4개 관리 방법 (Supabase URL, anon key, Slack Webhook URL, 사이트 URL), .gitignore 필수 추가 강조

06챕터: 핵심 API Route 코드 공개 — POST 요청 수신 → Supabase INSERT → Slack Webhook 전송(환경변수 있을 때만)의 3단계 구조

07챕터: Claude 프롬프트 템플릿 — 위 스택 기반 링크페이지 전체 코드를 한 번에 생성하는 방법 (Claude Code에 붙여넣기)

08챕터: Vercel 커스텀 도메인 + Vercel Analytics 설정, Supabase 콘솔에서 문의 데이터 CSV 다운로드 방법

09챕터: 배포 전 체크리스트 9항목 + 트러블슈팅 표 (5개 케이스 원인/해결 포함)

### 2. 마이스토어 적용 가능 여부 분석

가이드가 다루는 서비스는 단순 문의 폼이 달린 링크페이지임. 마이스토어는 여행 코스 + 인라인 상품 카드 + 크리에이터 관리 기능이 필요하여 복잡도가 훨씬 높음.

적용 가능한 요소로는 Supabase DB API Route 연동 구조, RLS 보안 정책, Slack Webhook 알림, 환경변수 관리 방식, Claude 프롬프트 활용법 5가지를 확인함.

제외 요소로는 Vercel 배포, Vercel Analytics, 커스텀 도메인 CNAME 설정을 확인함. 마이스토어는 MRT 내부 인프라를 사용하므로 해당 내용은 참고 불필요함.

### 3. 마이스토어 DB 스키마 복잡도 확인

가이드의 contacts 테이블(5컬럼)과 달리 마이스토어는 creators, stores, courses, spots, products, click_logs 6개 테이블이 필요함을 파악함. 상세 스키마 설계는 다음 개발 세션에서 별도로 진행하기로 함.

---

## 결정 사항

| 번호 | 결정 | 비고 |
|------|------|------|
| 1 | Supabase API Route + RLS 패턴 마이스토어에 재사용 | /api/store, /api/click 등 엔드포인트 동일 구조 적용 |
| 2 | Slack Webhook 알림 패턴 채택 | 크리에이터 가입 알림 + 상품 클릭 일보 용도 |
| 3 | Vercel 관련 요소 전체 제외 | MRT 내부 인프라(Jenkins)로 대체 |
| 4 | 환경변수 관리(.env.local + .gitignore) 동일 적용 | MyLink API key 등 마이스토어 추가 변수 포함 |
| 5 | 마이스토어 DB 스키마는 6개 테이블로 별도 설계 필요 | 다음 개발 세션에서 진행 |

---

## 액션 아이템

- [ ] 수갱주니어: 마이스토어 DB 스키마 6개 테이블 상세 설계 (다음 개발 세션)
- [ ] 수갱주니어: youtube-mcp 활성화 후 나고야 여행 영상(https://www.youtube.com/watch?v=t0O1hT7V7vc) 코스 추출 (Claude 재시작 후 즉시)
- [ ] 수경님: 목업 A/B/C 스타일 중 최종 선택
- [ ] 수경님: 영준님 보고 일정 확정
- [ ] 수경님: Slack 알림 채널 및 포맷 방향 확정

---

## 다음 회의

마이스토어 DB 스키마 설계 세션 + youtube-mcp 활성화 후 나고야 영상 코스 추출 진행
