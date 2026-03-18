#!/usr/bin/env python3
"""Scrape events from sfzc.org calendar and output Hugo-compatible Markdown."""

import os
import re
import time
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from markdownify import markdownify as md

BASE_URL = "https://www.sfzc.org"
CALENDAR_URL = f"{BASE_URL}/calendar"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "site", "content", "events")
STATE_FILE = os.path.join(os.path.dirname(__file__), ".event_state.json")
DELAY = 1.0

HEADERS = {
    "User-Agent": "SFZC-Hugo-Scraper/1.0 (site migration prototype)"
}

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"done": [], "failed": [], "event_urls": []}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def discover_event_urls():
    """Paginate through the calendar to find event URLs."""
    urls = set()
    page = 0

    while True:
        url = f"{CALENDAR_URL}?page={page}" if page > 0 else CALENDAR_URL
        print(f"  Fetching calendar page {page}...", end=" ", flush=True)
        try:
            r = requests.get(url, headers=HEADERS, timeout=30)
            if r.status_code != 200:
                print(f"status {r.status_code}, stopping")
                break

            soup = BeautifulSoup(r.text, "html.parser")

            found = 0
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if "/calendar/events/" in href:
                    full = urljoin(BASE_URL, href)
                    urls.add(full)
                    found += 1

            print(f"found {found} events")

            if found == 0:
                break

            # Check for next page
            next_link = soup.find("li", class_="pager-next")
            if not next_link:
                next_link = soup.find("a", string=re.compile(r"more|next|›", re.I))
                if not next_link:
                    break

            page += 1
            time.sleep(DELAY)

        except Exception as e:
            print(f"error: {e}")
            break

    return sorted(urls)

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s]+', '-', text)
    return text[:80]

def scrape_event(url):
    """Scrape a single event page."""
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    title_el = soup.find("h1") or soup.find("title")
    title = title_el.get_text(strip=True) if title_el else ""
    title = title.replace(" | San Francisco Zen Center", "").strip()

    content_area = soup.find("article") or soup.find("div", class_="field-item") or soup.find("main")
    if not content_area:
        content_area = soup.find("div", class_="content")

    event_date = ""
    end_date = ""
    center = ""
    event_type = ""
    teacher = ""
    event_format = ""

    if content_area:
        text = content_area.get_text()

        # Extract date
        date_patterns = [
            r"(\w+ \d{1,2},? \d{4})",
            r"(\d{1,2}/\d{1,2}/\d{4})",
        ]
        for pat in date_patterns:
            m = re.search(pat, text)
            if m:
                event_date = m.group(1).strip()
                break

        # Determine center from URL or text
        path = urlparse(url).path.lower()
        text_lower = text.lower()
        if "city-center" in path or "city center" in text_lower:
            center = "City Center"
        elif "green-gulch" in path or "green gulch" in text_lower:
            center = "Green Gulch Farm"
        elif "tassajara" in path or "tassajara" in text_lower:
            center = "Tassajara"
        elif "online" in path or "online" in text_lower:
            center = "Online"

        # Classify event type from title
        title_lower = title.lower()
        if "sesshin" in title_lower:
            event_type = "Sesshin"
        elif "retreat" in title_lower:
            event_type = "Retreat"
        elif "workshop" in title_lower:
            event_type = "Workshop"
        elif "class" in title_lower or "course" in title_lower:
            event_type = "Class"
        elif "practice period" in title_lower:
            event_type = "Practice Period"
        elif "lecture" in title_lower or "dharma talk" in title_lower:
            event_type = "Lecture"
        elif "guest season" in title_lower:
            event_type = "Guest Season"
        elif "sitting" in title_lower or "zazen" in title_lower:
            event_type = "Sitting"

        # Format
        if "online" in text_lower and ("in-person" in text_lower or "in person" in text_lower):
            event_format = "hybrid"
        elif "online" in text_lower or "zoom" in text_lower:
            event_format = "online"
        else:
            event_format = "in-person"

        for tag in content_area.find_all(["script", "style", "nav"]):
            tag.decompose()

    body_html = str(content_area) if content_area else ""
    body_md = md(body_html, heading_style="ATX", strip=["img"]).strip()
    body_md = re.sub(r'\n{3,}', '\n\n', body_md)

    slug = urlparse(url).path.rstrip("/").split("/")[-1]

    return {
        "slug": slug,
        "title": title,
        "event_date": event_date,
        "end_date": end_date,
        "centers": [center] if center else [],
        "event_type": event_type,
        "teacher": teacher,
        "format": event_format,
        "body": body_md,
        "url": url,
    }

def write_event(event):
    """Write event data as Hugo Markdown."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Ensure unique slug
    slug = event["slug"]
    filepath = os.path.join(OUTPUT_DIR, f"{slug}.md")

    centers_yaml = ""
    if event["centers"]:
        centers_yaml = "centers:\n" + "\n".join(f'  - "{c}"' for c in event["centers"])

    old_path = urlparse(event["url"]).path
    aliases_yaml = f'aliases:\n  - "{old_path}"'

    frontmatter = f"""---
title: "{event['title'].replace('"', '\\"')}"
event_date: "{event['event_date']}"
end_date: "{event['end_date']}"
event_type: "{event['event_type']}"
format: "{event['format']}"
teacher: "{event['teacher']}"
{centers_yaml}
{aliases_yaml}
---
"""
    with open(filepath, "w") as f:
        f.write(frontmatter)
        f.write(event["body"])
        f.write("\n")

    return filepath

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    state = load_state()

    if not state.get("event_urls"):
        print("Discovering event URLs...")
        state["event_urls"] = discover_event_urls()
        save_state(state)
    print(f"Total event URLs: {len(state['event_urls'])}")

    remaining = [u for u in state["event_urls"] if u not in state["done"]]
    print(f"Remaining to scrape: {len(remaining)}")

    for i, url in enumerate(remaining):
        slug = urlparse(url).path.rstrip("/").split("/")[-1]
        print(f"[{i+1}/{len(remaining)}] Scraping {slug}...", end=" ", flush=True)
        try:
            event = scrape_event(url)
            write_event(event)
            state["done"].append(url)
            print(f"OK ({event['title'][:50]})")
        except Exception as e:
            state["failed"].append(url)
            print(f"FAILED: {e}")

        save_state(state)
        time.sleep(DELAY)

    print(f"\nDone! {len(state['done'])} scraped, {len(state['failed'])} failed.")

if __name__ == "__main__":
    main()
