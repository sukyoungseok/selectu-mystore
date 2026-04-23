# MyLink API 구조 파악 — 마이스토어 어필리에이트 연동 방향 확정

- **날짜:** 2026-04-13
- **주제:** MyLink API 실제 구조 확인 및 마이스토어 연동 방안 확정
- **유형:** 기술 의사결정
- **배경:** 마이스토어 MVP 기획 중 어필리에이트 추적 인프라 구조 명확화 필요

---

## 최종 결정 사항

**1.** MyLink API 구조 확인 완료 — POST /v1/mylink, Bearer 인증, mylink_id는 링크별 고유 ID임
**2.** 크리에이터 파트너 계정 연동 방식(방안 A) 확정 — 크리에이터 각자 파트너 계정 보유 → API 키로 링크 생성 → 수익 각자 귀속
**3.** 기술 타당성 High로 상향 — 구조 파악 완료, 동훈님 별도 확인 불필요

---

## 1. 배경 및 문제 정의

마이스토어 MVP 기획 중 크리에이터 어필리에이트 추적을 위해 기존 MyLink API 재활용 방향을 검토 중이었음. 그러나 인증 방식(파트너 JWT 의존인지, 서버용 독립 API 키인지)이 불명확하여 기술 타당성이 Medium-High로 평가되어 있었음.

상희님으로부터 "UTM만 붙이면 된다"는 안내를 받아 공식 API 문서(docs.myrealtrip.com) 분석 진행.

---

## 2. API 구조 분석 결과

공식 문서(docs.myrealtrip.com JS 번들 분석) 확인 결과:

| 항목 | 내용 |
| --- | --- |
| 엔드포인트 | POST /v1/mylink |
| 인증 | Authorization: Bearer {API 키} |
| 핵심 파라미터 | targetUrl (필수, 2,000자 이하), utm_content (선택, 최대 100자), open_in_app (선택) |
| 응답 | mylink_id (링크별 고유 ID), 단축 URL (myrealt.rip/xxxxx) |

mylink_id는 파트너 계정 공통 ID가 아닌 링크 생성 시마다 발급되는 고유 ID임. 어필리에이트 수익은 mylink_id 기준으로 귀속됨.

링크 형식 예시:

| 유형 | URL 형식 |
| --- | --- |
| 웹 랜딩 | https://www.myrealtrip.com/offers/3467?mylink_id=1234567&utm_content=mystore_{slug} |
| 앱 오픈 포함 | https://www.myrealtrip.com/offers/3467?mylink_id=1234567&utm_content=mystore_{slug}&open_in_app=true |

---

## 3. 연동 방안 결정

방안 A(크리에이터 각자 파트너 계정 보유 → API 키 사용)로 확정.

방안 B(마이스토어 서비스 계정 하나로 통합 생성 후 내부 정산)는 수익 귀속 구조상 부적합하여 제외.

온보딩 흐름:

크리에이터 가입 → 마이리얼트립 파트너 계정 연동 → API 키 마이스토어 서버에 저장 → 상품 태그 시 해당 API 키로 POST /v1/mylink 호출 → mylink_id 발급 및 DB 저장 → 공개 페이지 클릭 시 수익 크리에이터 계정에 자동 귀속

---

## 4. 실행 계획

| Phase | 액션 | 담당 | 기한 |
| --- | --- | --- | --- |
| 온보딩 플로우 | 크리에이터 파트너 계정 연동 UI 설계 | 개발팀 | MVP 개발 중 |
| API 키 저장 | 크리에이터 API 키 서버 암호화 저장 방식 설계 | 개발팀 | MVP 개발 중 |
| 링크 생성 | 상품 태그 시 POST /v1/mylink 자동 호출 로직 구현 | 개발팀 | MVP 개발 중 |

---

## 변경 이력

| 버전 | 날짜 | 변경 내용 |
| --- | --- | --- |
| v1 | 2026-04-13 | 최초 작성 |
