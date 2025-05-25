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

        # Extract direct download link from page
        download_link = None
        try:
            # Selector might change - inspect the Terabox page for the actual selector
            # Here are some guesses based on Terabox structure:
            # Commonly a button or anchor with download link, or <a data-download-url> attribute

            # Try anchor with download attribute or class containing 'download'
            download_link = await page.eval_on_selector(
                "a[data-download-url]", "el => el.getAttribute('data-download-url')"
            )
            if not download_link:
                # fallback: try href with class or id that looks like download button
                download_link = await page.eval_on_selector(
                    "a.download-link, a.btn-download, a[download]", "el => el.href"
                )
            print(f"[+] Direct download link: {download_link}")
        except Exception as e:
            print(f"❌ Could not extract direct download link: {e}")

        # Optional: Extract file size or thumbnail from page if available
        # You can add more selectors here depending on the Terabox page layout

        await browser.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 2:
        link = sys.argv[1]
    else:
        link = TERABOX_LINK
    asyncio.run(main(link))
