import re, os

# tc-hero 클래스명 → 이미지 파일 매핑
mapping = {
    "danang-4n":         "neulchanmam-card1.jpg",
    "minpic-europe":     "minpic-card1.jpg",
    "mingoose-bali":     "mingus-card1.jpg",
    "byulbyul-danang":   "byeolbyeol-card1.jpg",
    "busanmatna-sapporo":"busanmatna-card1.jpg",
    "seulsup-ubud":      "seulsup-card1.jpg",
    "singa-nhatrang":    "singa-card1.jpg",
    "yeseulio-travel":   "yeseulio-card1.jpg",
    "jae9un-themepark":  "jaegueon-card1.jpg",
    "jayna-bohol":       "jayna-card1.jpg",
    "juyoung-local":     "juyoung-card1.jpg",
    "tep-nhatrang":      "teptrip-card1.jpg",
    "henry-travel":      "henry-card1.jpg",
    "hongdadak-travel":  "hongdadak-card1.jpg",
    "nagoya-5d":         "hwung-card1.jpg",
}

html_dir = "channel-pages-final"
TC_HERO_BASE = ".tc-hero{position:relative;height:150px;background-size:cover;background-position:center}"

updated = 0
for fname in sorted(os.listdir(html_dir)):
    if not fname.endswith(".html"):
        continue
    path = os.path.join(html_dir, fname)
    with open(path, encoding="utf-8") as f:
        content = f.read()

    # tc-hero 클래스명 추출
    m = re.search(r'class="tc-hero ([^"]+)"', content)
    if not m:
        print(f"[SKIP] {fname} - tc-hero 없음")
        continue

    hero_class = m.group(1).strip()
    img_file = mapping.get(hero_class)

    if not img_file:
        print(f"[SKIP] {fname} - 매핑 없음 ({hero_class})")
        continue

    # 이미 background-image 있으면 skip
    css_selector = f".tc-hero.{hero_class}"
    if css_selector in content:
        print(f"[SKIP] {fname} - 이미 적용됨")
        continue

    # tc-hero 기본 CSS 뒤에 배경 이미지 CSS 삽입
    new_css = f"{css_selector}{{background-image:url('../assets/images/{img_file}');background-size:cover;background-position:center}}"
    new_content = content.replace(TC_HERO_BASE, TC_HERO_BASE + new_css)

    if new_content != content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"[OK]   {fname} → {img_file}")
        updated += 1
    else:
        print(f"[FAIL] {fname} - 삽입 위치를 찾지 못함")

print(f"\n완료: {updated}개 파일 업데이트")
