import requests
import re
import json

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


def extract_ids(html):
    share_id = re.search(r'"shareid":"(.*?)"', html)
    uk = re.search(r'"uk":"(.*?)"', html)

    if share_id and uk:
        return share_id.group(1), uk.group(1)
    return None, None


def get_file_info(shareid, uk):
    api_url = f"https://www.terabox.com/share/list?app_id=250528&channel=0&web=1&shareid={shareid}&uk={uk}&clienttype=0"
    res = requests.get(api_url, headers=HEADERS)
    if res.status_code == 200:
        return res.json()
    return None


def get_download_link(fs_id, shareid, uk):
    post_url = "https://www.terabox.com/api/sharedownload"
    params = {
        "app_id": "250528",
        "channel": "0",
        "web": "1",
        "clienttype": "0",
    }

    data = {
        "encrypt": 0,
        "product": "share",
        "uk": uk,
        "primaryid": shareid,
        "fid_list": f"[{fs_id}]",
    }

    res = requests.post(post_url, headers=HEADERS, params=params, data=data)
    try:
        dlink = res.json()["list"][0]["dlink"]
        return dlink
    except:
        return None


if __name__ == "__main__":
    link = input("🔗 Enter Terabox video/file link: ").strip()
    print("[*] Fetching page...")
    page = requests.get(link, headers=HEADERS)
    if page.status_code != 200:
        print("❌ Failed to load page.")
        exit()

    shareid, uk = extract_ids(page.text)
    if not shareid or not uk:
        print("❌ Failed to extract shareid and uk.")
        exit()

    print("[*] Getting file info...")
    info = get_file_info(shareid, uk)
    try:
        file_data = info["list"][0]
        file_name = file_data["server_filename"]
        fs_id = file_data["fs_id"]
    except:
        print("❌ Could not extract file info.")
        exit()

    print(f"📁 File: {file_name}")
    print("[*] Getting direct download link...")
    dlink = get_download_link(fs_id, shareid, uk)
    if dlink:
        print("✅ Direct Link:\n", dlink)
    else:
        print("❌ Failed to get direct download link.")
