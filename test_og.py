import urllib.request, ssl, re

ctx = ssl._create_unverified_context()
url = "https://experiences.myrealtrip.com/products/4783325"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req, timeout=10, context=ctx).read().decode("utf-8", errors="ignore")
print("HTML len:", len(html))

# og:image
m = re.search(r'property=["\']og:image["\'][^>]+content=["\']([^"\']+)', html)
if not m:
    m = re.search(r'content=["\']([^"\']+)["\'][^>]*property=["\']og:image', html)
print("OG image:", m.group(1)[:120] if m else "NOT FOUND")

# 이미지 URL 패턴
imgs = re.findall(r'https://[^\s"\'<>]+(?:jpg|jpeg|png|webp)', html)
print("Sample image URLs:", imgs[:3])
