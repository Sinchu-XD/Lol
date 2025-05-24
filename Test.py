import asyncio
from playwright.async_api import async_playwright

# Paste your full cookie string here:
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

def parse_cookies(cookie_string, domain=".terabox.com"):
    cookies = []
    for c in cookie_string.split('; '):
        if '=' in c:
            name, value = c.split('=', 1)
            cookies.append({
                "name": name,
                "value": value,
                "domain": domain,
                "path": "/",
                "httpOnly": False,
                "secure": True,
            })
    return cookies

async def main():
    link = input("🔗 Enter Terabox video/file link: ").strip()
    print("[*] Launching browser...")

    cookies = parse_cookies(COOKIE_STRING)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Show browser window for debugging
        context = await browser.new_context()

        # Add cookies to context
        await context.add_cookies(cookies)

        page = await context.new_page()
        print("[*] Loading page in browser...")
        try:
            await page.goto(link, wait_until='load', timeout=60000)
        except Exception as e:
            print(f"❌ Error loading page: {e}")
            await browser.close()
            return

        print("[*] Waiting 10 seconds for dynamic content to load...")
        await asyncio.sleep(10)

        html = await page.content()
        print("----- PAGE CONTENT START -----")
        print(html[:1000])  # print first 1000 chars only
        print("----- PAGE CONTENT END -----")

        print("[*] Sleeping for 30 seconds. You can check the browser window manually...")
        await asyncio.sleep(30)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
