import asyncio
from playwright.async_api import async_playwright
import re

TERABOX_LINK = "https://teraboxlink.com/s/1_gOh4YzXqinDw1hu8IAHVg"

COOKIE = (
    "browserid=9CqZBM8040sdNs9pEGB_ihahaWeSMIcwt-WjMWgFPGNfFni6ktnp_UwUaGE=; lang=en; "
    "_bid_n=19703d60f3cf7354014207; _ga=GA1.1.311551041.1748116052; "
    "_ga_RSNVN63CM3=GS2.1.s1748121724$o2$g1$t1748122427$j48$10$h0$dP4mq4DrQbxwuHcV7Wm3u9aRyHNSDWS2RBw; "
    "ndus-YuV9VB1peHui-LSEjxhMTs4oTf8tPjXNJMtoOWkk; csrfToken=xdPcBHAws2UX219jZSq2eJOo; "
    "___stripe_mid=c731bf89-76b6-41a6-acf6-e00ba5bca600712c46; "
    "_stripe_sid=935941d3-2e54-43f8-83fe-721594b33a22647e8e; "
    "_ga_HSVH9T016H-GS2.1.s1748122492$o1$g1$t1748123261$j$10$h0; "
    "ndut_fmt=AE8EE8F0D41FCA50A1B7DC06A05435ABDF8A520472BA70029D01CD7588AC40F4"
)

def parse_cookies(cookie_str, domain):
    cookies = []
    for pair in cookie_str.split(';'):
        if '=' in pair:
            name, value = pair.strip().split('=', 1)
            cookies.append({
                'name': name,
                'value': value,
                'domain': domain,
                'path': '/',
                'httpOnly': False,
                'secure': False,
                'sameSite': 'Lax',
            })
    return cookies

async def main():
    print(f"🔗 Loading Terabox link: {TERABOX_LINK}")

    print("[*] Launching browser...")
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
            
            # Domain for setting cookies must match target domain
            domain = "teraboxlink.com"
            context = await browser.new_context()

            # Add cookies before opening the page
            cookies = parse_cookies(COOKIE, domain)
            await context.add_cookies(cookies)

            page = await context.new_page()

            print("[*] Loading page in browser...")
            try:
                await page.goto(TERABOX_LINK, wait_until='domcontentloaded', timeout=60000)
            except Exception as e:
                print(f"❌ Error loading page: {e}")
                await browser.close()
                return

            print("[*] Waiting 10 seconds for dynamic content to load...")
            await asyncio.sleep(10)

            content = await page.content()

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
