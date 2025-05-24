import asyncio
from playwright.async_api import async_playwright
import re

TERABOX_LINK = "https://teraboxlink.com/s/1_gOh4YzXqinDw1hu8IAHVg"

# Your cookies as a string (make sure it is valid and up-to-date)
COOKIE_STRING = (
    "browserid=9CqZBM8040sdNs9pEGB_ihahaWeSMIcwt-WjMWgFPGNfFni6ktnp_UwUaGE=; lang=en; "
    "_bid_n=19703d60f3cf7354014207; _ga=GA1.1.311551041.1748116052; "
    "_ga_RSNVN63CM3=GS2.1.s1748121724$o2$g1$t1748122427$j48$10$h0$dP4mq4DrQbxwuHcV7Wm3u9aRyHNSDWS2RBw; "
    "ndus-YuV9VB1peHui-LSEjxhMTs4oTf8tPjXNJMtoOWkk; csrfToken=xdPcBHAws2UX219jZSq2eJOo; "
    "___stripe_mid=c731bf89-76b6-41a6-acf6-e00ba5bca600712c46; "
    "_stripe_sid=935941d3-2e54-43f8-83fe-721594b33a22647e8e; "
    "_ga_HSVH9T016H-GS2.1.s1748122492$o1$g1$t1748123261$j$10$h0; "
    "ndut_fmt=AE8EE8F0D41FCA50A1B7DC06A05435ABDF8A520472BA70029D01CD7588AC40F4"
)

def parse_cookies(cookie_string, domain):
    cookies = []
    for pair in cookie_string.split(";"):
        if "=" in pair:
            name, value = pair.strip().split("=", 1)
            cookies.append({
                "name": name,
                "value": value,
                "domain": domain,
                "path": "/",
                "httpOnly": False,
                "secure": True,
                "sameSite": "Lax"
            })
    return cookies

async def main():
    link = TERABOX_LINK
    print(f"🔗 Loading Terabox link: {link}")

    print("[*] Launching browser...")
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
            context = await browser.new_context()

            # Add cookies before opening page
            domain = "teraboxlink.com"
            cookies = parse_cookies(COOKIE_STRING, domain)
            await context.add_cookies(cookies)
            print(f"[+] Added {len(cookies)} cookies to browser context.")

            page = await context.new_page()

            # Set realistic user agent and headers to avoid detection
            await page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/115.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
            })

            print("[*] Loading page in browser...")
            try:
                await page.goto(link, wait_until='domcontentloaded', timeout=120000)
                print("[*] Waiting for 'og:url' meta tag to appear...")
                await page.wait_for_selector("meta[property='og:url']", timeout=60000, state="attached")

                print("[*] Waiting 10 seconds for dynamic content to load...")
                await asyncio.sleep(10)
            except Exception as e:
                print(f"❌ Error loading page or waiting for selector: {e}")
                await browser.close()
                return

            # Extract surl from OG meta tag
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

            # Extract filename from title
            try:
                title = await page.title()
                print(f"[+] Page title: {title}")

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
