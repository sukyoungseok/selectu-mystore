import urllib.request, ssl, re, gzip

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'ko-KR,ko;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
}

for offer_id in [170560, 161684, 179375, 122690]:
    req = urllib.request.Request(f'https://www.myrealtrip.com/offers/{offer_id}', headers=headers)
    with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
        raw = r.read()
        enc = r.headers.get('Content-Encoding', '')
    html = gzip.decompress(raw).decode('utf-8', errors='ignore') if 'gzip' in enc else raw.decode('utf-8', errors='ignore')

    imgs = re.findall(r'og:image[^>]*content="([^"]+)"', html)
    if not imgs:
        imgs = re.findall(r'"og:image","content":"([^"]+)"', html)
    if not imgs:
        imgs = re.findall(r'cloudfront\.net[^\s"<]{10,200}', html[:20000])
    if not imgs:
        imgs = re.findall(r'https://[^\s"<]*(?:\.jpg|\.jpeg|\.png|\.webp)', html[:10000])

    print(f'{offer_id}: {imgs[0][:120] if imgs else "없음 (html=" + str(len(html)) + ")"}')
