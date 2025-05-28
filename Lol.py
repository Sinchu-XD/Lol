import os
import requests
import sys
import argparse

try:
    from TeraboxDL import TeraboxDL
except ImportError:
    print("Error: 'terabox-downloader' library not found.")
    print("Please install it using: pip install terabox-downloader")
    sys.exit(1)

DEFAULT_TERABOX_COOKIE = "lang=en; ndus=YuV9VB1peHui-LSEjxhMTs4oTf8tPjXNJMtoOWkk;"
DOWNLOAD_DIR = "downloads"

def get_terabox_direct_link(url: str, cookies: str) -> dict:
    if not cookies or ("YOUR_NDUS_VALUE_HERE" in cookies) or ("lang=en; ndus=YuV9VB1peHui-LSEjxhMTs4oTf8tPjXNJMtoOWkk;" == cookies):
        print("\nWARNING: Terabox cookies are not configured or still using example values.")
        print("Please provide your actual 'lang' and 'ndus' cookies from Terabox.com.")
        print("Without correct cookies, downloads will likely fail.\n")

    try:
        terabox = TeraboxDL(cookies)
        file_info = terabox.get_file_info(url)
        if "error" in file_info:
            return {"error": f"Error from TeraboxDL: {file_info['error']}. This might mean the URL is invalid, it's a folder, or cookies are incorrect/expired."}
        else:
            return {
                "file_name": file_info.get("file_name", "unknown_video"),
                "download_link": file_info.get("download_link"),
                "file_size": file_info.get("file_size")
            }
    except Exception as e:
        return {"error": f"Failed to process Terabox link: {e}. Please check the URL and your cookies."}

def download_video_from_terabox(terabox_url: str, cookies: str):
    print(f"Processing Terabox link: {terabox_url}")
    file_details = get_terabox_direct_link(terabox_url, cookies)
    if file_details.get("error"):
        print(f"Error: {file_details['error']}")
        return

    direct_link = file_details["download_link"]
    file_name = file_details["file_name"]
    file_size_bytes = file_details.get("file_size", 0)
    if not direct_link:
        print("Error: Could not extract a direct download link from the provided Terabox URL.")
        return

    file_size_mb = file_size_bytes / (1024 * 1024) if file_size_bytes else "unknown"
    print(f"Found video: '{file_name}' (Size: {file_size_mb:.2f} MB)")
    print("Starting download...")

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    safe_file_name = "".join(c if c.isalnum() or c in ('.', '_', '-') else '_' for c in file_name).strip()
    if not safe_file_name:
        safe_file_name = "terabox_video.mp4"
    if '.' not in safe_file_name or not any(safe_file_name.lower().endswith(ext) for ext in ['.mp4', '.avi', '.mkv', '.mov', '.webm']):
        safe_file_name += ".mp4"

    local_file_path = os.path.join(DOWNLOAD_DIR, safe_file_name)

    try:
        with requests.get(direct_link, stream=True) as r:
            r.raise_for_status()
            if file_size_bytes == 0:
                total_size_in_bytes = int(r.headers.get('content-length', 0))
            else:
                total_size_in_bytes = file_size_bytes

            block_size = 8192
            downloaded_bytes = 0

            with open(local_file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=block_size):
                    if chunk:
                        f.write(chunk)
                        downloaded_bytes += len(chunk)
                        if total_size_in_bytes > 0:
                            progress_percent = (downloaded_bytes / total_size_in_bytes) * 100
                            sys.stdout.write(f"\rDownloading: {progress_percent:.2f}% ({downloaded_bytes / (1024*1024):.2f}MB / {total_size_in_bytes / (1024*1024):.2f}MB)")
                            sys.stdout.flush()
                        else:
                            sys.stdout.write(f"\rDownloading: {downloaded_bytes / (1024*1024):.2f}MB downloaded...")
                            sys.stdout.flush()
            sys.stdout.write("\n")

        print(f"Download complete! Video saved to: {os.path.abspath(local_file_path)}")

    except requests.exceptions.RequestException as e:
        print(f"Error during download: {e}. The download link might be expired or invalid.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download videos from Terabox using a share URL.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "url",
        help="The Terabox share URL of the video."
    )
    parser.add_argument(
        "-c", "--cookies",
        default=DEFAULT_TERABOX_COOKIE,
        help=(
            "Your Terabox 'lang' and 'ndus' cookies in the format:\n"
            "'lang=your_lang_value; ndus=your_ndus_value;'\n"
            "If not provided, the hardcoded default will be used.\n"
            "See the script comments for how to get these cookies."
        )
    )

    args = parser.parse_args()
    if not args.url.startswith(("http://", "https://")):
        print("Error: The provided URL must start with http:// or https://.")
        sys.exit(1)
    
    if "terasharelink.com" not in args.url and "nephobox.com" not in args.url and "mirrobox.com" not in args.url and "go.terabox.com" not in args.url:
        print("Error: The provided URL does not appear to be a Terabox (or related) share link.")
        sys.exit(1)

    download_video_from_terabox(args.url, args.cookies)
