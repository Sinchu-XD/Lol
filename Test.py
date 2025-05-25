import asyncio
import random
import re
from playwright.async_api import async_playwright

# Terabox Link
TERABOX_LINK = "https://teraboxlink.com/s/1_gOh4YzXqinDw1hu8IAHVg"

# Proxies (HTTP and SOCKS5 supported)
PROXIES = [
    "23.247.136.248:80",
    "78.129.138.107:1080",
    "184.178.172.23:4145",
    "65.21.52.41:8888",
    "178.62.116.7:1080",
    "51.81.244.204:17981",
    "68.1.210.163:4145",
    "23.82.137.159:80",
    "98.152.200.61:8081",
    "167.71.171.141:1080",
    "135.125.1.230:80",
    "89.46.249.148:9969",
    "154.16.146.43:80",
    "170.187.145.238:1080",
    "159.65.245.255:80",
    "67.43.236.20:26069",
    "184.178.172.3:4145",
    "154.16.146.48:80"
]

def detect_proxy_type(proxy):
    port = int(proxy.split(":")[-1])
    if port in [1080, 4145]:
        return "socks5"
    return "http"

async def main():
    selected_proxy = random.choice(PROXIES)
    proxy_type = detect_proxy_type(selected_proxy)
    full_proxy = f"{proxy_type}://{selected_proxy}"

    print(f"[🌍] Using proxy: {full_proxy}")
    print(f"🔗 Loading Terabox link: {TERABOX_LINK}")

    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(
                headless=True,
                proxy={"server": full_proxy},
                args=["--no-sandbox"]
            )
            context = await browser.new_context()
            page = await context.new_page()

            download_url = None

            async def handle_request(request):
                url = request.url
                if any(x in url for x in [".mp4", ".m3u8", "download", "file"]):
                    nonlocal download_url
                    download_url = url
                    print(f"[✅] Found potential media URL: {download_url}")

            page.on("request", handle_request)

            print("[*] Loading page...")
            try:
                await page.goto(TERABOX_LINK, wait_until='domcontentloaded', timeout=60000)
            except Exception as e:
                print(f"[❌] Page load failed: {e}")
                await browser.close()
                return

            print("[*] Waiting for network traffic...")
            await asyncio.sleep(10)

            og_url = await page.eval_on_selector("meta[property='og:url']", "el => el.content", strict=False)
            print(f"[+] Extracted og:url: {og_url}")

            match = re.search(r"surl=([^&]+)", og_url or "")
            surl = match.group(1) if match else None
            print(f"[+] Extracted surl: {surl}")

            title = await page.title()
            print(f"[+] Page title: {title}")
            filename_match = re.search(r"telegram.*?(\S+\.\w+)", title)
            filename = filename_match.group(1) if filename_match else None
            print(f"[+] Extracted filename: {filename}")

            if download_url:
                print(f"[🎉] Final download link: {download_url}")
            else:
                print("❌ Could not capture download URL.")

            await browser.close()
        except Exception as e:
            print(f"[❌] Critical error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
