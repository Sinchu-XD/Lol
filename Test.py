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

        print("[*] Loading page in browser...")
        await page.goto(TERABOX_LINK, wait_until='domcontentloaded', timeout=60000)

        print("[*] Waiting 10 seconds for dynamic content to load...")
        await asyncio.sleep(10)

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

        # Wait for download button or scan for direct link
        print("[*] Looking for download link on page...")
        download_button = await page.query_selector("a[href*='/download']")
        if download_button:
            download_url = await download_button.get_attribute("href")
            print(f"[✅] Found download URL: {download_url}")
        else:
            print("❌ No direct download button found. Trying fallback...")

            # Fallback: try to scan all links and find possible .mp4 file
            links = await page.eval_on_selector_all("a", "els => els.map(e => e.href)")
            mp4_links = [l for l in links if l.endswith(".mp4")]
            if mp4_links:
                print(f"[✅] Found possible MP4 link: {mp4_links[0]}")
            else:
                print("❌ Could not find a download URL.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
