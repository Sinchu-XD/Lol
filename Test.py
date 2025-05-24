import asyncio
from playwright.async_api import async_playwright

TERABOX_LINK = "https://teraboxlink.com/s/1_gOh4YzXqinDw1hu8IAHVg"

async def main():
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            # Use 'domcontentloaded' to avoid infinite loading due to 'networkidle'
            await page.goto(TERABOX_LINK, wait_until="domcontentloaded", timeout=120000)
            print("[✅] Page loaded successfully!")

            # Wait for download button or any identifiable element (adjust selector based on actual page)
            await page.wait_for_timeout(5000)  # wait 5 seconds for content to settle

            # Example: Extract title of the page
            title = await page.title()
            print(f"[📄] Page Title: {title}")

            # Example: Extract visible text from the page
            content = await page.content()
            if "Download" in content:
                print("[⬇️] Download option detected on the page!")

            # Example: Get all visible links (customize as needed)
            links = await page.eval_on_selector_all("a", "elements => elements.map(e => e.href)")
            for link in links:
                if "download" in link.lower():
                    print(f"[🔗] Download Link Found: {link}")

        except Exception as e:
            print(f"[❌] Failed to load page or extract data: {e}")

        finally:
            await browser.close()

asyncio.run(main())
