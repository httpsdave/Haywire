"""
RSS Feed Scraper for Haywire
============================
Parses RSS feeds from Philippine and World news outlets.
"""

import hashlib
import logging
from datetime import datetime, timezone, timedelta

import feedparser
from dateutil import parser as dateutil_parser

from config import ALL_RSS_FEEDS, RSS_MAX_AGE_HOURS

logger = logging.getLogger(__name__)


def generate_article_id(url: str, title: str) -> str:
    """Generate a unique article ID."""
    raw = f"{url}:{title}"
    return hashlib.md5(raw.encode()).hexdigest()[:12]


def parse_feed(feed_config) -> list[dict]:
    """Parse a single RSS feed and return normalized articles."""
    articles = []

    try:
        logger.info(f"Parsing RSS feed: {feed_config.name} ({feed_config.url})")
        feed = feedparser.parse(feed_config.url)

        if feed.bozo and not feed.entries:
            logger.warning(f"Failed to parse feed {feed_config.name}: {feed.bozo_exception}")
            return []

        cutoff = datetime.now(timezone.utc) - timedelta(hours=RSS_MAX_AGE_HOURS)

        for entry in feed.entries:
            title = entry.get("title", "").strip()
            link = entry.get("link", "").strip()

            if not title or not link:
                continue

            # Parse publication date
            timestamp = None
            for date_field in ["published", "updated", "created"]:
                date_str = entry.get(date_field)
                if date_str:
                    try:
                        timestamp = dateutil_parser.parse(date_str)
                        if timestamp.tzinfo is None:
                            timestamp = timestamp.replace(tzinfo=timezone.utc)
                        break
                    except (ValueError, TypeError):
                        continue

            if not timestamp:
                timestamp = datetime.now(timezone.utc)

            # Skip articles older than cutoff
            if timestamp < cutoff:
                continue

            article = {
                "id": generate_article_id(link, title),
                "title": title,
                "url": link,
                "source": feed_config.name,
                "source_type": "rss",
                "category": feed_config.category,
                "timestamp": timestamp.isoformat(),
                "score": 0,
                "comment_count": 0,
                "is_featured": False,
                "thumbnail": None,
            }
            articles.append(article)

    except Exception as e:
        logger.error(f"Error parsing feed {feed_config.name}: {e}")

    return articles


def scrape_all_feeds() -> list[dict]:
    """Parse all configured RSS feeds and return a list of articles."""
    all_articles = []

    for feed_config in ALL_RSS_FEEDS:
        articles = parse_feed(feed_config)
        all_articles.extend(articles)
        logger.info(f"  {feed_config.name}: {len(articles)} articles")

    logger.info(f"Total RSS articles scraped: {len(all_articles)}")
    return all_articles


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    articles = scrape_all_feeds()
    print(f"\nTotal articles: {len(articles)}")
    for a in articles[:5]:
        print(f"  [{a['category']}] {a['source']}: {a['title'][:80]}")
