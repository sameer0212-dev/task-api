import json
import os
import sys
from datetime import datetime, timezone

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.scraper import (
    discover_book_urls, 
    extract_book_details, 
    normalize_and_validate,
    OUTPUT_DIR
)

def run_pipeline():
    start_time = datetime.now(timezone.utc)
    stats = {
        "start_time": start_time.isoformat(),
        "catalogue_pages": 0,
        "discovered_urls": 0,
        "pages_fetched": 0,
        "cache_hits": 0,
        "valid_records": 0,
        "invalid_records": 0,
        "failed_pages": 0,
        "failed_urls": []
    }

    print("Stage 0-2: Discovering URLs...")
    book_urls = discover_book_urls(stats)
    
    # Test error handling with one broken URL (Stage 5 requirement)
    test_urls = list(book_urls)
    test_urls.append("https://books.toscrape.com/catalogue/non_existent_broken_book_page.html")

    valid_books = []
    error_records = []

    print(f"Stage 3-5: Extracting and validating {len(test_urls)} pages...")
    for url in test_urls:
        try:
            raw_data = extract_book_details(url, stats)
            validated_record = normalize_and_validate(raw_data)
            
            if not any(b["product_url"] == str(validated_record.product_url) for b in valid_books):
                valid_books.append(json.loads(validated_record.model_dump_json()))
                stats["valid_records"] += 1
        except Exception as e:
            stats["failed_pages"] += 1
            stats["failed_urls"].append(url)
            error_records.append({"url": url, "error": str(e)})

    with open(os.path.join(OUTPUT_DIR, "books.json"), "w", encoding="utf-8") as f:
        json.dump(valid_books, f, indent=2)

    with open(os.path.join(OUTPUT_DIR, "errors.json"), "w", encoding="utf-8") as f:
        json.dump(error_records, f, indent=2)

    end_time = datetime.now(timezone.utc)
    stats["end_time"] = end_time.isoformat()
    stats["duration_seconds"] = round((end_time - start_time).total_seconds(), 2)

    with open(os.path.join(OUTPUT_DIR, "run-report.json"), "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)

    print("\n--- Pipeline Execution Summary ---")
    print(f"Discovered Unique URLs : {stats['discovered_urls']}")
    print(f"Valid Records Stored   : {stats['valid_records']}")
    print(f"Failed Pages Handled   : {stats['failed_pages']}")
    print(f"Cache Hits             : {stats['cache_hits']}")
    print(f"Duration               : {stats['duration_seconds']}s")

if __name__ == "__main__":
    run_pipeline()