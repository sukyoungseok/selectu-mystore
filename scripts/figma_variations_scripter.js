// ═══════════════════════════════════════════════════════════
// 마이스토어 베리에이션 생성 — Scripter용 (데스크톱 Figma)
// 파일: HHHwWdq7CyVAiOlZ2oHEcq · 페이지: 🟢 프로모션 페이지 템플릿
//
// 데스크톱 Figma엔 Pretendard가 설치돼 있으므로 폰트 대체 없이
// "디자인 그대로, 닉네임 텍스트만" 일괄 교체한다.
// 프로필 사진은 이 스크립트가 끝난 뒤 별도로 적용한다.
//
// 사용법: Scripter에 전체 붙여넣고 ▶(Cmd+Enter) 실행 → 결과창의
//        JSON 한 덩어리를 복사해서 수갱주니어에게 전달.
// ═══════════════════════════════════════════════════════════

const CREATORS = ["허니블링", "수블리", "류랑", "다은"];
const TEMPLATE_IDS = {
  "MO-1": "1:1892", "MO-2": "1:1912", "MO-3": "1:1804",
  "PC-1": "1:1865", "PC-2": "1:2185", "PC-3": "1:2292", "OG": "1:2020",
};
const OLD_NAME = "파덕츄";

// ── 폰트 프리로드 (설치 안 된 폰트는 자동 skip) ──
const FONT_CANDIDATES = [
  { family: "Pretendard", style: "Black" },
  { family: "Pretendard", style: "ExtraBold" },
  { family: "Pretendard", style: "Bold" },
  { family: "Pretendard", style: "SemiBold" },
  { family: "Pretendard", style: "Medium" },
  { family: "Pretendard", style: "Regular" },
  { family: "Pretendard", style: "Light" },
];
const loadedFonts = [];
for (const f of FONT_CANDIDATES) {
  try { await figma.loadFontAsync(f); loadedFonts.push(`${f.family} ${f.style}`); } catch (e) {}
}

// ── 소스 페이지 / 베리에이션 페이지 준비 ──
const sourcePage = figma.root.children.find(p => p.name.includes("프로모션 페이지 템플릿"));
if (!sourcePage) throw new Error("'프로모션 페이지 템플릿' 페이지를 찾을 수 없어요.");
await figma.setCurrentPageAsync(sourcePage);

let varPage = figma.root.children.find(p => p.name === "베리에이션");
if (!varPage) { varPage = figma.createPage(); varPage.name = "베리에이션"; }
else { for (const c of [...varPage.children]) c.remove(); }

const templates = {};
const missingTemplates = [];
for (const [k, id] of Object.entries(TEMPLATE_IDS)) {
  const n = figma.getNodeById(id);
  if (!n) missingTemplates.push(`${k}(${id})`);
  else templates[k] = n;
}

// ── 텍스트 교체 (mixed-style 보존) ──
async function replaceAllText(node, oldName, newName, fails) {
  if (node.type === "TEXT" && node.characters.includes(oldName)) {
    try { await replaceInTextNode(node, oldName, newName); }
    catch (e) { fails.push(`${node.id}: ${e.message}`); }
  }
  if ("children" in node) {
    for (const child of node.children) await replaceAllText(child, oldName, newName, fails);
  }
}
async function replaceInTextNode(t, oldName, newName) {
  const content = t.characters;
  const idx = content.indexOf(oldName);
  if (idx === -1) return;
  // 이 노드가 쓰는 폰트 전부 로드
  const fonts = new Map();
  for (let i = 0; i < content.length; i++) {
    const fn = t.getRangeFontName(i, i + 1);
    if (fn !== figma.mixed) fonts.set(`${fn.family}|${fn.style}`, fn);
  }
  for (const fn of fonts.values()) { try { await figma.loadFontAsync(fn); } catch (e) {} }
  // uniform → 단순 교체
  if (t.fontName !== figma.mixed && t.fills !== figma.mixed) {
    t.characters = content.split(oldName).join(newName);
    return;
  }
  // mixed-style → 글자별 스타일 저장 후 복원
  const styles = [];
  for (let i = 0; i < content.length; i++) {
    styles.push({
      fontName: t.getRangeFontName(i, i + 1),
      fontSize: t.getRangeFontSize(i, i + 1),
      fills: t.getRangeFills(i, i + 1),
      letterSpacing: t.getRangeLetterSpacing(i, i + 1),
      lineHeight: t.getRangeLineHeight(i, i + 1),
    });
  }
  t.characters = content.slice(0, idx) + newName + content.slice(idx + oldName.length);
  const shift = newName.length - oldName.length;
  const nameStyle = styles[idx];
  const apply = (ci, s) => {
    const a = ci, b = ci + 1;
    try {
      if (s.fontName && s.fontName !== figma.mixed) t.setRangeFontName(a, b, s.fontName);
      if (s.fontSize && s.fontSize !== figma.mixed) t.setRangeFontSize(a, b, s.fontSize);
      if (s.fills && s.fills !== figma.mixed) t.setRangeFills(a, b, s.fills);
      if (s.letterSpacing && s.letterSpacing !== figma.mixed) t.setRangeLetterSpacing(a, b, s.letterSpacing);
      if (s.lineHeight && s.lineHeight !== figma.mixed) t.setRangeLineHeight(a, b, s.lineHeight);
    } catch (e) {}
  };
  for (let i = 0; i < idx; i++) apply(i, styles[i]);
  for (let i = 0; i < newName.length; i++) apply(idx + i, nameStyle);
  for (let i = idx + oldName.length; i < content.length; i++) apply(i + shift, styles[i]);
}

// ── 메인: 4명 × 7프레임 클론 + 닉네임 교체 ──
const FRAME_GAP = 80, COL_GAP = 120;
let xOffset = 0;
const result = {};
const textFailures = [];

for (const nick of CREATORS) {
  let yOffset = 0, colWidth = 0;
  const frames = {}, profileSlots = [];
  for (const [key, tmpl] of Object.entries(templates)) {
    const clone = tmpl.clone();
    clone.name = `${nick}_${key}`;
    varPage.appendChild(clone);
    clone.x = xOffset; clone.y = yOffset;
    colWidth = Math.max(colWidth, clone.width);
    yOffset += clone.height + FRAME_GAP;
    await replaceAllText(clone, OLD_NAME, nick, textFailures);
    for (const s of clone.findAll(x => x.name === "profile-photo-slot")) profileSlots.push(s.id);
    frames[key] = clone.id;
  }
  result[nick] = { frames, profileSlots };
  xOffset += colWidth + COL_GAP;
}

print("✅ 베리에이션 생성 완료");
print("로드된 폰트: " + loadedFonts.join(", "));
print("템플릿 누락: " + (missingTemplates.length ? missingTemplates.join(", ") : "없음"));
print("텍스트 교체 실패: " + (textFailures.length ? textFailures.join(" / ") : "없음"));
print("");
print("──── 아래 JSON을 복사해서 전달하세요 ────");
print(JSON.stringify({ varPageId: varPage.id, result, textFailures, missingTemplates }));
