import os
import threading
from flask import Flask
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot actif !"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_flask, daemon=True).start()

# CONFIGURATION
TELEGRAM_TOKEN = "8922246133:AAElSpQlhrjtmxfNgubIdKWngAIIp823CkQ"
# Colle TOUT le texte copié depuis "Cookie: " entre les guillemets ci-dessous
FULL_COOKIE = """cto_bundle=2wAXAl9Jc3lHRnEyWTI1WlRLNWFlZSUyRm9USSUyRnNYZGFuN082RCUyRjRKRm43JTJCQlV2N1d3JTJCYjFGSzBINWs4YVVyYW9IVXVJNUVlcGRnd2xlQklWRiUyQm9rTlpVdlYxZW9UMUpzSHJZJTJCQ1dJb010bGxUZWJEVk5NSlloclpnaWFLc2Y3a1JsRDZV; _ga=GA1.1.1760373190.1793005915; _ga_8H12QY46R8=GS2.1.s1793013048$o2$g1$t1793014207$j60$l0$h0; _gcl_au=1.1.566683761.1793005915.-.-.1793005915.629654399.1793005915.1793014207; datadome=t8Xt8fcfhiZ1LQ_EKwm6PN2O9e8xF4A0yu7uq~6ot3Ico2_ZFyX~24jZxZHeyrvLmDS_kvCu7umFc~pzLg72t4dXiCrqdczU427qWflp9Ze8jccvEun93dmYEeC3d__2; __ps_slu=https://www.vinted.fr/session-refresh?ref_url=%2Fmember%2F3204508259; __ps_sr=_; _fbp=fb.1.1793005915154.913468535641546714; _ga_ZJHK1N3D75=GS2.1.s1793013048$o2$g1$t1793014206$j58$l0$h0; _lm_id=9U0RNM8YD86Z02GI; banners_ui_state=SUCCESS; braze_external_id=3204508259%3A160a5887f44bddff62adb319a457654fb3447893b36d8205f74b0d722723c25e; cto_bundle=2dls9F9Jc3lHRnEyWTI1WlRLNWFlZSUyRm9USXlLMzJ6aUg0JTJCSXY1V1N6YkZoVSUyQlBVRjN1ekRvVGJEQ3pwbTNCeFlRMkZqJTJGZW1qYzZaU0NWanNDUExURFQlMkYzYiUyQkJDJTJCRE5mMFVhTEpKbzJVWFRSbnlqMzZCWks3TGFRS01iWEFIcjZpVFVG; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Oct+26+2026+12%3A30%3A05+GMT%2B0100+(heure+normale+d%E2%80%99Europe+centrale)&version=202602.1.0&browserGpcFlag=0&isIABGlobal=false&consentId=3204508259&isAnonUser=1&hosts=&interactionCount=1&prevHadToken=0&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1%2CC0005%3A1%2CV2STACK42%3A1%2CC0035%3A1%2CC0038%3A1&genVendors=V5%3A1%2CV10%3A1%2CV2%3A1%2CV1%3A1%2C&intType=1&crTime=1793005914822&geolocation=FR%3BIDF&AwaitingReconsent=false; _vinted_fr_session=RGpLa3ZRVmNra2Y1MDJpaU1wQmQ0U3phejg4a2ZVZmk4UmtaUC9hWERUd2tqdDFYWVFBOUh2NmZsNHpKRzhUc0d6N3gybGJLN3c3Vy96WnBUY21FZGZmbGJ5MzRMMFU3Qmh5NThUTXhkRHU2ck1wNCtvb2E1aXVGYnRMYlhBZzYxcThmWG9VMUp2d1FLWUFUckFDT0F5Q3BMOGhkR0Z6TzNEYVJ6ZFdncjZWc0ZTNzNSQ2ZwZ0lSM3A5NjBjSEdMSGV6UnRrRUQ1anpVdzQ2eDlLY1QyOTJ6MlhqUHNDYTltSDNpSk5reUxJbmZrRzNjQmIwQzJlMjVhUGkxdFhUdG1jS1A5WHh6blNJVlNjZVp0YWM2NHkyaVYxc3VVNkVQTk1YTUEySWdvekdqT21MRVk5SzJjS0VpRUlYcyt0c1ctLVZ3b1d2UXlXdy9oS1hiSHF2SEdQS2c9PQ%3D%3D--8f6adc6aecb37624e4af90dc49a0cbf03eecddd7; anon_id=9e3e9ec7-8c7e-40c7-b42c-21051cf25b91; viewport_size=1710; cf_clearance=cyO19nQXuYamNYxEoW2ViJZpsve6N1pAzDMxLbnJ.5I-1793014204-1.2.1.1-VArMgaAdWxYvJ69BreuwT6VcAuUkHOyDNyqDsYs6Q60lb_y8naOoSQGewQwIZdp_9BQT3yrfp_zmTnhWD_r.lLeyLOOuOU94C6sdhamewgOjynlLvuEHyp1E1fTKDizybKv1K6nS.Ilhs8H8Eq_t9aWYyKsyX74gLDNgHKnE9zgdSCbXTK4IaiPnnyb.R8xVqFAWPeeepSsT.Tq5ggl8AGdXVgtCSYLaDn5DSMKzvrV8tdSW7mzi42vFh.0rkyC.RRku7CUgarR1akpzFBJ.3orBJ_VtuCrQKf.k_newCDVYN5KEpTw2LuZdluAK7TSUiKOae2XYlvoY.onrQQTJJBLrcA37xpAj26_i10QTvfw; __cf_bm=Kevm91ycG_kcomoiJw3nzSDssTONQaB0qNAJwebut1U-1793014204.7829592-1.0.1.1-mk91_41lCranFATprhgwQheISs5nMvOLhU2Owp9T4FxIKZFkLnvTvCys0O1ygfOaQXrY202aDeriKkgTq25_MvYOihlTsfuIydKY5JBD_9O4ApRmPDX7Uc7cfN_LoMedqNi5uQH1xvEXgvGie4wWoQ; v_udt=OThnTG9qTU5nODhmdFZiYlhuU3A5bzRQL3FiQi0tS2hWZGh3WWZYTldXeHBVaC0tUmQyL0Nhajh0YVJzL2VIaHNSU3cxdz09; user-iso-locale=fr-FR; access_token_web=eyJhbGciOiJQUzI1NiIsImtpZCI6IkU1N1lkcnVIcGxBanUyY05vMURvckgzajI3QnU1LXNfT1A1UHdQaWhuNU0ifQ.eyJhY2NvdW50X2lkIjozMjA4OTUxNjIzLCJhY3QiOnsic3ViIjoiMzIwNDUwODI1OSJ9LCJhbmlkIjoiOWUzZTllYzctOGM3ZS00MGM3LWI0MmMtMjEwNTFjZjI1YjkxIiwiYXBwX2lkIjo0LCJhdWQiOiJmci5jb3JlLmFwaS52aW50ZWQuY29tIiwiY2MiOiJGUiIsImNsaWVudF9pZCI6IndlYiIsImV4cCI6MTc5MzAxNjY0OSwiaWF0IjoxNzkzMDEzMDQ5LCJpc3MiOiJ2aW50ZWQtaWFtLW9hdXRoIiwibG9naW5fdHlwZSI6MywicHVycG9zZSI6ImFjY2VzcyIsInNjb3BlIjoicHVibGljIHVzZXIiLCJzaWQiOiJlMTY3OTNkMy0xNzkzMDA1OTUyIiwic3ViIjoiMzIwNDUwODI1OSJ9.zMJA4y0ryyJHVmsI-i4uqtdPAQQbEMdMJYyt-DctzbUqkEjVZFeybtpNY6MQCgW_RaHBCk8v3wVRjEsU7O9qDNq-Cc03KcQ5ZAVmBykXm4LXUYYGLq7c9VfoSUvwGtWXRV5I9hYbxBjDVWWg9Y1kyDVQ8jLgFtbc8Wpyjp26O4_M9sczkRuxa19Nbqpdg9yNaImJXc0HGf6KHsKFkqxuYtNdbA1C1Uo5M7YIXhHutIONfIzHuubgwgF-WJi_M_P_ccgYoKY4vTBpc8XBBIu_YfpKHsyT5rwVBYtT76DjUhnXQAWvaxcy_TVaK2Sc97iu_jNC9BDCIFXc7Y-CDfai9A; refresh_token_web=eyJhbGciOiJQUzI1NiIsImtpZCI6IkU1N1lkcnVIcGxBanUyY05vMURvckgzajI3QnU1LXNfT1A1UHdQaWhuNU0ifQ.eyJhY2NvdW50X2lkIjozMjA4OTUxNjIzLCJhY3QiOnsic3ViIjoiMzIwNDUwODI1OSJ9LCJhbmlkIjoiOWUzZTllYzctOGM3ZS00MGM3LWI0MmMtMjEwNTFjZjI1YjkxIiwiYXBwX2lkIjo0LCJhdWQiOiJmci5jb3JlLmFwaS52aW50ZWQuY29tIiwiY2MiOiJGUiIsImNsaWVudF9pZCI6IndlYiIsImV4cCI6MTc5MzYxNzg0OSwiaWF0IjoxNzkzMDEzMDQ5LCJpc3MiOiJ2aW50ZWQtaWFtLW9hdXRoIiwibG9naW5fdHlwZSI6MywicHVycG9zZSI6InJlZnJlc2giLCJzY29wZSI6InB1YmxpYyB1c2VyIiwic2lkIjoiZTE2NzkzZDMtMTc5MzAwNTk1MiIsInN1YiI6IjMyMDQ1MDgyNTkifQ.ofzqnQbVsPgrlHoVBiWhGyRXRS3yXyl9hYe3yftEHCFDhz3vYMBugUNkGNGzNiiPWjCSjg2ba39EJZvYaHWuPh6YdxlkA1l-bYHTaq0vV1dF48M9ty76gjnifpn5wL4G9niSfwEk30cj0mWySo8sYQyTTWbzta5M-i-Goeb89ul_XQqoyujD1BLHI2iv7Gl5tRYPcSP8aRMtvvV3ummXCuA-BWv0z-c3NLkHqXw5LPHVGQZdj0GBT_tAW7dqS8fZB5oUqKT8KGOTNTAdFujgtGGj61MkSorTMhSCrhqsnbhCLjqhEhU4K2tgHDtTgAGxtAsNzKkEJvHLhNSzWCAclQ; __eoi=ID=134f8deb08500c48:T=1793006560:RT=1793010154:S=AA-AfjZPDWku5kxs2S6jPhbBV1V4; __gads=ID=bb9c75e43b6d4f55:T=1793006560:RT=1793010154:S=ALNI_MbLFtEulhzqOsgh4ZzFbagZdK-gNQ; __gpi=UID=0000160c888128bd:T=1793006560:RT=1793010154:S=ALNI_MYOker07TSVceYeozCaz-43jpA8ow; RoktRecogniser=0308972b-9cfd-4c55-88fc-647be21817c5; _cc_id=c51250b3194e132d89826db7a33f20f4; cto_bundle=SnnOz19Jc3lHRnEyWTI1WlRLNWFlZSUyRm9USSUyRkx4Y3J3QWg3bFlmeTk0TWtOb1RUcSUyQmx6STl3WSUyQlBldDZ5MVBrZWZmakVvUCUyRlhURTJxcmVpYlFRTGIwZWVmN2ZUciUyQnlxTFdRN1VvVUp1YnVQbExjeCUyQnltOGs1aG5IR1lDM1l5ZFRUVVZW; panoramaId_expiry=1793092959126; seller_header_visits=2; v_sid=e16793d3-1793005952; v_uid=3204508259; anonymous-iso-locale=fr-FR; anonymous-locale=fr; domain_selected=true; __obref=9d423d97-7504-40d2-81cc-eaf938f39bc4; OTAdditionalConsentString=2~20.43.55.57.61.70.83.89.93.108.117.122.124.135.143.144.147.149.159.161.184.192.196.211.228.230.236.239.255.259.266.272.286.291.311.313.314.320.322.323.327.340.358.367.370.371.385.407.415.424.429.430.436.445.469.486.491.494.495.522.523.550.560.568.574.576.587.591.621.723.737.797.798.803.820.839.864.899.904.922.938.955.959.979.981.985.986.1003.1027.1031.1033.1046.1047.1048.1051.1053.1067.1092.1095.1097.1099.1107.1109.1126.1135.1143.1149.1152.1162.1166.1186.1188.1192.1205.1215.1220.1226.1227.1230.1252.1268.1270.1276.1284.1290.1301.1307.1312.1329.1342.1345.1356.1365.1403.1415.1416.1419.1421.1423.1440.1449.1455.1495.1512.1514.1516.1525.1540.1548.1555.1558.1567.1570.1577.1579.1583.1584.1598.1603.1616.1638.1651.1653.1659.1667.1677.1678.1682.1697.1699.1712.1716.1720.1721.1725.1732.1735.1745.1750.1753.1782.1786.1800.1808.1810.1825.1827.1832.1838.1840.1843.1845.1859.1870.1878.1880.1882.1889.1898.1911.1917.1928.1929.1942.1944.1958.1962.1963.1964.1967.1968.1969.1978.1985.1987.2003.2016.2027.2035.2038.2039.2044.2047.2052.2056.2064.2068.2069.2072.2074.2084.2088.2090.2107.2109.2115.2124.2130.2133.2135.2137.2140.2141.2147.2156.2166.2177.2186.2205.2213.2216.2219.2220.2222.2223.2224.2225.2234.2251.2253.2262.2271.2275.2279.2282.2295.2299.2309.2312.2316.2322.2325.2328.2331.2335.2336.2354.2358.2359.2370.2373.2376.2377.2400.2403.2405.2406.2411.2414.2415.2416.2418.2425.2427.2440.2447.2453.2461.2465.2468.2472.2477.2484.2486.2488.2498.2506.2510.2517.2526.2527.2531.2534.2535.2542.2552.2559.2564.2567.2568.2569.2571.2572.2575.2577.2579.2583.2584.2589.2595.2596.2604.2605.2609.2610.2612.2614.2621.2624.2627.2628.2629.2633.2636.2642.2643.2645.2646.2650.2651.2652.2656.2657.2658.2660.2661.2669.2670.2677.2681.2684.2687.2689.2690.2695.2698.2713.2714.2729.2739.2767.2768.2770.2772.2778.2784.2787.2791.2792.2798.2801.2805.2812.2813.2814.2816.2817.2821.2822.2824.2826.2827.2830.2831.2832.2833.2834.2838.2839.2844.2846.2849.2850.2852.2854.2860.2862.2863.2865.2867.2869.2872.2874.2875.2878.2880.2881.2882.2884.2886.2887.2888.2889.2891.2893.2894.2895.2897.2898.2900.2901.2908.2909.2916.2917.2918.2920.2922.2923.2927.2929.2930.2931.2940.2941.2947.2949.2950.2956.2958.2961.2963.2964.2965.2966.2968.2972.2973.2974.2975.2979.2980.2981.2983.2985.2986.2987.2994.2995.2997.2999.3000.3001.3002.3003.3005.3008.3009.3010.3012.3016.3017.3018.3019.3023.3028.3031.3034.3038.3043.3051.3052.3053.3055.3058.3059.3063.3066.3073.3074.3075.3076.3077.3089.3090.3093.3094.3095.3097.3099.3100.3106.3107.3109.3112.3117.3119.3120.3126.3127.3128.3130.3133.3135.3136.3137.3145.3149.3151.3153.3155.3167.3169.3172.3173.3177.3182.3184.3185.3186.3187.3188.3189.3190.3194.3196.3200.3201.3209.3210.3213.3214.3215.3217.3218.3222.3223.3225.3226.3227.3228.3230.3231.3233.3234.3235.3236.3237.3238.3240.3244.3250.3251.3253.3254.3257.3260.3266.3270.3272.3286.3288.3289.3290.3292.3293.3296.3299.3300.3306.3307.3309.3314.3315.3316.3318.3323.3324.3328.3330.3331.3531.3731.3831.4131.4531.4631.4731.4831.5231.6731.6931.7131.7235.7831.7931.8931.10231.10631.10831.11031.11531.11631.13431.13632.14034.14133.14237.15731.16831.16931.21233.21731.23031.25131.25931.26031.26631.27731.27831.28031.28332.28731.29631.30331.30532.30732.32531.33931.34231.34631.34731.36831.39131.39531.40632.41131.41531.43631.43731.43831.45931.47232.47531.48131.49231.49332.49431.50831.52831.54231.56831.56931.57131.57231.57531.57931.58131.58631.59831.59832.60731~dv; OptanonAlertBoxClosed=2026-10-26T09:11:54.608Z; __ps_did=pscrb_de236330-56ab-4ac5-ff56-e450957ef807; __ps_fva=1793005914931; __ps_lu=https://www.vinted.fr/; __ps_r=https://www.google.com/; eupubconsent-v2=CQssWNgQssWNgAcABBFRC2FsAP_gAEPgAAwIMGtR_G__bWlr-Tb3abpkeYxP99hr7sQxBgbIkm4FzLvW7JwCx2EaJAyatiIKmRIAu3DBIQNlHADURUCgKIAFLyDMaEyUoTNKJ6BkiAMRIyJQCEhum4pjWQCZYur_5kc0mB-M6dr-2dzyy4hHH3K5fuS1UJCcIYesDfn8ZBOS-9IE9-x8v4v4_EbpEm0eSVn9pEsp4zc6YlM6dBmxs-TyffyPn_f70fS7X_vc_n3zv8oXH7rr64AAAAAAAAQAAAAAAAAAIMGgAmGh0QBlkQCBAoCAECABQVhABQIAgAASAogIATBgQ5AwAXWESAEAKAAIIAQAAgwABAAAJAAhEAEABAIAQIBAoAAwAIAgIAGBgADABQiAQAAgOgYpAQQCBYAJEYUBggQgAIBAS2VCCQBAgDhCkWOAQQIiYKAABEAAoAAEA8LAQklRKxIIAuILoAEAAABKMEEAFICYAooDIFoKwIOAyNMAQPMEiSHQRAEwQkZBkQkqCQeKYogAAAAAAAAAAAAAAAAAAIAA.f_wACHwAAAAA.IMGtR_G__bXlv-Tb36bpkeYxf99hr7sQxBgbIsm4FzLvW7JwC32EaJEyatiIKmRIAu3DBIQNtHAjURUChKIAVLzDsaEyUoTtKJ-BkiDMRYyJQCEhum4pjWQCZYur_50d0mR-M6dr-2dzyy5hnH3K9fuS1UJicKYetHfn8ZBOS-_IU9_x-_4v4_MbpEm0eSVv9tEst4zc64tP6dpuxs-Tyffyfv_f72fS7X__c__33_8qXX_r764AAAAAAAAQAAAAAAAAAIAA; consent_version=eu; is_shipping_fees_applied_info_banner_dismissed=false; non_dot_com_www_domain_cookie_buster=1"""
" 

def dupliquer_annonce(item_id):
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "fr-FR,fr;q=0.9",
        "Cookie": FULL_COOKIE
    }
    session.headers.update(headers)

    # Récupération des infos de l'annonce
    res = session.get(f"https://www.vinted.fr/api/v2/items/{item_id}")
    
    if res.status_code in [401, 403]:
        return False, f"❌ Erreur {res.status_code} : Bloqué par Vinted/Cloudflare."
    elif res.status_code != 200:
        return False, f"❌ Échec (Code {res.status_code}). Annonce introuvable."

    item = res.json().get("item", {})
    payload = {
        "item": {
            "title": item.get("title"),
            "description": item.get("description"),
            "price": item.get("price"),
            "currency": item.get("currency"),
            "category_id": item.get("category_id"),
            "status_id": item.get("status_id"),
        }
    }

    # Suppression
    del_res = session.delete(f"https://www.vinted.fr/api/v2/items/{item_id}")
    if del_res.status_code not in [200, 204]:
        return False, f"❌ Erreur lors de la suppression (Code {del_res.status_code})."

    # Republication
    post_res = session.post("https://www.vinted.fr/api/v2/items", json=payload)
    if post_res.status_code in [200, 201]:
        return True, "✅ Annonce supprimée et republiée avec succès !"
    
    return False, f"❌ Erreur lors de la republication (Code {post_res.status_code})."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "vinted.fr" in text and "/items/" in text:
        try:
            item_id = text.split("/items/")[1].split("-")[0]
            await update.message.reply_text("🔄 Traitement de l'annonce en cours...")
            success, msg = dupliquer_annonce(item_id)
            await update.message.reply_text(msg)
        except Exception as e:
            await update.message.reply_text(f"❌ Erreur : {e}")
    else:
        await update.message.reply_text("Envoie-moi un lien d'annonce Vinted valide.")

if __name__ == "__main__":
    app_telegram = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app_telegram.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app_telegram.run_polling()
