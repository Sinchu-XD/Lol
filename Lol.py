import os
import requests
from TeraboxDL import TeraboxDL

TERABOX_COOKIE = "lang=en; ndus=YuV9VB1peHui-LSEjxhMTs4oTf8tPjXNJMtoOWkk;"  # Replace with your real cookies
DOWNLOAD_DIR = "downloads"

def get_direct_link(url):
    terabox = TeraboxDL(TERABOX_COOKIE)
    info = terabox.get_file_info(url)
    if "error" in info:
        print(f"Error: {info['error']}")
        return None
    return info

def download_file(url, filename):
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    path = os.path.join(DOWNLOAD_DIR, filename)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        with open(path, "wb") as f:
            downloaded = 0
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    percent = int(downloaded * 100 / total)
                    print(f"\rDownloading: {percent}%", end="", flush=True)
    print(f"\nDownload complete: {path}")

def main():
    url = input("Enter Terabox video URL: ").strip()
    if not url:
        print("No URL provided.")
        return
    info = get_direct_link(url)
    if not info:
        return
    print(f"Video: {info['file_name']} | Size: {info['file_size'] / (1024*1024):.2f} MB")
    download_file(info['download_link'], info['file_name'])

if __name__ == "__main__":
    main()
  
