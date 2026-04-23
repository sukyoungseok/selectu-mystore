# FULL-LOG — MyLink API 구조 파악

- **날짜:** 2026-04-13
- **세션 유형:** 기술 조사 및 의사결정

---

## 논의 흐름

상희님이 마이스토어 MyLink 연동에 대해 "UTM만 붙이면 된다"고 안내함.

공식 API 문서(docs.myrealtrip.com) 확인 시도. SPA(React)라 JS 번들 직접 분석으로 내용 추출.

확인 결과:
- POST /v1/mylink 엔드포인트 존재
- Authorization: Bearer {API 키} 인증 방식
- mylink_id는 링크별 고유 ID (처음엔 파트너 계정 ID로 오인했으나, 수경님이 "링크 고유 아이디"라고 정정)
- targetUrl 넘기면 myrealt.rip/xxxxx 단축 URL + mylink_id 발급
- utm_content 파라미터로 성과 추적 가능

연동 방식은 크리에이터 각자 파트너 계정 보유 방안(방안 A)으로 확정. 수경님이 "당연히 방안 A"라고 확인.

화이트글러브 방식 시 온보딩 복잡도 낮음 (운영팀이 파트너 계정 세팅 대행). 셀프 편집 툴 시 파트너 계정 연동 UI 추가 구현 필요 → 화이트글러브 방식의 기술적 이점 하나 추가 확인됨.

---

## 핵심 확인 사항 요약

| 항목 | 확인 전 | 확인 후 |
| --- | --- | --- |
| 인증 방식 | 불명확 (JWT 의존 여부 미확인) | Bearer 토큰 (파트너 계정 API 키) |
| mylink_id 성격 | 파트너 계정 ID로 오인 | 링크 생성 시마다 발급되는 고유 ID |
| 링크 생성 방법 | URL에 파라미터 붙이기로 오인 | POST /v1/mylink 호출 후 mylink_id 발급 필요 |
| 기술 타당성 | Medium-High | High |
