import urllib.request
import urllib.parse
import re
import json

urls = [
    ("만능 이심 Saily", "https://inpk.link/api/r/UuOHqH8K1pI9_wFiDtrobA18AsljbKRjSNk06-AlAYrh0K6Ujg0ExPWzio2GWAPl_fS90hGFV7SGtcSeDDLT5ZOBMGKRLmVIxS1QIl0yPPZH-M6mU7-gSkXBZBKy64E9f8Yc-z5etRLTZDs0kD2mRrc"),
    ("브랜든 세이플 플러스 도난방지 가방", "https://inpk.link/api/r/aIVmh5kmPu3vkjyzxxT3cX22thA1rKeIx4UQiFDsUYSqbxl79gfSRWERSxfy8nu6P2AdUYAik6ooSxoNDVc6Vz2QloDodRKpDBa1jcRBKyPx-BPIE6atNXZ59bfadMbr2RgxHFli989Ks5boQEzJTqbKxDx-uk2rng"),
    ("나고야 가성비 호텔", "https://inpk.link/api/r/ILtO197ACb7DvxabUzjAB4bzR6tVZeP01XbOb47OCGkVsEHFRfNJ3K1g5FDP06Rfb7CJBtQjKvgPARlvCRrCcYvIi-VwHBM2U1c1iWa2YvgJZfA9igSfr7bmdXTNv2oArs10edQr0JzQvprAs7PQ2_j4m9d8AMHyPE1tQvRajU9_6usKnOSX3hw_l39O4qNe5JBh2veQ4Pxoy9CYHFgPla2t6skmzrnDciyB"),
    ("나고야 근교 시라카와고 다카야마 버스투어", "https://inpk.link/api/r/CCtdQb6rcNxU6o38x_Esfk_AxbS8aVB1T6PGgheU2XMZOy-YG9DEqwTZty_l0uCgbKZRmZfZAYca5iQZu8x8sfcZpBypjGNyARDlZ1k-bh-YJgcMk7G-50s2e_x99g6n719ilBn9sYFBi9BOnUoMIOZG8JKI"),
    ("오사카 소테츠 그랜드 프레사", "https://inpk.link/api/r/C-5SZseP2kzTqC0-e4e4v2gyzeGr91lE16Xw1iAg9138ky6YLDmQq24GHQs3I4Rng66-ZM3KRaHFPGLiHv1Z2K2NM9Z5wiVLTdPYJcsaEqgIjXQo7eDYcv59NugyB8BeppfBZ7RM1JjcHjgw3YvG4w55jFDt2fwFbBWFqYXaRUJfUgUVjER3a5cyCx8x2bZOqYzAqfDix9DZPPqBYpeyjl_cw24ekKf5Iqh8HNOnGpe-V-4"),
    ("클룩 5% 할인코드", "https://inpk.link/api/r/V_eTD9OYMjcEqYyqA12-kDLAC662kWu4m-6FjDu3HwwjAOuJXSQEgeqXwBUJQJg6Ra_PFp5R0_c4kAgMdEz1FYph2YEL3W2raLAHNobFJzMRmYiwFIZIXkTV7dk9nlos1yog9thqNaCWnSeBD0uPxJRlHJVFvpKnxbWfGwCXvoklarY_y3wewflJmjWyDcQbrtrm4vOEAr91FVG3NQtoHOebydZ6UrppNOk9hx0juzXUV-JQb1kxI8zMF5SnNfxxlQ"),
    ("오사카 간사이 공항 픽드랍 서비스", "https://inpk.link/api/r/RlUzfodfO87lasGJA1AxWUSO22nITUrRJxG3LcSwPZff76vl8-DSREltoYIRMxpNa6ITtaHggrtvB9ixQR6ZoBIfA8rV8Ussx-2rbLZ7iRO9jdP6MqqbNO2SgnJTtMxKNsPhUQj91d0WYcNs6klmuCQcVOQ1"),
    ("오사카 가성비 럭스 호텔", "https://inpk.link/api/r/oLzOaRI7oIzBhpJwkKuPFnAfdruGPBXJEYLi_zF3J7G07yzbdOPZHkfVUXu9bSasJ51jzsNkdytBBYce6suD8mDpNfDtTmYIwBwFMTfiI3K6p15EX07Ag5B8lvnOCJP4h-jj5oFgtIbmUw-zX67xYpWSM3x5AfKI4G0xCx4oQe7JHskkNEIrorSrKzQl7TNZ65JK-P3Tl4v_xoR_CB57Nt4VQTpLuaiP_4STWEDITJ9lGnA"),
    ("BEB5 오키나와 세라가키 리조트", "https://inpk.link/api/r/NTdAQX10aL8FkQ3tezxDzaQ4hXxLwCwKpfBZKHeIY61PcyNleo44z4vQFJbWBN7Lym9lpnKKuz3p729WiriO7t2NCKg-butUKleJG4Dd-ZXNqQrdmswA8ZOZTD2WSzdkenrGs1tBUhFbLhMcfEbyAi52hesJmX1wKPgy2fiL01VaudVzP46tqVdJLX5WhabrM8MiZV5fXiI8r6eJNIBT15tNVfoIYCWBMNGI"),
    ("후쿠오카 근교 버스투어", "https://inpk.link/api/r/FGK1jcXBcuEryE6kOlrHdmgbDQPQFjSgQkzDINswqzDJZOEnhkOKdRPWD373ndCmT9H6WuKZQGR4o9oHgVstkVkIbWaBeO1EhZfVzam6ICPkzU749BM4mtiE8XKd3j2AyPAjZLWHLwy2rgs4gO-h70bNeztB"),
    ("대만 예스진지 택시 투어", "https://inpk.link/api/r/zofndUIXgiL9kl3wCL5ba2tC8-ZzEuZcE0b-hQlwlzhzj3gYyHorfijIlfVYk2lrdjxkhAQAE1fQndOFjLtkTcs_jPWJO8NsC-cklom9gkt4KO39VdwcNWsBMghj85JDFcni4q_7Rt05MuF0RS8ix4p5PeFX"),
    ("대만 예스폭지 버스투어", "https://inpk.link/api/r/ZfM8Szfp1TMkR7MxgbvfoD6Yl_Mj2sZnYE23ojvgYRAgEI235l0UxTh5Qdsyop-FsAFfR6xiNfn5ElNpYAWRDvR2GGk5K5vWyk5F3-hBOf5lntIcpje2XKjOZ6408fl0kNRQp3AcIT2ATC6cAZhY0gjFT-U5"),
    ("오사카 무제한 교통 주유패스", "https://inpk.link/api/r/iar5VXNoAaOVHke_fBIJCQ_EZlkE57dNV_zxIgRviMtuyHUE01xsbcX1dqyH3qCzbhEjOG4mEQ_dps7cOC-0aQD7-1PF6ECoGnI0Slxu7DaPDCej4hFVYvlWQvY8ovFvCyxd1Rl4xfnIoFPjNu3PhkUkM1d5tawig-_-A_14O6tFC8czjfkdWKdbFbL-FgZ9EWHCjHequjO2bN93uXta0Zxtrj0ygDr2bJQsq6jcp6b2OpOhUOYWtr5vlC9ID3YtD2RvfyamlWWWvlpUCn-rOZxIejLwP8g1S8KR8fwMVKAXvBwLfujceYBE"),
    ("교토 당일 버스투어", "https://inpk.link/api/r/A_mbS3Tm59HBzqM9F0bH5pw4UklDjzDegEJZuf1WjPInPvr81ugzK6kFualU6Hnxofjo8D2jRz03uYBhBt1rS0V8A6SxQwDnDDsxN386XXw5KRG7YktI75K-MewngWEjmlLGYYprgKoVxspzZqwFEAEUSw7NPBBlJ4vN-v7FwR12_wZNCM3dzDQVKZiTjh_n8xg32xfrJ3_q5pJuGURPjaAv36vgwOODvI1Cp_x4EHYUKtI7Ka-ed2ePxujKITUvkH76O69y-KyxROdtau8zoG2tRWYI4abz8pctrMpYOeia_mTjVbDNNM5s4ZoAgy9FjMob3HLEuGs6DCeuiOd4zgrPHutiIAkVtqs-U13lOZ_M09TAwkLdhki4Zq46Ne_0sR_LuK8Q52VeXSw"),
    ("로손 500엔 상품권", "https://inpk.link/api/r/9mtHJKqS1aceW-5TX5LFHSXytt8N87kozQmV4GqiDw0Pw5Hn7nw0T5qDLb2XUO5oPdBLSK-3LbboQjethekG0lbMhm-Cms8JOhU5LSa83Kp-zNquhXBUUqyilO29l7ydbiRCKLk6hFYMTsAeWsI0ik_Y-DYWckiIB-dS_iKaa65ppueJuTYm8Lw7R-TGU0wsZ3zlnMFGx3VZ_Ag63N_cy32Jwa0mB8HZdIvZMKPwl1QbHBoqoN-OVi34leg-cfJzwwLA8d8YUGo4n8CFA0sfX9YHjgz7eTJJhwZ7sncRF0_ldU-nRkcs1TcMaU3oZ4Wn4IeKpzT4Y690Mnc7PllpR9n4hW5Wf04KyO7BGkK8w9YCTL4VGPSjVRSMsKAUD0L_st_3RqePsoQPhyl-okxVpRE4Fk3hiVjc4NAOiEJ5WU3-t0TlDSAUESooXft1TgC_XaG8v2ecjEH2GOPMQ-Nvy0oqD3giq3sIWQ"),
    ("인천공항 승객 현황", "https://inpk.link/api/r/Y_I9wHL0nKD_uU9SbHOgaCOBXP_zG-ZGHbCMWvPGejWY0VHIg9mPulg7jvlXVGGLk05w2XH5ZbQa5Mfbf-tj6sOWLN78dDa8ZEhKlXoiKmBYZ-bVP_NApRF3-LC1pGMcW404qa4o-9KdaH8CsLYs-dwoCqTNXnd6Y-6PWWr2yA5sPvKBXXl9_LGNC09ogqVubCMly-SPDPX_9mad0kwZNShNZhPD2Z0IZSG9EwA8YEsaqENMVwnnoJg-r-tEwuWnfAhk925mJfYUhV8GZhXTHYBjOMxxHAD0uYwUa-YIq8d5Iagn9XTAVbVCNAIA7MO0Bnh0HjUKn_U"),
    ("일본 택시 꽁짜로 타기", "https://inpk.link/api/r/hmQ0NNQSLwaQlm-sstfgDzqu9V-E7nhMspr7-80qbQpCye-H-H7LCCJ6IH6tryx8lr37bqk98uroK16Kp8s9NC3OdLLdd8A3eFKdYjbibh5b6imh7kRV9HmFkDiuLYHMvuVmBAb8JkB3BNx_4rMYoqZK3k-g6DkybeEeyRu1NUWymN1vvuiCpMJqdulJAlwJrikkVCk7wS22zhZIDLo3gw"),
    ("후쿠오카 공항 ATM 정보", "https://inpk.link/api/r/1mpuNh4E5gguUxD5wMpTVaODw2jJ9AuAZfgnreZySqAoF0-gdsXUzB0deiJwWeLvLh-HEfghPrz74wqkTUYhKDz11OodC5Ebw4cIHgUAsnKebGTN78fWkg6wNBh9vGv0q6LT9Gh_QSbob1FY-3i-_Ny021oJL2hPEwsVKGYsNWXQRWiA6oRpaprnUz-MEq_XN8ciAffOhst7WPa8AoT7P1uuqgZYh7PhrvUcHn56"),
    ("돈키호테 할인쿠폰", "https://inpk.link/api/r/_hCYbD72Ayjk_7WDpoBTHle-b-rgpMGwlj9OrJYq4kc4I7uFrWT_N4Ih2hJ8dTVDfrewbzO_qMGfaRlw3nUWnEvolMK7e2DJB1oiGyMed4OlMOiVV0Xi51gKC7NqDW3_hNVwzcnOvA7JvUc-ZBGivGDpMNxbXmQfHO4HUrkLsc5rukoUdlUt6g"),
    ("대로와 나나 블로그", "https://inpk.link/api/r/9H_ZT7DXhNm-GayU9UXZSOfG8N8HeFGdtzQIhINwlNIkfxiMGPrKa-5x8v77lIBuEhGZvC5n2tVL6fM7HtiSNpySF3UDV68x5acyMRScpzjcuYyt_j2szyHy0qobEJFG0mUObnlPoyl7MmqLzmukv4Fr22ecDx8qiSV5"),
    ("대로와 나나 인스타그램", "https://inpk.link/api/r/LBJbwOjqJ3ThQNQMMk4M0AGeRETXNko-HUT4_ce_MiIaKi-8fl59uHGq5cSGzKmNB_SFs-9whTrioV-VvAmavR3FWb3LeelChphWlkkvAD3WfycMHpsxz4u6HYMd57pXGR-_TR5QWzOozEiv-fHiB5F2m_tt-mDpnjpFN4_yID6IMUWvc52JzPb0PFOo4ylxPlEvDd8O8A"),
    ("인스타360 플로우2 프로", "https://inpk.link/api/r/XLmVk8Lqnc2OKlaEgwYhPAqephrRJFEfmvisDHk6IzoEE8jKqYbLznhgyQ0Rpoijqb8Yp3frtO2UTNoppc16T9jjNuAPreRBk25_M4yKasqcEhLWLOpaUVuBlAxaLo9fwG-djlq0v8bR1mPw37kqaE3KW4eFN56mD_0lSQ"),
    ("주파집 어댑터+콘센트", "https://inpk.link/api/r/Z2H3UuodlwccaG-KnQmdrs75qVNGm0mnI9AIzPd07pZKqoEmuFF2pyXvmQLeRoqhyGpNdUBQBzcytJMDHT-prz2zpnN0nPl9GmY0Ntuii5R8VusPx-zPvj8M7NBLS-28cLAnZ73ahyeZ0sap87aD7kWhwWyMXqwEIGmzMA"),
    ("듀벨 여행용 샤워기 필터", "https://inpk.link/api/r/CVTcT1ofcOF0XKSvY0De3xSYaEP7SdiQgxMuTGh353f7e575UWyqrBnOk3cW9BYFF2z8xYLdxZXzSTBc25XNwMlkBdwNYdqIRWjhSOAP9x2d9gz0to5HvbRjSPzwfkwulT8a0BOqOU8ArCoj8F3j1N1PLlvLg_vAKbfqPQ"),
]

def get_og_data(name, url):
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            final_url = resp.url
            html = resp.read().decode('utf-8', errors='ignore')

        og_image = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\'](.*?)["\']', html)
        og_image2 = re.search(r'<meta[^>]+content=["\'](.*?)["\'][^>]+property=["\']og:image["\']', html)
        og_title = re.search(r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\'](.*?)["\']', html)
        og_title2 = re.search(r'<meta[^>]+content=["\'](.*?)["\'][^>]+property=["\']og:title["\']', html)

        image = (og_image or og_image2)
        title = (og_title or og_title2)

        return {
            "name": name,
            "inpk_url": url,
            "final_url": final_url,
            "og_image": image.group(1) if image else None,
            "og_title": title.group(1) if title else None,
        }
    except Exception as e:
        return {"name": name, "inpk_url": url, "final_url": None, "og_image": None, "og_title": None, "error": str(e)}

results = []
for name, url in urls:
    print(f"처리 중: {name}")
    r = get_og_data(name, url)
    results.append(r)
    print(f"  → {r.get('final_url', 'N/A')}")
    print(f"  → og:image: {r.get('og_image', 'NONE')}")

with open("og_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\n완료! og_results.json 저장됨")
