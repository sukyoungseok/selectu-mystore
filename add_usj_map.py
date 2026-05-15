#!/usr/bin/env python3
PATH = "/Users/sukyoung-seok/mystore-mockup/channel-pages-final/재구언.html"

with open(PATH, "r", encoding="utf-8") as f:
    html = f.read()

# ─── 1. CSS 추가 ───
CSS = (
    "#tip-map{height:190px;flex-shrink:0;border-bottom:1px solid var(--border);display:none}"
    ".leaflet-container{font-family:'Noto Sans KR',sans-serif}"
    ".leaflet-popup-content-wrapper{border-radius:10px;box-shadow:0 4px 12px rgba(0,0,0,.12);padding:0;border:none}"
    ".leaflet-popup-content{margin:8px 12px;font-size:12px;font-weight:700;color:#1a1714}"
    ".leaflet-popup-tip-container{display:none}"
)
html = html.replace("</style>", CSS + "\n</style>", 1)
print("[1] CSS 추가")

# ─── 2. Leaflet 스크립트 추가 ───
LEAFLET = (
    '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>\n'
    '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>\n'
)
html = html.replace("</head>", LEAFLET + "</head>", 1)
print("[2] Leaflet 추가")

# ─── 3. tip-sheet에 지도 div 삽입 ───
html = html.replace(
    '<div class="tip-list" id="tip-list"></div>',
    '<div id="tip-map"></div>\n      <div class="tip-list" id="tip-list"></div>',
    1
)
print("[3] 지도 div 삽입")

# ─── 4. nintendo5th에 stops 추가 ───
OLD_N = '    tours:[\n      {name:"슈퍼 닌텐도 월드 확약권 + 1일 입장권 + 간사이 조이패스"'
NEW_N = (
    '    stops:[\n'
    '      {lat:34.6665,lng:135.4331,label:"①",place:"USJ 메인 게이트",color:"#6B3AB8"},\n'
    '      {lat:34.6670,lng:135.4315,label:"②",place:"슈퍼 닌텐도 월드 입구",color:"#6B3AB8"},\n'
    '      {lat:34.6672,lng:135.4308,label:"③",place:"동키콩 컨트리",color:"#6B3AB8"},\n'
    '      {lat:34.6668,lng:135.4313,label:"④",place:"마리오 카트: 쿠파의 도전장",color:"#6B3AB8"},\n'
    '      {lat:34.6669,lng:135.4320,label:"⑤",place:"5주년 한정 굿즈 샵",color:"#6B3AB8"},\n'
    '      {lat:34.6666,lng:135.4316,label:"⑥",place:"5주년 기념 음식 (푸드코트)",color:"#6B3AB8"}\n'
    '    ],\n'
    '    tours:[\n'
    '      {name:"슈퍼 닌텐도 월드 확약권 + 1일 입장권 + 간사이 조이패스"'
)
html = html.replace(OLD_N, NEW_N, 1)
print("[4] nintendo5th stops 추가")

# ─── 5. usj25th에 stops 추가 ───
OLD_U = '    tours:[\n      {name:"프리미엄 간사이 조이패스 일주일권"'
NEW_U = (
    '    stops:[\n'
    '      {lat:34.6665,lng:135.4331,label:"①",place:"USJ 게이트 · 25주년 포토스팟",color:"#E07A38"},\n'
    '      {lat:34.6648,lng:135.4312,label:"②",place:"할리우드 에리어 · 가로등 배너",color:"#E07A38"},\n'
    '      {lat:34.6643,lng:135.4323,label:"③",place:"그래머시 파크 · NO LIMIT 퍼레이드",color:"#E07A38"},\n'
    '      {lat:34.6662,lng:135.4347,label:"④",place:"스페이스 판타지 스테이션 · 깃발 구매",color:"#E07A38"},\n'
    '      {lat:34.6643,lng:135.4342,label:"⑤",place:"워터월드 · Discover U!!! 버전",color:"#E07A38"},\n'
    '      {lat:34.6648,lng:135.4307,label:"⑥",place:"할리우드 드림 더 라이드",color:"#E07A38"}\n'
    '    ],\n'
    '    tours:[\n'
    '      {name:"프리미엄 간사이 조이패스 일주일권"'
)
html = html.replace(OLD_U, NEW_U, 1)
print("[5] usj25th stops 추가")

# ─── 6. openTipPanel 함수에 지도 초기화 로직 추가 ───
OLD_FN = 'function openTipPanel(key){const d=USJ_TIPS[key];if(!d)return;document.getElementById("tip-sheet-title").textContent=d.title;document.getElementById("tip-sheet-period").textContent=d.period;document.getElementById("tip-sheet-sub").textContent=d.sub;'
NEW_FN = (
    'let _tipMap=null;'
    'function initTipMap(stops,color){'
      'const el=document.getElementById("tip-map");'
      'if(!stops||!stops.length){el.style.display="none";return;}'
      'el.style.display="block";'
      'if(_tipMap){_tipMap.remove();_tipMap=null;}'
      '_tipMap=L.map(el,{zoomControl:false,attributionControl:false});'
      'L.tileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",{maxZoom:19}).addTo(_tipMap);'
      'const coords=stops.map(s=>[s.lat,s.lng]);'
      'if(coords.length>1)L.polyline(coords,{color:color||"#6B3AB8",weight:3,opacity:0.7,dashArray:"6,9"}).addTo(_tipMap);'
      'stops.forEach((s,i)=>{'
        'const icon=L.divIcon({className:"",html:`<div style="width:26px;height:26px;border-radius:50%;background:${s.color||color||"#6B3AB8"};color:#fff;font-size:11px;font-weight:900;display:flex;align-items:center;justify-content:center;border:2px solid #fff;box-shadow:0 2px 8px rgba(0,0,0,.25)">${s.label}</div>`,iconSize:[26,26],iconAnchor:[13,13]});'
        'L.marker([s.lat,s.lng],{icon}).addTo(_tipMap).bindPopup(`<div>${s.place}</div>`,{closeButton:false});'
      '});'
      '_tipMap.fitBounds(coords,{padding:[24,24]});'
    '}'
    'function openTipPanel(key){const d=USJ_TIPS[key];if(!d)return;document.getElementById("tip-sheet-title").textContent=d.title;document.getElementById("tip-sheet-period").textContent=d.period;document.getElementById("tip-sheet-sub").textContent=d.sub;'
)
html = html.replace(OLD_FN, NEW_FN, 1)
print("[6] openTipPanel 함수 교체 (initTipMap 추가)")

# ─── 7. openTipPanel 함수 내부에 지도 호출 삽입 ───
# document.getElementById("tip-panel").classList.add("open"); 직전에 지도 초기화 호출 삽입
OLD_OPEN = 'document.getElementById("tip-panel").classList.add("open");}'
NEW_OPEN = 'setTimeout(()=>{initTipMap(d.stops,d.stops?.[0]?.color);if(_tipMap)_tipMap.invalidateSize();},350);document.getElementById("tip-panel").classList.add("open");}'
html = html.replace(OLD_OPEN, NEW_OPEN, 1)
print("[7] openTipPanel 내 지도 호출 삽입")

# ─── 8. closeTipPanel에 지도 정리 추가 ───
OLD_CLOSE = 'function closeTipPanel(){document.getElementById("tip-panel").classList.remove("open");}'
NEW_CLOSE = 'function closeTipPanel(){document.getElementById("tip-panel").classList.remove("open");}'
# (지도는 다음 열 때 새로 그리므로 별도 정리 불필요)

with open(PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("\n완료!")
