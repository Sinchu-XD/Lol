import asyncio
import re
from playwright.async_api import async_playwright

async def main():
    link = input("🔗 Enter Terabox video/file link: ").strip()
    if not link.startswith("http"):
        print("❌ Invalid URL")
        return

    print("[*] Launching browser...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # headless for terminal
        page = await browser.new_page()

        print("[*] Loading page in browser...")
        try:
            await page.goto(link, wait_until='networkidle', timeout=45000)
        except Exception as e:
            print(f"❌ Error loading page: {e}")
            await browser.close()
            return

        print("[*] Waiting 10 seconds for dynamic content to load...")
        await asyncio.sleep(10)

        print("[*] Trying to extract shareid and uk...")

        # Try direct JS evaluation
        shareid = await page.evaluate("() => window.shareid || null")
        uk = await page.evaluate("() => window.uk || null")

        # Fallback to regex in HTML content if JS variables not found
        if not shareid or not uk:
            content = await page.content()
            shareid_match = re.search(r'shareid\s*=\s*"([^"]+)"', content)
            uk_match = re.search(r'uk\s*=\s*"([^"]+)"', content)
            shareid = shareid_match.group(1) if shareid_match else shareid
            uk = uk_match.group(1) if uk_match else uk

        if shareid and uk:
            print(f"✅ Found shareid: {shareid}")
            print(f"✅ Found uk: {uk}")
        else:
            print("❌ Could not extract shareid and uk.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
