import requests

# Replace this URL with the one you want to access
url = "https://zoom.us/profile"

# Paste the cookie string here
cookie_string = """
_zm_page_auth=aw1_c_iABkx3PpTUCT31x8hlnu4A; _zm_mtk_guid=56e1a7352e344ad0bdc11cc2884e0340; _zm_csp_script_nonce=U7XFzQGfRLme-rmiS1KV9g; ...
"""

# Convert the cookie string into a dictionary
cookies = {}
for item in cookie_string.split(";"):
    if "=" in item:
        key, value = item.strip().split("=", 1)
        cookies[key] = value

# Make a request using the cookies
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers, cookies=cookies)

# Save the result or print it
if response.status_code == 200:
    with open("zoom_profile.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    print("✅ Successfully fetched Zoom profile page (saved as zoom_profile.html)")
else:
    print(f"❌ Failed to fetch page. Status code: {response.status_code}")
