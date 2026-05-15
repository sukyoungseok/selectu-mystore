#!/usr/bin/env python3
import os, re

PAGES = "/Users/sukyoung-seok/mystore-mockup/channel-pages-final"

# 잘못된 패턴:
# .hero-cover{...background:url(...) center/cover no-repeat;position:absolute;inset:0;background:gradient}
# 올바른 패턴:
# .hero-cover{...background:url(...) center/cover no-repeat}.hero-cover::after{content:"";position:absolute;inset:0;background:gradient}

BROKEN_PATTERN = re.compile(
    r'(\.hero-cover\{[^}]*?background:url\([^)]+\) center/cover no-repeat)'
    r';(position:absolute;inset:0;background:[^}]+)'
    r'\}'
)

for filename in os.listdir(PAGES):
    if not filename.endswith('.html'):
        continue
    path = os.path.join(PAGES, filename)
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    def fix_match(m):
        hero_part = m.group(1)   # .hero-cover{...background:url(...)
        after_inner = m.group(2)  # position:absolute;inset:0;background:gradient
        return (
            hero_part + '}'
            + f'.hero-cover::after{{content:"";{after_inner}}}'
        )

    new_html, count = BROKEN_PATTERN.subn(fix_match, html)
    if count > 0:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_html)
        print(f"FIXED ({count}) {filename}")
    else:
        print(f"skip  {filename}")
