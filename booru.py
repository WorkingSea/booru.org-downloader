import os
import argparse
import requests
from bs4 import BeautifulSoup
import time
import urllib.parse


def get_image_links(page_url, cookies, headers):
    resp = requests.get(page_url, cookies=cookies, headers=headers)
    if resp.status_code == 403:
        print("[error] 403 Forbidden - your cookies may have expired")
        return []
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    thumbs = soup.select("span.thumb a")
    return [
        urllib.parse.urljoin(page_url, a["href"]) for a in thumbs if "href" in a.attrs
    ]


def get_full_image(post_url, cookies, headers):
    resp = requests.get(post_url, cookies=cookies, headers=headers)
    if resp.status_code == 503:
        print(f"[warn] 503 Service Unavailable for {post_url}, skipping...")
        return None
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    img = soup.select_one("#image")
    if img and "src" in img.attrs:
        return img["src"]
    return None


def download_image(url, save_path, cookies, headers):
    if os.path.exists(save_path):
        print(f"[skip] {save_path}")
        return
    resp = requests.get(url, cookies=cookies, headers=headers, stream=True)
    resp.raise_for_status()
    with open(save_path, "wb") as f:
        for chunk in resp.iter_content(8192):
            f.write(chunk)
    print(f"[ok] {save_path}")


def build_save_dir(url):
    parsed = urllib.parse.urlparse(url)
    domain = parsed.netloc.replace(".", "_")

    # Extract tags parameter for folder naming
    query = urllib.parse.parse_qs(parsed.query)
    tags = query.get("tags", [""])[0].replace(":", "_").replace(" ", "_")
    tags_part = f"_{tags}" if tags else ""

    return f"downloads_{domain}{tags_part}"


def main():
    parser = argparse.ArgumentParser(
        description="Download images from booru search results."
    )
    parser.add_argument(
        "url",
        help="Search results URL (e.g. https://animegirls2020.booru.org/index.php?page=post&s=list&tags=hu_tao_(genshin_impact)",
    )
    parser.add_argument(
        "--cf-clearance", required=True, help="Cloudflare clearance cookie value"
    )
    parser.add_argument("--user-id", required=True, help="user_id cookie value")
    parser.add_argument("--pass-hash", required=True, help="pass_hash cookie value")
    args = parser.parse_args()

    cookies = {
        "cf_clearance": args.cf_clearance,
        "user_id": args.user_id,
        "pass_hash": args.pass_hash,
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": args.url,
    }

    save_dir = build_save_dir(args.url)
    os.makedirs(save_dir, exist_ok=True)
    print(f"[dir] Saving images to: {save_dir}")

    page = 0
    total = 0
    while True:
        page_url = f"{args.url}&pid={page * 20}"
        print(f"\n[page] {page_url}")
        posts = get_image_links(page_url, cookies, headers)
        if not posts:
            print("No more posts, done.")
            break
        for post_url in posts:
            img_url = get_full_image(post_url, cookies, headers)
            if not img_url:
                continue
            filename = os.path.basename(img_url.split("?")[0])
            save_path = os.path.join(save_dir, filename)
            download_image(img_url, save_path, cookies, headers)
            total += 1
            print(f"[progress] Downloaded {total} images")
            time.sleep(1)  # polite delay
        page += 1


if __name__ == "__main__":
    main()
