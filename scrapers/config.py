"""
Haywire Scraper Configuration
============================
Central configuration for all news sources: Reddit subreddits, RSS feeds, and web scraping targets.
"""

import os
from dataclasses import dataclass, field

# --- Reddit API Credentials (from environment or GitHub Secrets) ---
REDDIT_CLIENT_ID = os.environ.get("REDDIT_CLIENT_ID", "")
REDDIT_CLIENT_SECRET = os.environ.get("REDDIT_CLIENT_SECRET", "")
REDDIT_USER_AGENT = os.environ.get("REDDIT_USER_AGENT", "Haywire News Aggregator v1.0")

# --- Paths ---
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
SITE_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site", "src", "data")

# --- Scraping Parameters ---
MAX_ARTICLES_PER_CATEGORY = 20
MAX_ARTICLES_PER_SUBREDDIT = 10
REDDIT_TIME_FILTER = "day"       # "hour", "day", "week"
RSS_MAX_AGE_HOURS = 24
DATA_RETENTION_DAYS = 7

# --- Categories ---
CATEGORIES = [
    "world_news",
    "ph_news",
    "technology",
    "sports",
    "science",
    "health",
    "politics",
    "entertainment",
    "esports",
    "memes",
]

CATEGORY_DISPLAY_NAMES = {
    "world_news": "World News",
    "ph_news": "Philippine News",
    "technology": "Technology",
    "sports": "Sports",
    "science": "Science",
    "health": "Health",
    "politics": "Politics",
    "entertainment": "Entertainment",
    "esports": "E-Sports",
    "memes": "Memes",
}

CATEGORY_SLUGS = {
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


# ==============================================================
# REDDIT SUBREDDIT → CATEGORY MAPPING
# ==============================================================

# --- World News ---
WORLD_NEWS_SUBREDDITS = [
    "worldnews",
    "NeutralNews",
    "NeutralPolitics",
    "geopolitics",
    "IndepthStories",
    "news",
    "inthenews",
]

# --- Philippine News (General) ---
PH_NEWS_SUBREDDITS = [
    "Philippines",
    "newsph",
    "philippinesnews",
    "inquirerdotnet",
    "philippinefreepress",
    "kakaibalita",
    "pilipinas",
    "filipinohistory",
    "philippinehistory",
    "coronavirus_ph",
]

# --- Technology ---
TECHNOLOGY_SUBREDDITS = [
    "technology",
    "tech_philippines",
    "pinoyprogrammer",
    "phbuildapc",
    "pinoytechsaga",
    "internetph",
    "convergeict",
    "convergeph",
    "globetelecom",
]

# --- Sports ---
SPORTS_SUBREDDITS = [
    "sports",
    "fitnessph",
    "pba",
    "gilasbasketball",
    "azkals",
    "philippinebasketball",
    "philippinevolleyball",
    "phitness",
    "phwomensvolleyball",
    "phfitnessandhealth",
    "uaapvolleyball",
    "sabong",
]

# --- Science ---
SCIENCE_SUBREDDITS = [
    "science",
    "EverythingScience",
    "sciencenews",
]

# --- Health ---
HEALTH_SUBREDDITS = [
    "health",
    "HealthNews",
    "coronavirus_ph",
    "PCOSPhilippines",
    "phfitnessandhealth",
]

# --- Politics ---
POLITICS_SUBREDDITS = [
    "politics",
    "ph_politics",
    "philippinepolitics",
    "phgov",
    "batasnatin",
    "EpalPH",
    "angatbuhay",
    "angatbuhayph",
    "laborlawph",
    "lawph",
    "lawyersph",
    "PhilippineMilitary",
]

# --- Entertainment ---
ENTERTAINMENT_SUBREDDITS = [
    "entertainment",
    "pinoycinema",
    "pelikula",
    "opm",
    "eraserheads",
    "animeph",
    "AniweebPH",
    "filmclubph",
    "movieclubph",
    "sb19",
    "fliptop",
    "indiemusicph",
    "ppopcommunity",
    "dragraceph",
]

# --- E-Sports ---
ESPORTS_SUBREDDITS = [
    "esports",
    "phgamers",
    "phgaming",
    "valorantph",
    "mobilelegendspinas",
    "lolph",
    "wildriftph",
    "csgoph",
    "PHGamerPals",
    "playstationph",
    "nintendoph",
    "xboxphilippines",
    "pokemongoph",
    "ragnarokonlineph",
]

# --- Memes ---
MEMES_SUBREDDITS = [
    "2philippines4u",
    "pinoymemes",
    "filipinomeme",
    "nanikposting",
    "naniksubmission",
    "insanepinoyfacebook",
    "philippinememes",
    "darkmemesph",
    "delawan",
    "filipuns",
    "jokesph",
    "leopardsatemyfaceph",
    "linkedinlunaticsph",
    "moosegearposting",
    "okmamsertanga",
    "pinoyjokes",
    "tatayjokes",
    "suntukanph",
    "phcirclejerk",
    "mabuhayangkorporeyt",
    "akolangba",
    "uniteambasura",
]

# Unified mapping
SUBREDDIT_CATEGORY_MAP = {}
for sub in WORLD_NEWS_SUBREDDITS:
    SUBREDDIT_CATEGORY_MAP[sub] = "world_news"
for sub in PH_NEWS_SUBREDDITS:
    SUBREDDIT_CATEGORY_MAP[sub] = "ph_news"
for sub in TECHNOLOGY_SUBREDDITS:
    SUBREDDIT_CATEGORY_MAP[sub] = "technology"
for sub in SPORTS_SUBREDDITS:
    SUBREDDIT_CATEGORY_MAP[sub] = "sports"
for sub in SCIENCE_SUBREDDITS:
    SUBREDDIT_CATEGORY_MAP[sub] = "science"
for sub in HEALTH_SUBREDDITS:
    SUBREDDIT_CATEGORY_MAP[sub] = "health"
for sub in POLITICS_SUBREDDITS:
    SUBREDDIT_CATEGORY_MAP[sub] = "politics"
for sub in ENTERTAINMENT_SUBREDDITS:
    SUBREDDIT_CATEGORY_MAP[sub] = "entertainment"
for sub in ESPORTS_SUBREDDITS:
    SUBREDDIT_CATEGORY_MAP[sub] = "esports"
for sub in MEMES_SUBREDDITS:
    SUBREDDIT_CATEGORY_MAP[sub] = "memes"


# ==============================================================
# RSS FEEDS
# ==============================================================

@dataclass
class RSSFeed:
    name: str
    url: str
    category: str
    logo: str = ""

# Philippine News RSS Feeds
PH_RSS_FEEDS = [
    RSSFeed("Inquirer.net", "https://newsinfo.inquirer.net/feed", "ph_news"),
    RSSFeed("Manila Bulletin", "https://mb.com.ph/feed", "ph_news"),
    RSSFeed("Manila Times", "https://www.manilatimes.net/feed", "ph_news"),
    RSSFeed("ABS-CBN News", "https://news.abs-cbn.com/rss", "ph_news"),
    RSSFeed("GMA News", "https://data.gmanetwork.com/gno/rss/news/feed.xml", "ph_news"),
    RSSFeed("Rappler", "https://www.rappler.com/feed", "ph_news"),
    RSSFeed("PhilStar", "https://www.philstar.com/rss/headlines", "ph_news"),
    RSSFeed("PNA", "https://www.pna.gov.ph/feed", "ph_news"),
    RSSFeed("SunStar", "https://www.sunstar.com.ph/feeds", "ph_news"),
]

# World News RSS Feeds
WORLD_RSS_FEEDS = [
    RSSFeed("Reuters", "https://www.rss.reuters.com/news/topNews", "world_news"),
    RSSFeed("AP News", "https://apnews.com/feed", "world_news"),
    RSSFeed("BBC World", "https://feeds.bbci.co.uk/news/world/rss.xml", "world_news"),
    RSSFeed("Al Jazeera", "https://www.aljazeera.com/xml/rss/all.xml", "world_news"),
    RSSFeed("The Guardian", "https://www.theguardian.com/world/rss", "world_news"),
]

# Technology RSS Feeds
TECH_RSS_FEEDS = [
    RSSFeed("Ars Technica", "https://feeds.arstechnica.com/arstechnica/index", "technology"),
    RSSFeed("The Verge", "https://www.theverge.com/rss/index.xml", "technology"),
    RSSFeed("TechCrunch", "https://techcrunch.com/feed", "technology"),
]

# Science RSS Feeds
SCIENCE_RSS_FEEDS = [
    RSSFeed("Nature", "https://www.nature.com/nature.rss", "science"),
    RSSFeed("Science Daily", "https://www.sciencedaily.com/rss/all.xml", "science"),
]

# Health RSS Feeds
HEALTH_RSS_FEEDS = [
    RSSFeed("WHO News", "https://www.who.int/rss-feeds/news-english.xml", "health"),
]

ALL_RSS_FEEDS = PH_RSS_FEEDS + WORLD_RSS_FEEDS + TECH_RSS_FEEDS + SCIENCE_RSS_FEEDS + HEALTH_RSS_FEEDS


# ==============================================================
# WEB SCRAPING TARGETS
# ==============================================================

@dataclass
class ScrapeTarget:
    name: str
    url: str
    category: str
    selector_title: str = ""
    selector_link: str = ""
    selector_date: str = ""

WEB_SCRAPE_TARGETS = [
    ScrapeTarget(
        name="CNN Philippines",
        url="https://www.cnnphilippines.com",
        category="ph_news",
        selector_title="h3.story-title a",
        selector_link="h3.story-title a",
        selector_date="span.story-date",
    ),
]
