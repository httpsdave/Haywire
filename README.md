# 📰 Haywire

> *"All the News We Could Scrape"*

**Haywire** is a crowdsourced news aggregation website styled like a classic newspaper. It collects trending stories from Reddit communities, Philippine media outlets, and world news sources — rebuilt automatically every 2 hours via GitHub Actions.

## 🌐 Live Site

Coming soon — deployed on GitHub Pages.

## ✨ Features

- **Newspaper-Style Layout** — Classic broadsheet design with blackletter masthead, columned articles, and section headers
- **Crowdsourced News** — Aggregates from 200+ Reddit communities + RSS feeds from major news outlets
- **Categories** — World News, Philippine News, Technology, Sports, Science, Health, Politics, Entertainment, E-Sports, Memes
- **Date Archive** — Access today's paper or browse up to 7 days back
- **Auto-Updated** — GitHub Actions rebuilds the site every 2 hours with fresh content
- **PWA** — Installable on mobile devices with offline reading support
- **Responsive** — Optimized for desktop, tablet, and mobile screens
- **Zero JavaScript** — Static HTML/CSS by default (Astro), with minimal JS for interactive panels

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Static Site Generator | [Astro 5.x](https://astro.build) |
| Styling | Vanilla CSS (custom properties + grid) |
| Scraping | Python 3.12+ (PRAW, httpx, BeautifulSoup4, feedparser) |
| Automation | GitHub Actions (cron schedule) |
| Deployment | GitHub Pages |
| PWA | Service Worker + Web Manifest |

## 📁 Project Structure

```
Haywire/
├── site/              # Astro frontend
│   ├── src/
│   │   ├── components/   # Reusable Astro components
│   │   ├── layouts/      # Page layouts
│   │   ├── pages/        # Route pages
│   │   ├── styles/       # Global CSS
│   │   └── utils/        # Data loading helpers
│   └── public/           # Static assets (PWA manifest, icons)
├── scrapers/          # Python news scrapers
│   ├── config.py         # Subreddit/RSS configuration
│   ├── reddit_scraper.py
│   ├── rss_scraper.py
│   ├── web_scraper.py
│   ├── aggregator.py
│   └── main.py           # Entry point
├── data/              # Generated JSON (by scrapers)
└── .github/workflows/ # CI/CD automation
```

## 🚀 Local Development

### Prerequisites

- Node.js 20+
- Python 3.12+
- Reddit API credentials ([create app here](https://www.reddit.com/prefs/apps))

### Frontend (Astro)

```bash
cd site
npm install
npm run dev
```

### Scrapers (Python)

```bash
cd scrapers
pip install -r requirements.txt

# Set environment variables
export REDDIT_CLIENT_ID=your_client_id
export REDDIT_CLIENT_SECRET=your_client_secret

python main.py
```

## 📰 News Sources

### Reddit Communities
- **World News**: r/worldnews, r/NeutralNews, r/geopolitics, r/NeutralPolitics, r/IndepthStories
- **Philippine News**: r/Philippines, r/newsph, r/philippinesnews, r/ph_politics, and 200+ more
- Plus category-specific subreddits for technology, sports, science, etc.

### Media Outlets (RSS)
- **Philippine**: Inquirer.net, Manila Bulletin, Manila Times, ABS-CBN News, GMA News, Rappler, PhilStar, PNA
- **World**: Reuters, AP News, BBC World, Al Jazeera, The Guardian

## 📄 License

Content is aggregated from external sources and remains the property of their respective owners.
Haywire is not affiliated with Reddit.com.

---

*News. Crowdsourced by the Hive Mind.*
