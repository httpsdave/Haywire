"""
Web Scraper for Haywire
=======================
Uses httpx + BeautifulSoup for sites without RSS feeds.
"""

import hashlib
import logging
from datetime import datetime, timezone

import httpx
from bs4 import BeautifulSoup

from config import WEB_SCRAPE_TARGETS

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}


def generate_article_id(url: str, title: str) -> str:
    """Generate a unique article ID."""
    raw = f"{url}:{title}"
    return hashlib.md5(raw.encode()).hexdigest()[:12]


def scrape_target(target) -> list[dict]:
    """Scrape a single web target."""
    articles = []

    try:
        logger.info(f"Scraping: {target.name} ({target.url})")

        with httpx.Client(headers=HEADERS, follow_redirects=True, timeout=15.0) as client:
            response = client.get(target.url)
            response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Find article elements using configured selectors
        if target.selector_title:
            elements = soup.select(target.selector_title)
        else:
            # Fallback: look for common article patterns
            elements = soup.select("article h2 a, article h3 a, .headline a, .story-title a")

        for el in elements[:15]:
            title = el.get_text(strip=True)
            link = el.get("href", "")

            if not title or not link:
                continue

            # Resolve relative URLs
            if link.startswith("/"):
                link = f"{target.url.rstrip('/')}{link}"

            article = {
                "id": generate_article_id(link, title),
                "title": title,
                "url": link,
                "source": target.name,
                "source_type": "scrape",
                "category": target.category,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "score": 0,
                "comment_count": 0,
                "is_featured": False,
                "thumbnail": None,
            }
            articles.append(article)

    except httpx.HTTPError as e:
        logger.warning(f"HTTP error scraping {target.name}: {e}")
    except Exception as e:
        logger.error(f"Error scraping {target.name}: {e}")

    return articles


def scrape_all_targets() -> list[dict]:
    """Scrape all configured web targets."""
    all_articles = []

    for target in WEB_SCRAPE_TARGETS:
        articles = scrape_target(target)
        all_articles.extend(articles)
        logger.info(f"  {target.name}: {len(articles)} articles")

    logger.info(f"Total web-scraped articles: {len(all_articles)}")
    return all_articles


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    articles = scrape_all_targets()
    print(f"\nTotal articles: {len(articles)}")
    for a in articles[:5]:
        print(f"  [{a['category']}] {a['source']}: {a['title'][:80]}")
