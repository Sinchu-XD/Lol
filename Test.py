import requests
import re

# === Your cookie string from config ===
COOKIE_STRING = (
    "browserid=9CqZBM8040sdNs9pEGB_ihahaWeSMIcwt-WjMWgFPGNfFni6ktnp_UwUaGE=; lang=en; "
    "_bid_n=19703d60f3cf7354014207; _ga=GA1.1.311551041.1748116052; "
    "_ga_RSNVN63CM3=GS2.1.s1748121724$o2$g1$t1748122427$j48$10$h0$dP4mq4DrQbxwuHcV7Wm3u9aRyHNSDWS2RBw; "
    "ndus-YuV9VB1peHui-LSEjxhMTs4oTf8tPjXNJMtoOWkk; csrfToken=xdPcBHAws2UX219jZSq2eJOo; "
    "___stripe_mid=c731bf89-76b6-41a6-acf6-e00ba5bca600712c46; "
    "_stripe_sid=935941d3-2e54-43f8-83fe-721594b33a22647e8e; "
    "_ga_HSVH9T016H-GS2.1.s1748122492$o1$g1$t1748123261$j$10$h0; "
    "ndut_fmt=AE8EE8F0D41FCA50A1B7DC06A05435ABDF8A520472BA70029D01CD7588AC40F4"
)

HEADERS = {
    "Cookie": COOKIE_STRING,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

def extract_download_link(terabox_url):
    print("[*] Fetching page...")
    response = requests.get(terabox_url, headers=HEADERS)
    if response.status_code != 200:
        print("[!] Failed to fetch page:", response.status_code)
        return None

    html = response.text
    match = re.search(r'"downloadUrl":"(https:[^"]+)"', html)
    if match:
        direct_link = match.group(1).replace("\\u002F", "/")
        return direct_link

    print("[!] Could not extract direct download link.")
    return None

if __name__ == "__main__":
    terabox_url = input("🔗 Enter Terabox video/file link: ").strip()
    download_url = extract_download_link(terabox_url)

    if download_url:
        print("\n✅ Direct Download Link:\n", download_url)
    else:
        print("\n❌ Failed to extract download link. Check cookie or link validity.")
      
