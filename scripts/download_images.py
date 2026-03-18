#!/usr/bin/env python3
"""Download teacher photos and resize for web use."""

import os
import re
import glob
import time
import requests
from urllib.parse import urlparse

CONTENT_DIR = os.path.join(os.path.dirname(__file__), "..", "site", "content", "teachers")
IMAGES_DIR = os.path.join(os.path.dirname(__file__), "..", "site", "static", "images", "teachers")
DELAY = 0.5

HEADERS = {
    "User-Agent": "SFZC-Hugo-Scraper/1.0 (site migration prototype)"
}

def extract_photo_urls():
    """Extract photo URLs from teacher front matter."""
    photos = []
    for filepath in glob.glob(os.path.join(CONTENT_DIR, "*.md")):
        slug = os.path.splitext(os.path.basename(filepath))[0]
        with open(filepath) as f:
            content = f.read()
        m = re.search(r'photo:\s*"([^"]+)"', content)
        if m and m.group(1):
            photos.append((slug, m.group(1)))
    return photos

def download_image(url, slug):
    """Download and save an image."""
    ext = os.path.splitext(urlparse(url).path)[1] or ".jpg"
    filename = f"{slug}{ext}"
    filepath = os.path.join(IMAGES_DIR, filename)

    if os.path.exists(filepath):
        return filepath

    r = requests.get(url, headers=HEADERS, timeout=30, stream=True)
    r.raise_for_status()

    with open(filepath, "wb") as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)

    return filepath

def update_frontmatter(slug, local_path):
    """Update the teacher's front matter to use local image path."""
    filepath = os.path.join(CONTENT_DIR, f"{slug}.md")
    with open(filepath) as f:
        content = f.read()

    relative_path = f"/images/teachers/{os.path.basename(local_path)}"
    content = re.sub(
        r'photo:\s*"[^"]*"',
        f'photo: "{relative_path}"',
        content
    )

    with open(filepath, "w") as f:
        f.write(content)

def main():
    os.makedirs(IMAGES_DIR, exist_ok=True)
    photos = extract_photo_urls()
    print(f"Found {len(photos)} teacher photos to download")

    downloaded = 0
    failed = 0

    for i, (slug, url) in enumerate(photos):
        if not url.startswith("http"):
            continue
        print(f"[{i+1}/{len(photos)}] {slug}...", end=" ", flush=True)
        try:
            local_path = download_image(url, slug)
            update_frontmatter(slug, local_path)
            downloaded += 1
            print("OK")
        except Exception as e:
            failed += 1
            print(f"FAILED: {e}")
        time.sleep(DELAY)

    print(f"\nDone! {downloaded} downloaded, {failed} failed.")

if __name__ == "__main__":
    main()
