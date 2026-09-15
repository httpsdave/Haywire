"""
Reddit Scraper for Haywire
=========================
Uses PRAW (Python Reddit API Wrapper) to fetch top posts from configured subreddits.
"""

import hashlib
import logging
from datetime import datetime, timezone
from typing import Optional

import praw
from praw.exceptions import PRAWException

from config import (
    REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET,
    REDDIT_USER_AGENT,
    SUBREDDIT_CATEGORY_MAP,
    MAX_ARTICLES_PER_SUBREDDIT,
    REDDIT_TIME_FILTER,
)

logger = logging.getLogger(__name__)


def create_reddit_client() -> Optional[praw.Reddit]:
    """Create and return a Reddit API client."""
    if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
        logger.warning("Reddit API credentials not configured. Skipping Reddit scraping.")
        return None

    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT,
        )
        # Test the connection
        reddit.read_only = True
        return reddit
    except PRAWException as e:
        logger.error(f"Failed to create Reddit client: {e}")
        return None


def generate_article_id(url: str, title: str) -> str:
    """Generate a unique article ID from URL and title."""
    raw = f"{url}:{title}"
    return hashlib.md5(raw.encode()).hexdigest()[:12]


def scrape_subreddit(reddit: praw.Reddit, subreddit_name: str, category: str, limit: int = MAX_ARTICLES_PER_SUBREDDIT) -> list[dict]:
    """Scrape top posts from a single subreddit."""
    articles = []

    try:
        subreddit = reddit.subreddit(subreddit_name)
        top_posts = subreddit.top(time_filter=REDDIT_TIME_FILTER, limit=limit)

        for post in top_posts:
            # Skip self-posts without external links (for news aggregation)
            url = post.url
            if post.is_self:
                url = f"https://www.reddit.com{post.permalink}"

            # Skip image/video-only posts for news categories
            if category not in ("memes", "entertainment", "esports"):
                if any(url.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.webm']):
                    continue

            timestamp = datetime.fromtimestamp(post.created_utc, tz=timezone.utc).isoformat()

            article = {
                "id": generate_article_id(url, post.title),
                "title": post.title,
                "url": url,
                "source": f"r/{subreddit_name}",
                "source_type": "reddit",
                "category": category,
                "timestamp": timestamp,
                "score": post.score,
                "comment_count": post.num_comments,
                "is_featured": False,
                "thumbnail": post.thumbnail if post.thumbnail.startswith("http") else None,
            }
            articles.append(article)

    except PRAWException as e:
        logger.warning(f"Failed to scrape r/{subreddit_name}: {e}")
    except Exception as e:
        logger.warning(f"Unexpected error scraping r/{subreddit_name}: {e}")

    return articles


def scrape_all_subreddits() -> list[dict]:
    """Scrape all configured subreddits and return a list of articles."""
    reddit = create_reddit_client()
    if not reddit:
        return []

    all_articles = []
    total_subs = len(SUBREDDIT_CATEGORY_MAP)

    for i, (subreddit_name, category) in enumerate(SUBREDDIT_CATEGORY_MAP.items()):
        logger.info(f"[{i+1}/{total_subs}] Scraping r/{subreddit_name} → {category}")
        articles = scrape_subreddit(reddit, subreddit_name, category)
        all_articles.extend(articles)
        logger.info(f"  Found {len(articles)} articles")

    logger.info(f"Total Reddit articles scraped: {len(all_articles)}")
    return all_articles


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    articles = scrape_all_subreddits()
    print(f"\nTotal articles: {len(articles)}")
    for a in articles[:5]:
        print(f"  [{a['category']}] {a['title'][:80]}... (score: {a['score']})")
