#!/usr/bin/env python3
"""Phase 1: Add course/expense panel structure to 11 skeleton creator pages."""
import os, re

BASE = '/Users/sukyoung-seok/mystore-mockup/channel-pages-final'

CREATORS = {
    '별별리뷰.html':  {'city':'danang',  'name':'별별리뷰',  'total':'70만~',  'badge':'🔥 인기', 'sub':'항공·숙박·투어 포함'},
    '밍구스월드.html': {'city':'bali',    'name':'밍구스월드', 'total':'100만~', 'badge':'🌴 인기', 'sub':'항공·숙박 포함'},
    '슬숲.html':      {'city':'bali',    'name':'슬숲',      'total':'100만~', 'badge':'🌴 추천', 'sub':'항공·숙박·투어 포함'},
    '부산맛나.html':  {'city':'sapporo', 'name':'부산맛나',  'total':'85만~',  'badge':'⛄ 인기', 'sub':'항공·숙박 포함'},
    '민픽.html':      {'city':'rome',    'name':'민픽',      'total':'180만~', 'badge':'🏛️ 인기', 'sub':'항공·숙박·투어 포함'},
    '예슬리오.html':  {'city':'tokyo',   'name':'예슬리오',  'total':'65만~',  'badge':'🍜 인기', 'sub':'항공·숙박 포함'},
    '유블리.html':    {'city':'jeju',    'name':'유블리',    'total':'25만~',  'badge':'🍊 추천', 'sub':'숙박·렌트카 포함'},
    '주영이랑.html':  {'city':'busan',   'name':'주영이랑',  'total':'15만~',  'badge':'🌊 인기', 'sub':'숙박·식비 포함'},
    '헨리.html':      {'city':'hawaii',  'name':'헨리',      'total':'200만~', 'badge':'🌺 인기', 'sub':'항공·숙박·투어 포함'},
    '혜밍웨이.html':  {'city':'europe',  'name':'혜밍웨이',  'total':'200만~', 'badge':'🏰 인기', 'sub':'항공·숙박·투어 포함'},
    '홍다닥.html':    {'city':'vietnam', 'name':'홍다닥',    'total':'65만~',  'badge':'🍜 인기', 'sub':'항공·숙박 포함'},
}

EXTRA_CSS = """\
.share-btn{display:inline-flex;align-items:center;gap:5px;background:rgba(224,122,56,.1);color:var(--amber);border:1px solid rgba(224,122,56,.3);font-size:11px;font-weight:700;padding:5px 11px;border-radius:99px;cursor:pointer;font-family:inherit;white-space:nowrap;flex-shrink:0}
.share-btn svg{width:12px;height:12px}
.exp-title-row{display:flex;align-items:flex-start;justify-content:space-between;gap:10px;margin-bottom:3px}
#course-panel{position:absolute;top:0;left:0;right:0;bottom:0;background:var(--cream);transform:translateY(100%);transition:transform .42s cubic-bezier(.32,.72,0,1);z-index:100;display:flex;flex-direction:column;overflow:hidden}
#course-panel.open{transform:translateY(0)}
.panel-topbar{display:flex;align-items:center;gap:12px;padding:16px 20px 14px;background:var(--cream);border-bottom:1px solid var(--border);flex-shrink:0}
.panel-back{width:36px;height:36px;background:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:16px;cursor:pointer;border:1px solid var(--border);flex-shrink:0}
.panel-title{font-size:16px;font-weight:800;color:var(--text)}
.day-tabs{display:flex;padding:0 20px;border-bottom:1px solid var(--border);flex-shrink:0;background:var(--cream);overflow-x:auto;scrollbar-width:none}
.day-tabs::-webkit-scrollbar{display:none}
.day-tab{padding:12px 18px;font-size:13px;font-weight:600;color:var(--light);cursor:pointer;border-bottom:2px solid transparent;transition:all .2s;white-space:nowrap}
.day-tab.active{color:var(--text);border-bottom-color:var(--amber)}
.day-content{flex:1;overflow-y:auto;-webkit-overflow-scrolling:touch;padding:20px 20px 40px}
.stop-item{display:flex;gap:14px;margin-bottom:28px}
.stop-timeline{display:flex;flex-direction:column;align-items:center;flex-shrink:0}
.stop-dot{width:12px;height:12px;border-radius:50%;background:var(--amber);border:2px solid #fff;box-shadow:0 0 0 2px var(--amber);flex-shrink:0}
.stop-line{width:2px;flex:1;background:rgba(224,122,56,.25);margin:4px 0;min-height:20px}
.stop-body{flex:1}
.stop-time{font-size:11px;font-weight:600;color:var(--mid);margin-bottom:3px}
.stop-place{font-size:15px;font-weight:700;color:var(--text);margin-bottom:4px}
.stop-desc{font-size:12px;color:var(--mid);line-height:1.5;margin-bottom:4px}
.inline-product{background:#fffaf5;border-radius:14px;padding:14px;display:flex;align-items:center;gap:12px;border:1px solid rgba(224,122,56,.2);margin-top:8px}
.inline-product-icon{width:48px;height:48px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:24px;flex-shrink:0}
.inline-product-info{flex:1}
.inline-product-tag{font-size:11px;font-weight:700;padding:2px 7px;border-radius:5px;display:inline-block;margin-bottom:4px}
.inline-product-name{font-size:13px;font-weight:600;color:var(--text);margin-bottom:2px;line-height:1.3}
.inline-product-price{font-size:14px;font-weight:800;color:var(--amber)}
.inline-product-btn{background:var(--amber);color:#fff;font-size:11px;font-weight:700;padding:9px 13px;border-radius:10px;border:none;cursor:pointer;font-family:inherit;flex-shrink:0;line-height:1.3;text-align:center}
#expense-panel{position:absolute;top:0;left:0;right:0;bottom:0;z-index:200;display:flex;flex-direction:column;justify-content:flex-end;pointer-events:none;opacity:0;transition:opacity .3s}
#expense-panel.open{pointer-events:all;opacity:1}
.exp-overlay{position:absolute;inset:0;background:rgba(0,0,0,.45);cursor:pointer}
.exp-sheet{position:relative;z-index:1;background:var(--cream);border-radius:24px 24px 0 0;padding:8px 20px 44px;transform:translateY(100%);transition:transform .38s cubic-bezier(.32,.72,0,1);max-height:88vh;overflow-y:auto}
#expense-panel.open .exp-sheet{transform:translateY(0)}
.exp-title{font-size:18px;font-weight:900;color:var(--text);margin-bottom:3px}
.exp-subtitle{font-size:12px;color:var(--mid);margin-bottom:18px}
.exp-item{display:flex;align-items:center;gap:12px;background:#fff;border-radius:14px;padding:14px;margin-bottom:8px;border:1px solid var(--border)}
.exp-group-header{display:flex;align-items:baseline;justify-content:space-between;margin:18px 2px 8px;font-size:13px;font-weight:800;color:var(--text)}
.exp-emoji{font-size:22px;flex-shrink:0}
.exp-info{flex:1;min-width:0}
.exp-name{font-size:14px;font-weight:700;color:var(--text);margin-bottom:2px}
.exp-live-tag{display:inline-block;margin-left:6px;font-size:9px;font-weight:700;color:var(--amber);background:rgba(224,122,56,.12);border-radius:4px;padding:2px 5px;vertical-align:middle}
.exp-note{font-size:11px;color:var(--mid)}
.exp-right{display:flex;flex-direction:column;align-items:flex-end;gap:5px;flex-shrink:0}
.exp-price-val{font-size:15px;font-weight:900;color:var(--text)}
.exp-book-btn{background:var(--amber);color:#fff;font-size:10px;font-weight:700;padding:6px 10px;border-radius:8px;border:none;cursor:pointer;font-family:inherit}
.exp-total-row{display:flex;justify-content:space-between;align-items:center;padding:14px 4px 4px;border-top:1.5px solid var(--text);margin-top:4px}
.exp-total-label{font-size:13px;font-weight:700;color:var(--text)}
.exp-total-val{font-size:20px;font-weight:900;color:var(--amber)}
.exp-fine-print{font-size:10px;color:var(--light);margin:8px 0 16px}
#map-full{height:220px;flex-shrink:0}
.leaflet-container{font-family:"Noto Sans KR",sans-serif}
.leaflet-popup-content-wrapper{border-radius:12px;box-shadow:0 4px 16px rgba(0,0,0,.12);border:none;padding:0}
.leaflet-popup-content{margin:10px 14px;font-size:12px;font-weight:700;color:#1a1714}
.leaflet-popup-tip-container{display:none}"""

LEAFLET = '''\
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>'''

PANELS_HTML = '''\
  <div id="course-panel">
    <div class="panel-topbar">
      <div class="panel-back" onclick="closeCourse()">←</div>
      <div><div class="panel-title" id="course-panel-title">추천 코스</div></div>
      <button class="share-btn" onclick="copyShareLink(\'course\')"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.6" y1="13.5" x2="15.4" y2="17.5"/><line x1="15.4" y1="6.5" x2="8.6" y2="10.5"/></svg>링크 복사</button>
    </div>
    <div id="map-full"></div>
    <div class="day-tabs" id="day-tabs"></div>
    <div class="day-content" id="day-content"></div>
  </div>
  <div id="expense-panel">
    <div class="exp-overlay" onclick="closeExpensePanel()"></div>
    <div class="exp-sheet">
      <div style="width:36px;height:4px;background:var(--border);border-radius:2px;margin:6px auto 16px"></div>
      <div class="exp-title-row">
        <div class="exp-title" id="exp-title-text">총경비</div>
        <button class="share-btn" onclick="copyShareLink(\'expense\')"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.6" y1="13.5" x2="15.4" y2="17.5"/><line x1="15.4" y1="6.5" x2="8.6" y2="10.5"/></svg>링크 복사</button>
      </div>
      <div class="exp-subtitle" id="exp-subtitle-text">추천 코스 · 1인 기준</div>
      <div class="exp-item"><div class="exp-emoji">✈️</div><div class="exp-info"><div class="exp-name" id="exp-flight-name">항공권 <span class="exp-live-tag">직항</span></div><div class="exp-note" id="exp-flight-note">항공권 기준</div></div><div class="exp-right"><div class="exp-price-val" id="exp-flight">₩-</div><button class="exp-book-btn" id="exp-flight-btn">예약 바로가기</button></div></div>
      <div id="exp-hotel-section"><div class="exp-item"><div class="exp-emoji">🏨</div><div class="exp-info"><div class="exp-name" id="exp-hotel-name">호텔 <span class="exp-live-tag">추천</span></div><div class="exp-note" id="exp-hotel-note">3박 2인 1실 1인 기준</div></div><div class="exp-right"><div class="exp-price-val" id="exp-hotel">₩-</div><button class="exp-book-btn" id="exp-hotel-btn">예약 바로가기</button></div></div></div>
      <div class="exp-item"><div class="exp-emoji">🍜</div><div class="exp-info"><div class="exp-name">식비 · 현지 경비</div><div class="exp-note" id="exp-food-note">현지 식당 포함</div></div><div class="exp-right"><div class="exp-price-val" id="exp-food-price">₩-</div></div></div>
      <div id="exp-tours-list"></div>
      <div class="exp-total-row"><div class="exp-total-label">총 경비</div><div class="exp-total-val" id="exp-total">₩-</div></div>
      <div class="exp-fine-print" id="exp-fine-print">· 1인 기준 평균값</div>
    </div>
  </div>'''

# JS template — uses {CITY} {NAME} placeholders substituted per file
JS_TEMPLATE = r"""
const CREATOR={name:"{NAME}",email:"sukyoung.seok@myrealtrip.com"};
const CITY_DAYS={"{CITY}":[
  {day:1,date:"D1 · 출발 → 도착",dayCost:"",stops:[
    {time:"오전",place:"공항 출발",lat:0,lng:0,pinColor:"amber",pinLabel:"D1",desc:"출발!",cost:"항공 별도",product:null},
  ]},
]};
const CITY_EXPENSE={"{CITY}":{
  title:"총경비",
  food:100000,foodNote:"현지 식비 포함",
  defaultFlight:0,defaultHotel:300000,defaultTotal:400000,
  flightNote:"",flightUrl:"",
  hotelName:"추천 숙소",hotelNote:"3박 2인 1실 1인 기준",hotelUrl:"",
  tours:[],toursLabel:"🎫 추천 상품",finePrint:"· 1인 기준 평균값"
}};
let currentExpenseCity="{CITY}";let currentDay=1;let currentCourseCity="{CITY}";let mapFull;
function openCourse(city){city=city||"{CITY}";currentCourseCity=city;currentDay=1;document.getElementById("course-panel").classList.add("open");const t=CITY_EXPENSE[city];document.getElementById("course-panel-title").textContent=(t&&t.title)||"추천 코스";renderDayTabs();renderDayContent(1);setTimeout(()=>{initMapFull(city);if(mapFull)mapFull.invalidateSize();},450);}
function closeCourse(){document.getElementById("course-panel").classList.remove("open");}
function renderDayTabs(){document.getElementById("day-tabs").innerHTML=CITY_DAYS[currentCourseCity].map(d=>`<div class="day-tab ${d.day===currentDay?"active":""}" onclick="selectDay(${d.day})">DAY ${d.day}</div>`).join("");}
function renderDayContent(n){const imgMap=Object.fromEntries(products.filter(p=>p.img).map(p=>[p.url,p.img]));const day=CITY_DAYS[currentCourseCity].find(d=>d.day===n);if(!day)return;document.getElementById("day-content").innerHTML=`<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:18px;"><div style="font-size:14px;font-weight:700;color:var(--sage)">${day.date}</div>${day.dayCost?`<div style="font-size:12px;font-weight:700;color:var(--amber);background:#FFF3E8;padding:5px 10px;border-radius:8px;">💰 ${day.dayCost}</div>`:""}</div>${day.stops.map((s,i)=>`<div class="stop-item"><div class="stop-timeline"><div class="stop-dot"></div>${i<day.stops.length-1?'<div class="stop-line"></div>':""}</div><div class="stop-body"><div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:2px;"><div class="stop-time">${s.time}</div>${s.cost?`<div style="font-size:11px;color:var(--mid);font-weight:600;">${s.cost}</div>`:""}</div><div class="stop-place">${s.place}</div><div class="stop-desc">${s.desc}</div>${(s.products||(s.product?[s.product]:[])).map(p=>`<div class="inline-product"><div class="inline-product-icon" style="background:${p.bg};${imgMap[p.url]?'padding:0;overflow:hidden;':''}">${imgMap[p.url]?'<img src="'+imgMap[p.url]+'" style="width:100%;height:100%;object-fit:cover;border-radius:12px;" alt=""/>':p.icon}</div><div class="inline-product-info"><span class="inline-product-tag" style="background:${p.tagBg};color:${p.tagColor}">${p.tag}</span><div class="inline-product-name">${p.name}</div><div class="inline-product-price">${p.price}</div></div><button class="inline-product-btn" onclick="window.open('${p.url}','_blank')">예약하기</button></div>`).join("")}</div></div>`).join("")}`;document.getElementById("day-content").scrollTop=0;}
function selectDay(n){currentDay=n;renderDayTabs();renderDayContent(n);if(mapFull){const d=CITY_DAYS[currentCourseCity].find(x=>x.day===n);if(d){const coords=d.stops.filter(s=>s.lat).map(s=>[s.lat,s.lng]);if(coords.length)mapFull.fitBounds(coords,{padding:[30,30],maxZoom:13});}}}
function openExpensePanel(city){city=city||"{CITY}";currentExpenseCity=city;const d=CITY_EXPENSE[city];if(!d)return;document.getElementById("exp-title-text").textContent=d.title;document.getElementById("exp-subtitle-text").textContent=`${CREATOR.name} 추천 코스 · 1인 기준`;document.getElementById("exp-food-price").textContent="₩"+d.food.toLocaleString();document.getElementById("exp-food-note").textContent=d.foodNote;document.getElementById("exp-flight").textContent=d.defaultFlight?("₩"+d.defaultFlight.toLocaleString()):"유류비 별도";document.getElementById("exp-total").textContent="₩"+d.defaultTotal.toLocaleString();document.getElementById("exp-fine-print").textContent=d.finePrint;if(d.flightNote)document.getElementById("exp-flight-note").textContent=d.flightNote;const flightBtn=document.getElementById("exp-flight-btn");if(flightBtn){flightBtn.style.display=d.flightUrl?"":"none";if(d.flightUrl)flightBtn.onclick=()=>window.open(d.flightUrl,"_blank");}const hotelSection=document.getElementById("exp-hotel-section");if(d.hotels){hotelSection.innerHTML=d.hotels.map(h=>`<div class="exp-item"><div class="exp-emoji">🏨</div><div class="exp-info"><div class="exp-name">${h.name} <span class="exp-live-tag">${CREATOR.name} 추천</span></div><div class="exp-note">${h.note}</div></div><div class="exp-right"><div class="exp-price-val">₩${h.price.toLocaleString()}</div><button class="exp-book-btn" onclick="window.open('${h.url}','_blank')">예약 바로가기</button></div></div>`).join("");}else{hotelSection.innerHTML=`<div class="exp-item"><div class="exp-emoji">🏨</div><div class="exp-info"><div class="exp-name">${d.hotelName||"호텔"} <span class="exp-live-tag">${CREATOR.name} 추천</span></div><div class="exp-note">${d.hotelNote||""}</div></div><div class="exp-right"><div class="exp-price-val">₩${d.defaultHotel.toLocaleString()}</div>${d.hotelUrl?`<button class="exp-book-btn" onclick="window.open('${d.hotelUrl}','_blank')">예약 바로가기</button>`:""}</div></div>`;}document.getElementById("exp-tours-list").innerHTML=d.tours.length?`<div class="exp-group-header"><span>${d.toursLabel||"🎫 추천 상품"}</span></div>${d.tours.map(t=>`<div class="exp-item"><div class="exp-emoji">${t.emoji}</div><div class="exp-info"><div class="exp-name">${t.name}</div><div class="exp-note">${t.note}</div></div><div class="exp-right"><div class="exp-price-val">₩${t.price.toLocaleString()}</div>${t.url?`<button class="exp-book-btn" onclick="window.open('${t.url}','_blank')">예약 바로가기</button>`:""}</div></div>`).join("")}`:"";document.getElementById("expense-panel").classList.add("open");}
function closeExpensePanel(){document.getElementById("expense-panel").classList.remove("open");}
function copyShareLink(v){let url=location.origin+location.pathname+"?view="+v;if(v==="expense")url+="&city="+currentExpenseCity;navigator.clipboard?.writeText(url).then(()=>showToast("링크가 복사되었어요 🔗"));}
function showToast(msg){let t=document.getElementById("share-toast");if(!t){t=document.createElement("div");t.id="share-toast";t.className="toast";document.body.appendChild(t)}t.textContent=msg;t.classList.add("show");clearTimeout(t._timer);t._timer=setTimeout(()=>t.classList.remove("show"),2200);}
const pinColors={amber:"#E07A38",sage:"#6B9080",blush:"#C97D6E"};
function createPinIcon(color,label){return L.divIcon({html:`<div style="width:30px;height:30px;border-radius:50%;background:${pinColors[color]||"#E07A38"};border:2.5px solid #fff;box-shadow:0 2px 8px rgba(0,0,0,0.28);display:flex;align-items:center;justify-content:center;"><span style="color:#fff;font-size:9px;font-weight:800">${label}</span></div>`,className:"",iconSize:[30,30],iconAnchor:[15,15],popupAnchor:[0,-18]});}
function drawRoutes(map,city){CITY_DAYS[city].forEach(day=>{const coords=day.stops.filter(s=>s.lat).map(s=>[s.lat,s.lng]);if(coords.length>1)L.polyline(coords,{color:pinColors[day.stops[0].pinColor]||"#E07A38",weight:3,opacity:0.65,dashArray:"6,9"}).addTo(map);});}
function initMapFull(city){city=city||currentCourseCity;if(mapFull){mapFull.remove();mapFull=null;}mapFull=L.map("map-full",{zoomControl:false,attributionControl:false});L.tileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",{maxZoom:19}).addTo(mapFull);const allCoords=CITY_DAYS[city].flatMap(d=>d.stops.filter(s=>s.lat).map(s=>[s.lat,s.lng]));if(allCoords.length)mapFull.fitBounds(allCoords,{padding:[20,20]});drawRoutes(mapFull,city);CITY_DAYS[city].forEach(day=>day.stops.filter(s=>s.lat).forEach(s=>{const m=L.marker([s.lat,s.lng],{icon:createPinIcon(s.pinColor,s.pinLabel)}).addTo(mapFull);m.bindPopup(`<div>${s.place}</div>`,{closeButton:false});m.on("click",()=>selectDay(day.day));}));}
document.addEventListener("DOMContentLoaded",()=>{renderProducts();const p=new URLSearchParams(location.search),v=p.get("view"),c=p.get("city")||"{CITY}";if(v==="expense")setTimeout(()=>openExpensePanel(c),400);if(v==="course")setTimeout(()=>openCourse(c),400);});"""

# Updated renderProducts (adds img support, removes sold badge)
NEW_RENDER_PRODUCTS = (
    'function renderProducts(){const el=document.getElementById("product-grid");'
    'const q=(document.getElementById("product-search-input")?.value||"").trim().toLowerCase();'
    'const f=q?products.filter(p=>(p.name+" "+(p.tag||"")).toLowerCase().includes(q)):products;'
    'if(!f.length){el.innerHTML=`<div style="grid-column:1/-1;padding:32px 12px;text-align:center;color:var(--light);font-size:13px;">"${q}"에 해당하는 상품이 없어요</div>`;return}'
    'el.innerHTML=f.map(p=>`<div class="product-card-v3" onclick="window.open(\'${p.url}\',\'_blank\')">'
    '<div class="pc-img" style="background:${p.bg}">${p.img?`<img src="${p.img}" alt="${p.name}"/>`:`${p.icon}`}</div>'
    '<div class="pc-body"><span class="pc-tag" style="background:${p.tagBg};color:${p.tagColor}">${p.tag}</span>'
    '<div class="pc-name">${p.name}</div><div class="pc-price">${p.price}</div>'
    '<button class="pc-btn">예약하기</button></div></div>`).join("");}'
)

# pc-img CSS update (adds height + overflow + img child)
OLD_PC_IMG_CSS = '.pc-img{width:100%;aspect-ratio:1;display:flex;align-items:center;justify-content:center;font-size:44px}'
NEW_PC_IMG_CSS = '.pc-img{width:100%;height:130px;display:flex;align-items:center;justify-content:center;font-size:44px;overflow:hidden}.pc-img img{width:100%;height:100%;object-fit:cover;display:block}'


def process_file(filename, cfg):
    path = os.path.join(BASE, filename)
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    city = cfg['city']
    name = cfg['name']
    total = cfg['total']
    badge = cfg['badge']
    sub = cfg['sub']

    # 1. Add extra CSS before </style>
    html = html.replace('</style>', EXTRA_CSS + '\n</style>', 1)

    # 2. Fix pc-img CSS
    html = html.replace(OLD_PC_IMG_CSS, NEW_PC_IMG_CSS, 1)

    # 3. Add Leaflet after </style> (before </head>)
    html = html.replace('</style>\n</head>', f'</style>\n{LEAFLET}\n</head>', 1)

    # 4. Add "코스" tab to page-tabs
    old_tabs = '<div class="page-tab on" data-tab="posts" onclick="switchTab(\'posts\')">링크</div>\n      <div class="page-tab" data-tab="products" onclick="switchTab(\'products\')">필수템</div>'
    new_tabs = f'<div class="page-tab on" data-tab="posts" onclick="switchTab(\'posts\')">링크</div>\n      <div class="page-tab" data-tab="products" onclick="switchTab(\'products\')">필수템</div>'
    # (tabs stay the same — course is accessed via trip card, not a separate tab)

    # 5. Insert course + expense panels before coupon-panel
    html = html.replace(
        '  <div id="coupon-panel">',
        PANELS_HTML + '\n  <div id="coupon-panel">',
        1
    )

    # 6. Update trip card plan button: window.open → openCourse
    html = re.sub(
        r'<button class="plan" onclick="window\.open\(\'[^\']+\',\'_blank\'\)">(\s*)<div><strong>[^<]+</strong><span>[^<]+</span></div>',
        f'<button class="plan" onclick="openCourse(\'{city}\')">\\1<div><strong>일정표 보기</strong><span>동선 먼저</span></div>',
        html
    )

    # 7. Update trip card cost button: window.open → openExpensePanel + update content
    html = re.sub(
        r'<button class="cost" onclick="window\.open\(\'[^\']+\',\'_blank\'\)">(\s*)'
        r'<div class="tc-c-row1"><strong>지금 예약하기</strong>'
        r'<div class="tc-c-price"><span class="tc-c-num">[^<]+</span>'
        r'<span class="tc-arr" style="margin-left:4px">›</span></div></div>(\s*)'
        r'<div class="tc-c-row2"><span class="tc-c-badge">[^<]+</span>'
        r'<span class="tc-c-sub">[^<]+</span></div>',
        f'<button class="cost" onclick="openExpensePanel(\'{city}\')">\\1'
        f'<div class="tc-c-row1"><strong>총 경비 보기</strong>'
        f'<div class="tc-c-price"><span class="tc-c-num">{total}</span>'
        f'<span class="tc-arr" style="margin-left:0">›</span></div></div>\\2'
        f'<div class="tc-c-row2"><span class="tc-c-badge">{badge}</span>'
        f'<span class="tc-c-sub">{sub}</span></div>',
        html
    )

    # 8. Update renderProducts (add img support, remove sold)
    old_render = re.search(r'function renderProducts\(\)\{.*?\}', html)
    if old_render:
        html = html[:old_render.start()] + NEW_RENDER_PRODUCTS + html[old_render.end():]

    # 9. Replace old DOMContentLoaded + add all JS (after existing functions)
    js_block = JS_TEMPLATE.replace('{CITY}', city).replace('{NAME}', name)
    # Remove old DOMContentLoaded
    html = re.sub(
        r"document\.addEventListener\(\"DOMContentLoaded\",\(\)=>\{renderProducts\(\);\}\);",
        '',
        html
    )
    # Insert new JS before </script>
    html = html.replace('</script>\n</body>', js_block + '\n</script>\n</body>', 1)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    return True


updated = 0
errors = []
for fname, cfg in CREATORS.items():
    try:
        process_file(fname, cfg)
        updated += 1
        print(f"✅ {fname}")
    except Exception as e:
        errors.append(f"{fname}: {e}")
        print(f"❌ {fname}: {e}")

print(f"\n완료: {updated}/{len(CREATORS)}개 파일 업데이트")
if errors:
    print("오류:", errors)
