"""
Haywire Scraper — Main Entry Point
===================================
Orchestrates all scrapers, aggregation, and cleanup.

Usage:
    python main.py              # Run all scrapers
    python main.py --dry-run    # Preview without saving
    python main.py --reddit     # Reddit only
    python main.py --rss        # RSS only
    python main.py --web        # Web scraping only
    python main.py --cleanup    # Cleanup only
"""

import argparse
import logging
import sys

from reddit_scraper import scrape_all_subreddits
from rss_scraper import scrape_all_feeds
from web_scraper import scrape_all_targets
from aggregator import aggregate
from cleanup import cleanup_old_data

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Haywire News Scraper")
    parser.add_argument("--dry-run", action="store_true", help="Preview without saving data")
    parser.add_argument("--reddit", action="store_true", help="Scrape Reddit only")
    parser.add_argument("--rss", action="store_true", help="Scrape RSS feeds only")
    parser.add_argument("--web", action="store_true", help="Scrape web targets only")
    parser.add_argument("--cleanup", action="store_true", help="Run cleanup only")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose logging")
    args = parser.parse_args()

    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Cleanup only mode
    if args.cleanup:
        logger.info("Running cleanup only...")
        cleanup_old_data()
        return

    # Determine which scrapers to run
    run_all = not (args.reddit or args.rss or args.web)

    all_articles = []

    # --- Reddit ---
    if run_all or args.reddit:
        logger.info("=" * 50)
        logger.info("PHASE 1: Scraping Reddit")
        logger.info("=" * 50)
        reddit_articles = scrape_all_subreddits()
        all_articles.extend(reddit_articles)

    # --- RSS Feeds ---
    if run_all or args.rss:
        logger.info("=" * 50)
        logger.info("PHASE 2: Parsing RSS Feeds")
        logger.info("=" * 50)
        rss_articles = scrape_all_feeds()
        all_articles.extend(rss_articles)

    # --- Web Scraping ---
    if run_all or args.web:
        logger.info("=" * 50)
        logger.info("PHASE 3: Web Scraping")
        logger.info("=" * 50)
        web_articles = scrape_all_targets()
        all_articles.extend(web_articles)

    if not all_articles:
        logger.warning("No articles collected from any source!")
        sys.exit(1)

    # --- Aggregation ---
    logger.info("=" * 50)
    logger.info("PHASE 4: Aggregation")
    logger.info("=" * 50)

    if args.dry_run:
        logger.info(f"DRY RUN: Would aggregate {len(all_articles)} articles")
        from collections import Counter
        cats = Counter(a["category"] for a in all_articles)
        for cat, count in cats.most_common():
            logger.info(f"  {cat}: {count} articles")
        return

    grouped = aggregate(all_articles)

    # --- Cleanup ---
    logger.info("=" * 50)
    logger.info("PHASE 5: Cleanup")
    logger.info("=" * 50)
    cleanup_old_data()

    # --- Summary ---
    logger.info("=" * 50)
    logger.info("DONE!")
    logger.info(f"Total articles aggregated: {sum(len(a) for a in grouped.values())}")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()
