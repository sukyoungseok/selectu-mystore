const fs = require('fs');
const path = require('path');

const THEMES = {
  ember:  { amber:'#C83020', sage:'#E05848', accent:'#7A0A0A' },
  ocean:  { amber:'#1D6FB8', sage:'#3E9BD6', accent:'#0A3A5C' },
  forest: { amber:'#2E7D4F', sage:'#5BA877', accent:'#14502E' },
  grape:  { amber:'#7C3AED', sage:'#A78BDA', accent:'#4C1D95' },
  rose:   { amber:'#D6336C', sage:'#E885A8', accent:'#8C1D40' },
  slate:  { amber:'#475569', sage:'#7B8A9E', accent:'#1E293B' },
};

function esc(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function renderBgCss(trips) {
  return trips
    .map(t => `.tc-hero.${t.city}{background:url('${t.cardImg}') center/cover no-repeat}`)
    .join('\n');
}

function buildPage(data) {
  let html = fs.readFileSync(path.join(__dirname, 'shell.html'), 'utf8');
  const theme = THEMES[data.theme] || THEMES.ember;

  const repl = {
    '{{NAME}}': data.creator.name,
    '{{TAGLINE}}': data.creator.tagline,
    '{{EMAIL}}': data.creator.email,
    '{{PROFILE_IMG}}': data.creator.profileImg,
    '{{HERO_IMG}}': data.creator.heroImg,
    '{{C_AMBER}}': theme.amber,
    '{{C_SAGE}}': theme.sage,
    '{{C_ACCENT}}': theme.accent,
    '{{COUPON_URL}}': data.coupon.showcaseUrl,
    '{{COUPON_KICKER}}': data.coupon.kicker,
    '{{COUPON_TITLE}}': data.coupon.title,
    '{{COUPON_AMOUNT}}': data.coupon.amount,
    '{{COUPON_COUNT}}': data.coupon.count,
    '{{TEXTBLOCK_TITLE}}': data.textblock.title,
    '{{TEXTBLOCK_BODY}}': data.textblock.body,
    '/*{{BG_CSS}}*/': renderBgCss(data.trips),
  };

  for (const [k, v] of Object.entries(repl)) {
    html = html.split(k).join(v);
  }
  return html;
}

module.exports = { buildPage, THEMES };
