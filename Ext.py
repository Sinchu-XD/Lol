import asyncio
import re
from playwright.async_api import async_playwright

TERABOX_LINK = "https://teraboxlink.com/s/1_gOh4YzXqinDw1hu8IAHVg"

async def main(link):
    print(f"🔗 Processing Terabox link: {link}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
        context = await browser.new_context()
        page = await context.new_page()

        print("[*] Loading Terabox page...")
        await page.goto(link, wait_until='domcontentloaded', timeout=60000)

        print("[*] Waiting 10 seconds for dynamic content to load...")
        await asyncio.sleep(10)

        # Extract og:url meta content
        og_url = None
        try:
            og_url = await page.eval_on_selector(
                "meta[property='og:url']", "el => el.content"
            )
            print(f"[+] Extracted og:url content: {og_url}")
        except Exception as e:
            print(f"❌ Could not extract og:url: {e}")

        # Extract surl param
        surl = None
        if og_url:
            match = re.search(r"surl=([^&]+)", og_url)
            surl = match.group(1) if match else None
            print(f"[+] Extracted surl: {surl}")

        # Extract filename from title
        filename = None
        try:
            title = await page.title()
            print(f"[+] Page title: {title}")
            filename_match = re.search(r"telegram.*?(\S+\.\w+)", title)
            filename = filename_match.group(1) if filename_match else None
            print(f"[+] Extracted filename: {filename}")
        except Exception as e:
            print(f"❌ Could not extract filename: {e}")

        # Try multiple selectors to find direct download link
        download_link = None
        selectors_to_try = [
            "a[data-download-url]",
            "a[class*='download']",
            "a.btn-download",
            "a[aria-label='Download']",
            "a[href*='download']",
            "a[href*='terabox']",
        ]

        for selector in selectors_to_try:
            try:
                download_link = await page.eval_on_selector(selector, "el => el.href")
                if download_link:
                    print(f"[+] Found download link using selector: {selector}")
                    break
            except Exception:
                pass

        if not download_link:
            print("❌ Could not find direct download link with known selectors.")
            # Dump all <a> hrefs for debug
            links = await page.eval_on_selector_all("a", "els => els.map(el => el.href)")
            print("All anchor links on page:")
            for l in links:
                print(l)
        else:
            print(f"[+] Direct download link: {download_link}")

        await browser.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 2:
        link = sys.argv[1]
    else:
        link = TERABOX_LINK
    asyncio.run(main(link))
