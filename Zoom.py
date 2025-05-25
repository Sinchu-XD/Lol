import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

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
            passcode_filled = False
            try:
                await page.wait_for_selector("input[type='password']", timeout=10000)
                await page.fill("input[type='password']", passcode)
                print("[*] Filled passcode in input[type='password']")
                passcode_filled = True
            except PlaywrightTimeoutError:
                print("❌ Passcode field not found.")
                return ["❌ Failed: Passcode input not found"]

            await asyncio.sleep(2)  # Wait a bit before submitting

            # Try to click submit or press Enter
            submitted = False
            button_selectors = [
                "button[type='submit']",
                "button:has-text('Access recording')",
                "button:has-text('Submit')",
                "button:has-text('Watch Recording')"
            ]

            for selector in button_selectors:
                try:
                    await page.wait_for_selector(selector, timeout=5000)
                    await page.click(selector)
                    print(f"[*] Clicked submit button: {selector}")
                    submitted = True
                    break
                except Exception:
                    continue

            if not submitted:
                try:
                    # Try pressing ENTER in the password input
                    await page.press("input[type='password']", "Enter")
                    print("[*] Pressed Enter key as fallback.")
                    submitted = True
                except Exception:
                    pass

            if not submitted:
                print("❌ Could not find or click submit button.")
                return ["❌ Failed: Submit button not found"]

            print("[*] Submitted passcode. Waiting for video to load...")
            await asyncio.sleep(8)
            await page.reload()
            await asyncio.sleep(10)

            await browser.close()

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
