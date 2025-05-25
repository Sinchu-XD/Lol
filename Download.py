import asyncio
from playwright.async_api import async_playwright
import random

PROXIES = [
    "socks5://78.129.138.107:1080",
    "socks5://184.178.172.23:4145",
    "socks5://68.1.210.163:4145",
    "socks5://184.178.172.3:4145"
]

async def get_video_info(terabox_url):
    async with async_playwright() as p:
        for proxy in PROXIES:
            print(f"[🌍] Trying proxy: {proxy}")
            try:
                browser = await p.chromium.launch(proxy={"server": proxy}, headless=True)
                context = await browser.new_context()
                page = await context.new_page()

                video_url_holder = {"url": None}

                # Intercept .mp4 only
                def handle_response(resp):
                    url = resp.url
                    if ".mp4" in url and "google" not in url and "analytics" not in url:
                        video_url_holder["url"] = url

                page.on("response", handle_response)

                print("[*] Loading page...")
                await page.goto(terabox_url, timeout=30000, wait_until="networkidle")
                await page.wait_for_timeout(10000)

                title = await page.title()
                print(f"[+] Page title: {title}")

                await browser.close()

                if video_url_holder["url"]:
                    filename = title.split(" - ")[0].strip()
                    if not filename.endswith(".mp4"):
                        filename += ".mp4"
                    return {
                        "title": title,
                        "filename": filename,
                        "video_url": video_url_holder["url"]
                    }, None
                else:
                    return None, "[❌] No valid .mp4 video found."

            except Exception as e:
                print(f"[❌] Proxy failed: {proxy} — {str(e)}")
                continue

    return None, "[❌] All proxies failed or no video found."
