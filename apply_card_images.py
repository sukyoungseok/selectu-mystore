#!/usr/bin/env python3
import os, re

BASE = "/Users/sukyoung-seok/mystore-mockup"
PAGES = f"{BASE}/channel-pages-final"
IMAGES = f"{BASE}/assets/images"

# 파일명 → 이미지 prefix
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

# .tc-hero.{class}{...background:gradient...} 패턴 (전체 블록 캡처)
TC_PATTERN = re.compile(r'(\.tc-hero\.[a-zA-Z0-9_-]+)\{([^}]+)\}')

for filename, prefix in MAPPING.items():
    path = os.path.join(PAGES, filename)
    if not os.path.exists(path):
        print(f"SKIP {filename}: 파일 없음")
        continue

    card1 = os.path.join(IMAGES, f"{prefix}-card1.jpg")
    card2 = os.path.join(IMAGES, f"{prefix}-card2.jpg")
    if not os.path.exists(card1) or os.path.getsize(card1) < 10000:
        print(f"SKIP {filename}: 카드 이미지 없음")
        continue

    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 이미 이미지 적용된 경우 스킵
    if f"{prefix}-card" in html:
        print(f"SKIP {filename}: 이미 적용됨")
        continue

    card_idx = [0]  # mutable for closure

    def replace_tc(m):
        selector = m.group(1)  # e.g. .tc-hero.byulbyul-danang
        inner = m.group(2)     # e.g. background:linear-gradient(...)

        # background 속성만 교체
        if 'background:linear-gradient' not in inner and 'background:url' not in inner:
            return m.group(0)

        # 이미 이미지면 스킵
        if 'url(' in inner:
            return m.group(0)

        idx = card_idx[0]
        card_idx[0] += 1
        card_file = f"{prefix}-card{idx + 1}.jpg" if idx < 2 else f"{prefix}-card2.jpg"
        img_url = f"url('../assets/images/{card_file}') center/cover no-repeat"

        new_inner = re.sub(r'background:[^;]+', f'background:{img_url}', inner, count=1)
        return f"{selector}{{{new_inner}}}"

    new_html = TC_PATTERN.sub(replace_tc, html)

    if new_html != html and card_idx[0] > 0:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_html)
        print(f"OK   {filename}: 카드 {card_idx[0]}개 적용 ({prefix})")
    else:
        print(f"NONE {filename}: 교체 없음")
