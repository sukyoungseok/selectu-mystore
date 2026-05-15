#!/usr/bin/env python3
import subprocess
import os

BASE = "/Users/sukyoung-seok/mystore-mockup/assets/images"

# Twitterbot UA로 OG 이미지 URL 추출
def get_og_image(reel_id):
    url = f"https://www.instagram.com/reel/{reel_id}/"
    result = subprocess.run(
        ["curl", "-s", "-L", "--max-time", "15", "-A", "Twitterbot/1.0", url],
        capture_output=True, text=True
    )
    html = result.stdout
    for line in html.split("\n"):
        if 'og:image' in line and 'content="' in line:
            start = line.find('content="') + 9
            end = line.find('"', start)
            if start > 9 and end > start:
                return line[start:end]
    # Try JSON format
    import re
    m = re.search(r'"og:image","content":"([^"]+)"', html)
    if m:
        return m.group(1).replace("\\u0026", "&")
    return None

def download(url, filename):
    path = os.path.join(BASE, filename)
    result = subprocess.run(
        ["curl", "-s", "-L", "--max-time", "20", "-A", "Mozilla/5.0", url, "-o", path],
        capture_output=True
    )
    size = os.path.getsize(path) if os.path.exists(path) else 0
    return size

# 크리에이터별 릴스 ID (링크탭 + 추가 검색)
creators = {
    "neulchanmam": {
        "reels": ["DW8-FOMD58s"],
        "targets": ["neulchanmam-hero.jpg", "neulchanmam-card1.jpg", "neulchanmam-card2.jpg"]
    },
    "singa": {
        "reels": ["DNS2SIzyQvc"],
        "targets": ["singa-hero.jpg", "singa-card1.jpg", "singa-card2.jpg"]
    },
    "hyemingway": {
        "reels": ["DXZzWMbDA7n"],
        "targets": ["hyemingway-hero.jpg", "hyemingway-card1.jpg", "hyemingway-card2.jpg"]
    },
    "busanmatna": {
        "reels": ["DSCL2k-EpkW"],
        "targets": ["busanmatna-card1.jpg", "busanmatna-card2.jpg"]
    },
    "hwung": {
        "reels": ["DTscruhAWHj"],
        "targets": ["hwung-hero.jpg"]
    },
}

# 추가 릴스 검색 (각 크리에이터 프로필에서)
extra_reels = {
    "neulchanmam": ["today.brighten"],
    "singa": ["sing.______"],
    "hyemingway": ["hyemingway0707"],
    "busanmatna": ["busan_matna_"],
}

results = {}
for creator, info in creators.items():
    results[creator] = []
    for reel_id in info["reels"]:
        print(f"[{creator}] reel {reel_id} 처리 중...")
        img_url = get_og_image(reel_id)
        if img_url:
            print(f"  URL 확보: {img_url[:80]}...")
            results[creator].append(img_url)
        else:
            print(f"  URL 없음")

# 이미지 다운로드 (hero, card1, card2 순서로 같은 이미지 복사)
for creator, info in creators.items():
    urls = results.get(creator, [])
    targets = info["targets"]
    for i, target in enumerate(targets):
        existing_path = os.path.join(BASE, target)
        if os.path.exists(existing_path) and os.path.getsize(existing_path) > 10000:
            print(f"  [SKIP] {target} 이미 존재 ({os.path.getsize(existing_path)//1024}KB)")
            continue
        url_idx = min(i, len(urls) - 1) if urls else -1
        if url_idx >= 0:
            size = download(urls[url_idx], target)
            print(f"  [{creator}] {target} → {size//1024}KB")
        else:
            print(f"  [{creator}] {target} → URL 없음, 스킵")

print("\n=== 완료 ===")
for f in sorted(os.listdir(BASE)):
    if f.endswith(".jpg"):
        size = os.path.getsize(os.path.join(BASE, f))
        if size < 10000:
            print(f"  [소형] {f}: {size}bytes")
        else:
            print(f"  [OK] {f}: {size//1024}KB")
