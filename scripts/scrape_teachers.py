#!/usr/bin/env python3
"""Scrape teacher profiles from sfzc.org and output Hugo-compatible Markdown."""

import os
import re
import sys
import time
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from markdownify import markdownify as md

BASE_URL = "https://www.sfzc.org"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "site", "content", "teachers")
STATE_FILE = os.path.join(os.path.dirname(__file__), ".teacher_state.json")
DELAY = 1.5  # seconds between requests

HEADERS = {
    "User-Agent": "SFZC-Hugo-Scraper/1.0 (site migration prototype)"
}

# Center listing pages that contain teacher links
CENTER_TEACHER_PAGES = [
    "/practice-centers/city-center/zen-meditation-practice-city-center/teachers-city-center",
    "/practice-centers/green-gulch-farm/zen-meditation-practice-green-gulch/zen-teachers-practice-leaders",
    "/practice-centers/tassajara/zen-practice-programs/resident-practice-leaders",
]

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"done": [], "failed": []}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def discover_teacher_urls():
    """Find all teacher profile URLs from center pages and the teachers listing."""
    urls = set()

    # Try the main teachers listing page
    try:
        r = requests.get(f"{BASE_URL}/teachers", headers=HEADERS, timeout=30)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if "/teachers/" in href and href.count("/") >= 2:
                    full = urljoin(BASE_URL, href)
                    path = urlparse(full).path.rstrip("/")
                    if path.startswith("/teachers/") and path.count("/") == 2:
                        urls.add(full)
    except Exception as e:
        print(f"Warning: Could not fetch /teachers: {e}")

    time.sleep(DELAY)

    # Also check center-specific teacher pages
    for page_url in CENTER_TEACHER_PAGES:
        try:
            r = requests.get(f"{BASE_URL}{page_url}", headers=HEADERS, timeout=30)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "html.parser")
                for a in soup.find_all("a", href=True):
                    href = a["href"]
                    if "/teachers/" in href:
                        full = urljoin(BASE_URL, href)
                        path = urlparse(full).path.rstrip("/")
                        if path.startswith("/teachers/") and path.count("/") == 2:
                            urls.add(full)
        except Exception as e:
            print(f"Warning: Could not fetch {page_url}: {e}")
        time.sleep(DELAY)

    return sorted(urls)

def classify_center(url, text):
    """Guess center affiliation from URL or page text."""
    centers = []
    text_lower = (text or "").lower()
    if "city center" in text_lower or "city-center" in url:
        centers.append("City Center")
    if "green gulch" in text_lower or "green-gulch" in url:
        centers.append("Green Gulch Farm")
    if "tassajara" in text_lower:
        centers.append("Tassajara")
    return centers if centers else ["City Center"]  # default

def classify_role(text):
    """Extract role from page text."""
    text_lower = (text or "").lower()
    roles = [
        ("central abbot", "Central Abbot"),
        ("abbot", "Abbot"),
        ("abbess", "Abbess"),
        ("senior dharma teacher", "Senior Dharma Teacher"),
        ("dharma teacher", "Dharma Teacher"),
        ("practice leader", "Practice Leader"),
        ("tanto", "Tanto"),
        ("guest teacher", "Guest Teacher"),
        ("teacher", "Teacher"),
    ]
    for pattern, role in roles:
        if pattern in text_lower:
            return role
    return ""

def scrape_teacher(url):
    """Scrape a single teacher profile page."""
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    # Get title
    title_el = soup.find("h1") or soup.find("title")
    name = title_el.get_text(strip=True) if title_el else ""
    # Clean up title
    name = name.replace(" | San Francisco Zen Center", "").strip()

    # Get main content
    content_area = soup.find("article") or soup.find("div", class_="field-item") or soup.find("main")
    if not content_area:
        content_area = soup.find("div", class_="content")

    # Get photo
    photo_url = ""
    if content_area:
        img = content_area.find("img")
        if img and img.get("src"):
            photo_url = urljoin(BASE_URL, img["src"])

    # Get bio text
    bio_html = ""
    if content_area:
        # Remove scripts, styles, nav
        for tag in content_area.find_all(["script", "style", "nav"]):
            tag.decompose()
        bio_html = str(content_area)

    bio_md = md(bio_html, heading_style="ATX", strip=["img"]).strip()
    # Clean up excessive whitespace
    bio_md = re.sub(r'\n{3,}', '\n\n', bio_md)

    role = classify_role(bio_md)
    centers = classify_center(url, bio_md)
    slug = urlparse(url).path.rstrip("/").split("/")[-1]

    return {
        "slug": slug,
        "name": name,
        "role": role,
        "centers": centers,
        "photo": photo_url,
        "bio": bio_md,
        "url": url,
    }

def write_teacher(teacher):
    """Write teacher data as Hugo Markdown."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, f"{teacher['slug']}.md")

    centers_yaml = "\n".join(f'  - "{c}"' for c in teacher["centers"])
    photo_line = f'photo: "{teacher["photo"]}"' if teacher["photo"] else 'photo: ""'

    # Build aliases for old URLs
    old_path = f"/teachers/{teacher['slug']}"
    aliases_yaml = f'aliases:\n  - "{old_path}"'

    frontmatter = f"""---
title: "{teacher['name'].replace('"', '\\"')}"
role: "{teacher['role']}"
centers:
{centers_yaml}
{photo_line}
status: "active"
{aliases_yaml}
---
"""
    with open(filepath, "w") as f:
        f.write(frontmatter)
        f.write(teacher["bio"])
        f.write("\n")

    return filepath

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    state = load_state()

    print("Discovering teacher URLs...")
    urls = discover_teacher_urls()
    print(f"Found {len(urls)} teacher URLs")

    # Filter out already-done URLs
    remaining = [u for u in urls if u not in state["done"]]
    print(f"Remaining to scrape: {len(remaining)}")

    for i, url in enumerate(remaining):
        slug = urlparse(url).path.rstrip("/").split("/")[-1]
        print(f"[{i+1}/{len(remaining)}] Scraping {slug}...", end=" ", flush=True)
        try:
            teacher = scrape_teacher(url)
            filepath = write_teacher(teacher)
            state["done"].append(url)
            print(f"OK ({teacher['name']})")
        except Exception as e:
            state["failed"].append(url)
            print(f"FAILED: {e}")

        save_state(state)
        time.sleep(DELAY)

    print(f"\nDone! {len(state['done'])} scraped, {len(state['failed'])} failed.")
    if state["failed"]:
        print("Failed URLs:")
        for u in state["failed"]:
            print(f"  {u}")

if __name__ == "__main__":
    main()
