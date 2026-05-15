"""
신규 인플루언서 바이오링크 수집기
결과: bio_links_new.csv 저장
"""

import csv
import os
import time
from playwright.sync_api import sync_playwright

SESSION_DIR = os.path.expanduser("~/.instagram-playwright-session")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "bio_links_new.csv")

INSTAGRAM_IDS = [
    "holiday__zip",
    "freehan_is",
    "soodori_travel",
    "jinnie_j__",
    "sing.______",
    "jh__appy_",
    "life.traveler.jayna",
    "itsotravel",
    "busan_matna_",
    "ggami_travel",
    "hyemingway0707",
    "tk__natasha",
    "tulney_",
    "dorossi_life",
    "urang.trip",
    "choojangtrip",
    "seoli_o3o",
    "uely_",
    "undefined_uhfc",
]


def extract_bio_link(page):
    try:
        link_el = page.query_selector('a[href*="l.instagram.com"]')
        if link_el:
            href = link_el.get_attribute("href")
            if "u=" in href:
                import urllib.parse
                parsed = urllib.parse.urlparse(href)
                params = urllib.parse.parse_qs(parsed.query)
                return urllib.parse.unquote(params.get("u", [""])[0])
            return href

        header = page.query_selector("header")
        if header:
            links = header.query_selector_all("a[href]")
            for link in links:
                href = link.get_attribute("href") or ""
                text = link.inner_text().strip()
                if href.startswith("http") and "instagram.com" not in href:
                    return href
                if text and ("." in text) and not text.startswith("@") and len(text) < 60:
                    return text
    except Exception as e:
        print(f"  ⚠️ 링크 추출 오류: {e}")
    return ""


def scrape_profile(page, username):
    url = f"https://www.instagram.com/{username}/"
    print(f"\n🔍 [{username}] 수집 중...")
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=15000)
        time.sleep(2)

        try:
            close_btn = page.query_selector('svg[aria-label="닫기"]') or page.query_selector('svg[aria-label="Close"]')
            if close_btn:
                close_btn.click()
                time.sleep(0.5)
        except:
            pass

        bio_link = extract_bio_link(page)
        print(f"  바이오링크: {bio_link or '없음'}")
        return {"id": username, "instagram": f"https://www.instagram.com/{username}/", "bio_link": bio_link}

    except Exception as e:
        print(f"  ❌ 오류: {e}")
        return {"id": username, "instagram": f"https://www.instagram.com/{username}/", "bio_link": ""}


def main():
    session_exists = os.path.exists(SESSION_DIR)

    with sync_playwright() as p:
        print("🚀 브라우저 실행 중...")
        context = p.chromium.launch_persistent_context(
            SESSION_DIR,
            headless=False,
            viewport={"width": 1280, "height": 900},
            locale="ko-KR",
        )
        page = context.new_page()
        page.goto("https://www.instagram.com/", timeout=15000)
        time.sleep(2)

        if not session_exists:
            print("\n👉 브라우저에서 인스타그램에 로그인해주세요.")
            input("✅ 로그인 완료 후 Enter 눌러주세요...")
        else:
            print("✅ 기존 세션 재사용 — 바로 수집 시작!")

        results = []
        for username in INSTAGRAM_IDS:
            result = scrape_profile(page, username)
            results.append(result)
            time.sleep(1.5)

        context.close()

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "instagram", "bio_link"])
        writer.writeheader()
        writer.writerows(results)

    print(f"\n🎉 완료! bio_links_new.csv 저장됨 ({len(results)}개)")
    for r in results:
        print(f"  {r['id']}: {r['bio_link'] or '없음'}")


if __name__ == "__main__":
    main()
