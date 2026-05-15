import re

with open('channel-pages-final/혜밍웨이.html', 'r', encoding='utf-8') as f:
    content = f.read()

replacements = [
    ("비즈니스/협업", "https://cdn.litt.ly/images/ucnzAuAS6RVQjmpnJGPb8FGqohmRViEp?s=240x240&f=webp"),
    ("가염", "https://cdn.litt.ly/images/GnKogECVLHpVpVi30cKQRIPk1cehc7nl?s=240x240&f=webp"),
    ("무염", "http://thumbnail.coupangcdn.com/thumbnails/remote/492x492ex/image/vendor_inventory/b7d0/cbde59248b01a282467dcaf6d1081a1d0b891dce28eee6f93f1bb4c90afc.jpg"),
    ("키레잇코", "https://cdn.litt.ly/images/plsAAplXlirBaVyntmHrjoILmHpwSJ8x?s=240x240&f=webp"),
    ("소화제", "https://cdn.litt.ly/images/LK2xfxTZOmUrZxONPGalCi7ynHIEOCc2?s=240x240&f=webp"),
    ("구연산", "https://cdn.litt.ly/images/Q5BQEDxGToSxU5aLtxGgqk3MUF0JJlPY?s=240x240&f=webp"),
    ("위트빅스", "https://cdn.litt.ly/images/aej9UcDeptPLvYIagbyr2ZIuXHml7Mtn?s=240x240&f=webp"),
    ("위타빅스", "https://cdn.litt.ly/images/INhcFIM0zX4kJmYRoZ7BEogA0OgA0SbI?s=240x240&f=webp"),
    ("마칼디", "https://cdn.litt.ly/images/c9MBb8rFWqowGroXt7JmzkVE17kxebQu?s=240x240&f=webp"),
    ("마그네슘 추천", "https://cdn.litt.ly/images/Op7iKlOMA3DtmZLFBA6lTTvErChOuN3r?s=240x240&f=webp"),
    ("인덕션 클리너", "https://cdn.litt.ly/images/Af6pcRFmBoYSj6ZD3xjceO3CI1RNapT5?s=240x240&f=webp"),
    ("오이오차", "https://cdn.litt.ly/images/jECsi2wDBuXz3Omuh4ycEb2lT98UiSO1?s=240x240&f=webp"),
    ("퓨처셀프", "https://cdn.litt.ly/images/U3KyCpXDTIwsk5BNqkb5PELjQDwYa4xb?s=240x240&f=webp"),
    ("레버리지", "https://cdn.litt.ly/images/wTlst7uY3Iimu4pjbNj36mHIFUC85S9U?s=240x240&f=webp"),
    ("파친코", "https://cdn.litt.ly/images/d7WXmOUuyUE80HGk1cGQIatLOMo44pib?s=240x240&f=webp"),
    ("100만 번", "https://cdn.litt.ly/images/7prUNRWapoABWr9A2XzOv2Z2FOa3C38M?s=240x240&f=webp"),
]

pattern = r'(<a class="ls-og"[^>]*>)\s*(<div class="ls-og-placeholder">[^<]*</div>)(.*?ls-og-title">)(.*?)(<)'

def make_replacer(img_src):
    def replacer(m):
        if True:
            img_tag = f'<img src="{img_src}" style="width:100%;height:150px;object-fit:cover">'
            return m.group(1) + '\n          ' + img_tag + m.group(3) + m.group(4) + m.group(5)
        return m.group(0)
    return replacer

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

with open('channel-pages-final/혜밍웨이.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n총 {count}개 이미지 교체 완료")
