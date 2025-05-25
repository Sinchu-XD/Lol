import requests

# The signed URL you gave
url = "https://ssrweb.zoom.us/replay02/2024/03/04/B3974E60-16A8-4226-A44F-92AE0F67D632/GMT20240304-040653_Recording_avo_1280x720.mp4?response-content-type=video%2Fmp4&response-cache-control=max-age%3D0%2Cs-maxage%3D86400&data=de009697c76ecb236215335e2bc1b5dfe43bf7f0885d87b5847eab43a19ab86e&s001=yes&cid=aw1&fid=B46i0u0_ZeoNN5mk0RvbXesPT6ZBYLphDnj899n6JikCWK7tUnukNAC7y-nlYslPuLBv2XBS4-YnLDPS.v3Xz4kf24Xjga45Y&s002=b-YaeMKGS8Hr-2N0SDissblIima4jsCUUVpkpOoeDHzezLIsH4wEVx3JRaMX4qxTC5i4a3yi_qElkMcHRJ2jEu54ySg0.c-EV5P1I9844wSLN&tid=v=2.0;clid=aw1;rid=WEB_e8ba0adfa19cfaa173128df2561c2e92&Policy=eyJTdGF0ZW1lbnQiOiBbeyJSZXNvdXJjZSI6Imh0dHBzOi8vc3Nyd2ViLnpvb20udXMvcmVwbGF5MDIvMjAyNC8wMy8wNC9CMzk3NEU2MC0xNkE4LTQyMjYtQTQ0Ri05MkFFMEY2N0Q2MzIvR01UMjAyNDAzMDQtMDQwNjUzX1JlY29yZGluZ19hdm9fMTI4MHg3MjAubXA0P3Jlc3BvbnNlLWNvbnRlbnQtdHlwZT12aWRlbyUyRm1wNCZyZXNwb25zZS1jYWNoZS1jb250cm9sPW1heC1hZ2UlM0QwJTJDcy1tYXhhZ2UlM0Q4NjQwMCZkYXRhPWRlMDA5Njk3Yzc2ZWNiMjM2MjE1MzM1ZTJiYzFiNWRmZTQzYmY3ZjA4ODVkODdiNTg0N2VhYjQzYTE5YWI4NmUmczAwMT15ZXMmY2lkPWF3MSZmaWQ9QjQ2aTB1MF9aZW9OTjVtazBSdmJYZXNQVDZaQllMcGhEbmo4OTluNkppa0NXSzd0VW51a05BQzd5LW5sWXNsUHVMQnYyWEJTNC1ZbkxEUFMudjNYejRrZjI0WGpnYTQ1WSZzMDAyPWItWWFlTUtHUzhIci0yTjBTRGlzc2JsSWltYTRqc0NVVVZwa3BPb2VESHplekxJc0g0d0VWeDNKUmFNWDRxeFRDNWk0YTN5aV9xRWxrTWNIUkoyakV1NTR5U2cwLmMtRVY1UDFJOTg0NHdTTE4mdGlkPXY9Mi4wO2NsaWQ9YXcxO3JpZD1XRUJfZThiYTBhZGZhMTljZmFhMTczMTI4ZGYyNTYxYzJlOTIiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3NDgxNTc4MDF9fX1dfQ&Signature=Y7q4Scce2Dn2vBNn2yBYyerXnaE7NEkBWept9W2ugYcBfHy84Ztjx19a7YxuRjpZAszlh12Ws2x2GQ0kVH49jbVZ8eqPTfHtL2XwRH1EUH3xAxy7nPHmyx62GxDqL0g0daD6sF1sDe5DMSDqIURkgkx9f2zrJpiuGcFxj7mKuawV8RL15TkbQbvwBDKqcEQOrSknjMeQa1f7IzYy-KX8UJ0saIh0iJwqIcq~AJZHuThR7DOof-Eeoo0IPCZd6qtvUnedvF9YNU9XR4mCrx2EzRItVijcd9FGIlhL~H2TBLEFKk9rvSEHHCEx2w5-PAx4wvLs3C-MwwmYnVJBKOczpA&Key-Pair-Id=APKAJFHNSLHYCGFYQGIA"

# Your Zoom cookies here, in dict form, e.g. from your browser or from scraping
cookies = {
    # 'cookie_name': 'cookie_value',
    # Add your real cookies here (usually multiple cookies)
    # Example:
    # 'ssrweb': 'your_cookie_value_here',
    # 'another_cookie': 'value',
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/113.0.0.0 Safari/537.36",
    "Referer": "https://ssrweb.zoom.us/",  # Sometimes required
}

response = requests.get(url, cookies=cookies, headers=headers, stream=True)

if response.status_code == 200:
    with open("zoom_recording.mp4", "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print("✅ Download completed: zoom_recording.mp4")
else:
    print(f"❌ Failed to download, status code: {response.status_code}")
