import json
import re
import os

with open("og_mrt_products.json", encoding="utf-8") as f:
    og_map = json.load(f)  # key: "https://www.myrealtrip.com/experiences/GID", value: img_url

html_dir = "channel-pages-final"
files = [f for f in os.listdir(html_dir) if f.endswith(".html")]

# renderProducts의 pc-img 부분 교체 (img 필드 반영)
OLD_RENDER = '<div class="pc-img" style="background:${p.bg}">${p.icon}</div>'
NEW_RENDER = '<div class="pc-img" style="${p.img?`background-image:url(${p.img});background-size:cover;background-position:center`:`background:${p.bg}`}">${p.img?"":p.icon}</div>'

def inject_img_field(content, og_map):
    # url:"https://www.myrealtrip.com/experiences/GID" 뒤에 ,img:"..." 추가
    def replacer(m):
        url = m.group(1)
        img = og_map.get(url)
        if img and not img.startswith("data:"):
            return f'url:"{url}",img:"{img}"'
        return m.group(0)

    content = re.sub(r'url:"(https://www\.myrealtrip\.com/(?:experiences|offers)/\d+)"', replacer, content)
    return content

updated = 0
for fname in sorted(files):
    path = os.path.join(html_dir, fname)
    with open(path, encoding="utf-8") as f:
        content = f.read()

    # img 필드 이미 있으면 skip
    if ",img:" in content:
        print(f"[SKIP] {fname} (already injected)")
        continue

    new_content = inject_img_field(content, og_map)

    # renderProducts 함수의 pc-img 렌더링 교체
    new_content = new_content.replace(OLD_RENDER, NEW_RENDER)

    if new_content != content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"[OK]   {fname}")
        updated += 1
    else:
        print(f"[NOOP] {fname}")

print(f"\n완료: {updated}/{len(files)} 파일 업데이트")
