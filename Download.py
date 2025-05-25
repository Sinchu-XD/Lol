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

                print("[*] Loading page...")
                await page.goto(terabox_url, timeout=30000, wait_until="domcontentloaded")

                await page.wait_for_timeout(8000)
                title = await page.title()
                print(f"[+] Page title: {title}")

                # Extract all requests and look for .mp4 or video content
                media_urls = []

                page.on("response", lambda resp: media_urls.append(resp.url) if (
                    ".mp4" in resp.url or "video" in resp.url
                ) else None)

                await page.wait_for_timeout(10000)

                if media_urls:
                    video_url = media_urls[-1]
                    filename = title.split(" - ")[0].strip()
                    if not filename.endswith(".mp4"):
                        filename += ".mp4"

                    await browser.close()
                    return {
                        "title": title,
                        "filename": filename,
                        "video_url": video_url
                    }, None
                else:
                    await browser.close()
            except Exception as e:
                print(f"[❌] Proxy failed: {proxy} — {str(e)}")
                continue

    return None, "[❌] No valid video URL found from TeraBox link using available proxies."
  
