import { chromium } from 'playwright';
import fs from 'fs';
import https from 'https';
import http from 'http';
import path from 'path';

const DIR = '/Users/sukyoung-seok/mystore-mockup/assets/images';

async function downloadFile(url, filePath) {
  return new Promise((resolve, reject) => {
    const proto = url.startsWith('https') ? https : http;
    const file = fs.createWriteStream(filePath);
    proto.get(url, { headers: { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36' } }, (res) => {
      res.pipe(file);
      file.on('finish', () => {
        file.close();
        const size = fs.statSync(filePath).size;
        resolve(size);
      });
    }).on('error', (err) => {
      fs.unlink(filePath, () => {});
      reject(err);
    });
  });
}

async function getImagesFromProfile(page, url, label) {
  console.log(`\n=== ${label} 접속 중: ${url} ===`);

  const interceptedImages = [];

  page.on('response', async (response) => {
    const respUrl = response.url();
    if (respUrl.includes('cdninstagram.com') &&
        (respUrl.includes('.jpg') || respUrl.includes('.webp')) &&
        !respUrl.includes('s150x150') && !respUrl.includes('s100x100') &&
        !respUrl.includes('s32x32')) {
      try {
        const buffer = await response.body();
        if (buffer.length > 10000) {
          interceptedImages.push({ url: respUrl, size: buffer.length, buffer });
          console.log(`  캡처: ${buffer.length} bytes - ${respUrl.substring(0, 80)}`);
        }
      } catch (e) {}
    }
  });

  try {
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(5000);

    // 스크롤해서 더 많은 이미지 로드
    await page.evaluate(() => window.scrollBy(0, 500));
    await page.waitForTimeout(2000);

  } catch (e) {
    console.log(`  접속 오류: ${e.message}`);
  }

  // DOM에서도 이미지 수집
  const domImages = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('img'))
      .map(img => ({ src: img.src, width: img.naturalWidth, height: img.naturalHeight }))
      .filter(img => img.src.includes('cdninstagram') && img.width > 100);
  });

  console.log(`  DOM 이미지: ${domImages.length}개, 네트워크 캡처: ${interceptedImages.length}개`);

  return { interceptedImages, domImages };
}

async function main() {
  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
    viewport: { width: 390, height: 844 },
  });

  const targets = [
    { url: 'https://www.instagram.com/today.brighten/', label: '늘찬맘', files: ['neulchanmam-hero.jpg', 'neulchanmam-card1.jpg', 'neulchanmam-card2.jpg'] },
    { url: 'https://www.instagram.com/sing.______/', label: '씽아', files: ['singa-hero.jpg', 'singa-card1.jpg', 'singa-card2.jpg'] },
    { url: 'https://www.instagram.com/hyemingway0707/', label: '혜밍웨이', files: ['hyemingway-hero.jpg', 'hyemingway-card1.jpg', 'hyemingway-card2.jpg'] },
    { url: 'https://www.instagram.com/busan_matna_/', label: '부산맛나', files: ['busanmatna-card1.jpg', 'busanmatna-card2.jpg'] },
    { url: 'https://www.instagram.com/hwung_travel/', label: '훵', files: ['hwung-hero.jpg'] },
    { url: 'https://www.instagram.com/daero._.nana/', label: '대로와나나', files: ['daero-card2.jpg'] },
  ];

  const results = {};

  for (const target of targets) {
    const page = await context.newPage();
    const { interceptedImages, domImages } = await getImagesFromProfile(page, target.url, target.label);

    // 네트워크 캡처된 이미지 저장 (크기순 정렬)
    const sorted = interceptedImages.sort((a, b) => b.size - a.size);

    const saved = [];
    for (let i = 0; i < Math.min(sorted.length, target.files.length); i++) {
      const filePath = path.join(DIR, target.files[i]);
      fs.writeFileSync(filePath, sorted[i].buffer);
      saved.push({ file: target.files[i], size: sorted[i].size });
      console.log(`  저장: ${target.files[i]} (${sorted[i].size} bytes)`);
    }

    // DOM 이미지로 보완 (네트워크 캡처 부족 시)
    if (saved.length < target.files.length && domImages.length > 0) {
      console.log(`  DOM 이미지로 보완 시도...`);
      const domSorted = domImages.sort((a, b) => (b.width * b.height) - (a.width * a.height));
      for (let i = saved.length; i < Math.min(domImages.length + saved.length, target.files.length); i++) {
        const domImg = domSorted[i - saved.length];
        if (domImg) {
          const filePath = path.join(DIR, target.files[i]);
          try {
            const size = await downloadFile(domImg.src, filePath);
            saved.push({ file: target.files[i], size });
            console.log(`  DOM 저장: ${target.files[i]} (${size} bytes)`);
          } catch (e) {
            console.log(`  DOM 저장 실패: ${e.message}`);
          }
        }
      }
    }

    results[target.label] = saved;
    await page.close();
  }

  await browser.close();

  console.log('\n\n=== 최종 결과 ===');
  for (const [label, saved] of Object.entries(results)) {
    console.log(`${label}: ${saved.length}개 저장`);
    saved.forEach(s => console.log(`  - ${s.file} (${s.size} bytes)`));
  }
}

main().catch(console.error);
