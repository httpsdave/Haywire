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

            # Extract thumbnail from media tags
            thumbnail = _extract_thumbnail(entry)

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
                "thumbnail": thumbnail,
            }
            articles.append(article)

    except Exception as e:
        logger.error(f"Error parsing feed {feed_config.name}: {e}")

    return articles


def _extract_thumbnail(entry) -> str | None:
    """Extract thumbnail URL from RSS entry media tags."""
    # Try media_content (e.g., <media:content url="..."/>)
    media_content = entry.get("media_content", [])
    if media_content:
        for media in media_content:
            url = media.get("url", "")
            media_type = media.get("type", "")
            if url and ("image" in media_type or media_type == "" or url.endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif'))):
                return url

    # Try media_thumbnail (e.g., <media:thumbnail url="..."/>)
    media_thumbnails = entry.get("media_thumbnail", [])
    if media_thumbnails:
        for thumb in media_thumbnails:
            url = thumb.get("url", "")
            if url:
                return url

    # Try enclosure (e.g., <enclosure url="..." type="image/jpeg"/>)
    enclosures = entry.get("enclosures", [])
    if enclosures:
        for enc in enclosures:
            url = enc.get("href", "") or enc.get("url", "")
            enc_type = enc.get("type", "")
            if url and "image" in enc_type:
                return url

    # Try content for inline images
    content = entry.get("content", [])
    if content:
        html = content[0].get("value", "")
        if html:
            import re
            img_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', html)
            if img_match:
                return img_match.group(1)

    # Try summary/description for inline images
    summary = entry.get("summary", "")
    if summary:
        import re
        img_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', summary)
        if img_match:
            return img_match.group(1)

    return None


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
