// 쿠폰페이지 크리에이터 자동화 — Figma 플러그인
//
// 워크플로우 역할 분담:
//   - 인스타 프로필 사진 수집  → Python (scripts/fetch_instagram_profiles.py)
//                               결과: assets/profiles/{닉네임}.jpg
//   - Figma 복제/텍스트/사진   → 이 플러그인 (네트워크 없음, Desktop에서 실행)
//
// 입력: 프로필 이미지 파일들 (파일명 = {닉네임}__{인스타핸들}). 예) 허니블링__honey_veling.jpg
// 각 파일마다:
//   1. 마스터세트 복제 → 프레임 이름 = 닉네임 (이미 있으면 그 프레임 재사용)
//   2. #크리에이터 텍스트 레이어를 닉네임으로 교체
//   3. #인스타아이디 텍스트 레이어를 인스타 핸들로 교체 (= 추천인 코드)
//   4. 이미지 바이트 → figma.createImage → profile-photo-slot에 적용

const MASTER_NAME = "마스터세트";
const VAR_NAME = "#크리에이터";
const VAR_HANDLE = "#인스타아이디";
const SLOT_NAME = "profile-photo-slot";
const GAP = 400; // 세트 사이 세로 간격(px)

figma.showUI(__html__, { width: 360, height: 440 });

figma.ui.onmessage = async (msg) => {
  if (msg.type === "run") {
    try {
      const result = await run(msg.creators);
      figma.ui.postMessage({ type: "done", result: result });
    } catch (e) {
      figma.ui.postMessage({ type: "error", message: errMsg(e) });
    }
  } else if (msg.type === "cancel") {
    figma.closePlugin();
  }
};

async function run(creators) {
  const master = figma.currentPage.findOne(
    (n) => n.type === "FRAME" && n.name === MASTER_NAME
  );
  if (!master) throw new Error("'" + MASTER_NAME + "' 프레임을 찾을 수 없습니다.");

  const results = [];
  for (let i = 0; i < creators.length; i++) {
    const nickname = creators[i].nickname;
    const instagramId = creators[i].instagramId || "";
    const imageBytes = creators[i].imageBytes; // Uint8Array | null
    const r = { nickname: nickname, textReplaced: 0, handleReplaced: 0, photosApplied: 0, note: "" };

    // 1) 복제 or 기존 프레임 재사용 (재실행 안전)
    let frame = figma.currentPage.findOne(
      (n) => n.type === "FRAME" && n.name === nickname && n.id !== master.id
    );
    if (!frame) {
      frame = master.clone();
      frame.name = nickname;
      frame.x = master.x;
      frame.y = master.y + (i + 1) * (master.height + GAP);
    }

    // 2) #크리에이터 텍스트 교체
    const textNodes = frame.findAll(
      (n) => n.type === "TEXT" && n.name === VAR_NAME
    );
    for (const t of textNodes) {
      await loadNodeFonts(t);
      t.characters = nickname;
    }
    r.textReplaced = textNodes.length;

    // 2-1) #인스타아이디 텍스트 교체 (= 추천인 코드)
    const handleNodes = frame.findAll(
      (n) => n.type === "TEXT" && n.name === VAR_HANDLE
    );
    for (const t of handleNodes) {
      await loadNodeFonts(t);
      t.characters = instagramId;
    }
    r.handleReplaced = handleNodes.length;

    // 3) 프로필 사진 적용
    if (imageBytes && imageBytes.length) {
      try {
        const image = figma.createImage(imageBytes);
        const slots = frame.findAll(
          (n) => n.type === "ELLIPSE" && n.name === SLOT_NAME
        );
        for (const s of slots) {
          s.fills = [{ type: "IMAGE", imageHash: image.hash, scaleMode: "FILL" }];
        }
        r.photosApplied = slots.length;
      } catch (e) {
        r.note = "사진 처리 오류: " + errMsg(e);
      }
    } else {
      r.note = "이미지 파일 없음 (텍스트만 처리)";
    }

    results.push(r);
    figma.ui.postMessage({
      type: "progress",
      done: i + 1,
      total: creators.length,
      nickname: nickname,
    });
  }

  // 처리한 프레임 선택 + 화면 이동
  const nodes = [];
  for (const r of results) {
    const node = figma.currentPage.findOne(
      (n) => n.type === "FRAME" && n.name === r.nickname
    );
    if (node) nodes.push(node);
  }
  if (nodes.length) {
    figma.currentPage.selection = nodes;
    figma.viewport.scrollAndZoomIntoView(nodes);
  }
  return results;
}

// 텍스트 노드 하나의 폰트를 로드 (혼합 폰트도 처리)
async function loadNodeFonts(textNode) {
  if (textNode.fontName === figma.mixed) {
    const len = textNode.characters.length;
    for (let c = 0; c < len; c++) {
      await figma.loadFontAsync(textNode.getRangeFontName(c, c + 1));
    }
  } else {
    await figma.loadFontAsync(textNode.fontName);
  }
}

function errMsg(e) {
  return String((e && e.message) || e);
}
