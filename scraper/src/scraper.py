import os
import re
import time
import hashlib
from datetime import datetime, timezone
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

from src.schema import ValidatedBookRecord

USER_AGENT = "FlyRankInternship-A9/1.0 (+https://github.com/SameerSamsoon/internship)"
BASE_URL = "https://books.toscrape.com/"
CATALOGUE_START = "https://books.toscrape.com/catalogue/page-1.html"
TIMEOUT = 10.0
DELAY = 0.5  # 500ms politeness delay

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(BASE_DIR, "cache")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_with_cache(url: str, stats: dict) -> tuple[str, bool]:
    url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
    cache_path = os.path.join(CACHE_DIR, f"{url_hash}.html")

    if os.path.exists(cache_path):
        stats["cache_hits"] += 1
        with open(cache_path, "r", encoding="utf-8") as f:
            return f.read(), True

    time.sleep(DELAY)
    headers = {"User-Agent": USER_AGENT}
    
    response = requests.get(url, headers=headers, timeout=TIMEOUT)
    stats["pages_fetched"] += 1
    
    if response.status_code != 200:
        raise Exception(f"HTTP Error {response.status_code} on {url}")

    html_content = response.text
    with open(cache_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return html_content, False

def discover_book_urls(stats: dict) -> list[str]:
    current_page_url = CATALOGUE_START
    book_urls = []
    pages_crawled = 0

    while current_page_url and pages_crawled < 3:
        html, _ = fetch_with_cache(current_page_url, stats)
        soup = BeautifulSoup(html, "html.parser")
        
        for h3 in soup.select("ol.row li article.product_pod h3 a"):
            relative_href = h3.get("href")
            if "catalogue/" in current_page_url and not relative_href.startswith("catalogue/"):
                full_url = urljoin(current_page_url, relative_href)
            else:
                full_url = urljoin(BASE_URL, relative_href if relative_href.startswith("catalogue/") else f"catalogue/{relative_href}")
            
            if full_url not in book_urls:
                book_urls.append(full_url)

        next_button = soup.select_one("li.next a")
        if next_button:
            next_href = next_button.get("href")
            current_page_url = urljoin(current_page_url, next_href)
        else:
            current_page_url = None

        pages_crawled += 1

    stats["catalogue_pages"] = pages_crawled
    stats["discovered_urls"] = len(book_urls)
    return book_urls

def extract_book_details(url: str, stats: dict) -> dict:
    html, _ = fetch_with_cache(url, stats)
    soup = BeautifulSoup(html, "html.parser")

    main_content = soup.select_one("article.product_page")
    if not main_content:
        raise Exception("Product page article element not found")

    title = main_content.select_one("h1").get_text(strip=True)
    price_text = main_content.select_one("p.price_color").get_text(strip=True)
    availability_text = main_content.select_one("p.instock.availability").get_text(strip=True)
    
    rating_el = main_content.select_one("p.star-rating")
    rating_classes = rating_el.get("class", []) if rating_el else []
    rating_text = next((cls for cls in rating_classes if cls != "star-rating"), "Unknown")

    desc_header = main_content.find("div", id="product_description")
    description = desc_header.find_next_sibling("p").get_text(strip=True) if desc_header else None

    return {
        "title": title,
        "product_url": url,
        "price_text": price_text,
        "availability_text": availability_text,
        "rating_text": rating_text,
        "description": description,
        "source_page": url,
        "fetched_at": datetime.now(timezone.utc).isoformat()
    }

def normalize_and_validate(raw_record: dict) -> ValidatedBookRecord:
    price_match = re.search(r"[\d\.]+", raw_record["price_text"])
    price_gbp = float(price_match.group(0)) if price_match else 0.0

    return ValidatedBookRecord(
        title=raw_record["title"],
        product_url=raw_record["product_url"],
        price_gbp=price_gbp,
        price_text=raw_record["price_text"],
        availability_text=raw_record["availability_text"],
        rating_text=raw_record["rating_text"],
        description=raw_record["description"],
        source_page=raw_record["source_page"],
        fetched_at=datetime.fromisoformat(raw_record["fetched_at"])
    )