"""
Instagram 바이오링크 수집기
- 첫 실행 시: 브라우저 열리면 직접 인스타 로그인
- 이후 실행: 세션 재사용 (로그인 불필요)
- 결과: bio_links_result.csv 저장
"""

import csv
import os
import time
from playwright.sync_api import sync_playwright

SESSION_DIR = os.path.expanduser("~/.instagram-playwright-session")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "bio_links_result.csv")

INSTAGRAM_IDS = [
    "ttoodiii",
    "mozzi_orzl_",
    "hwung_travel",
    "iamsleyle",
    "azzapi_",
    "trip_db_",
    "mingoose_world",
    "balbal_trip",
    "ssalb_travel",
    "bbaekkom_okasan",
    "today.brighten",
    "heying.pu",
    "everymoment_writer",
    "seulsup_",
    "dadahe_b",
    "arang.travel",
    "puwoo_travel",
    "travel_baek",
    "trip_heesutory",
    "mangottaeng0",
    "zoey._.vely",
    "ryong_trip",
    "aeriiiiiunni",
    "mingreen_travel",
    "daero._.nana",
    "sihanmom_trip",
]


def extract_bio_link(page):
    """프로필 페이지에서 바이오링크 추출"""
    try:
        # 인스타그램 프로필의 외부 링크는 header 영역 <a> 태그에 위치
        link_el = page.query_selector('a[href*="l.instagram.com"]')
        if link_el:
            href = link_el.get_attribute("href")
            # l.instagram.com 트래킹 링크에서 실제 URL 추출
            if "u=" in href:
                import urllib.parse
                parsed = urllib.parse.urlparse(href)
                params = urllib.parse.parse_qs(parsed.query)
                return urllib.parse.unquote(params.get("u", [""])[0])
            return href

        # 직접 외부 링크인 경우
        header = page.query_selector("header")
        if header:
            links = header.query_selector_all("a[href]")
            for link in links:
                href = link.get_attribute("href") or ""
                text = link.inner_text().strip()
                # 외부 도메인 링크 (인스타 내부 링크 제외)
                if href.startswith("http") and "instagram.com" not in href:
                    return href
                # 링크 텍스트가 URL처럼 생긴 경우
                if text and ("." in text) and not text.startswith("@") and len(text) < 60:
                    return text
    except Exception as e:
        print(f"  ⚠️ 링크 추출 오류: {e}")
    return ""


def extract_follower_count(page):
    """팔로워 수 추출"""
    try:
        for span in page.query_selector_all("span"):
            text = span.inner_text()
            if "팔로워" in text or "followers" in text.lower():
                parent = span.query_selector("xpath=..")
                if parent:
                    count_span = parent.query_selector("span")
                    if count_span:
                        return count_span.inner_text().strip()
    except:
        pass
    return ""


def scrape_profile(page, username):
    url = f"https://www.instagram.com/{username}/"
    print(f"\n🔍 [{username}] 수집 중...")
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=15000)
        time.sleep(2)

        # 로그인 요구 팝업 닫기
        try:
            close_btn = page.query_selector('svg[aria-label="닫기"]') or page.query_selector('svg[aria-label="Close"]')
            if close_btn:
                close_btn.click()
                time.sleep(0.5)
        except:
            pass

        bio_link = extract_bio_link(page)
        follower = extract_follower_count(page)

        print(f"  바이오링크: {bio_link or '없음'}")
        print(f"  팔로워: {follower or '파싱 실패'}")
        return {"id": username, "bio_link": bio_link, "follower": follower}

    except Exception as e:
        print(f"  ❌ 오류: {e}")
        return {"id": username, "bio_link": "", "follower": ""}


def main():
    with sync_playwright() as p:
        print("🚀 브라우저 실행 중...")
        context = p.chromium.launch_persistent_context(
            SESSION_DIR,
            headless=False,
            viewport={"width": 1280, "height": 900},
            locale="ko-KR",
        )
        page = context.new_page()

        # 로그인
        page.goto("https://www.instagram.com/", timeout=15000)
        print("\n👉 브라우저에서 인스타그램에 로그인해주세요.")
        print("   (이미 로그인돼 있으면 그냥 Enter)")
        input("✅ 로그인 완료 후 Enter 눌러주세요...")

        print("\n✅ 수집 시작!")
        results = []

        for username in INSTAGRAM_IDS:
            result = scrape_profile(page, username)
            results.append(result)
            time.sleep(1.5)  # 요청 간격

        context.close()

    # CSV 저장
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "bio_link", "follower"])
        writer.writeheader()
        writer.writerows(results)

    print(f"\n🎉 완료! {OUTPUT_FILE} 저장됨 ({len(results)}개)")


if __name__ == "__main__":
    main()
