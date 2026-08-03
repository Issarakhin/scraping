# Kampuchea Thmey News Scraper

A BeautifulSoup-based web scraper for **Kampuchea Thmey** that extracts news articles from the site's main categories and saves each article as a clean Markdown file.

## Features

- Automatic category discovery — finds all main news categories from the homepage
- Category-based scraping — scrapes articles from every discovered category
- Category validation — only collects articles that belong to the current category (e.g. `/local-news/*` for Local News)
- Metadata extraction — title, URL, publication date, author
- Article content extraction — removes unnecessary HTML and extracts only the article body
- Markdown output — saves every article as an individual Markdown file
- Duplicate prevention — avoids collecting duplicate article links
- Configurable scraping — choose how many articles to scrape per category

---

# Requirements

- Python 3.9+
- Internet connection

---

# Environment Setup

## macOS

```bash
# Install Python
brew install python

# Clone repository
git clone <your-repository-url>
cd kampucheathmey-scraper

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install requests beautifulsoup4
```

## Windows (PowerShell)

```powershell
# Install Python from
https://python.org

# Clone repository
git clone <your-repository-url>
cd kampucheathmey-scraper

# Create virtual environment
python -m venv venv

# Activate
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install requests beautifulsoup4
```

## Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv

git clone <your-repository-url>
cd kampucheathmey-scraper

python3 -m venv venv

source venv/bin/activate

pip install requests beautifulsoup4
```

---

# Usage

Run the scraper

```bash
python scrape.py
```

The scraper will

1. Discover all available news categories.
2. Visit each category page.
3. Collect article links that belong to that category.
4. Visit each article.
5. Extract metadata and article content.
6. Save each article as a Markdown file.

---

# Configuration

Change the number of articles scraped from each category.

```python
articles_per_category = 3
```

Change the delay between requests.

```python
delay = 2
```

Change the output directory.

```python
output_directory = "kampucheathmey_articles"
```

---

# Example Output

```
Found 15 categories.

========================================================

Category: ព័ត៌មានជាតិ

URL:
https://www.kampucheathmey.com/category/local-news

Found 3 articles.

[1/3]
https://www.kampucheathmey.com/local-news/1162333

Saved:
kampucheathmey_articles/local-news/article1.md
```

---

# Output Structure

```
kampucheathmey_articles/

├── local-news/
│   ├── article1.md
│   ├── article2.md
│   └── article3.md
│
├── global-news/
│   ├── article1.md
│   ├── article2.md
│   └── article3.md
│
├── politics/
│
├── sports/
│
├── tech/
│
└── ...
```

---

# Output Format

Each article is saved as

```markdown
# Article Title

> **URL**: https://www.kampucheathmey.com/local-news/1162333
> **Date**: 2026-08-03
> **Author**: Reporter Name

---

First paragraph of the article.

Second paragraph.

Third paragraph.
```

---

# How It Works

### 1. Category Discovery

The scraper requests the Kampuchea Thmey homepage and automatically collects all navigation links matching the format

```
/category/*
```

Examples

```
/category/local-news
/category/global-news
/category/politics
/category/business-economic
/category/sports
```

---

### 2. Article Link Collection

Each category page is visited individually.

Only article URLs that belong to the current category are collected.

For example, when scraping

```
/category/local-news
```

the scraper accepts

```
/local-news/1162333
/local-news/1162215
/local-news/1161980
```

and ignores unrelated links such as

```
/security/1162181
/sports/1161200
/global-news/1160500
```

This prevents sidebar, trending, and recommended articles from being scraped.

---

### 3. Article Extraction

For every article, BeautifulSoup extracts

- Title
- URL
- Publication date
- Author
- Main article content

Unnecessary HTML elements such as scripts, advertisements, navigation bars, sidebars, and embedded content are ignored.

---

### 4. Markdown Export

Each article is converted into a Markdown document and saved inside its corresponding category folder.

---

# Technologies Used

- Python
- Requests
- BeautifulSoup4
- pathlib
- urllib.parse
- Regular Expressions

---

# Notes

- Uses a Chrome User-Agent for requests.
- Automatically discovers categories from the homepage.
- Prevents duplicate article URLs.
- Saves each article as an individual Markdown file.
- Designed for educational and research purposes.

---

# Disclaimer

This project is intended for educational and research purposes only. Please respect Kampuchea Thmey's Terms of Service, robots.txt, and applicable copyright laws when scraping or redistributing website content.
