import asyncio
from playwright.async_api import async_playwright


async def extract_zoom_stream(url: str, passcode: str):
    print("[*] Launching browser...")
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            links = []

            page.on("response", lambda response: links.append(response.url)
                    if ".m3u8" in response.url or ".mp4" in response.url else None)

            print("[*] Navigating to Zoom URL...")
            await page.goto(url, timeout=60000)

            await page.wait_for_selector("input[type='password']", timeout=15000)
            await page.fill("input[type='password']", passcode)
            await page.click("button[type='submit']")
            print("[*] Submitted passcode, waiting for video...")

            await page.wait_for_timeout(8000)
            await page.reload()
            await page.wait_for_timeout(10000)

            await browser.close()

            video_links = list(set(filter(lambda l: ".m3u8" in l or ".mp4" in l, links)))
            return video_links if video_links else ["❌ No video link found. Wrong passcode or expired URL."]
    except Exception as e:
        return [f"❌ Error: {str(e)}"]


if __name__ == "__main__":
    print("🔗 Enter Zoom Recording URL:")
    url = input().strip()
    print("🔐 Enter Zoom Recording Passcode:")
    passcode = input().strip()

    print("\n⏳ Extracting video stream links...\n")
    links = asyncio.run(extract_zoom_stream(url, passcode))

    print("📥 Video Links Found:")
    for link in links:
        print(link)
      
