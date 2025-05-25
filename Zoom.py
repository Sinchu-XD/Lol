import asyncio
from playwright.async_api import async_playwright

async def extract_zoom_stream(url: str, passcode: str):
    print("⏳ Extracting video stream links...\n")

    try:
        async with async_playwright() as p:
            print("[*] Launching browser...")
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            links = []

            # Listen for video URL responses
            page.on("response", lambda response: links.append(response.url)
                    if ".m3u8" in response.url or ".mp4" in response.url else None)

            print("[*] Navigating to Zoom URL...")
            await page.goto(url, timeout=60000)

            # Try to find and fill passcode field
            password_selectors = [
                "input[type='password']",
                "input[name='passcode']",
                "input[aria-label='Passcode']",
            ]

            filled = False
            for selector in password_selectors:
                try:
                    await page.wait_for_selector(selector, timeout=8000)
                    await page.fill(selector, passcode)
                    print(f"[*] Filled passcode in: {selector}")
                    filled = True
                    break
                except Exception:
                    continue

            if not filled:
                print("❌ Could not find passcode input field.")
                return ["❌ Failed: Passcode input not found"]

            # Try to click submit button
            submit_selectors = [
                "button[type='submit']",
                "button[aria-label='Submit']",
                "button:has-text('Submit')",
                "button:has-text('Unlock')",
                "button:has-text('Join')",
            ]

            clicked = False
            for btn_selector in submit_selectors:
                try:
                    await page.wait_for_selector(btn_selector, timeout=15000)
                    await page.click(btn_selector)
                    print(f"[*] Clicked submit button: {btn_selector}")
                    clicked = True
                    break
                except Exception:
                    continue

            if not clicked:
                print("❌ Could not find or click submit button.")
                return ["❌ Failed: Submit button not found"]

            print("[*] Submitted passcode. Waiting for video to load...")

            # Wait and reload to ensure video is loaded
            await page.wait_for_timeout(8000)
            await page.reload()
            await page.wait_for_timeout(10000)

            await browser.close()

            # Filter unique video links
            video_links = list(set(filter(lambda l: ".m3u8" in l or ".mp4" in l, links)))
            return video_links if video_links else ["❌ No video link found. Wrong passcode or expired link."]
    except Exception as e:
        return [f"❌ Error: {str(e)}"]


if __name__ == "__main__":
    import sys

    try:
        zoom_url = input("🔗 Enter Zoom Recording URL:\n").strip()
        passcode = input("🔐 Enter Zoom Recording Passcode:\n").strip()

        results = asyncio.run(extract_zoom_stream(zoom_url, passcode))

        print("\n📥 Video Links Found:")
        for r in results:
            print(r)

    except KeyboardInterrupt:
        print("\n❌ Cancelled by user")
        sys.exit(0)
