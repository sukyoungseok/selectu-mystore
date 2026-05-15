"""
export_figma_images.py

Figma REST API로 "베리에이션" 페이지의 크리에이터별 프레임을 PNG로 export한다.

사용법:
  FIGMA_TOKEN=xxx python3 scripts/export_figma_images.py

출력:
  exports/{닉네임}/MO-1.png
  exports/{닉네임}/MO-2.png
  exports/{닉네임}/MO-3.png
  exports/{닉네임}/PC-1.png
  exports/{닉네임}/PC-2.png
  exports/{닉네임}/PC-3.png
  exports/{닉네임}/OG.png

필요:
  pip install requests
"""

import os
import re
import json
import time
import requests
from pathlib import Path

# ─────────────────────────────────────────────
# 설정
# ─────────────────────────────────────────────
FIGMA_TOKEN   = os.environ.get("FIGMA_TOKEN", "")        # 환경변수 또는 직접 입력
FILE_KEY      = "HHHwWdq7CyVAiOlZ2oHEcq"                 # 마케팅파트너 마이스토어 베리에이션
PAGE_NAME     = "베리에이션"                              # figma_create_variations.js가 만드는 결과 페이지
EXPORT_DIR    = Path(__file__).parent.parent / "exports"
SCALE         = 2      # 2x 해상도
IMAGE_FORMAT  = "png"

FRAME_TYPES = ["MO-1", "MO-2", "MO-3", "PC-1", "PC-2", "PC-3", "OG"]

BASE_URL = "https://api.figma.com/v1"
HEADERS  = lambda: {"X-Figma-Token": FIGMA_TOKEN}


def get_variation_page_id() -> str:
    """파일에서 베리에이션 페이지 ID 조회"""
    r = requests.get(f"{BASE_URL}/files/{FILE_KEY}?depth=1", headers=HEADERS())
    r.raise_for_status()
    data = r.json()
    for page in data["document"]["children"]:
        if page["name"] == PAGE_NAME:
            return page["id"]
    raise ValueError(f"'{PAGE_NAME}' 페이지를 찾을 수 없음")


def get_frame_ids(page_id: str) -> dict[str, dict[str, str]]:
    """
    베리에이션 페이지에서 {닉네임}_{프레임타입} 패턴의 프레임 ID 수집
    반환: { "훵": { "MO-1": "node_id", "PC-1": "node_id", ... }, ... }
    """
    r = requests.get(
        f"{BASE_URL}/files/{FILE_KEY}/nodes?ids={page_id}&depth=2",
        headers=HEADERS()
    )
    r.raise_for_status()
    data = r.json()

    node = data["nodes"][page_id]["document"]
    creator_frames: dict[str, dict[str, str]] = {}

    pattern = re.compile(r"^(.+)_(MO-1|MO-2|MO-3|PC-1|PC-2|PC-3|OG)$")
    for child in node.get("children", []):
        m = pattern.match(child["name"])
        if m:
            nickname, frame_type = m.group(1), m.group(2)
            creator_frames.setdefault(nickname, {})[frame_type] = child["id"]

    return creator_frames


def export_nodes(node_ids: list[str]) -> dict[str, str]:
    """노드 ID 목록 → {node_id: image_url} 반환 (Figma 이미지 렌더 API)"""
    ids_param = ",".join(node_ids)
    r = requests.get(
        f"{BASE_URL}/images/{FILE_KEY}?ids={ids_param}&format={IMAGE_FORMAT}&scale={SCALE}",
        headers=HEADERS()
    )
    r.raise_for_status()
    return r.json()["images"]


def download_image(url: str, path: Path):
    r = requests.get(url)
    r.raise_for_status()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(r.content)


def run():
    if not FIGMA_TOKEN:
        print("❌ FIGMA_TOKEN 환경변수가 없어요.")
        print("   Figma → Settings → Personal access tokens 에서 발급 후:")
        print("   export FIGMA_TOKEN=your_token")
        return

    print("📄 베리에이션 페이지 ID 조회 중...")
    page_id = get_variation_page_id()
    print(f"   → {page_id}")

    print("🔍 프레임 목록 조회 중...")
    creator_frames = get_frame_ids(page_id)
    creators = sorted(creator_frames.keys())
    print(f"   → {len(creators)}명: {', '.join(creators)}")

    # 모든 노드 ID를 한번에 export 요청 (최대 30개씩 배치)
    all_node_ids = [
        nid
        for frames in creator_frames.values()
        for nid in frames.values()
    ]

    BATCH = 30
    url_map: dict[str, str] = {}
    for i in range(0, len(all_node_ids), BATCH):
        batch = all_node_ids[i:i+BATCH]
        print(f"🖼  이미지 렌더 요청 ({i+1}~{i+len(batch)}/{len(all_node_ids)})...")
        url_map.update(export_nodes(batch))
        if i + BATCH < len(all_node_ids):
            time.sleep(1)  # rate limit

    # 다운로드
    print(f"\n⬇️  PNG 저장 중 → {EXPORT_DIR}/")
    for nickname in creators:
        frames = creator_frames[nickname]
        for frame_type, node_id in frames.items():
            img_url = url_map.get(node_id)
            if not img_url:
                print(f"  ⚠️  {nickname}/{frame_type} URL 없음 (렌더 실패)")
                continue
            dest = EXPORT_DIR / nickname / f"{frame_type}.png"
            download_image(img_url, dest)
            print(f"  ✅ {nickname}/{frame_type}.png")

    print(f"\n🎉 완료! {EXPORT_DIR} 에 저장됨")

    # 크리에이터 목록 JSON 저장 (cms_upload.py에서 사용)
    manifest = {
        "creators": creators,
        "frames": {k: list(v.keys()) for k, v in creator_frames.items()},
    }
    manifest_path = EXPORT_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    print(f"📋 manifest.json 저장됨")


if __name__ == "__main__":
    run()
