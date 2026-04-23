# 마이스토어 아키텍처 설계 — Supabase+Vercel 가이드 분석 및 참고점 도출

- **날짜:** 2026-04-13
- **주제:** 외부 링크인바이오 구현 가이드(Supabase+Vercel) 전체 분석 및 마이스토어 설계에 참고할 요소 정리
- **유형:** 제품 기획 + 아키텍처 분석
- **배경:** 인스타그램에서 발견한 growbeat.company의 Supabase+Vercel 링크인바이오 가이드(PDF 11페이지)가 마이스토어와 유사한 구조를 가짐. 단, 마이스토어는 Vercel 미사용 예정이므로 선택적으로 참고할 요소를 분리하고 기록함.

---

## 최종 결정 사항

**1.** Supabase DB 연동 패턴(API Route → INSERT + RLS 보안 정책)을 마이스토어에 재사용하기로 함

**2.** Slack Webhook 알림 패턴을 크리에이터 신규 가입 및 상품 클릭 일보 알림에 적용하기로 함

**3.** Vercel, Vercel Analytics, 커스텀 도메인 CNAME 설정은 MRT 내부 인프라로 대체하므로 참고에서 제외함

**4.** 환경변수 관리(.env.local + .gitignore 필수) 패턴을 마이스토어 개발 환경에 동일하게 적용하기로 함

**5.** 마이스토어 DB 스키마는 이 가이드의 단순 contacts 테이블보다 훨씬 복잡하게 설계해야 함 (크리에이터 프로필 + 여행 코스 + 스팟 + 상품 링크 + 클릭 로그 등)

---

## 1. 배경 및 문제 정의

마이스토어는 여행 크리에이터 전용 링크인바이오 서비스로, 여행 코스 섹션 내 MRT 상품 연결이 핵심 기능임. 기술 스택과 아키텍처 방향 결정 전에 유사 서비스 구현 사례를 참고하고자 함.

growbeat.company가 공개한 가이드는 Next.js 14 + Supabase + Vercel 기반의 링크페이지 구현 방법을 단계별로 설명하며, 아키텍처 패턴 차원에서 마이스토어와 유사한 구조를 가짐.

---

## 2. 가이드 전체 구조 요약

| 챕터 | 내용 |
|------|------|
| 01 | 개요: 코드 없이 15분 안에 링크페이지 구축 (Next.js 14 + Supabase + Vercel) |
| 02 | Why Supabase + Vercel — 무료, 자동 배포, DB 관리 용이 |
| 03 | GitHub 레포 생성 + Vercel 연동 |
| 04 | Supabase DB 설정 (contacts 테이블 + RLS 정책) |
| 05 | 환경변수 설정 (.env.local, Vercel 환경변수 관리) |
| 06 | 핵심 API Route 코드 (POST → Supabase INSERT + Slack Webhook 전송) |
| 07 | Claude 프롬프트로 전체 코드 한 번에 생성하는 방법 |
| 08 | 커스텀 도메인 연결 + Vercel Analytics (방문자 추적) |
| 09 | 배포 전 체크리스트 + 트러블슈팅 표 |

---

## 3. 마이스토어 적용 분석

### 3-1. 재사용 가능한 패턴

**Supabase DB + API Route 연동 구조**

가이드의 `/api/contact` 엔드포인트 패턴 (POST 요청 → Supabase INSERT → Slack Webhook)은 마이스토어의 다음 엔드포인트에 그대로 적용 가능함:
- `/api/store` — 크리에이터 마이스토어 데이터 저장
- `/api/click` — 상품 클릭 로그 기록
- `/api/creator` — 크리에이터 신규 가입 처리

**RLS (Row Level Security) 보안 정책**

가이드에서 contacts 테이블에 INSERT-only 공개 정책, SELECT/DELETE는 콘솔에서만 허용하는 방식을 사용함. 마이스토어에서는 크리에이터별 데이터 격리(자기 코스만 수정 가능)에 동일한 RLS 패턴 적용 가능함.

**Slack Webhook 알림**

가이드는 폼 제출 시 운영자 Slack DM으로 알림을 전송함. 마이스토어 적용 시:
- 크리에이터 신규 가입 알림 → 운영팀 Slack 채널
- 일별 상품 클릭수 리포트 → 슬랙 자동 발송

**환경변수 관리 방식**

.env.local에 Supabase URL, anon key, Slack Webhook URL을 분리 관리하고 .gitignore에 필수 추가하는 방식을 마이스토어 개발 환경에 그대로 적용함. 마이스토어 추가 환경변수: MyLink API key, MRT 내부 API 키 등.

**Claude 프롬프트 템플릿 방식 (07챕터)**

"Next.js 14 + Supabase 기반 전체 코드를 한 번에 생성해줘" 방식의 Claude 활용법을 마이스토어 초기 뼈대 코드 생성 시 동일하게 활용 가능함.

### 3-2. 제외할 부분

| 항목 | 제외 이유 |
|------|---------|
| Vercel 배포 | MRT 내부 Jenkins 배포 방식 사용 |
| Vercel Analytics | MRT 내부 분석 도구로 대체 |
| 커스텀 도메인 CNAME | MRT 도메인 체계(예: mystore.myrealtrip.com) 따름 |
| Vercel 환경변수 설정 | MRT 인프라 환경변수 관리 방식 따름 |

### 3-3. 마이스토어와의 복잡도 차이

가이드는 contacts 테이블 1개(id, name, phone, message, created_at)의 단순 문의 폼 서비스임. 마이스토어는 다음 엔티티가 필요하여 스키마 설계가 별도로 필요함:

| 테이블 | 주요 컬럼 |
|--------|---------|
| creators | id, handle, name, bio, avatar_url, created_at |
| stores | id, creator_id, title, description, theme, published |
| courses | id, store_id, day_number, title, order |
| spots | id, course_id, name, description, order |
| products | id, spot_id, mrt_product_id, name, price, mylink_url |
| click_logs | id, product_id, clicked_at, user_agent |

---

## 4. 트러블슈팅 참고표 (가이드 09챕터)

| 증상 | 원인 | 해결 |
|------|------|------|
| 폼 제출 시 500 에러 | Supabase 환경변수 누락 | 환경변수 확인 후 재배포 |
| Slack 알림 미수신 | SLACK_WEBHOOK_URL 미설정 | 환경변수 추가 후 재배포 |
| Supabase INSERT 실패 | RLS 정책 없음 | allow_insert 정책 SQL 재실행 |
| 빌드 실패 | 타입 오류 | 에러 메시지 확인 후 수정 |
| 모바일 레이아웃 깨짐 | 고정 px 값 사용 | 반응형 단위로 수정 |

---

## 5. 실행 계획

| 액션 | 담당 | 기한 |
|------|------|------|
| 마이스토어 DB 스키마 상세 설계 (6개 테이블) | 수갱주니어 | 다음 개발 세션 |
| Next.js API Route + Supabase 연동 뼈대 코드 작성 | 수갱주니어 | 스키마 확정 후 |
| RLS 정책 설계 (크리에이터별 데이터 격리) | 수갱주니어 | 스키마 확정 후 |
| Slack 알림 채널 및 메시지 포맷 확정 | 수경님 | 미정 |
| 목업 A/B/C 중 최종 스타일 결정 | 수경님 | 미정 |
| youtube-mcp 활성화 후 나고야 영상 코스 추출 | 수갱주니어 | Claude 재시작 후 즉시 |
| 영준님 보고 자료 최종 점검 | 수경님 | 미정 |

---

## 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|---------|
| v1.0 | 2026-04-13 | 최초 작성 |

---

다음 리뷰 예정: 마이스토어 DB 스키마 설계 세션 / 담당자: 석수경
