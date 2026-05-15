#!/usr/bin/env python3
import re

PATH = "/Users/sukyoung-seok/mystore-mockup/channel-pages-final/재구언.html"

with open(PATH, "r", encoding="utf-8") as f:
    html = f.read()

# ─── 1. tab-products HTML 교체 ───
OLD_TAB = re.compile(
    r'<div id="tab-products" class="tab-panel">.*?<div class="links-section-pb"></div>\s*</div>',
    re.DOTALL
)

NEW_TAB = '''<div id="tab-products" class="tab-panel">
      <div class="products-section">
        <div class="product-search">
          <svg class="product-search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
          <input id="product-search-input" type="text" placeholder="테마파크 검색" oninput="renderProducts()"/>
        </div>
        <div class="product-grid" id="product-grid"></div>
      </div>
      <div class="links-section-pb"></div>
    </div>'''

html, n1 = OLD_TAB.subn(NEW_TAB, html, count=1)
print(f"[1] tab-products 교체: {n1}회")

# ─── 2. JS 추가: products[] + renderProducts ───
PRODUCTS_JS = """const products=[
  // 해외 테마파크
  {name:"도쿄 디즈니랜드 & 디즈니씨 이용권",price:"",tag:"🇯🇵 해외",icon:"🎢",bg:"#f0f4ff",tagColor:"#1d4ed8",tagBg:"#dbeafe",img:"https://cdn.litt.ly/images/XiH6nOd6FuUyOcKXfeV7WTuzNda5Fov9?s=300x300&m=outside&f=webp",url:"https://myrealt.rip/6CKM9e"},
  {name:"유니버설 스튜디오 재팬(USJ) 이용권",price:"",tag:"🇯🇵 해외",icon:"🎢",bg:"#f0f4ff",tagColor:"#1d4ed8",tagBg:"#dbeafe",img:"https://cdn.litt.ly/images/UmoDl8TzM1FzXBvcpbn9sCPz6bIWTwJz?s=300x300&m=outside&f=webp",url:"https://3ha.in/r/298090"},
  {name:"USJ 익스프레스 패스",price:"",tag:"🇯🇵 해외",icon:"⚡",bg:"#f0f4ff",tagColor:"#1d4ed8",tagBg:"#dbeafe",img:"https://cdn.litt.ly/images/85u6fPql4WkzCAEfQBhlBIWfPpHxv1tp?s=300x300&m=outside&f=webp",url:"https://myrealt.rip/6xX5ea"},
  {name:"LA 캘리포니아 디즈니랜드",price:"",tag:"🇺🇸 해외",icon:"🎢",bg:"#f0f4ff",tagColor:"#1d4ed8",tagBg:"#dbeafe",img:"https://cdn.litt.ly/images/B17LSUpV70zjYVtEyOWH6vwp9NaUQdtv?s=300x300&m=outside&f=webp",url:"https://myrealt.rip/78eaac"},
  {name:"유니버설 스튜디오 할리우드 1+1",price:"",tag:"🇺🇸 해외",icon:"🎬",bg:"#f0f4ff",tagColor:"#1d4ed8",tagBg:"#dbeafe",img:"https://cdn.litt.ly/images/sovMbTq0H0u3EKUxvHaIUlDeBOKQ8bf5?s=300x300&m=outside&f=webp",url:"https://myrealt.rip/7H5I25"},
  {name:"유니버설 스튜디오 싱가포르",price:"",tag:"🇸🇬 해외",icon:"🎢",bg:"#f0f4ff",tagColor:"#1d4ed8",tagBg:"#dbeafe",img:"https://cdn.litt.ly/images/BqBvEBl7xeXZXfZC0WcRlLjDO0FI8Yw6?s=300x300&m=outside&f=webp",url:"https://myrealt.rip/8NTf1e"},
  {name:"파리 디즈니랜드 이용권",price:"",tag:"🇫🇷 해외",icon:"🏰",bg:"#f0f4ff",tagColor:"#1d4ed8",tagBg:"#dbeafe",img:"https://cdn.litt.ly/images/GYg6vFsfCb5gWbVC9r86pHJDsmOWLUii?s=300x300&m=outside&f=webp",url:"https://myrealt.rip/7C8oa0"},
  {name:"홍콩 디즈니랜드 이용권",price:"",tag:"🇭🇰 해외",icon:"🏰",bg:"#f0f4ff",tagColor:"#1d4ed8",tagBg:"#dbeafe",img:"https://cdn.litt.ly/images/XAZczBYiaH9Dyp6tBJrTyundItOcL88c?s=300x300&m=outside&f=webp",url:"https://myrealt.rip/OZ5if1"},
  {name:"상하이 디즈니랜드",price:"",tag:"🇨🇳 해외",icon:"🏰",bg:"#f0f4ff",tagColor:"#1d4ed8",tagBg:"#dbeafe",img:"https://cdn.litt.ly/images/BCPPMk7HuItHlt2DwFnViSGK2WDxaQom?s=300x300&m=outside&f=webp",url:"https://affiliate.klook.com/redirect?aid=31034&aff_adid=647188&k_site=https%3A%2F%2Fwww.klook.com%2Fko%2Factivity%2F2128-disney-resort-shang-hai%2F"},
  {name:"도쿄 조이폴리스 이용권",price:"",tag:"🇯🇵 해외",icon:"🎮",bg:"#f0f4ff",tagColor:"#1d4ed8",tagBg:"#dbeafe",img:"https://cdn.litt.ly/images/TetqIqmMkvUylJqzKO8XOMdoTV87ZFLN?s=300x300&m=outside&f=webp",url:"https://api3.myrealtrip.com/partner/v1/marketing/advertising-link/7paWRu"},
  {name:"후지큐 하이랜드 이용권",price:"",tag:"🇯🇵 해외",icon:"🎢",bg:"#f0f4ff",tagColor:"#1d4ed8",tagBg:"#dbeafe",img:"https://cdn.litt.ly/images/S6V1VR6m9SAmGAsmzj4YreVvyz0GXqAF?s=300x300&m=outside&f=webp",url:"https://affiliate.klook.com/redirect?aid=31034&aff_adid=669939&k_site=https%3A%2F%2Fwww.klook.com%2Fko%2Factivity%2F51278-one-day-fuji-q-highland-pass%2F"},
  {name:"도쿄 돔 시티 어트랙션스 이용권",price:"",tag:"🇯🇵 해외",icon:"🎡",bg:"#f0f4ff",tagColor:"#1d4ed8",tagBg:"#dbeafe",img:"https://cdn.litt.ly/images/v2UHBWOSrRECjRwhM9i8vPoukcOkr5pe?s=300x300&m=outside&f=webp",url:"https://affiliate.klook.com/redirect?aid=31034&aff_adid=676799&k_site=https%3A%2F%2Fwww.klook.com%2Fko%2Factivity%2F17371-tokyo-dome-attractions-ticket-tokyo%2F"},
  {name:"도쿄 돔 시티 호텔 특가",price:"",tag:"🇯🇵 호텔",icon:"🏨",bg:"#f0f4ff",tagColor:"#7c3aed",tagBg:"#ede9fe",img:"https://cdn.litt.ly/images/lI8St1ztzpIVOELC6OU0MSAK3SBmul4n?s=300x300&m=outside&f=webp",url:"https://www.klook.com/ko/hotels/detail/275894-tokyo-dome-hotel/?aid=31034&aff_adid=681458"},
  {name:"레고랜드 재팬 이용권",price:"",tag:"🇯🇵 해외",icon:"🧱",bg:"#f0f4ff",tagColor:"#1d4ed8",tagBg:"#dbeafe",img:"https://cdn.litt.ly/images/AlwHaUtmMu5jCzByMbgN5Z52UngrI0Vx?s=300x300&m=outside&f=webp",url:"https://affiliate.klook.com/redirect?aid=31034&aff_adid=718444&k_site=https%3A%2F%2Fwww.klook.com%2Fko%2Factivity%2F44688-legoland-japan-nagoya-domestic%2F"},
  // 국내 테마파크
  {name:"서울 롯데월드 어드벤처 이용권",price:"",tag:"🇰🇷 국내",icon:"🎢",bg:"#f0fdf4",tagColor:"#16a34a",tagBg:"#dcfce7",img:"https://cdn.litt.ly/images/jJCZuP71mNxeMWQMlawNCJvFHW9PfSuF?s=300x300&m=outside&f=webp",url:"https://3ha.in/r/230453"},
  {name:"부산 롯데월드 어드벤처 이용권",price:"",tag:"🇰🇷 국내",icon:"🎢",bg:"#f0fdf4",tagColor:"#16a34a",tagBg:"#dcfce7",img:"https://cdn.litt.ly/images/4KDdbUGqBFRVsxF79JXHz4460g1lC1IP?s=300x300&m=outside&f=webp",url:"https://api3.myrealtrip.com/partner/v1/marketing/advertising-link/LgOwUM"},
  {name:"에버랜드 이용권",price:"",tag:"🇰🇷 국내",icon:"🎠",bg:"#f0fdf4",tagColor:"#16a34a",tagBg:"#dcfce7",img:"https://cdn.litt.ly/images/8h2zCLRQT3UfCDH8wvnkHjXgJiEMt2RA?s=300x300&m=outside&f=webp",url:"https://3ha.in/r/230441"},
  {name:"에버랜드 오후권(애프터2) 최저가",price:"",tag:"🔥 특가",icon:"🔥",bg:"#fff7ed",tagColor:"#c2410c",tagBg:"#ffedd5",img:"https://cdn.litt.ly/images/w0YRH1po7TN7m7muRiOw345yaxjZIGup?s=300x300&m=outside&f=webp",url:"https://myrealt.rip/6MKc1c"},
  {name:"이월드 이용권",price:"",tag:"🇰🇷 국내",icon:"🎡",bg:"#f0fdf4",tagColor:"#16a34a",tagBg:"#dcfce7",img:"https://cdn.litt.ly/images/Ctg0fBlYqAu0NzAP327YBNdCBrfr0lgu?s=300x300&m=outside&f=webp",url:"https://api3.myrealtrip.com/partner/v1/marketing/advertising-link/mooIen"},
  {name:"제주 신화월드 테마파크 이용권",price:"",tag:"🇰🇷 국내",icon:"🏝️",bg:"#f0fdf4",tagColor:"#16a34a",tagBg:"#dcfce7",url:"https://myrealt.rip/6DPP49"},
  {name:"경주월드 이용권",price:"",tag:"🇰🇷 국내",icon:"🎢",bg:"#f0fdf4",tagColor:"#16a34a",tagBg:"#dcfce7",img:"https://cdn.litt.ly/images/XYCHeRTwwkOwINwbkdSKyw8YHpIrJS3a?s=300x300&m=outside&f=webp",url:"https://affiliate.klook.com/redirect?aid=31034&aff_adid=668337&k_site=https%3A%2F%2Fwww.klook.com%2Fko%2Factivity%2F51533-gyeongju-world-gyeongju%2F"},
  {name:"춘천 레고랜드 이용권",price:"",tag:"🇰🇷 국내",icon:"🧱",bg:"#f0fdf4",tagColor:"#16a34a",tagBg:"#dcfce7",img:"https://cdn.litt.ly/images/EQf1LV8QNy7e1WHtiw39z0RsKCtWus21?s=300x300&m=outside&f=webp",url:"https://affiliate.klook.com/redirect?aid=31034&aff_adid=668334&k_site=https%3A%2F%2Fwww.klook.com%2Fko%2Factivity%2F70318-lego-land-korea-resort-pass%2F"},
  {name:"서울랜드 이용권",price:"",tag:"🇰🇷 국내",icon:"🎡",bg:"#f0fdf4",tagColor:"#16a34a",tagBg:"#dcfce7",img:"https://cdn.litt.ly/images/5bvEbPZp0FiqO2tab1fcsZ79oj56QBLy?s=300x300&m=outside&f=webp",url:"https://affiliate.klook.com/redirect?aid=31034&aff_adid=668337&k_site=https%3A%2F%2Fwww.klook.com%2Fko%2Factivity%2F48485-seoul-land-gyeonggido%2F"},
  {name:"김해 롯데워터파크",price:"",tag:"🇰🇷 국내",icon:"💦",bg:"#f0fdf4",tagColor:"#16a34a",tagBg:"#dcfce7",img:"https://cdn.litt.ly/images/XhM1G6RUw3x9BNR7c0zMA4eKkquh1Oxv?s=300x300&m=outside&f=webp",url:"https://affiliate.klook.com/redirect?aid=31034&aff_adid=723028&k_site=https%3A%2F%2Fwww.klook.com%2Fko%2Factivity%2F88947-lotte-waterpark-pass-gimhae%2F"},
];
function renderProducts(){const el=document.getElementById("product-grid");if(!el)return;const q=(document.getElementById("product-search-input")?.value||"").trim().toLowerCase();const f=q?products.filter(p=>(p.name+" "+(p.tag||"")).toLowerCase().includes(q)):products;if(!f.length){el.innerHTML=`<div style="grid-column:1/-1;padding:32px 12px;text-align:center;color:var(--light);font-size:13px;">"${q}"에 해당하는 상품이 없어요</div>`;return;}el.innerHTML=f.map(p=>`<div class="product-card-v3" onclick="window.open('${p.url}','_blank')"><div class="pc-img" style="background:${p.bg||'#f5f5f5'}">${p.img?`<img src="${p.img}" alt="${p.name}" style="width:100%;height:100%;object-fit:cover;display:block;"/>`:`<span style="font-size:32px">${p.icon}</span>`}</div><div class="pc-body"><span class="pc-tag" style="background:${p.tagBg};color:${p.tagColor}">${p.tag}</span><div class="pc-name">${p.name}</div>${p.price?`<div class="pc-price">${p.price}</div>`:""}<button class="pc-btn">예약하기</button></div></div>`).join("");}
"""

# <script> 태그 바로 다음에 삽입
html = html.replace("<script>\n", "<script>\n" + PRODUCTS_JS, 1)
print(f"[2] products[] + renderProducts 추가")

# ─── 3. DOMContentLoaded에 renderProducts() 호출 추가 ───
OLD_DCL = 'document.addEventListener("DOMContentLoaded",()=>{'
NEW_DCL = 'document.addEventListener("DOMContentLoaded",()=>{renderProducts();'
html = html.replace(OLD_DCL, NEW_DCL, 1)
print("[3] DOMContentLoaded renderProducts() 추가")

with open(PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("완료!")
