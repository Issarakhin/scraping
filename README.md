# Kampuchea Thmey News Scraper

A BeautifulSoup-based web scraper for **Kampuchea Thmey** that automatically discovers the website's main news categories, scrapes articles from each category, extracts article metadata and content, and saves every article as a clean Markdown file.

---

## Features

- Automatic category discovery from the Kampuchea Thmey homepage
- Scrapes articles from all main news categories
- Category-aware scraping (only collects articles belonging to the selected category)
- Metadata extraction
  - Title
  - URL
  - Publication date
  - Author
- Article body extraction
- Markdown output (one file per article)
- Duplicate article filtering
- Configurable number of articles per category
- Uses a Chrome User-Agent for HTTP requests

---

# Programing language

- Python 3.11


---



# Usage

Run the scraper

```bash
python scrape.py
```


The scraper  will automatically

1. Discover all available news categories.
2. Visit every category page.
3. Collect article URLs that belong to the current category.
4. Visit each article.
5. Extract article metadata and content.
6. Save each article as an individual Markdown file.

---

# Configuration

Number of articles scraped from each category

```python
articles_per_category = 3
```

Delay between requests

```python
delay = 2
```

Output directory

```python
output_directory = "kampucheathmey_articles"
```

---

# Example Output

```
Found 15 categories.

============================================================

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

├── announcement/
│
├── belief/
│
├── business-economic/
│
├── commentary/
│
├── entertainment/
│
├── global-news/
│
├── health/
│
├── local-news/
│
├── politics/
│
├── profession-work/
│
├── security/
│
├── sports/
│
├── tech/
│
└── traffic/
```

---

# Output Format

Each article is saved as

```markdown
# Article Title

> **URL:** https://www.kampucheathmey.com/local-news/1162333
> **Date:** 2026-08-03
> **Author:** Reporter Name

---

Article paragraph one.

Article paragraph two.

Article paragraph three.
```

---

# How It Works

### 1. Category Discovery

The scraper requests the Kampuchea Thmey homepage and automatically discovers all news categories whose URLs follow the format

```
/category/*
```

For example

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

The scraper only accepts article URLs that belong to the current category.

Example

Category

```
/category/local-news
```

Accepted

```
/local-news/1162333
/local-news/1162215
/local-news/1161980
```

Ignored

```
/security/1162181
/global-news/1160105
/sports/1160421
```

This prevents unrelated sidebar and recommended articles from being scraped.

---

### 3. Article Extraction

For every article page, BeautifulSoup extracts

- Title
- URL
- Publication date
- Author
- Main article body

Non-content elements such as advertisements, scripts, navigation menus, sidebars, and embedded content are removed before extracting the article text.

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

- Uses a Chrome browser User-Agent.
- Automatically discovers categories from the homepage.
- Prevents duplicate article URLs.
- Saves each article as an individual Markdown file.
- The number of scraped articles per category can be configured.

---
