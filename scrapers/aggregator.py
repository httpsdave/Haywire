"""
Aggregator for Haywire
=====================
Combines articles from all sources, deduplicates, ranks, and outputs JSON per category.
"""

import hashlib
import json
import logging
import os
from collections import defaultdict
from datetime import datetime, timezone
from difflib import SequenceMatcher

from config import CATEGORIES, CATEGORY_DISPLAY_NAMES, CATEGORY_SLUGS, DATA_DIR, SITE_DATA_DIR, MAX_ARTICLES_PER_CATEGORY

logger = logging.getLogger(__name__)


def similarity(a: str, b: str) -> float:
    """Calculate string similarity ratio between two titles."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def deduplicate_articles(articles: list[dict], threshold: float = 0.75) -> list[dict]:
    """Remove duplicate articles based on URL and title similarity."""
    seen_urls = set()
    unique = []

    for article in articles:
        url = article["url"].rstrip("/")

        # Exact URL match
        if url in seen_urls:
            continue

        # Title similarity check against existing articles
        is_dupe = False
        for existing in unique:
            if existing["category"] == article["category"]:
                if similarity(existing["title"], article["title"]) > threshold:
                    # Keep the one with higher score
                    if article.get("score", 0) > existing.get("score", 0):
                        unique.remove(existing)
                        seen_urls.discard(existing["url"].rstrip("/"))
                        break
                    else:
                        is_dupe = True
                        break

        if not is_dupe:
            seen_urls.add(url)
            unique.append(article)

    return unique


def rank_articles(articles: list[dict]) -> list[dict]:
    """Rank articles by a composite score (Reddit score + recency)."""
    now = datetime.now(timezone.utc)

    for article in articles:
        # Parse timestamp
        try:
            ts = datetime.fromisoformat(article["timestamp"])
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
            hours_ago = (now - ts).total_seconds() / 3600
        except (ValueError, KeyError):
            hours_ago = 24

        # Composite ranking: score * recency_decay
        reddit_score = article.get("score", 0)
        recency_multiplier = max(0.1, 1.0 - (hours_ago / 48))  # Decay over 48 hours

        if article["source_type"] == "reddit":
            article["_rank"] = reddit_score * recency_multiplier
        else:
            # RSS/scraped articles get a base score boosted by recency
            article["_rank"] = 100 * recency_multiplier

    articles.sort(key=lambda a: a.get("_rank", 0), reverse=True)

    # Mark the top article in each category as featured
    featured_categories = set()
    for article in articles:
        cat = article["category"]
        if cat not in featured_categories:
            article["is_featured"] = True
            featured_categories.add(cat)

    return articles


def group_by_category(articles: list[dict]) -> dict[str, list[dict]]:
    """Group articles by category."""
    grouped = defaultdict(list)
    for article in articles:
        cat = article["category"]
        if cat in CATEGORIES:
            grouped[cat].append(article)
    return dict(grouped)


def save_json(data: dict, date_str: str) -> str:
    """Save category JSON files to the data directory."""
    date_dir = os.path.join(DATA_DIR, date_str)
    os.makedirs(date_dir, exist_ok=True)

    for category, articles in data.items():
        # Limit articles per category
        limited = articles[:MAX_ARTICLES_PER_CATEGORY]

        # Remove internal ranking field
        for a in limited:
            a.pop("_rank", None)

        filepath = os.path.join(date_dir, f"{category}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump({
                "category": category,
                "display_name": CATEGORY_DISPLAY_NAMES.get(category, category),
                "slug": CATEGORY_SLUGS.get(category, category),
                "articles": limited,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }, f, indent=2, ensure_ascii=False)

        logger.info(f"  Saved {len(limited)} articles to {filepath}")

    # Save metadata
    metadata = {
        "build_date": date_str,
        "build_timestamp": datetime.now(timezone.utc).isoformat(),
        "categories": {cat: len(articles) for cat, articles in data.items()},
        "total_articles": sum(len(a) for a in data.values()),
    }
    meta_path = os.path.join(date_dir, "metadata.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    logger.info(f"Metadata saved to {meta_path}")
    return date_dir


def aggregate(all_articles: list[dict]) -> dict[str, list[dict]]:
    """Full aggregation pipeline: deduplicate → rank → group → save."""
    logger.info(f"Starting aggregation with {len(all_articles)} total articles")

    # Step 1: Deduplicate
    unique = deduplicate_articles(all_articles)
    logger.info(f"After deduplication: {len(unique)} articles")

    # Step 2: Rank
    ranked = rank_articles(unique)

    # Step 3: Group by category
    grouped = group_by_category(ranked)
    for cat, articles in grouped.items():
        logger.info(f"  {CATEGORY_DISPLAY_NAMES.get(cat, cat)}: {len(articles)} articles")

    # Step 4: Save to JSON (data/ directory for archival)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    save_json(grouped, today)

    # Step 5: Save to site/src/data/ for Astro build
    save_site_data(grouped, today)

    return grouped


def save_site_data(data: dict, date_str: str):
    """Save category JSON files to the Astro site's data directory for build-time consumption."""
    os.makedirs(SITE_DATA_DIR, exist_ok=True)

    all_categories = []

    for category, articles in data.items():
        limited = articles[:MAX_ARTICLES_PER_CATEGORY]

        # Clean up internal fields
        clean_articles = []
        for a in limited:
            clean = {k: v for k, v in a.items() if not k.startswith("_")}
            # Normalize source_type to sourceType for TypeScript
            if "source_type" in clean:
                clean["sourceType"] = clean.pop("source_type")
            if "comment_count" in clean:
                clean["commentCount"] = clean.pop("comment_count")
            if "is_featured" in clean:
                clean["isFeatured"] = clean.pop("is_featured")
            clean_articles.append(clean)

        cat_data = {
            "name": CATEGORY_DISPLAY_NAMES.get(category, category),
            "slug": CATEGORY_SLUGS.get(category, category),
            "articles": clean_articles,
        }
        all_categories.append(cat_data)

        # Also save individual category files
        filepath = os.path.join(SITE_DATA_DIR, f"{CATEGORY_SLUGS.get(category, category)}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(cat_data, f, indent=2, ensure_ascii=False)

    # Save combined file
    combined = {
        "date": date_str,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "categories": all_categories,
    }
    combined_path = os.path.join(SITE_DATA_DIR, "all_news.json")
    with open(combined_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)

    logger.info(f"Site data saved to {SITE_DATA_DIR} ({len(all_categories)} categories)")

