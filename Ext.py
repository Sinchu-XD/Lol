import asyncio
import re
import httpx
from playwright.async_api import async_playwright

TERABOX_LINK = "https://teraboxlink.com/s/1_gOh4YzXqinDw1hu8IAHVg"

API_DOWNLOAD_INFO = "https://www.terabox.app/api/share/anon/file?shorturl={surl}&root=1"

async def fetch_surl_from_link(link):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(link, wait_until='domcontentloaded', timeout=60000)
        og_url = await page.eval_on_selector("meta[property='og:url']", "el => el.content")
        await browser.close()
        match = re.search(r"surl=([^&]+)", og_url)
        return match.group(1) if match else None

async def get_file_info(surl):
    url = API_DOWNLOAD_INFO.format(surl=surl)
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        data = resp.json()
        if data.get("errno") != 0:
            raise Exception(f"API error: {data.get('errmsg')}")
        file_info = data.get("list", [{}])[0]
        return file_info

async def main(link):
    print(f"🔗 Processing Terabox link: {link}")

    if "surl=" in link:
        surl = re.search(r"surl=([^&]+)", link).group(1)
    else:
        surl = await fetch_surl_from_link(link)

    if not surl:
        print("❌ Could not extract surl.")
        return

    print(f"[+] Extracted surl: {surl}")

    try:
        info = await get_file_info(surl)
    except Exception as e:
        print(f"❌ Failed to fetch file info: {e}")
        return

    print(f"[+] Filename: {info.get('server_filename')}")
    print(f"[+] Size: {info.get('size')} bytes")
    print(f"[+] Upload Time: {info.get('server_ctime')}")
    print(f"[+] Direct Download URL: {info.get('dlink')}")
    print(f"[+] Thumbnail URL: {info.get('thumbs', [None])[0]}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python terabox_cli.py <terabox_share_link_or_surl>")
        sys.exit(1)
    link = sys.argv[1]
    asyncio.run(main(link))
