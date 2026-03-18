#!/usr/bin/env python3
"""Scrape dharma talks from sfzc.org and output Hugo-compatible Markdown."""

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
ARCHIVE_URL = f"{BASE_URL}/offerings/dharma-talk-archive"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "site", "content", "dharma-talks")
STATE_FILE = os.path.join(os.path.dirname(__file__), ".talk_state.json")
DELAY = 1.5

HEADERS = {
    "User-Agent": "SFZC-Hugo-Scraper/1.0 (site migration prototype)"
}

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"done": [], "failed": [], "talk_urls": []}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def discover_talk_urls():
    """Paginate through the dharma talk archive to find individual talk URLs."""
    urls = set()
    page = 0

    while True:
        url = f"{ARCHIVE_URL}?page={page}" if page > 0 else ARCHIVE_URL
        print(f"  Fetching archive page {page}...", end=" ", flush=True)
        try:
            r = requests.get(url, headers=HEADERS, timeout=30)
            if r.status_code != 200:
                print(f"status {r.status_code}, stopping")
                break

            soup = BeautifulSoup(r.text, "html.parser")

            # Find talk links
            found = 0
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if "/teachings/dharma-talks/" in href or "/dharma-talks/" in href:
                    full = urljoin(BASE_URL, href)
                    path = urlparse(full).path.rstrip("/")
                    # Only individual talk pages
                    if path.count("/") >= 3 and "archive" not in path:
                        urls.add(full)
                        found += 1

            print(f"found {found} talks")

            if found == 0:
                break

            # Check for "next" / "more" link
            next_link = soup.find("a", string=re.compile(r"more|next|›", re.I))
            if not next_link:
                # Also check for pager links
                pager = soup.find("li", class_="pager-next")
                if not pager:
                    break

            page += 1
            time.sleep(DELAY)

        except Exception as e:
            print(f"error: {e}")
            break

    return sorted(urls)

def slugify_speaker(name):
    """Convert speaker name to a slug matching teacher file names."""
    name = name.lower().strip()
    name = re.sub(r'[^a-z0-9\s-]', '', name)
    name = re.sub(r'[\s]+', '-', name)
    return name

def scrape_talk(url):
    """Scrape a single dharma talk page."""
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    title_el = soup.find("h1") or soup.find("title")
    title = title_el.get_text(strip=True) if title_el else ""
    title = title.replace(" | San Francisco Zen Center", "").strip()

    content_area = soup.find("article") or soup.find("div", class_="field-item") or soup.find("main")
    if not content_area:
        content_area = soup.find("div", class_="content")

    # Extract structured data
    speaker = ""
    talk_date = ""
    center = ""

    if content_area:
        text = content_area.get_text()

        # Try to find speaker
        speaker_patterns = [
            r"(?:Speaker|Teacher|By)[:\s]+([A-Z][a-z]+ [A-Z][a-z]+(?:\s[A-Z][a-z]+)?)",
            r"(?:given by|talk by|with)\s+([A-Z][a-z]+ [A-Z][a-z]+(?:\s[A-Z][a-z]+)?)",
        ]
        for pat in speaker_patterns:
            m = re.search(pat, text)
            if m:
                speaker = m.group(1).strip()
                break

        # Try to find date
        date_patterns = [
            r"(\w+ \d{1,2},? \d{4})",
            r"(\d{1,2}/\d{1,2}/\d{4})",
        ]
        for pat in date_patterns:
            m = re.search(pat, text)
            if m:
                talk_date = m.group(1).strip()
                break

        # Determine center
        text_lower = text.lower()
        if "city center" in text_lower:
            center = "City Center"
        elif "green gulch" in text_lower:
            center = "Green Gulch Farm"
        elif "tassajara" in text_lower:
            center = "Tassajara"

        # Remove scripts, styles
        for tag in content_area.find_all(["script", "style", "nav"]):
            tag.decompose()

    body_html = str(content_area) if content_area else ""
    body_md = md(body_html, heading_style="ATX", strip=["img"]).strip()
    body_md = re.sub(r'\n{3,}', '\n\n', body_md)

    slug = urlparse(url).path.rstrip("/").split("/")[-1]

    return {
        "slug": slug,
        "title": title,
        "speaker": slugify_speaker(speaker) if speaker else "",
        "speaker_name": speaker,
        "talk_date": talk_date,
        "centers": [center] if center else [],
        "body": body_md,
        "url": url,
    }

def write_talk(talk):
    """Write talk data as Hugo Markdown."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, f"{talk['slug']}.md")

    centers_yaml = ""
    if talk["centers"]:
        centers_yaml = "centers:\n" + "\n".join(f'  - "{c}"' for c in talk["centers"])

    # Build aliases
    old_path = f"/teachings/dharma-talks/{talk['slug']}"
    aliases_yaml = f'aliases:\n  - "{old_path}"'

    frontmatter = f"""---
title: "{talk['title'].replace('"', '\\"')}"
speaker: "{talk['speaker']}"
talk_date: "{talk['talk_date']}"
{centers_yaml}
{aliases_yaml}
---
"""
    with open(filepath, "w") as f:
        f.write(frontmatter)
        f.write(talk["body"])
        f.write("\n")

    return filepath

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    state = load_state()

    if not state.get("talk_urls"):
        print("Discovering talk URLs...")
        state["talk_urls"] = discover_talk_urls()
        save_state(state)
    print(f"Total talk URLs: {len(state['talk_urls'])}")

    remaining = [u for u in state["talk_urls"] if u not in state["done"]]
    print(f"Remaining to scrape: {len(remaining)}")

    for i, url in enumerate(remaining):
        slug = urlparse(url).path.rstrip("/").split("/")[-1]
        print(f"[{i+1}/{len(remaining)}] Scraping {slug}...", end=" ", flush=True)
        try:
            talk = scrape_talk(url)
            write_talk(talk)
            state["done"].append(url)
            print(f"OK ({talk['title'][:50]})")
        except Exception as e:
            state["failed"].append(url)
            print(f"FAILED: {e}")

        save_state(state)
        time.sleep(DELAY)

    print(f"\nDone! {len(state['done'])} scraped, {len(state['failed'])} failed.")

if __name__ == "__main__":
    main()
