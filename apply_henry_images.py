import re

with open('channel-pages-final/헨리.html', 'r', encoding='utf-8') as f:
    content = f.read()

replacements = [
    ("오늘도 헨리플랜", "https://ugc.production.linktr.ee/3e51cefa-98fb-464d-a15b-21b78376e641_C2176D74-FD41-4895-A404-466635B2DDB7-1-105-c.jpeg?io=true&size=thumbnail-stack_v1_0"),
    ("대마도 배편", "https://ugc.production.linktr.ee/2ad02f58-9f2c-4ede-a921-5177656f9cec_IMG-4722.jpeg?io=true&size=thumbnail-stack_v1_0"),
    ("판랑사막투어", "https://ugc.production.linktr.ee/06cb1270-cb11-4e36-beb7-2603543235af_2026-02-16-5.44.49.png?io=true&size=thumbnail-stack_v1_0"),
    ("유심사 이심", "https://ugc.production.linktr.ee/bcb4770d-3f4a-46d5-b7b5-8aec0aef7ff1_2026-01-25-6.06.38.png?io=true&size=thumbnail-stack_v1_0"),
    ("클룩(Klook)", "https://ugc.production.linktr.ee/fddbfd63-4b94-4d22-9d6e-b93091e2a415_.png?io=true&size=thumbnail-stack_v1_0"),
]

pattern = r'(<a class="ls-og"[^>]*>)\s*(<div class="ls-og-placeholder">[^<]*</div>)(.*?ls-og-title">)(.*?)(<)'

count = 0
for keyword, img_src in replacements:
    def replacer(m, kw=keyword, src=img_src):
        if kw in m.group(4):
            img_tag = f'<img src="{src}" style="width:100%;height:150px;object-fit:cover">'
            return m.group(1) + '\n          ' + img_tag + m.group(3) + m.group(4) + m.group(5)
        return m.group(0)

    new_content = re.sub(pattern, replacer, content, flags=re.DOTALL)
    if new_content != content:
        print(f"✅ 교체됨: {keyword}")
        count += 1
        content = new_content
    else:
        print(f"⚠️  못찾음: {keyword}")

with open('channel-pages-final/헨리.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n총 {count}개 이미지 교체 완료")
