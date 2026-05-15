// 크리에이터별 이메일 가이드 일괄 생성 스크립트
// 실행: node generate-creator-emails.js
// 결과: emails/{크리에이터명}.html

const fs = require('fs');
const path = require('path');

const ROOT = __dirname;
const TEMPLATE_PATH = path.join(ROOT, 'email-template.html');
const IMAGE_PATH = path.join(ROOT, 'referrer-code-form.png');
const OUTPUT_DIR = path.join(ROOT, 'emails');

// 협업 대상자 데이터 (시트 "협업 대상자" 탭 기준)
const creators = [
  {
    creator_name: '허니블링',
    instagram_id: 'honey_veling',
    fee: '2,800,000원',
    draft_due_date: '~ 5/17',
    coupon_url: 'https://www.myrealtrip.com/promotions/mkpt-igcoupon-honeyveling',
    form_url: 'https://docs.google.com/forms/d/e/1FAIpQLScag_7-0_XTxVLbSyQYcvokKY2BXQXLjEzjiNXIOk2ysjCMUw/viewform?usp=pp_url&entry.243801486=honey_veling',
    submission_form_url: 'https://docs.google.com/forms/d/e/1FAIpQLSecqSxL-e3AE813OlYTVHP3ropb9xv57444RWRHiYYnLgPpsQ/viewform?usp=pp_url&entry.1034623927=honeyveling%40naver.com&entry.2000063906=%5B%EB%A7%88%EC%BC%80%ED%8C%85%ED%8C%8C%ED%8A%B8%EB%84%88%5D%20%EC%9D%B8%EC%8A%A4%ED%83%80%EA%B7%B8%EB%9E%98%EB%A8%B8%20%EC%A0%84%EC%9A%A9%20%EC%BF%A0%ED%8F%B0%ED%8C%A9%20%28%EC%9B%90%EA%B3%A0%EB%A3%8C%29',
  },
  {
    creator_name: '수블리',
    instagram_id: 'suvely07',
    fee: '1,200,000원',
    draft_due_date: '~ 5/18',
    coupon_url: 'https://www.myrealtrip.com/promotions/mkpt-igcoupon-suvely07',
    form_url: 'https://docs.google.com/forms/d/e/1FAIpQLScag_7-0_XTxVLbSyQYcvokKY2BXQXLjEzjiNXIOk2ysjCMUw/viewform?usp=pp_url&entry.243801486=suvely07',
    submission_form_url: 'https://docs.google.com/forms/d/e/1FAIpQLSecqSxL-e3AE813OlYTVHP3ropb9xv57444RWRHiYYnLgPpsQ/viewform?usp=pp_url&entry.1034623927=tndusdl2948%40naver.com&entry.2000063906=%5B%EB%A7%88%EC%BC%80%ED%8C%85%ED%8C%8C%ED%8A%B8%EB%84%88%5D%20%EC%9D%B8%EC%8A%A4%ED%83%80%EA%B7%B8%EB%9E%98%EB%A8%B8%20%EC%A0%84%EC%9A%A9%20%EC%BF%A0%ED%8F%B0%ED%8C%A9%20%28%EC%9B%90%EA%B3%A0%EB%A3%8C%29',
  },
  {
    creator_name: '다은',
    instagram_id: '_danie_e',
    fee: '1,500,000원',
    draft_due_date: '~ 5/17',
    coupon_url: 'https://www.myrealtrip.com/promotions/mkpt-igcoupon-daniee',
    form_url: 'https://docs.google.com/forms/d/e/1FAIpQLScag_7-0_XTxVLbSyQYcvokKY2BXQXLjEzjiNXIOk2ysjCMUw/viewform?usp=pp_url&entry.243801486=_danie_e',
    submission_form_url: 'https://docs.google.com/forms/d/e/1FAIpQLSecqSxL-e3AE813OlYTVHP3ropb9xv57444RWRHiYYnLgPpsQ/viewform?usp=pp_url&entry.1034623927=ekdms0518%40naver.com&entry.2000063906=%5B%EB%A7%88%EC%BC%80%ED%8C%85%ED%8C%8C%ED%8A%B8%EB%84%88%5D%20%EC%9D%B8%EC%8A%A4%ED%83%80%EA%B7%B8%EB%9E%98%EB%A8%B8%20%EC%A0%84%EC%9A%A9%20%EC%BF%A0%ED%8F%B0%ED%8C%A9%20%28%EC%9B%90%EA%B3%A0%EB%A3%8C%29',
  },
  {
    creator_name: '조선여자 모나',
    instagram_id: 'hanbok_travelarts',
    fee: '2,000,000원',
    draft_due_date: '~ 5/18',
    coupon_url: 'https://www.myrealtrip.com/promotions/mkpt-igcoupon-hanboktravelarts',
    form_url: 'https://docs.google.com/forms/d/e/1FAIpQLScag_7-0_XTxVLbSyQYcvokKY2BXQXLjEzjiNXIOk2ysjCMUw/viewform?usp=pp_url&entry.243801486=hanbok_travelarts',
    submission_form_url: 'https://docs.google.com/forms/d/e/1FAIpQLSecqSxL-e3AE813OlYTVHP3ropb9xv57444RWRHiYYnLgPpsQ/viewform?usp=pp_url&entry.1034623927=hanbok.mona%40gmail.com&entry.2000063906=%5B%EB%A7%88%EC%BC%80%ED%8C%85%ED%8C%8C%ED%8A%B8%EB%84%88%5D%20%EC%9D%B8%EC%8A%A4%ED%83%80%EA%B7%B8%EB%9E%98%EB%A8%B8%20%EC%A0%84%EC%9A%A9%20%EC%BF%A0%ED%8F%B0%ED%8C%A9%20%28%EC%9B%90%EA%B3%A0%EB%A3%8C%29',
  },
  {
    creator_name: '다챌',
    instagram_id: 'dachallll',
    fee: '200,000원',
    draft_due_date: '~ 5/17',
    coupon_url: 'https://www.myrealtrip.com/promotions/mkpt-igcoupon-dachallll',
    form_url: 'https://docs.google.com/forms/d/e/1FAIpQLScag_7-0_XTxVLbSyQYcvokKY2BXQXLjEzjiNXIOk2ysjCMUw/viewform?usp=pp_url&entry.243801486=dachallll',
    submission_form_url: 'https://docs.google.com/forms/d/e/1FAIpQLSecqSxL-e3AE813OlYTVHP3ropb9xv57444RWRHiYYnLgPpsQ/viewform?usp=pp_url&entry.1034623927=amica1110%40naver.com&entry.2000063906=%5B%EB%A7%88%EC%BC%80%ED%8C%85%ED%8C%8C%ED%8A%B8%EB%84%88%5D%20%EC%9D%B8%EC%8A%A4%ED%83%80%EA%B7%B8%EB%9E%98%EB%A8%B8%20%EC%A0%84%EC%9A%A9%20%EC%BF%A0%ED%8F%B0%ED%8C%A9%20%28%EC%9B%90%EA%B3%A0%EB%A3%8C%29',
  },
];

// 출력 폴더 생성
if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR, { recursive: true });

// 이미지 base64 인코딩 (한 번만)
const imageBase64 = fs.readFileSync(IMAGE_PATH).toString('base64');
const imageDataUrl = `data:image/png;base64,${imageBase64}`;

// 템플릿 읽기
const template = fs.readFileSync(TEMPLATE_PATH, 'utf-8');

// 각 크리에이터별 HTML 생성
const results = [];
for (const c of creators) {
  let html = template;
  html = html.replaceAll('{{creator_name}}', c.creator_name);
  html = html.replaceAll('{{instagram_id}}', c.instagram_id);
  html = html.replaceAll('{{fee}}', c.fee);
  html = html.replaceAll('{{draft_due_date}}', c.draft_due_date);
  html = html.replaceAll('{{coupon_url}}', c.coupon_url);
  html = html.replaceAll('{{form_url}}', c.form_url);
  html = html.replaceAll('{{submission_form_url}}', c.submission_form_url);
  html = html.replaceAll('{{IMAGE_BASE64}}', imageDataUrl);

  const outPath = path.join(OUTPUT_DIR, `${c.creator_name}.html`);
  fs.writeFileSync(outPath, html, 'utf-8');
  results.push({ name: c.creator_name, path: outPath, size: Buffer.byteLength(html) });
}

console.log('생성 완료:');
results.forEach(r => console.log(`  - ${r.name}: ${r.path} (${(r.size / 1024).toFixed(1)}KB)`));
