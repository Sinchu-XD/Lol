import asyncio
from playwright.async_api import async_playwright
import re

TERABOX_LINK = "https://teraboxlink.com/s/1_gOh4YzXqinDw1hu8IAHVg"

async def main():
    print(f"🔗 Loading Terabox link: {TERABOX_LINK}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
        context = await browser.new_context()
        page = await context.new_page()

        download_url = None

        # Intercept all requests and look for media/download URLs
        async def handle_request(request):
            url = request.url
            if any(x in url for x in [".mp4", ".m3u8", "download", "file"]):
                nonlocal download_url
                download_url = url
                print(f"[✅] Found potential media URL: {download_url}")

        page.on("request", handle_request)

        print("[*] Loading page in browser...")
        await page.goto(TERABOX_LINK, wait_until='networkidle', timeout=60000)

        print("[*] Waiting 10 seconds for network requests to complete...")
        await asyncio.sleep(10)

        # Get metadata
        og_url = await page.eval_on_selector("meta[property='og:url']", "el => el.content")
        print(f"[+] Extracted og:url content: {og_url}")

        match = re.search(r"surl=([^&]+)", og_url)
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
            print("❌ Could not capture any download URL from network.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
