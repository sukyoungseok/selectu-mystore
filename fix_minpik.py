import urllib.request, ssl, re, json

ctx = ssl._create_unverified_context()
gids = ["3147802", "3147814", "3430514", "3431668", "5907780"]

def fetch_og(gid):
    url = f"https://experiences.myrealtrip.com/products/{gid}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        html = urllib.request.urlopen(req, timeout=10, context=ctx).read().decode("utf-8", errors="ignore")
        m = re.search(r'property=["\']og:image["\'][^>]+content=["\']([^"\']+)', html)
        if not m:
            m = re.search(r'content=["\']([^"\']+)["\'][^>]*property=["\']og:image', html)
        return m.group(1) if m else None
    except Exception as e:
        print(f"  ERROR {gid}: {e}")
        return None

og_map = {}
for gid in gids:
    img = fetch_og(gid)
    url_key = f"https://experiences.myrealtrip.com/products/{gid}"
    og_map[url_key] = img
    print(f"{gid}: {'OK' if img else 'null'}")

# 민픽.html의 url 필드 뒤에 img 필드 주입
with open("channel-pages-final/민픽.html", encoding="utf-8") as f:
    content = f.read()

def replacer(m):
    url = m.group(1)
    img = og_map.get(url)
    if img and not img.startswith("data:"):
        return f'url:"{url}",img:"{img}"'
    return m.group(0)

new_content = re.sub(r'url:"(https://experiences\.myrealtrip\.com/products/\d+)"', replacer, content)

if new_content != content:
    with open("channel-pages-final/민픽.html", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("\n민픽.html 업데이트 완료")
else:
    print("\n변경 없음")
