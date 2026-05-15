# 쿠폰페이지 크리에이터 자동화

마이스토어 쿠폰페이지 템플릿(`마스터세트` 프레임)을 크리에이터별로
한 번에 생성하는 Figma 플러그인.

## 워크플로우 (2단계)

| 단계 | 도구 | 하는 일 |
|------|------|---------|
| 1. 프로필 사진 수집 | Python | 인스타에서 프로필 사진 다운로드 → `assets/profiles/{닉네임}.jpg` |
| 2. Figma 생성 | 플러그인 | 마스터세트 복제 + `#크리에이터` 텍스트 교체 + 프로필 사진 적용 |

> 인스타 호출은 Python `requests`로만 안정적으로 된다. 플러그인의 브라우저
> `fetch()`는 CORS/차단에 막히므로, 네트워크 작업은 Python이 전담하고
> 플러그인은 로컬 파일만 받아 처리한다.

## 1단계 — 프로필 사진 수집 (Python)

```bash
cd ~/mystore-mockup
python3 scripts/fetch_instagram_profiles.py --file scripts/coupon_creators.txt
```

- `scripts/coupon_creators.txt` 는 한 줄에 `닉네임,인스타URL` 형식.
- 결과: `assets/profiles/{닉네임}.jpg` (320×320)
- 실패한 크리에이터는 마지막에 목록으로 표시 → 수동으로 채우면 됨.

## 2단계 — Figma 생성 (플러그인)

### 사전 준비 (Figma 파일)
- 현재 페이지에 `마스터세트` 프레임이 있어야 한다.
- `마스터세트` 안에서:
  - 닉네임이 들어갈 텍스트 레이어 이름은 `#크리에이터`
  - 프로필 사진이 들어갈 원형 노드 이름은 `profile-photo-slot`
- `마스터세트`, `템플릿 원본` 프레임은 플러그인이 건드리지 않는다.

### 설치 (최초 1회)
1. Figma Desktop 앱에서 대상 파일을 연다.
2. `Plugins → Development → Import plugin from manifest...`
3. 이 폴더의 `manifest.json` 을 선택한다.

### 실행
1. `Plugins → Development → 쿠폰페이지 크리에이터 자동화`
2. **파일 선택** — `assets/profiles/` 에서 크리에이터 이미지들을 고른다.
   파일명이 곧 닉네임 (`허니블링.jpg` → 닉네임 "허니블링").
3. `실행` 클릭 → `마스터세트` 아래에 닉네임별 세트가 생성·완성된다.

- 같은 이름의 프레임이 이미 있으면 새로 복제하지 않고 갱신한다 (재실행 안전).

## 파일 구성

| 파일 | 역할 |
|------|------|
| `manifest.json` | 플러그인 등록 정보 |
| `code.js` | 복제 + 텍스트 교체 + 프로필 사진 적용 (네트워크 없음) |
| `ui.html` | 이미지 파일 선택 UI + 진행 로그 |
