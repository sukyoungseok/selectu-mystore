/**
 * figma_create_variations.js
 *
 * use_figma 툴에 code 파라미터로 붙여넣기 해서 실행.
 * Figma 파일: 마케팅파트너 마이스토어 베리에이션 (HHHwWdq7CyVAiOlZ2oHEcq)
 * 소스 페이지: 🟢 프로모션 페이지 템플릿
 *
 * 실행 전:
 *   1. CREATORS 배열을 sheets_to_creators.py 출력으로 교체
 *   2. Figma 앱에서 해당 파일이 열려 있어야 함
 */

// ─────────────────────────────────────────────
// 1. 크리에이터 데이터 (sheets_to_creators.py 출력으로 교체)
// ─────────────────────────────────────────────
const CREATORS = [
  { nickname: "훵",    profileUrl: "https://mystore-mrt.vercel.app/assets/profiles/훵.jpg" },
  { nickname: "헨리",  profileUrl: "https://mystore-mrt.vercel.app/assets/profiles/헨리.jpg" },
  { nickname: "홍다닥", profileUrl: "https://mystore-mrt.vercel.app/assets/profiles/홍다닥.jpg" },
  { nickname: "파파트래블", profileUrl: "https://mystore-mrt.vercel.app/assets/profiles/파파트래블.jpg" },
  { nickname: "트이프", profileUrl: "https://mystore-mrt.vercel.app/assets/profiles/트이프.jpg" },
  { nickname: "재구언", profileUrl: "https://mystore-mrt.vercel.app/assets/profiles/재구언.jpg" },
  { nickname: "제이나", profileUrl: "https://mystore-mrt.vercel.app/assets/profiles/제이나.jpg" },
  { nickname: "씽아",  profileUrl: "https://mystore-mrt.vercel.app/assets/profiles/씽아.jpg" },
  { nickname: "부산맛나", profileUrl: "https://mystore-mrt.vercel.app/assets/profiles/부산맛나.jpg" },
  { nickname: "백자매", profileUrl: "https://mystore-mrt.vercel.app/assets/profiles/백자매.jpg" },
  { nickname: "민픽",  profileUrl: "https://mystore-mrt.vercel.app/assets/profiles/민픽.jpg" },
  { nickname: "대로와나나", profileUrl: "https://mystore-mrt.vercel.app/assets/profiles/대로와나나.jpg" },
  { nickname: "늘찬맘", profileUrl: "https://mystore-mrt.vercel.app/assets/profiles/늘찬맘.jpg" },
];

// ─────────────────────────────────────────────
// 2. 템플릿 프레임 ID
//    파일: HHHwWdq7CyVAiOlZ2oHEcq / 페이지: 🟢 프로모션 페이지 템플릿
//    (2026-05-14 전수 확인 — 파일 수정 시 재확인 필요)
// ─────────────────────────────────────────────
const TEMPLATE_IDS = {
  "MO-1": "1:1892",  // 390x409  · 크리에이터명 + 프로필슬롯
  "MO-2": "1:1912",  // 390x537  · 크리에이터명
  "MO-3": "1:1804",  // 393x394  · 크리에이터명
  "PC-1": "1:1865",  // 1060x378 · 크리에이터명 + 프로필슬롯
  "PC-2": "1:2185",  // 1060x422 · 크리에이터명
  "PC-3": "1:2292",  // 1060x331 · 크리에이터명
  "OG":   "1:2020",  // 1200x630 · 크리에이터명(헤드라인+폰목업) + 프로필슬롯
};

// 7개 프레임 전부 닉네임이 "파덕츄"로 통일돼 있어 단일 OLD_NAME으로 처리 가능.
const OLD_NAME = "파덕츄";

// ─────────────────────────────────────────────
// 3. 메인
// ─────────────────────────────────────────────
async function main() {
  // 소스 페이지 찾기
  const sourcePage = figma.root.children.find(p => p.name.includes("프로모션 페이지 템플릿"));
  if (!sourcePage) throw new Error("'🟢 프로모션 페이지 템플릿' 페이지를 찾을 수 없어요.");

  // 베리에이션 페이지 준비
  let varPage = figma.root.children.find(p => p.name === "베리에이션");
  if (!varPage) {
    varPage = figma.createPage();
    varPage.name = "베리에이션";
  } else {
    // 기존 내용 초기화
    for (const child of [...varPage.children]) child.remove();
  }
  await figma.setCurrentPageAsync(varPage);

  // 폰트 로드
  const fonts = [
    { family: "Pretendard", style: "Bold" },
    { family: "Pretendard", style: "Extra Bold" },
    { family: "Pretendard", style: "Semi Bold" },
    { family: "Pretendard", style: "Regular" },
  ];
  for (const f of fonts) {
    try { await figma.loadFontAsync(f); } catch(e) { /* 없는 폰트는 skip */ }
  }

  // 템플릿 노드 가져오기
  const templates = {};
  const missingTemplates = [];
  for (const [key, id] of Object.entries(TEMPLATE_IDS)) {
    const node = figma.getNodeById(id);
    if (!node) { missingTemplates.push(`${key}(${id})`); continue; }
    templates[key] = node;
  }

  const FRAME_GAP = 80;
  const COL_GAP  = 120;
  let xOffset = 0;
  const exportedFrameIds = {};
  const imageFailures = [];

  for (const creator of CREATORS) {
    const creatorFrameIds = {};
    let yOffset = 0;
    let colWidth = 0;

    for (const [key, tmpl] of Object.entries(templates)) {
      // 클론
      const clone = tmpl.clone();
      clone.name = `${creator.nickname}_${key}`;
      varPage.appendChild(clone);
      clone.x = xOffset;
      clone.y = yOffset;

      colWidth = Math.max(colWidth, clone.width);
      yOffset += clone.height + FRAME_GAP;
      creatorFrameIds[key] = clone.id;

      // 텍스트 교체 (내용 기반) — 7개 프레임 전부 "파덕츄" 통일이라 재귀 교체 한 번으로 끝.
      // OG-tag는 헤드라인 "파덕츄" + 폰목업 안 닉네임까지 모두 이 함수가 처리.
      await replaceAllText(clone, OLD_NAME, creator.nickname);

      // 프로필 사진 교체
      if (creator.profileUrl) {
        try {
          const img = await figma.createImageAsync(creator.profileUrl);
          replaceProfileImage(clone, img.hash);
        } catch(e) {
          imageFailures.push(`${creator.nickname}_${key}: ${e.message}`);
        }
      }
    }

    exportedFrameIds[creator.nickname] = creatorFrameIds;
    xOffset += colWidth + COL_GAP;
  }

  return { creators: CREATORS.length, exportedFrameIds, missingTemplates, imageFailures };
}

// ─────────────────────────────────────────────
// 4. 텍스트 교체 (mixed-style 보존)
// ─────────────────────────────────────────────
async function replaceAllText(node, oldName, newName) {
  if (node.type === "TEXT" && node.characters.includes(oldName)) {
    await replaceInTextNode(node, oldName, newName);
  }
  if ("children" in node) {
    for (const child of node.children) {
      await replaceAllText(child, oldName, newName);
    }
  }
}

async function replaceInTextNode(textNode, oldName, newName) {
  const content = textNode.characters;
  const idx = content.indexOf(oldName);
  if (idx === -1) return;

  // 사용된 폰트 로드
  const uniqueFonts = new Map();
  for (let i = 0; i < content.length; i++) {
    const fn = textNode.getRangeFontName(i, i + 1);
    if (fn !== figma.mixed) uniqueFonts.set(`${fn.family}|${fn.style}`, fn);
  }
  for (const fn of uniqueFonts.values()) {
    try { await figma.loadFontAsync(fn); } catch(e) {}
  }

  // uniform 텍스트 → 단순 교체
  if (textNode.fontName !== figma.mixed && textNode.fills !== figma.mixed) {
    textNode.characters = content.replace(oldName, newName);
    return;
  }

  // mixed-style → 스타일 저장 후 교체 후 복원
  const charStyles = [];
  for (let i = 0; i < content.length; i++) {
    charStyles.push({
      fontName:      textNode.getRangeFontName(i, i + 1),
      fontSize:      textNode.getRangeFontSize(i, i + 1),
      fills:         textNode.getRangeFills(i, i + 1),
      letterSpacing: textNode.getRangeLetterSpacing(i, i + 1),
      lineHeight:    textNode.getRangeLineHeight(i, i + 1),
    });
  }

  const newContent = content.slice(0, idx) + newName + content.slice(idx + oldName.length);
  textNode.characters = newContent;

  const shift = newName.length - oldName.length;
  const nameStyle = charStyles[idx];

  for (let i = 0; i < idx; i++) applyStyle(textNode, i, charStyles[i]);
  for (let i = 0; i < newName.length; i++) applyStyle(textNode, idx + i, nameStyle);
  for (let i = idx + oldName.length; i < content.length; i++) {
    applyStyle(textNode, i + shift, charStyles[i]);
  }
}

function applyStyle(textNode, charIdx, style) {
  const s = charIdx, e = charIdx + 1;
  try {
    if (style.fontName      && style.fontName      !== figma.mixed) textNode.setRangeFontName(s, e, style.fontName);
    if (style.fontSize      && style.fontSize      !== figma.mixed) textNode.setRangeFontSize(s, e, style.fontSize);
    if (style.fills         && style.fills         !== figma.mixed) textNode.setRangeFills(s, e, style.fills);
    if (style.letterSpacing && style.letterSpacing !== figma.mixed) textNode.setRangeLetterSpacing(s, e, style.letterSpacing);
    if (style.lineHeight    && style.lineHeight    !== figma.mixed) textNode.setRangeLineHeight(s, e, style.lineHeight);
  } catch(e) {}
}

// ─────────────────────────────────────────────
// 5. 프로필 이미지 교체
// ─────────────────────────────────────────────
function replaceProfileImage(node, imageHash) {
  if (node.name === "profile-photo-slot" && "fills" in node) {
    node.fills = [{ type: "IMAGE", scaleMode: "FILL", imageHash }];
  }
  if ("children" in node) {
    for (const child of node.children) replaceProfileImage(child, imageHash);
  }
}

// use_figma는 코드를 async 컨텍스트로 감싸므로 top-level await/return 사용 가능.
return await main();
