import re

def make_bubble_css(bg, border, shadow_rgb):
    return (
        f'.ls-tb-bubble{{flex:1;position:relative;background:{bg};border:1.5px solid {border};'
        f'border-radius:18px;padding:14px 16px;box-shadow:0 4px 14px rgba({shadow_rgb},.08);'
        f'font-size:13px;line-height:1.7;color:var(--text)}}'
        f'.ls-tb-bubble::before{{content:"";position:absolute;left:-10px;top:14px;width:0;height:0;'
        f'border:8px solid transparent;border-right-color:{border};border-left:0}}'
        f'.ls-tb-bubble::after{{content:"";position:absolute;left:-7px;top:15px;width:0;height:0;'
        f'border:7px solid transparent;border-right-color:{bg};border-left:0}}'
    )

# 파일명: (배경색, 테두리색, shadow-rgb)
# 주황 계열은 현재 색 유지, 나머지는 --amber 테마에 맞게 조정
bubble_map = {
    '훵.html':       ('#fff5e8', '#ffd9ae', '224,122,56'),   # 주황 유지
    '트이프.html':   ('#fff5e8', '#ffd9ae', '224,122,56'),   # 주황 유지
    '늘찬맘.html':   ('#fff5e8', '#ffd9ae', '224,122,56'),   # 주황 유지
    '별별리뷰.html': ('#fff3ec', '#f0b890', '216,112,64'),   # 오렌지 조정
    '제이나.html':   ('#fff3eb', '#f0b488', '212,112,56'),   # 오렌지 조정
    '씽아.html':     ('#edf7f4', '#a4d0c8', '12,122,107'),   # 틸 그린
    '밍구스월드.html':('#eef7f5', '#a8d4ce', '26,138,122'),  # 틸 그린
    '헨리.html':     ('#eef5f7', '#a8ccd4', '42,122,138'),   # 틸 블루
    '혜밍웨이.html': ('#eef2fb', '#b0c4ec', '46,90,200'),    # 블루
    '슬숲.html':     ('#eef8ef', '#b0d8b4', '58,138,64'),    # 그린
    '홍다닥.html':   ('#eef8f2', '#b0d8bc', '58,138,80'),    # 그린
    '재구언.html':   ('#f2eef9', '#c4ace8', '107,58,184'),   # 퍼플
    '예슬리오.html': ('#f3eef8', '#c8b0e0', '122,74,154'),   # 퍼플
    '부산맛나.html': ('#fdf0ee', '#eca8a0', '200,48,32'),    # 레드
    '민픽.html':     ('#f7f2ea', '#d0b888', '139,112,72'),   # 브라운
    # 주영이랑은 이미 노란색으로 처리되어 있으므로 유지
}

pattern = re.compile(r'\.ls-tb-bubble\{.*?\.ls-tb-bubble::after\{.*?border-left:0\}', re.DOTALL)

count = 0
for filename, (bg, border, shadow) in bubble_map.items():
    path = f'channel-pages-final/{filename}'
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        new_css = make_bubble_css(bg, border, shadow)
        new_content = pattern.sub(new_css, content)

        if new_content != content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'✅ {filename}')
            count += 1
        else:
            print(f'⚠️  패턴 미매칭: {filename}')
    except FileNotFoundError:
        print(f'⏭️  파일없음: {filename}')
    except Exception as e:
        print(f'❌ {filename}: {e}')

print(f'\n총 {count}개 파일 말풍선 색상 수정 완료')
