import os
import requests
from tqdm import tqdm
from urllib.parse import urlparse, unquote

def get_filename_from_url(url):
    path = urlparse(url).path
    return unquote(path.split('/')[-1].split('?')[0])

def download_zoom_video(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    print("⏳ Starting download...")
    response = requests.get(url, headers=headers, stream=True)

    if response.status_code != 200:
        print(f"❌ Failed: HTTP {response.status_code}")
        return

    filename = get_filename_from_url(url)
    if not filename.endswith(".mp4"):
        filename += ".mp4"

    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 KB
    progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)

    with open(filename, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()

    print(f"✅ Download complete: {filename}")

if __name__ == "__main__":
    zoom_url = input("🔗 Paste Zoom .mp4 URL: ").strip()
    download_zoom_video(zoom_url)
  
