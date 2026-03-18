#!/usr/bin/env python3
"""Scrape regular pages from sfzc.org and output Hugo-compatible Markdown."""

import os
import re
import time
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from markdownify import markdownify as md

BASE_URL = "https://www.sfzc.org"
SITE_DIR = os.path.join(os.path.dirname(__file__), "..", "site", "content")
STATE_FILE = os.path.join(os.path.dirname(__file__), ".page_state.json")
DELAY = 1.5

HEADERS = {
    "User-Agent": "SFZC-Hugo-Scraper/1.0 (site migration prototype)"
}

# Map of old URLs to new Hugo paths (section/filename)
# Based on the architecture document
PAGE_MAP = {
    # About section
    "/about-san-francisco-zen-center": ("about", "_index", []),
    "/about/mission-and-vision": ("about", "mission-and-vision", []),
    "/about/San-Francisco-Zen-Center-Lineage": ("about", "lineage", ["/about/San-Francisco-Zen-Center-Lineage"]),
    "/about/affiliations": ("about", "affiliations", []),
    "/about/non-profit-status": ("about", "non-profit-status", []),
    "/about/contact": ("about", "contact", []),
    "/about/how-san-francisco-zen-center-operates": ("about", "how-we-operate", ["/about/how-san-francisco-zen-center-operates"]),
    "/about/how-san-francisco-zen-center-operates/board-directors": ("about", "board-of-directors", ["/about/how-san-francisco-zen-center-operates/board-directors"]),
    "/about/how-san-francisco-zen-center-operates/diversity-equity-inclusion-and-accessibility-deia": ("about", "deia", ["/about/how-san-francisco-zen-center-operates/diversity-equity-inclusion-and-accessibility-deia"]),
    "/about/how-san-francisco-zen-center-operates/conflict-complaint-and-ethical-review-processes": ("about", "ethics-and-complaints", ["/about/how-san-francisco-zen-center-operates/conflict-complaint-and-ethical-review-processes"]),
    "/about/community": ("about", "community", []),

    # Practice Centers
    "/practice-centers": ("practice-centers", "_index", []),
    "/practice-centers/city-center": ("practice-centers/city-center", "_index", ["/locations/city-center"]),
    "/practice-centers/city-center/about-city-center": ("practice-centers/city-center", "about", []),
    "/practice-centers/city-center/zen-meditation-practice-city-center/beginners": ("practice-centers/city-center", "beginners", ["/practice-centers/city-center/zen-meditation-practice-city-center/beginners"]),
    "/practice-centers/city-center/zen-meditation-practice-city-center/daily-schedule-city-center": ("practice-centers/city-center", "schedule", ["/practice-centers/city-center/zen-meditation-practice-city-center/daily-schedule-city-center"]),
    "/practice-centers/city-center/zen-meditation-practice-city-center/classes-courses-city-center": ("practice-centers/city-center", "classes", ["/practice-centers/city-center/zen-meditation-practice-city-center/classes-courses-city-center"]),
    "/practice-centers/city-center/zen-meditation-practice-city-center/sitting-meditation-sesshins-at-city-center": ("practice-centers/city-center", "sesshins", ["/practice-centers/city-center/zen-meditation-practice-city-center/sitting-meditation-sesshins-at-city-center"]),
    "/practice-centers/city-center/zen-meditation-practice-city-center/practice-periods-intensives-city": ("practice-centers/city-center", "practice-periods", ["/practice-centers/city-center/zen-meditation-practice-city-center/practice-periods-intensives-city"]),
    "/practice-centers/city-center/conference-center-city-center": ("practice-centers/city-center", "conference-center", []),
    "/practice-centers/city-center/getting-city-center": ("practice-centers/city-center", "directions", ["/practice-centers/city-center/getting-city-center"]),
    "/practice-centers/city-center/contact-city-center": ("practice-centers/city-center", "contact", ["/practice-centers/city-center/contact-city-center"]),

    "/practice-centers/green-gulch-farm": ("practice-centers/green-gulch", "_index", ["/locations/green-gulch-farm", "/practice-centers/green-gulch-farm"]),
    "/practice-centers/green-gulch-farm/about-green-gulch": ("practice-centers/green-gulch", "about", []),
    "/practice-centers/green-gulch-farm/zen-meditation-practice-green-gulch/beginners-green-gulch": ("practice-centers/green-gulch", "beginners", ["/practice-centers/green-gulch-farm/zen-meditation-practice-green-gulch/beginners-green-gulch"]),
    "/practice-centers/green-gulch-farm/zen-meditation-practice-green-gulch/daily-schedule-green-gulch": ("practice-centers/green-gulch", "schedule", ["/practice-centers/green-gulch-farm/zen-meditation-practice-green-gulch/daily-schedule-green-gulch"]),
    "/practice-centers/green-gulch-farm/zen-meditation-practice-green-gulch/sunday-program": ("practice-centers/green-gulch", "sunday-program", []),
    "/practice-centers/green-gulch-farm/zen-meditation-practice-green-gulch/classes-courses-green-gulch": ("practice-centers/green-gulch", "classes", ["/practice-centers/green-gulch-farm/zen-meditation-practice-green-gulch/classes-courses-green-gulch"]),
    "/practice-centers/green-gulch-farm/zen-meditation-practice-green-gulch/sitting-meditation-sesshins": ("practice-centers/green-gulch", "sesshins", ["/practice-centers/green-gulch-farm/zen-meditation-practice-green-gulch/sitting-meditation-sesshins"]),
    "/practice-centers/green-gulch-farm/zen-meditation-practice-green-gulch/practice-periods-green-gulch": ("practice-centers/green-gulch", "practice-periods", []),
    "/practice-centers/green-gulch-farm/about-green-gulch/farm-garden-programs": ("practice-centers/green-gulch", "farm-garden", []),
    "/practice-centers/green-gulch-farm/about-green-gulch/farm-garden/green-gulch-farmers-market": ("practice-centers/green-gulch", "farmers-market", []),
    "/practice-centers/green-gulch-farm/zen-meditation-practice-green-gulch/way-tea": ("practice-centers/green-gulch", "way-of-tea", []),
    "/practice-centers/green-gulch-farm/about-green-gulch/volunteer-program": ("practice-centers/green-gulch", "volunteer", []),
    "/practice-centers/green-gulch-farm/conference-center-green-gulch-facilities-rates-policies": ("practice-centers/green-gulch", "conference-center", []),
    "/practice-centers/green-gulch-farm/getting-green-gulch-farm": ("practice-centers/green-gulch", "directions", ["/practice-centers/green-gulch-farm/getting-green-gulch-farm"]),
    "/practice-centers/green-gulch-farm/contact-green-gulch": ("practice-centers/green-gulch", "contact", []),

    "/practice-centers/tassajara": ("practice-centers/tassajara", "_index", ["/locations/tassajara"]),
    "/practice-centers/tassajara/about-tassajara": ("practice-centers/tassajara", "about", []),
    "/practice-centers/tassajara/about-tassajara/hot-springs": ("practice-centers/tassajara", "hot-springs", []),
    "/practice-centers/tassajara/about-tassajara/zen-monastery": ("practice-centers/tassajara", "zen-monastery", []),
    "/practice-centers/tassajara/zen-practice-programs": ("practice-centers/tassajara", "practice-programs", []),
    "/practice-centers/tassajara/contact-tassajara": ("practice-centers/tassajara", "contact", ["/practice-centers/tassajara/contact-tassajara"]),
    "/guest-season-reservations": ("practice-centers/tassajara", "guest-season", ["/guest-season-reservations"]),
    "/practice-centers/tassajara/guest-season-reservations/what-to-expect-and-how-to-prepare": ("practice-centers/tassajara", "what-to-expect", []),
    "/tassajara-summer-practice": ("practice-centers/tassajara", "summer-practice", ["/tassajara-summer-practice"]),

    "/online-page": ("practice-centers/online", "_index", ["/online-page"]),
    "/online-programs/online-zendo": ("practice-centers/online", "zendo", ["/online-programs/online-zendo"]),

    # Practice section
    "/entering-practice": ("practice", "new-to-zen", ["/entering-practice", "/offerings/entering-practice"]),
    "/offerings/establishing-practice/finding-teacher": ("practice", "finding-a-teacher", ["/offerings/establishing-practice/finding-teacher"]),
    "/live-temple-life": ("practice", "residential", ["/live-temple-life"]),
    "/offerings/deepening-practice/sewing-buddhas-robe": ("practice", "sewing-buddhas-robe", ["/offerings/deepening-practice/sewing-buddhas-robe"]),
    "/services-sutras-texts-songs": ("practice", "chants-and-texts", ["/services-sutras-texts-songs"]),
    "/sfzc-family-sangha": ("practice", "family-sangha", ["/sfzc-family-sangha"]),
    "/visa-information-international-visitors": ("practice", "visa-information", ["/visa-information-international-visitors"]),

    # Giving
    "/ways-to-support-sfzc": ("giving", "_index", ["/ways-to-support-sfzc"]),
    "/leave-legacy": ("giving", "legacy", ["/leave-legacy"]),
    "/giving/outreach-volunteering": ("giving", "volunteer", ["/support/outreach-volunteering"]),

    # Other
    "/offerings/livestream-media": ("dharma-talks", "livestream", ["/offerings/livestream-media", "/upcoming-livestream-events"]),
    "/sr-archive": ("dharma-talks", "suzuki-roshi", ["/sr-archive"]),
    "/rooms-rentals": (".", "rooms-rentals", ["/rooms-rentals"]),
    "/newsletter-signup": (".", "newsletter-signup", ["/newsletter-signup"]),
    "/website-privacy-policy": (".", "privacy-policy", ["/website-privacy-policy"]),
}

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"done": [], "failed": []}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def scrape_page(url_path):
    """Scrape a single page."""
    url = f"{BASE_URL}{url_path}"
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    title_el = soup.find("h1") or soup.find("title")
    title = title_el.get_text(strip=True) if title_el else ""
    title = title.replace(" | San Francisco Zen Center", "").strip()

    content_area = soup.find("article") or soup.find("div", class_="field-item") or soup.find("main")
    if not content_area:
        content_area = soup.find("div", class_="content")

    if content_area:
        for tag in content_area.find_all(["script", "style", "nav"]):
            tag.decompose()
        body_html = str(content_area)
    else:
        body_html = ""

    body_md = md(body_html, heading_style="ATX", strip=["img"]).strip()
    body_md = re.sub(r'\n{3,}', '\n\n', body_md)

    return title, body_md

def write_page(section, filename, title, body, aliases):
    """Write a page as Hugo Markdown."""
    if section == ".":
        out_dir = SITE_DIR
    else:
        out_dir = os.path.join(SITE_DIR, section)
    os.makedirs(out_dir, exist_ok=True)

    filepath = os.path.join(out_dir, f"{filename}.md")

    aliases_yaml = ""
    if aliases:
        aliases_yaml = "aliases:\n" + "\n".join(f'  - "{a}"' for a in aliases)

    frontmatter = f"""---
title: "{title.replace('"', '\\"')}"
{aliases_yaml}
---
"""
    with open(filepath, "w") as f:
        f.write(frontmatter)
        f.write(body)
        f.write("\n")

    return filepath

def main():
    state = load_state()

    remaining = {k: v for k, v in PAGE_MAP.items() if k not in state["done"]}
    print(f"Pages to scrape: {len(remaining)} (of {len(PAGE_MAP)} total)")

    for i, (url_path, (section, filename, aliases)) in enumerate(remaining.items()):
        print(f"[{i+1}/{len(remaining)}] {url_path} -> {section}/{filename}...", end=" ", flush=True)
        try:
            title, body = scrape_page(url_path)
            write_page(section, filename, title, body, aliases)
            state["done"].append(url_path)
            print(f"OK ({title[:40]})")
        except Exception as e:
            state["failed"].append(url_path)
            print(f"FAILED: {e}")

        save_state(state)
        time.sleep(DELAY)

    print(f"\nDone! {len(state['done'])} scraped, {len(state['failed'])} failed.")

if __name__ == "__main__":
    main()
