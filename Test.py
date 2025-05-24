import asyncio
from playwright.async_api import async_playwright

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
                # Wait for DOMContentLoaded instead of networkidle to reduce timeout risk
                await page.goto(link, wait_until='domcontentloaded', timeout=60000)
            except Exception as e:
                print(f"❌ Error loading page: {e}")
                await browser.close()
                return

            print("[*] Waiting 10 seconds for dynamic content to load...")
            await asyncio.sleep(10)

            print("----- PAGE CONTENT START -----")
            content = await page.content()
            print(content[:2000])  # print first 2000 characters for brevity
            print("----- PAGE CONTENT END -----")

            # Attempt to extract shareid and uk from the page (adjust selector if needed)
            try:
                shareid = await page.eval_on_selector("input[name=shareid]", "el => el.value")
                uk = await page.eval_on_selector("input[name=uk]", "el => el.value")
                print(f"[+] Extracted shareid: {shareid}")
                print(f"[+] Extracted uk: {uk}")
            except Exception:
                print("❌ Could not extract shareid and uk.")

            await browser.close()
    except Exception as e:
        print(f"❌ Browser launch failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
