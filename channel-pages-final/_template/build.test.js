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
