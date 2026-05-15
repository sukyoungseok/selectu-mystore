#!/usr/bin/env python3
import os, re

BASE = "/Users/sukyoung-seok/mystore-mockup"
PAGES = f"{BASE}/channel-pages-final"
IMAGES = f"{BASE}/assets/images"

# 파일명 → 이미지 prefix 매핑
MAPPING = {
    "별별리뷰.html": "byeolbyeol",
    "밍구스월드.html": "mingus",
    "민픽.html": "minpic",
    "슬숲.html": "seulsup",
    "주영이랑.html": "juyoung",
    "재구언.html": "jaegueon",
    "제이나.html": "jayna",
    "홍다닥.html": "hongdadak",
    "예슬리오.html": "yeseulio",
    "트이프.html": "teptrip",
    "훵.html": "hwung",
    "늘찬맘.html": "neulchanmam",
    "씽아.html": "singa",
    "부산맛나.html": "busanmatna",
}

results = []

for filename, prefix in MAPPING.items():
    hero_path = os.path.join(IMAGES, f"{prefix}-hero.jpg")
    if not os.path.exists(hero_path) or os.path.getsize(hero_path) < 10000:
        results.append(f"SKIP {filename}: 이미지 없음 또는 너무 작음")
        continue

    page_path = os.path.join(PAGES, filename)
    if not os.path.exists(page_path):
        results.append(f"SKIP {filename}: 페이지 없음")
        continue

    with open(page_path, "r", encoding="utf-8") as f:
        html = f.read()

    # 이미 이미지 적용된 경우 스킵
    if f"{prefix}-hero.jpg" in html:
        results.append(f"SKIP {filename}: 이미 적용됨")
        continue

    # .hero-cover{...background:linear-gradient(...)}  →  이미지로 교체
    # background 값만 교체 (position:absolute;inset:0; 유지)
    pattern = r'(\.hero-cover\{[^}]*?)background:[^;]+;'
    img_url = f"url('../assets/images/{prefix}-hero.jpg') center/cover no-repeat"
    new_html, count = re.subn(
        pattern,
        r'\1background:' + img_url + ';',
        html,
        count=1
    )

    if count == 0:
        results.append(f"FAIL {filename}: 패턴 없음")
        continue

    with open(page_path, "w", encoding="utf-8") as f:
        f.write(new_html)
    results.append(f"OK   {filename}: {prefix}-hero.jpg 적용")

for r in results:
    print(r)
