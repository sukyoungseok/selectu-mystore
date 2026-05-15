import urllib.request
import ssl
import re
import json
import time

ssl_ctx = ssl._create_unverified_context()

urls = [
    "https://www.myrealtrip.com/experiences/3153598",
    "https://www.myrealtrip.com/experiences/3159964",
    "https://www.myrealtrip.com/experiences/3409985",
    "https://www.myrealtrip.com/experiences/3410102",
    "https://www.myrealtrip.com/experiences/3410106",
    "https://www.myrealtrip.com/experiences/3412046",
    "https://www.myrealtrip.com/experiences/3412124",
    "https://www.myrealtrip.com/experiences/3412141",
    "https://www.myrealtrip.com/experiences/3412145",
    "https://www.myrealtrip.com/experiences/3417852",
    "https://www.myrealtrip.com/experiences/3424821",
    "https://www.myrealtrip.com/experiences/3425906",
    "https://www.myrealtrip.com/experiences/3425907",
    "https://www.myrealtrip.com/experiences/3425917",
    "https://www.myrealtrip.com/experiences/3441184",
    "https://www.myrealtrip.com/experiences/3441265",
    "https://www.myrealtrip.com/experiences/3441379",
    "https://www.myrealtrip.com/experiences/3441399",
    "https://www.myrealtrip.com/experiences/3441433",
    "https://www.myrealtrip.com/experiences/3441498",
    "https://www.myrealtrip.com/experiences/3441501",
    "https://www.myrealtrip.com/experiences/3441914",
    "https://www.myrealtrip.com/experiences/3441921",
    "https://www.myrealtrip.com/experiences/3441940",
    "https://www.myrealtrip.com/experiences/3442814",
    "https://www.myrealtrip.com/experiences/3442880",
    "https://www.myrealtrip.com/experiences/3456817",
    "https://www.myrealtrip.com/experiences/3471571",
    "https://www.myrealtrip.com/experiences/3510271",
    "https://www.myrealtrip.com/experiences/3510284",
    "https://www.myrealtrip.com/experiences/3511536",
    "https://www.myrealtrip.com/experiences/3517012",
    "https://www.myrealtrip.com/experiences/3520244",
    "https://www.myrealtrip.com/experiences/3520268",
    "https://www.myrealtrip.com/experiences/3521467",
    "https://www.myrealtrip.com/experiences/3530078",
    "https://www.myrealtrip.com/experiences/3550628",
    "https://www.myrealtrip.com/experiences/3555399",
    "https://www.myrealtrip.com/experiences/3569966",
    "https://www.myrealtrip.com/experiences/3650240",
    "https://www.myrealtrip.com/experiences/3712862",
    "https://www.myrealtrip.com/experiences/3735536",
    "https://www.myrealtrip.com/experiences/3735545",
    "https://www.myrealtrip.com/experiences/3860884",
    "https://www.myrealtrip.com/experiences/3862816",
    "https://www.myrealtrip.com/experiences/3880714",
    "https://www.myrealtrip.com/experiences/3880715",
    "https://www.myrealtrip.com/experiences/3880869",
    "https://www.myrealtrip.com/experiences/3881289",
    "https://www.myrealtrip.com/experiences/3885470",
    "https://www.myrealtrip.com/experiences/3885807",
    "https://www.myrealtrip.com/experiences/3886810",
    "https://www.myrealtrip.com/experiences/3886885",
    "https://www.myrealtrip.com/experiences/3887547",
    "https://www.myrealtrip.com/experiences/3887808",
    "https://www.myrealtrip.com/experiences/3888147",
    "https://www.myrealtrip.com/experiences/3888153",
    "https://www.myrealtrip.com/experiences/3888171",
    "https://www.myrealtrip.com/experiences/4149387",
    "https://www.myrealtrip.com/experiences/4153624",
    "https://www.myrealtrip.com/experiences/4206886",
    "https://www.myrealtrip.com/experiences/4480031",
    "https://www.myrealtrip.com/experiences/4556013",
    "https://www.myrealtrip.com/experiences/4743451",
    "https://www.myrealtrip.com/experiences/4779931",
    "https://www.myrealtrip.com/experiences/4780599",
    "https://www.myrealtrip.com/experiences/4783325",
    "https://www.myrealtrip.com/experiences/4783336",
    "https://www.myrealtrip.com/experiences/4850033",
    "https://www.myrealtrip.com/experiences/4901394",
    "https://www.myrealtrip.com/experiences/4913938",
    "https://www.myrealtrip.com/experiences/4982593",
    "https://www.myrealtrip.com/experiences/5009870",
    "https://www.myrealtrip.com/experiences/5009871",
    "https://www.myrealtrip.com/experiences/5541608",
    "https://www.myrealtrip.com/experiences/5541726",
    "https://www.myrealtrip.com/experiences/5542495",
    "https://www.myrealtrip.com/experiences/5542504",
    "https://www.myrealtrip.com/experiences/5685003",
    "https://www.myrealtrip.com/experiences/5809205",
    "https://www.myrealtrip.com/experiences/5812485",
    "https://www.myrealtrip.com/experiences/5812853",
    "https://www.myrealtrip.com/experiences/5869252",
    "https://www.myrealtrip.com/experiences/5869272",
    "https://www.myrealtrip.com/experiences/5869311",
    "https://www.myrealtrip.com/experiences/5869313",
    "https://www.myrealtrip.com/experiences/5869355",
    "https://www.myrealtrip.com/experiences/5889797",
    "https://www.myrealtrip.com/offers/123042",
    "https://www.myrealtrip.com/offers/29036",
    "https://www.myrealtrip.com/offers/63983",
]

def to_fetch_url(url):
    # experiences URL → 새 도메인으로 변환
    url = url.replace("https://www.myrealtrip.com/experiences/", "https://experiences.myrealtrip.com/products/")
    return url

def fetch_og_image(url):
    fetch_url = to_fetch_url(url)
    try:
        req = urllib.request.Request(fetch_url, headers={"User-Agent": "Mozilla/5.0"})
        html = urllib.request.urlopen(req, timeout=10, context=ssl_ctx).read().decode("utf-8", errors="ignore")
        m = re.search(r'property=["\']og:image["\'][^>]+content=["\']([^"\']+)', html)
        if not m:
            m = re.search(r'content=["\']([^"\']+)["\'][^>]*property=["\']og:image', html)
        return m.group(1) if m else None
    except Exception as e:
        print(f"  ERROR: {e}")
        return None

results = {}
for i, url in enumerate(urls):
    gid = url.rstrip("/").split("/")[-1]
    print(f"[{i+1}/{len(urls)}] {gid} ...", end=" ", flush=True)
    img = fetch_og_image(url)
    results[url] = img
    print("OK" if img else "null")
    time.sleep(0.2)

with open("og_mrt_products.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

ok = sum(1 for v in results.values() if v)
print(f"\n완료: {ok}/{len(urls)} 이미지 수집")
