"""
cms_upload.py

마이리얼트립 프로모션 CMS에 쿠폰페이지 베리에이션을 자동 업로드한다.
허니블링 1건을 Playwright MCP로 수동 검증한 플로우를 그대로 스크립트화한 것.

크리에이터 1명당:
  1. 목록에서 SOURCE_CODE 검색 → 복제 → 새 프로모션 ID 확보
  2. 복제본 수정하기 진입
  3. [정보설정] 코드/제목/설명/메타Title 입력 + 메타이미지·썸네일 업로드(OG-tag)
  4. [에디터-Desktop] PC-1·2·3 교체
  5. [에디터-Mobile] MO-1·2·3 교체
  6. 저장 → 발행

v1은 순차 실행. process_creator() 가 크리에이터별로 독립적이라
나중에 편집 단계만 병렬화하기 쉬운 구조로 짜뒀다.

사용법:
  python3 scripts/cms_upload.py            # CREATORS 전체 처리
  python3 scripts/cms_upload.py 수블리       # 특정 크리에이터만

사전 준비:
  - export_coupon_pages.py 로 exports/{닉네임}/*.jpg 가 있어야 함
  - 최초 1회: 브라우저가 뜨면 직접 Google 로그인 → 콘솔에서 Enter
    (로그인 세션은 ~/.config/mrt-promotion/auth.json 에 저장되어 재사용)

필요:
  pip install playwright
  playwright install chromium
"""

import asyncio
import re
import sys
from pathlib import Path

from playwright.async_api import async_playwright, Page, BrowserContext

# ─────────────────────────────────────────────
# 설정
# ─────────────────────────────────────────────
PROMOTION_BASE = "https://promotion.myrealtrip.com"
SOURCE_CODE = "mkpt-igcoupon-myrealtrip"  # 복제 원본 프로모션 코드
EXPORT_DIR = Path(__file__).parent.parent / "쿠폰페이지 자동화" / "exports"
AUTH_STATE = Path.home() / ".config" / "mrt-promotion" / "auth.json"

# 처리할 크리에이터 (닉네임, 인스타 핸들)
CREATORS = [
    {"nickname": "허니블링", "ig": "honey_veling"},
    {"nickname": "수블리", "ig": "suvely07"},
    {"nickname": "다은", "ig": "_danie_e"},
    {"nickname": "조선여자 모나", "ig": "hanbok_travelarts"},
    {"nickname": "다챌", "ig": "dachallll"},
]

# 에디터에서 위에서부터 교체할 이미지 레이어 (Desktop / Mobile 공통: 앞 4장)
DESKTOP_FRAMES = ["PC-1", "PC-2", "PC-3", "PC-4"]
MOBILE_FRAMES = ["MO-1", "MO-2", "MO-3", "MO-4"]

HEADLESS = False  # CMS는 SSO 로그인이 필요해서 headful 권장

# 프로모션 목록 페이지의 검색창 — "완전히 로그인됨"의 확정 신호
SEARCH_BOX = 'input[placeholder*="검색할 코드"]'

# 복제 단계는 직렬화한다 — 복제 직후 '목록 맨 위 = 내 복제본' 으로 새 ID를
# 잡는데, 병렬로 동시에 복제하면 어느 게 누구 건지 섞이기 때문.
DUP_LOCK = asyncio.Lock()


# ─────────────────────────────────────────────
# 유틸
# ─────────────────────────────────────────────
def make_code(ig: str) -> str:
    """인스타 핸들 → 프로모션 코드. 영문/숫자만 남기고 특수문자 제거."""
    cleaned = re.sub(r"[^a-zA-Z0-9]", "", ig).lower()
    return f"mkpt-igcoupon-{cleaned}"


def labeled_input(page: Page, label: str):
    """라벨 텍스트와 같은 컨테이너 안의 input/textarea 를 찾는다.

    프로모션 설명처럼 <textarea> 인 필드도 있어서 둘 다 매칭한다.
    """
    return page.locator(
        f'xpath=//*[normalize-space(text())="{label}"]'
        f'/parent::*//*[self::input or self::textarea]'
    ).first


async def accept_dialogs(page: Page):
    """confirm/alert 다이얼로그를 자동 수락하도록 등록."""
    page.on("dialog", lambda d: asyncio.ensure_future(d.accept()))


async def upload_via_chooser(page: Page, choose_button, file_path: Path):
    """'파일 선택' 버튼을 눌러 file chooser 로 파일을 업로드."""
    async with page.expect_file_chooser() as fc_info:
        await choose_button.click()
    fc = await fc_info.value
    await fc.set_files(str(file_path))


# ─────────────────────────────────────────────
# 인증
# ─────────────────────────────────────────────
async def get_logged_in_context(browser) -> BrowserContext:
    """저장된 세션을 재사용하고, 없거나 만료면 수동 로그인 후 저장.

    로그인 판정은 URL 추측이 아니라 '프로모션 목록의 검색창이 실제로 뜨는지'로
    확정한다 — 2단계 인증(2FA)까지 완전히 끝나야만 검색창이 나타나기 때문.
    """
    AUTH_STATE.parent.mkdir(parents=True, exist_ok=True)

    # 1) 저장된 세션 재사용 시도
    if AUTH_STATE.exists():
        context = await browser.new_context(storage_state=str(AUTH_STATE))
        page = await context.new_page()
        await page.goto(f"{PROMOTION_BASE}/promotion")
        try:
            await page.wait_for_selector(SEARCH_BOX, timeout=15000)
            print("  ✅ 저장된 로그인 세션 재사용")
            await page.close()
            return context
        except Exception:
            print("  ⚠️  세션 만료 — 다시 로그인이 필요합니다")
            await page.close()
            await context.close()

    # 2) 수동 로그인 — 검색창이 나타날 때까지 대기 (2FA 포함, 최대 5분)
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto(f"{PROMOTION_BASE}/promotion")
    print("\n  🔐 브라우저에서 Google 로그인을 끝까지 완료해주세요 (2단계 인증 포함).")
    print("     프로모션 목록 페이지가 뜨면 자동으로 이어집니다 (최대 5분 대기)...")
    try:
        await page.wait_for_selector(SEARCH_BOX, timeout=300000)
    except Exception:
        raise RuntimeError("로그인 감지 실패 (5분 초과). 다시 실행해주세요.")

    await page.wait_for_load_state("networkidle")
    await context.storage_state(path=str(AUTH_STATE))
    print(f"  💾 로그인 세션 저장됨 → {AUTH_STATE}")
    await page.close()
    return context


# ─────────────────────────────────────────────
# 1. 복제
# ─────────────────────────────────────────────
async def duplicate_source(page: Page) -> str:
    """SOURCE_CODE 검색 → 복제 → 새 프로모션 ID 반환."""
    await page.goto(f"{PROMOTION_BASE}/promotion")
    await page.wait_for_selector(SEARCH_BOX, timeout=30000)

    search = page.locator(SEARCH_BOX)
    await search.fill(SOURCE_CODE)
    await search.press("Enter")
    await page.wait_for_timeout(1500)

    # 검색은 prefix 매칭이라 'mkpt-igcoupon-myrealtrip_타임스탬프'(복제본)도 걸린다.
    # 코드가 '정확히' SOURCE_CODE 인 행의 복제 버튼만 클릭한다.
    # (confirm/alert 는 accept_dialogs 가 처리)
    dup_btn = page.locator(
        f'xpath=//a[normalize-space(text())="{SOURCE_CODE}"]'
        f'/ancestor::*[.//button[normalize-space()="복제"]][1]'
        f'//button[normalize-space()="복제"]'
    ).first
    await dup_btn.click()
    await page.wait_for_timeout(2500)  # 복제 + alert 처리 + 목록 갱신 대기

    # 복제본은 목록 맨 위 1행. /promotion/{id} 링크에서 ID 추출
    first_link = page.locator('a[href^="/promotion/"]').first
    href = await first_link.get_attribute("href")
    new_id = href.rstrip("/").split("/")[-1]
    print(f"  📄 복제 완료 → 새 프로모션 ID: {new_id}")
    return new_id


# ─────────────────────────────────────────────
# 2~3. 정보설정 탭
# ─────────────────────────────────────────────
async def fill_info_tab(page: Page, nickname: str, code: str, og_image: Path):
    await page.get_by_text("정보 설정", exact=True).click()
    await page.wait_for_timeout(800)

    await labeled_input(page, "프로모션 코드").fill(code)
    await labeled_input(page, "프로모션 제목").fill(f"[마케팅파트너] {nickname} 전용 쿠폰팩")
    await labeled_input(page, "프로모션 설명").fill(
        f"{nickname} 전용 마이리얼트립 쿠폰팩 페이지입니다."
    )
    await labeled_input(page, "메타 Title").fill(
        f"{nickname} 전용 마이스토어에서 시크릿 혜택을 받아보세요!"
    )

    # 썸네일(0번) + 메타 이미지(1번) 둘 다 OG-tag 로 업로드
    choosers = page.get_by_role("button", name="Choose File")
    await upload_via_chooser(page, choosers.nth(0), og_image)  # 썸네일
    await page.wait_for_timeout(800)
    await upload_via_chooser(page, choosers.nth(1), og_image)  # 메타 이미지
    await page.wait_for_timeout(800)
    print(f"  ✏️  정보설정 완료 (코드: {code})")


# ─────────────────────────────────────────────
# 4~5. 에디터 탭 (Desktop / Mobile)
# ─────────────────────────────────────────────
async def replace_editor_images(page: Page, nickname: str, device: str, frames: list):
    """device='Desktop' 또는 'Mobile'. frames 순서대로 위 N개 이미지 레이어를 교체."""
    await page.get_by_text("에디터", exact=True).click()
    await page.wait_for_timeout(800)
    await page.get_by_role("button", name=device).click()
    await page.wait_for_timeout(800)

    creator_dir = EXPORT_DIR / nickname
    for idx, frame in enumerate(frames):
        img_path = creator_dir / f"{frame}.jpg"
        if not img_path.exists():
            print(f"  ⚠️  {nickname}/{frame}.jpg 없음 — skip")
            continue

        # 위에서부터 idx번째 이미지 레이어의 Setting(연필) 버튼
        await page.get_by_role("button", name="Setting").nth(idx).click()
        await page.wait_for_timeout(800)

        # 모달 안의 '파일 선택' → 업로드 → '수정'
        await upload_via_chooser(
            page, page.get_by_role("button", name="Choose File"), img_path
        )
        await page.wait_for_timeout(800)
        await page.get_by_role("button", name="수정", exact=True).click()
        await page.wait_for_timeout(1000)
        print(f"  🖼  [{device}] {frame} 교체 완료")


async def replace_form_links(page: Page, instagram_id: str, device: str):
    """현재 디바이스 탭에서 #신청폼링크 링크 컴포넌트의 4개 URL을 새 핸들로 교체.

    마스터 페이지의 #신청폼링크 4개 input(PC웹/Mobile웹/iOS앱/Android앱)에는
    'honey_veling' 이 placeholder로 들어있으므로, 단순 string replace 로 새 핸들로 바꾼다.
    """
    # #신청폼링크 텍스트 클릭 → 컴포넌트 선택
    link_label = page.locator('text=#신청폼링크').first
    await link_label.click()
    await page.wait_for_timeout(800)

    # 선택된 컴포넌트의 ✏ 버튼 클릭 — Setting 버튼 중 마지막 것이 활성화된 컴포넌트의 액션
    setting_btns = page.get_by_role("button", name="Setting")
    btn_count = await setting_btns.count()
    if btn_count == 0:
        print(f"  ⚠️  [{device}] #신청폼링크 Setting 버튼 못 찾음 — skip")
        return
    # 마지막 Setting 버튼 = 가장 최근에 활성화된(=#신청폼링크) 컴포넌트의 것
    await setting_btns.last.click()
    await page.wait_for_timeout(1000)

    # 모달 4개 input 각각 honey_veling → instagram_id 치환
    labels = ["PC웹 링크", "Mobile웹 링크", "iOS앱 링크", "Android앱 링크"]
    replaced = 0
    for label in labels:
        input_loc = labeled_input(page, label)
        try:
            current = await input_loc.input_value()
        except Exception as e:
            print(f"  ⚠️  [{device}] '{label}' input 못 찾음: {e}")
            continue
        if "honey_veling" in current:
            new_val = current.replace("honey_veling", instagram_id)
            await input_loc.fill(new_val)
            await page.wait_for_timeout(200)
            replaced += 1
        else:
            print(f"  ⚠️  [{device}] '{label}': honey_veling 패턴 없음 (값: {current[:60]}...)")

    # 수정 버튼 클릭 → 모달 닫힘
    await page.get_by_role("button", name="수정", exact=True).click()
    await page.wait_for_timeout(1200)
    print(f"  🔗 [{device}] #신청폼링크 {replaced}/4 링크 교체 완료 → {instagram_id}")


# ─────────────────────────────────────────────
# 6. 저장 + 발행
# ─────────────────────────────────────────────
PUBLISH_ENABLED_JS = """() => {
    const b = [...document.querySelectorAll('button')]
        .find(x => x.textContent.trim() === '발행');
    return b && !b.disabled;
}"""


async def save_and_publish(page: Page):
    """저장 → 발행. confirm/alert 는 accept_dialogs 가 처리.

    발행 버튼은 '한 번이라도 발행된 적 있어야' 활성화되므로,
    저장 후 버튼이 enabled 될 때까지 명시적으로 대기한다.
    """
    await page.get_by_role("button", name="저장").click()
    await page.wait_for_timeout(1500)  # confirm + alert 처리 여유
    # 발행 버튼 활성화 대기 (저장이 서버에 반영됐다는 신호)
    await page.wait_for_function(PUBLISH_ENABLED_JS, timeout=20000)
    print("  💾 저장 완료 (발행 버튼 활성화 확인)")

    # 발행: 헤더 발행 → '발행 전 확인' 모달 → 모달 발행 → confirm + alert
    await page.get_by_role("button", name="발행").first.click()
    await page.wait_for_timeout(1200)
    # 모달 안의 발행 버튼 (헤더 것 말고 마지막 것)
    await page.get_by_role("button", name="발행").last.click()
    await page.wait_for_timeout(2500)
    print("  🚀 발행 완료")


async def set_public_and_republish(page: Page):
    """1차 발행 후: 공개로 전환 → 저장 → 재발행.

    발행 버튼은 최초 1회 발행 이후에야 활성화되므로,
    공개 전환은 1차 발행을 끝낸 뒤에 한다.
    """
    await page.get_by_text("정보 설정", exact=True).click()
    await page.wait_for_timeout(800)
    await page.get_by_role("radio", name="공개 (페이지 접근 가능)").click()
    await page.wait_for_timeout(500)
    print("  🔓 공개로 전환")
    await save_and_publish(page)


# ─────────────────────────────────────────────
# 크리에이터 1명 전체 처리
# ─────────────────────────────────────────────
async def process_creator(context: BrowserContext, creator: dict):
    nickname = creator["nickname"]
    code = make_code(creator["ig"])
    og_image = EXPORT_DIR / nickname / "OG-tag.jpg"

    print(f"\n👤 [{nickname}] 처리 시작 (코드: {code})")

    if not (EXPORT_DIR / nickname).exists():
        print(f"  ❌ {EXPORT_DIR / nickname} 폴더 없음 — skip")
        return

    page = await context.new_page()
    await accept_dialogs(page)

    try:
        # 복제는 직렬화 (DUP_LOCK) — 새 ID 매칭이 섞이지 않도록
        async with DUP_LOCK:
            new_id = await duplicate_source(page)
        await page.goto(f"{PROMOTION_BASE}/promotion/{new_id}")
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(1000)

        await fill_info_tab(page, nickname, code, og_image)
        await replace_editor_images(page, nickname, "Desktop", DESKTOP_FRAMES)
        await replace_editor_images(page, nickname, "Mobile", MOBILE_FRAMES)
        await save_and_publish(page)         # 1차: 비공개 상태로 발행
        await set_public_and_republish(page)  # 2차: 공개로 전환 후 재발행

        print(f"✅ [{nickname}] 완료 — 프로모션 {new_id} (공개 발행)")
    except Exception as e:
        print(f"❌ [{nickname}] 실패: {e}")
        await page.screenshot(path=f"cms_upload_error_{nickname}.png")
        print(f"   스크린샷 저장: cms_upload_error_{nickname}.png")
    finally:
        await page.close()


# ─────────────────────────────────────────────
# 메인
# ─────────────────────────────────────────────
async def run(names: list):
    """names 가 비어있으면 CREATORS 전체, 아니면 해당 닉네임들만.

    여러 명이면 각자 자기 탭(page)에서 병렬 진행한다.
    복제 단계만 DUP_LOCK 으로 직렬화된다.
    """
    targets = CREATORS
    if names:
        targets = [c for c in CREATORS if c["nickname"] in names]
        missing = set(names) - {c["nickname"] for c in targets}
        if missing:
            print(f"⚠️  CREATORS 에 없는 닉네임 무시: {', '.join(missing)}")
        if not targets:
            print("⚠️  처리할 크리에이터가 없습니다.")
            return

    mode = "병렬" if len(targets) > 1 else "단일"
    print(f"📋 {len(targets)}명 처리 ({mode}): {', '.join(c['nickname'] for c in targets)}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=HEADLESS)
        context = await get_logged_in_context(browser)

        # 각 크리에이터를 자기 탭에서 동시 진행 (복제만 DUP_LOCK 으로 직렬화)
        await asyncio.gather(*[process_creator(context, c) for c in targets])

        await context.close()
        await browser.close()

    print("\n🎉 전체 완료!")


if __name__ == "__main__":
    asyncio.run(run(sys.argv[1:]))
