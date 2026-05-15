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

test('스크립트 데이터: CREATOR·CITY_DAYS·CITY_EXPENSE·TRIP_KEYS가 주입된다', () => {
  const html = buildPage(data);
  assert.ok(html.includes('const CREATOR={"name":"부산맛나","email":"ttt0831@naver.com","couponUrl":"https://www.myrealtrip.com/coupons"};'));
  assert.ok(html.includes('const TRIP_KEYS=["sapporo"];'));
  assert.ok(html.includes('"sapporo":'));
  assert.ok(html.includes('"삿포로 3박 4일 총경비"'));
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
