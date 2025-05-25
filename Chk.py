import requests
from urllib.parse import unquote
import sys

def parse_cookies(cookie_str):
    cookies = {}
    for item in cookie_str.split(';'):
        if '=' in item:
            key, value = item.strip().split('=', 1)
            cookies[key] = value
    return cookies

def parse_headers(headers_str):
    headers = {}
    for line in headers_str.strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            headers[key.strip()] = value.strip()
    return headers

def download_file(url, headers, cookies, filename="output.mp4"):
    with requests.get(url, headers=headers, cookies=cookies, stream=True) as r:
        total = int(r.headers.get('content-length', 0))
        if r.status_code != 200:
            print(f"Failed to download: HTTP {r.status_code}")
            sys.exit(1)

        print(f"Downloading {filename} ({total / (1024*1024):.2f} MB)...")
        with open(filename, 'wb') as f:
            downloaded = 0
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    done = int(50 * downloaded / total) if total else 0
                    sys.stdout.write(f"\r[{'=' * done}{' ' * (50 - done)}] {downloaded / (1024*1024):.2f}/{total / (1024*1024):.2f} MB")
                    sys.stdout.flush()
        print("\nDownload complete!")

if __name__ == "__main__":
    url = input("Enter URL: ").strip()

    print("Paste your Cookies string (format: key1=value1; key2=value2):")
    cookie_str = input().strip()
    cookies = parse_cookies(cookie_str)

    print("Paste your Headers (format: Header-Key: value, one per line, finish with empty line):")
    headers_lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        headers_lines.append(line)
    headers = parse_headers("\n".join(headers_lines))

    filename = input("Enter filename to save as (default output.mp4): ").strip() or "output.mp4"

    download_file(url, headers, cookies, filename)
