#!/usr/bin/env python3
"""
Export scraped data to the Astro site's data directory.

This script is called by the GitHub Actions workflow to transform
raw scraper output (data/<date>/*.json) into the format expected
by the Astro frontend (site/src/data/*.json).

Usage:
    python scripts/export_site_data.py [--data-dir DATA_DIR] [--site-dir SITE_DIR]

If --data-dir is not given, it auto-discovers the most recent date
directory under data/.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Slug mapping — the canonical source of truth for URL slugs.
# Kept here (not imported from scrapers/) so this script has zero
# internal dependencies and can run on any CI image with Python 3.9+.
SLUG_MAP = {
    "world_news": "world-news",
    "ph_news": "ph-news",
    "technology": "technology",
    "sports": "sports",
    "science": "science",
    "health": "health",
    "politics": "politics",
    "entertainment": "entertainment",
    "esports": "esports",
    "memes": "memes",
}


def find_data_dir(base: str) -> str | None:
    """Find the best data directory to export.

    Checks for today's date first (UTC), then falls back to the most
    recent date directory available.
    """
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    today_dir = os.path.join(base, today)
    if os.path.isdir(today_dir):
        return today_dir

    # Fall back to the most recent date directory
    try:
        date_dirs = sorted(
            (d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d)) and d[:2] == "20"),
            reverse=True,
        )
    except FileNotFoundError:
        return None

    if date_dirs:
        return os.path.join(base, date_dirs[0])

    return None


def normalize_article(article: dict) -> dict:
    """Normalize Python-style field names to camelCase for TypeScript."""
    out = dict(article)
    if "source_type" in out:
        out["sourceType"] = out.pop("source_type")
    if "comment_count" in out:
        out["commentCount"] = out.pop("comment_count")
    if "is_featured" in out:
        out["isFeatured"] = out.pop("is_featured")
    out.pop("_rank", None)
    return out


def export(data_dir: str, site_dir: str) -> int:
    """Read category JSON files from data_dir and write site-ready JSON to site_dir.

    Returns the number of categories exported.
    """
    os.makedirs(site_dir, exist_ok=True)

    categories = []
    for fname in sorted(os.listdir(data_dir)):
        if not fname.endswith(".json") or fname == "metadata.json":
            continue

        cat_key = fname.removesuffix(".json")
        filepath = os.path.join(data_dir, fname)

        with open(filepath, "r", encoding="utf-8") as f:
            raw = json.load(f)

        slug = raw.get("slug", SLUG_MAP.get(cat_key, cat_key))
        articles = [normalize_article(a) for a in raw.get("articles", [])]

        cat_data = {
            "name": raw.get("display_name", cat_key),
            "slug": slug,
            "articles": articles,
        }
        categories.append(cat_data)

        out_path = os.path.join(site_dir, f"{slug}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(cat_data, f, indent=2, ensure_ascii=False)

    # Write combined file
    date_str = os.path.basename(data_dir)
    combined = {
        "date": date_str,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "categories": categories,
    }
    combined_path = os.path.join(site_dir, "all_news.json")
    with open(combined_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)

    return len(categories)


def main() -> int:
    parser = argparse.ArgumentParser(description="Export scraped data to Astro site")
    parser.add_argument(
        "--data-dir",
        default=None,
        help="Path to the date directory containing category JSON files. "
        "If omitted, auto-discovers the latest under data/.",
    )
    parser.add_argument(
        "--site-dir",
        default=None,
        help="Output directory for site-ready JSON (default: site/src/data).",
    )
    args = parser.parse_args()

    # Resolve project root (two levels up from scripts/)
    project_root = Path(__file__).resolve().parent.parent

    # Resolve data directory
    if args.data_dir:
        data_dir = args.data_dir
    else:
        data_base = str(project_root / "data")
        data_dir = find_data_dir(data_base)

    if not data_dir or not os.path.isdir(data_dir):
        print(f"ERROR: No data directory found. Looked in: {data_dir or 'data/'}", file=sys.stderr)
        # List what's available for debugging
        data_base = str(project_root / "data")
        if os.path.isdir(data_base):
            contents = os.listdir(data_base)
            print(f"  Available in data/: {contents}", file=sys.stderr)
        else:
            print(f"  data/ directory does not exist at {data_base}", file=sys.stderr)
        return 1

    # Resolve site directory
    site_dir = args.site_dir or str(project_root / "site" / "src" / "data")

    print(f"Exporting data from: {data_dir}")
    print(f"Writing to: {site_dir}")

    count = export(data_dir, site_dir)

    if count == 0:
        print("WARNING: No categories exported!", file=sys.stderr)
        return 1

    print(f"Successfully exported {count} categories.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
