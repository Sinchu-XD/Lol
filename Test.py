import asyncio
from playwright.async_api import async_playwright
import re
import requests

TERABOX_LINK = "https://teraboxlink.com/s/1_gOh4YzXqinDw1hu8IAHVg"

def get_download_url(surl):
    api_url = f"https://www.1024tera.com/api/shared_files/{surl}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json",
}
    resp = requests.get(api_url, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    file_info = data.get("file_info") or data.get("data") or {}
    download_url = None
    if file_info:
        download_url = file_info.get("download_url") or file_info.get("download_url_preview")
    return download_url

def download_file(url, filename):
    print(f"[*] Downloading file from: {url}")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    print(f"[+] Download completed and saved as: {filename}")

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

            try:
                og_url = await page.eval_on_selector(
                    "meta[property='og:url']", "el => el.content"
                )
                print(f"[+] Extracted og:url content: {og_url}")

                match = re.search(r"surl=([^&]+)", og_url)
                surl = match.group(1) if match else None
                print(f"[+] Extracted surl: {surl}")

            except Exception as e:
                print(f"❌ Could not extract surl: {e}")
                await browser.close()
                return

            try:
                title = await page.title()
                print(f"[+] Page title: {title}")
                filename_match = re.search(r"telegram.*?(\S+\.\w+)", title)
                filename = filename_match.group(1) if filename_match else "file.mp4"
                print(f"[+] Extracted filename: {filename}")
            except Exception as e:
                print(f"❌ Could not extract filename: {e}")
                filename = "file.mp4"

            await browser.close()

            download_url = get_download_url(surl)
            if download_url:
                download_file(download_url, filename)
            else:
                print("❌ Could not get the direct download URL from API.")

    except Exception as e:
        print(f"❌ Browser launch failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
