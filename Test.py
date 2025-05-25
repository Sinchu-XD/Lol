import asyncio
import aiohttp
import aiofiles
import os
from Download import get_video_info

async def download_video(video_url, filename):
    print(f"[⬇️] Downloading video from: {video_url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(video_url) as resp:
            if resp.status != 200:
                print(f"[❌] Failed to download video: HTTP {resp.status}")
                return
            os.makedirs("downloads", exist_ok=True)
            fpath = f"downloads/{filename}"
            async with aiofiles.open(fpath, mode='wb') as f:
                await f.write(await resp.read())
            print(f"[✅] Download complete: {fpath}")

async def main():
    url = input("🔗 Enter TeraBox link: ").strip()
    print("[🌐] Scraping video info...")
    info, error = await get_video_info(url)

    if error:
        print(error)
        return

    print(f"[🎬] Title: {info['title']}")
    print(f"[📁] Filename: {info['filename']}")
    print(f"[🔗] Video URL: {info['video_url']}")

    await download_video(info['video_url'], info['filename'])

if __name__ == "__main__":
    asyncio.run(main())
