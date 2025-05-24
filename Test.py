import asyncio
from playwright.async_api import async_playwright
import re

TERABOX_LINK = "https://teraboxlink.com/s/1_gOh4YzXqinDw1hu8IAHVg"

async def main():
    link = TERABOX_LINK
    print(f"🔗 Loading Terabox link: {link}")

    print("[*] Launching browser...")
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
            context = await browser.new_context()
            page = await context.new_page()

            print("[*] Loading page in browser...")
            try:
                await page.goto(link, wait_until='domcontentloaded', timeout=60000)
            except Exception as e:
                print(f"❌ Error loading page: {e}")
                await browser.close()
                return

            print("[*] Waiting 10 seconds for dynamic content to load...")
            await asyncio.sleep(10)

            # Get full page content (for debug)
            content = await page.content()

            # Extract surl from OG meta tag
            try:
                og_url = await page.eval_on_selector(
                    "meta[property='og:url']", "el => el.content"
                )
                print(f"[+] Extracted og:url content: {og_url}")

                # Extract surl param from URL
                match = re.search(r"surl=([^&]+)", og_url)
                surl = match.group(1) if match else None
                print(f"[+] Extracted surl: {surl}")

            except Exception as e:
                print(f"❌ Could not extract surl: {e}")

            # Extract filename from title tag
            try:
                title = await page.title()
                print(f"[+] Page title: {title}")
                # Attempt to extract filename from title, example: "telegram @getnewlink J2VFNS.mp4 - Share Files Online"
                filename_match = re.search(r"telegram.*?(\S+\.\w+)", title)
                filename = filename_match.group(1) if filename_match else None
                print(f"[+] Extracted filename: {filename}")
            except Exception as e:
                print(f"❌ Could not extract filename: {e}")

            await browser.close()

    except Exception as e:
        print(f"❌ Browser launch failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
