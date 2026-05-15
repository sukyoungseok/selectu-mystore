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

const SNS_ICONS = {
  instagram: '../assets/icons/insta.png',
  youtube:   '../assets/icons/youtube.png',
  tiktok:    '../assets/icons/tiktok-logo.png',
  threads:   '../assets/icons/threads-logo.png',
  blog:      '../assets/icons/blog.png',
};

function renderSnsPills(sns) {
  return sns.map(s => {
    if (s.type === 'email') {
      return `<a class="sns-icon" href="${s.url}" title="이메일 문의">✉️</a>`;
    }
    const icon = SNS_ICONS[s.type] || SNS_ICONS.instagram;
    const label = s.type.charAt(0).toUpperCase() + s.type.slice(1);
    return `<a class="sns-icon" href="${s.url}" target="_blank" aria-label="${label}"><img src="${icon}" alt="${label}"/></a>`;
  }).join('\n            ');
}

function renderTripCards(trips) {
  return trips.map(t => {
    const badges = t.badges.map(b => `<span class="tc-badge">${esc(b)}</span>`).join('');
    return `<div class="trip-card">
          <div class="tc-hero ${t.city}">
            <div class="tc-hero-content">
              <div class="tc-flag">${t.flag}</div>
              <div class="tc-title-col">
                <div class="tc-badges">${badges}</div>
                <div class="tc-title">${esc(t.title)}</div>
              </div>
            </div>
          </div>
          <div class="tc-body">
            <div class="tc-ask">어디부터 볼까요?</div>
            <div class="tc-choice">
              <button class="plan" onclick="openCourse('${t.city}')">
                <div><strong>일정표 보기</strong><span>DAY별 동선 확인</span></div>
                <div class="tc-arr">›</div>
              </button>
              <button class="cost" onclick="openExpensePanel('${t.city}')">
                <div class="tc-c-row1"><strong>상세 경비 보기</strong><div class="tc-c-price"><span class="tc-c-num">${esc(t.costFrom)}</span><span class="tc-arr" style="margin-left:0">›</span></div></div>
                <div class="tc-c-row2"><span class="tc-c-badge">🔥 인기</span><span class="tc-c-sub">항공·숙소·투어 한 번에</span></div>
              </button>
            </div>
          </div>
        </div>`;
  }).join('\n        ');
}

function renderTripDots(trips) {
  return trips.map((t, i) => `<span class="trip-dot${i === 0 ? ' on' : ''}"></span>`).join('');
}

function renderLinkSections(sections) {
  return sections.map(sec => {
    const items = sec.items.map(it => {
      const badges = (it.badges || [])
        .map(b => `<span class="ls-badge ${b.style || 'hot'}">${esc(b.text)}</span>`)
        .join('');
      if (it.type === 'og') {
        return `<a class="ls-og" href="${it.url}" target="_blank">
          <img src="${it.img}" style="width:100%;height:150px;object-fit:cover;display:block"/>
          <div class="ls-og-body">
            ${badges ? `<div class="ls-badges">${badges}</div>` : ''}
            <div class="ls-og-title">${esc(it.title)}</div>
            <div class="ls-og-domain">${esc(it.domain || '')}</div>
          </div>
        </a>`;
      }
      return `<a class="ls-thumb" href="${it.url}" target="_blank">
          <div class="ls-thumb-icon">${it.icon || ''}</div>
          <div class="ls-thumb-body">
            ${badges ? `<div class="ls-badges">${badges}</div>` : ''}
            <div class="ls-thumb-title">${esc(it.title)}</div>
            ${it.sub ? `<div class="ls-thumb-sub">${esc(it.sub)}</div>` : ''}
          </div>
          <div class="ls-thumb-arrow">›</div>
        </a>`;
    }).join('\n        ');
    return `<div class="links-section">
        <h3>${esc(sec.heading)}</h3>
        ${items}
      </div>`;
  }).join('\n      ');
}

function renderCouponCards(cards) {
  return cards.map(c =>
    `<div class="coupon-card"><div class="cc-stripe" style="background:${c.color}"></div><div class="cc-body"><div class="cc-label" style="color:${c.color}">${esc(c.label)}</div><div class="cc-title">${esc(c.title)}</div><div class="cc-desc">${esc(c.desc)}</div><div class="cc-footer"><div class="cc-expire">${esc(c.expire)}</div><div class="cc-remain">${esc(c.remain)}</div></div></div><button class="cc-btn" style="background:${c.color}" onclick="window.open('${c.url}','_blank')">받기</button></div>`
  ).join('\n      ');
}

function renderBgCss(trips) {
  return trips
    .map(t => `.tc-hero.${t.city}{background:url('${t.cardImg}') center/cover no-repeat}`)
    .join('\n');
}

function buildPage(data) {
  let html = fs.readFileSync(path.join(__dirname, 'shell.html'), 'utf8');
  const theme = THEMES[data.theme] || THEMES.ember;

  const cityDays = Object.fromEntries(data.trips.map(t => [t.city, t.days]));
  const cityExpense = Object.fromEntries(data.trips.map(t => [t.city, t.expense]));
  const tripKeys = data.trips.map(t => t.city);
  const creator = {
    name: data.creator.name,
    email: data.creator.email,
    couponUrl: data.coupon.showcaseUrl,
  };

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
    '<!--{{SNS_PILLS}}-->': renderSnsPills(data.sns),
    '<!--{{TRIP_CARDS}}-->': renderTripCards(data.trips),
    '<!--{{TRIP_DOTS}}-->': renderTripDots(data.trips),
    '<!--{{LINK_SECTIONS}}-->': renderLinkSections(data.linkSections),
    '<!--{{COUPON_CARDS}}-->': renderCouponCards(data.coupon.cards),
    '{{CREATOR_JSON}}': JSON.stringify(creator),
    '{{PRODUCTS_JSON}}': JSON.stringify(data.products),
    '{{CITY_DAYS_JSON}}': JSON.stringify(cityDays),
    '{{CITY_EXPENSE_JSON}}': JSON.stringify(cityExpense),
    '{{TRIP_KEYS_JSON}}': JSON.stringify(tripKeys),
  };

  for (const [k, v] of Object.entries(repl)) {
    html = html.split(k).join(v);
  }
  return html;
}

if (require.main === module) {
  const name = process.argv[2];
  if (!name) {
    console.error('사용법: node build.js <크리에이터명>');
    process.exit(1);
  }
  let data;
  try {
    data = require(path.join(__dirname, 'data', name + '.js'));
  } catch (e) {
    console.error(`데이터 파일을 찾을 수 없습니다: data/${name}.js`);
    process.exit(1);
  }
  const out = buildPage(data);
  const dest = path.join(__dirname, '..', 'done', name + '.html');
  fs.writeFileSync(dest, out, 'utf8');
  console.log('생성 완료:', dest);
}

module.exports = { buildPage, THEMES };
