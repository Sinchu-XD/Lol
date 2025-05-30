import requests

def download_video(url, filename, headers):
    try:
        print(f"Downloading from: {url}")
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()  # Raise HTTPError for bad status codes
        
        total_size = int(response.headers.get('content-length', 0))
        print(f"Total size: {total_size / 1024 / 1024:.2f} MB")

        with open(filename, "wb") as f:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    done = int(50 * downloaded / total_size)
                    print(f"\r[{'=' * done}{' ' * (50-done)}] {downloaded*100/total_size:.2f}%", end='')
        print("\nDownload completed successfully!")
    except requests.exceptions.HTTPError as e:
        print(f"\nFailed to download: HTTP {response.status_code} - {response.reason}")
    except Exception as e:
        print(f"\nError occurred: {e}")

if __name__ == "__main__":
    url = "https://ssrweb.zoom.us/replay02/2024/03/04/B3974E60-16A8-4226-A44F-92AE0F67D632/GMT20240304-040653_Recording_avo_1280x720.mp4?response-content-type=video%2Fmp4&response-cache-control=max-age%3D0%2Cs-maxage%3D86400&data=de009697c76ecb236215335e2bc1b5dfe43bf7f0885d87b5847eab43a19ab86e&s001=yes&cid=aw1&fid=B46i0u0_ZeoNN5mk0RvbXesPT6ZBYLphDnj899n6JikCWK7tUnukNAC7y-nlYslPuLBv2XBS4-YnLDPS.v3Xz4kf24Xjga45Y&s002=b-YaeMKGS8Hr-2N0SDissblIima4jsCUUVpkpOoeDHzezLIsH4wEVx3JRaMX4qxTC5i4a3yi_qElkMcHRJ2jEu54ySg0.c-EV5P1I9844wSLN&tid=v=2.0;clid=aw1;rid=WEB_e8ba0adfa19cfaa173128df2561c2e92&Policy=eyJTdGF0ZW1lbnQiOiBbeyJSZXNvdXJjZSI6Imh0dHBzOi8vc3Nyd2ViLnpvb20udXMvcmVwbGF5MDIvMjAyNC8wMy8wNC9CMzk3NEU2MC0xNkE4LTQyMjYtQTQ0Ri05MkFFMEY2N0Q2MzIvR01UMjAyNDAzMDQtMDQwNjUzX1JlY29yZGluZ19hdm9fMTI4MHg3MjAubXA0P3Jlc3BvbnNlLWNvbnRlbnQtdHlwZT12aWRlbyUyRm1wNCZyZXNwb25zZS1jYWNoZS1jb250cm9sPW1heC1hZ2UlM0QwJTJDcy1tYXhhZ2UlM0Q4NjQwMCZkYXRhPWRlMDA5Njk3Yzc2ZWNiMjM2MjE1MzM1ZTJiYzFiNWRmZTQzYmY3ZjA4ODVkODdiNTg0N2VhYjQzYTE5YWI4NmUmczAwMT15ZXMmY2lkPWF3MSZmaWQ9QjQ2aTB1MF9aZW9OTjVtazBSdmJYZXNQVDZaQllMcGhEbmo4OTluNkppa0NXSzd0VW51a05BQzd5LW5sWXNsUHVMQnYyWEJTNC1ZbkxEUFMudjNYejRrZjI0WGpnYTQ1WSZzMDAyPWItWWFlTUtHUzhIci0yTjBTRGlzc2JsSWltYTRqc0NVVVZwa3BPb2VESHplekxJc0g0d0VWeDNKUmFNWDRxeFRDNWk0YTN5aV9xRWxrTWNIUkoyakV1NTR5U2cwLmMtRVY1UDFJOTg0NHdTTE4mdGlkPXY9Mi4wO2NsaWQ9YXcxO3JpZD1XRUJfZThiYTBhZGZhMTljZmFhMTczMTI4ZGYyNTYxYzJlOTIiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3NDgxNTc4MDF9fX1dfQ&Signature=Y7q4Scce2Dn2vBNn2yBYyerXnaE7NEkBWept9W2ugYcBfHy84Ztjx19a7YxuRjpZAszlh12Ws2x2GQ0kVH49jbVZ8eqPTfHtL2XwRH1EUH3xAxy7nPHmyx62GxDqL0g0daD6sF1sDe5DMSDqIURkgkx9f2zrJpiuGcFxj7mKuawV8RL15TkbQbvwBDKqcEQOrSknjMeQa1f7IzYy-KX8UJ0saIh0iJwqIcq~AJZHuThR7DOof-Eeoo0IPCZd6qtvUnedvF9YNU9XR4mCrx2EzRItVijcd9FGIlhL~H2TBLEFKk9rvSEHHCEx2w5-PAx4wvLs3C-MwwmYnVJBKOczpA&Key-Pair-Id=APKAJFHNSLHYCGFYQGIA"

    # Put your cookies string here (exact as in your browser, no line breaks)
    cookies = "_zm_page_auth=aw1_c_iABkx3PpTUCT31x8hlnu4A; _zm_mtk_guid=56e1a7352e344ad0bdc11cc2884e0340; _zm_csp_script_nonce=U7XFzQGfRLme-rmiS1KV9g; _zm_currency=INR; wULrMv6t=BVb0CwaXAQAAfvB44Pmkdeycvw7vrbwqMu9n3gcdtw4tKvYufz9x1nB9cXw-JK5ys3nAfwAAQHcAAAAAJAFJAFalzAv8ozUsDcvwSg|1|0|e8f2d7834720989dc02b6194ff1105c724dc8fd9; _zm_visitor_guid=bf8c5e5314120556ca192a7b10bc63e9; _zm_lang=en-US; _zm_fingerprint=23ac7bd9e9404d4fa5cbc94c2edbe0ee; IR_gbd=zoom.us; _cs_c=0; OptanonAlertBoxClosed=2025-05-25T06:05:44.852Z; OnetrustActiveGroups=C0001C0002C0003C0004; _zm_tracking_guid=b4b57d5377004465babb4dac757952ea; _fbp=fb.1.1748153146992.124210476125047735; _yjsu_yjad=1748153147.50e1a95b-ade0-440b-9efc-d7060c2f0292; _zitok=b256a6f3fac928d9c8591748153147; _ga=GA1.1.2068187785.1748153255; _cs_cvars=%7B%7D; _cs_id=684ac27f-c4c2-abc2-82af-1553b0ae0cf7.1748153134.1.1748153258.1748153134.1.1782317134386.1.x; __utmzz=source=www.zoom.com|medium=referral|campaign=(not set); __utmzzses=source=www.zoom.com|medium=referral|campaign=(not set); _gcl_au=1.1.174580337.1748153145.867999408.1748153263.1748153263; _cs_s=5.5.0.9.1748155178637; _zm_ssid=us05_c_R0khiUekTpujQp3SC4H6Ug; zm_cluster=us05; zm_aid=gflRLQpWS8e-mZz-MCkzHA; zm_haid=300; _zm_login_acctype=2; _zm_multi_ac=~USER_CRYPTO~DM50lP6bhO2e_LiolQAAoAAAACKp7cZoBXy1qCeTxG5tw0GQfLxfzSAhU8gqm_PtDOXA2zVGkCYGRqoSc9a0F_vzu7QyPb_iG7kXv5ZsWv9kGYmUCJxrCz1suWHFzkwcajJrlOcXHwWVjhxGiVDt9AlU3L2sWUsmiSMh86U7HzoBYr8sUMuniwSo21LK41TUhN3elR7lyHmkxH_X5GjZV49MIRAPfVhZuILPDyJDspHr45YVlpsKqZLJtbyJNFnLx2wwMDAwMDAx; _zm_cid2=1%3BMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE%2BQqcC%2BfRDK4jE7AbvtFn4dLzbkvlfXuBQ45NmbVdCAS5ttkkjzDVi4PCyfAKybrg0dN3zN7GveWNZ7l7MDyQrg%3D%3D%3BemhEcXVEc2thQW85%3BMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEk378aQxb3%2BkuI2wZDgxKgQbQK%2FqlA25NJYNtuaKdRNumPZZ7mVqLBjmJVGPBiJPpHqX7Vl216IdOIRBIsfMeag%3D%3D%3BD19%2F5IJs5I8gVLuJ5zNnW3%2BJ2XPO7yXCrg1Jwr4GPRT67rIU%2FLCblzShT6Aeh10xeHSnFqjqwoAuHEBWGkRe00yiMxEqU%2BgBPicDpELg06z8lvX4s4%2BWoJyNuG0LOPd3BTWIl4zkSW8%3D; __cf_bm=xNNHf1Hn87S6R.a6JvmRjd2_Y4j6DyBEVC8f0nGra9o-1748153392-1.0.1.1-_u.deLDTGEPx4CBEoGGUlTtwjQnQNYd6VPoo60zdY25fURYD9TEDasftQ6foDSCgT7CJdv5WPbnCBTqxsbxNOgS4a3.Km9ibwzL3ULhN4Kzqmgx3uGXqCX2lX4DluLHA; _zm_cms_guid=DB3hGJzGmbbZ7DYZIwAAFgAAABs4ksSTZK51kGGff0i2PyHycJvTBxycWDUarqyaefTuihEPAnVEMDAwMDAx; _zm_date_format=mm/dd/yy; _zm_date_format_standard=MM/DD/YYYY; _zm_12-hour=1; _zm_start_day_of_week=7; _zm_billing_visitor_guid=98713524d8da4e7d8870591f601149cd; IR_17910=1748153395822%7C0%7C1748153395822%7C~4ZOHzyuxBDAFGyvqsujqh~-10WMNFzofa84XYNOFAvng92XNLFCs%7C; _tq_id.TV-7209362763-1.616e=42952052426cbda3.1748153396.0.1748153396..; is=5463be92-5e1e-4491-9294-e31a9c13b479; iv=45577231-fd9c-43dd-b4c0-cb4a3ef64f50; _rdt_uuid=1748153147133.6a714fc3-bb39-4bac-bf9f-b386a3bc0709; OptanonConsent=isGpcEnabled=0&datestamp=Sun+May+25+2025+11%3A39%3A56+GMT%2B0530+(India+Standard+Time)&version=6.21.0&isIABGlobal=false&hosts=&consentId=35c823fd-f750-45f1-9ba4-49c9618fd98e&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&geolocation=IN%3BMP&AwaitingReconsent=false; IR_PI=36651042-1690-11f0-a672-d7acb6923054%7C1748153395822; _uetsid=4d3b15d0392e11f0aa90571875faea73; _uetvid=4d3b52f0392e11f0b1fe8beb1fa80282; _zm_cdn_blocked=log_unblk; _zm_ga_trackid=14508c36da42d9611b277d0d14e24ea48c78defeb0c2500df61cfd0516a31f59; _zm_everlogin_type=2; optimizelySession=1748153396773; _ga_L8TBF28DDX=GS2.1.s1748153254$o1$g1$t1748153396$j0$l0$h0; slireg=https://scout.us1.salesloft.com; sliguid=db8b28c7-8a5d-4a5b-90a2-01ef9fc2b4a4; slirequested=true; __Secure-Fgp=F1CF85D5143F566C0B6D4AB699CF536AA16E7708F7F50ED70B56BF810988DF14; cdn_detect_result=1; _zitok=b256a6f3fac928d9c8591748153147; cred=8580A1FE5956AD9CDE9902D57B1E08C3; __cf_bm=GtV1s9P6sRP8PEsE7fnNRdJsZOXr_6TDJrY9SXwjY94-1748153400-1.0.1.1-E7nW5e06.JjwHccotHF9ns38rVYzFp9mgN_fXzB4UUYCLVCiYjpXh9vVaZe4xgvtQ.D9RkQugjJvJPkkfV.WhlCNIIDGXGF.90ebDkHSUtU; AMP_0753e77572=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjIyOGVmZmU2NC1jMzU4LTQ0NWItYTQ1ZC1hNWQ5ZDQ1ZjQxN2YlMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjJzMm9OVWxmYXc2QzNoZCUyQkJ3WWhTYndVNlI5NFFxczRxZTBWSlF3YVFSUlklM0QlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzQ4MTUzMTMzMjQ2JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTc0ODE1MzQwMjc0NiUyQyUyMmxhc3RFdmVudElkJTIyJTNBMjYlMkMlMjJwYWdlQ291bnRlciUyMiUzQTglN0Q="

    # Complete headers dictionary (including User-Agent, Referer, Accept, Cookies)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Referer": "https://ssrweb.zoom.us/",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://ssrweb.zoom.us",
        "Connection": "keep-alive",
        "Cookie": cookies
    }

    filename = input("Enter filename to save as (default output.mp4): ").strip()
    if not filename:
        filename = "output.mp4"

    download_video(url, filename, headers)
