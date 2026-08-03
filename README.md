# Kampuchea Thmey News Scraper

A Python web scraper for **Kampuchea Thmey** that uses `Requests` and `BeautifulSoup` to automatically discover news categories, collect articles from each category, extract article metadata and content, and save every article as a Markdown file.

---

## Features

- Automatically discovers category links from the Kampuchea Thmey homepage
- Scrapes articles from all discovered news categories
- Collects only articles that match the current category
- Extracts:
  - Article title
  - Article URL
  - Publication date
  - Author
  - Main article content
- Saves each article as an individual Markdown file
- Creates a separate folder for each category
- Prevents duplicate article links
- Removes selected unwanted HTML elements
- Uses a Chrome User-Agent for HTTP requests
- Scrapes three articles from each category by default
- Includes a configurable delay between requests

---

## Programming Language

- Python 3.11

---

## Requirements

The project uses these external Python libraries:

- Requests
- BeautifulSoup4

The following modules are included with Python and do not need to be installed separately:

- `re`
- `time`
- `pathlib`
- `urllib.parse`

Create a `requirements.txt` file containing:

```txt
requests
beautifulsoup4
```

Install the dependencies with:

```bash
pip install -r requirements.txt
```

You can also install them directly:

```bash
pip install requests beautifulsoup4
```

---

## Project Structure

```text
webscraping/
├── scrape.py
├── README.md
├── requirements.txt
└── kampucheathmey_articles/
```

The `kampucheathmey_articles` folder is created automatically when the scraper runs.

---

## Usage

Run the scraper with:

```bash
python scrape.py
```

On Windows PowerShell:

```powershell
python .\scrape.py
```

The scraper will automatically:

1. Request the Kampuchea Thmey homepage.
2. Discover category links that use the `/category/` URL structure.
3. Visit every category page.
4. Collect article URLs that match the current category.
5. Visit each accepted article.
6. Extract the title, URL, date, author, and article content.
7. Save each article as a separate Markdown file.
8. Store the article inside its corresponding category folder.

---

## Configuration

The main settings are located at the bottom of `scrape.py`:

```python
if __name__ == "__main__":
    scrape_all_categories(
        output_directory="kampucheathmey_articles",
        articles_per_category=3,
        delay=2
    )
```

### Number of articles per category

```python
articles_per_category=3
```

This collects up to three articles from each category.

### Delay between requests

```python
delay=2
```

This adds a two-second pause between requests.

### Output directory

```python
output_directory="kampucheathmey_articles"
```

This is the root folder where all scraped articles are saved.

---

## Example Console Output

```text
Found 15 categories.

============================================================
Category: ព័ត៌មានជាតិ
URL: https://www.kampucheathmey.com/category/local-news
Found 3 articles.

[1/3] https://www.kampucheathmey.com/local-news/1162333
Saved: kampucheathmey_articles\local-news\article-title.md
```

---

## Output Structure

The scraper creates one folder for each discovered category:

```text
kampucheathmey_articles/
├── announcement/
├── belief/
├── business-economic/
├── commentary/
├── entertainment/
├── global-news/
├── health/
├── local-news/
├── politics/
├── profession-work/
├── security/
├── sports/
├── tech/
└── traffic/
```

Each category folder contains up to three Markdown files:

```text
kampucheathmey_articles/
└── local-news/
    ├── article-title-1.md
    ├── article-title-2.md
    └── article-title-3.md
```

The actual filenames are created from article titles.

---

## Output Format

Each article is saved in this format:

```markdown
# Article Title

URL: https://www.kampucheathmey.com/local-news/1162333
Date: 2026-08-03
Author: Reporter Name

---

First article paragraph.

Second article paragraph.

Third article paragraph.
```

The date and author are included only when they are found on the article page.

---

## How It Works

### 1. HTTP Session and Headers

The scraper creates a reusable `requests.Session`:

```python
session = requests.Session()
session.headers.update(HEADERS)
```

It uses a Chrome User-Agent:

```python
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/149.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "image/avif,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "km-KH,km;q=0.9,en-US;q=0.8,en;q=0.7",
}
```

Although the User-Agent begins with `Mozilla/5.0`, it is still a Chrome User-Agent. Modern Chrome User-Agent strings include `Mozilla/5.0` for compatibility.

---

### 2. Page Requests

The `get_soup()` function downloads a page and converts its HTML into a BeautifulSoup object:

```python
def get_soup(url: str) -> BeautifulSoup:
    response = session.get(url, timeout=30)
    response.raise_for_status()

    return BeautifulSoup(response.content, "html.parser")
```

---

### 3. Category Discovery

The scraper requests:

```text
https://www.kampucheathmey.com
```

It searches for links whose path begins with:

```text
/category/
```

Examples:

```text
/category/local-news
/category/global-news
/category/politics
/category/business-economic
/category/sports
```

Pagination and feed URLs are ignored:

```python
if "/page/" in path or path.endswith("/feed"):
    continue
```

---

### 4. Article Link Collection

Each category page is visited separately.

Example category page:

```text
https://www.kampucheathmey.com/category/local-news
```

The category slug is extracted from the URL:

```python
category_slug = category_url.rstrip("/").split("/")[-1]
```

For the example above, the slug is:

```text
local-news
```

The scraper creates this regular-expression pattern:

```python
pattern = rf"^/{re.escape(category_slug)}/\d+$"
```

For `local-news`, accepted article paths look like:

```text
/local-news/1162333
/local-news/1162215
/local-news/1161980
```

Unrelated article paths are skipped:

```text
/security/1162181
/global-news/1160105
/sports/1160421
```

The filtering code is:

```python
pattern = rf"^/{re.escape(category_slug)}/\d+$"

if not re.match(pattern, path):
    continue
```

The scraper does not directly replace the word `category`. It extracts the category slug and only accepts article paths that begin with the same slug.

Example:

```text
Category page: /category/local-news
Article path:  /local-news/1162333
```

---

### 5. Duplicate Prevention

The scraper uses a set called `seen`:

```python
seen = set()
```

Duplicate article links are skipped:

```python
if article_url in seen:
    continue
```

Accepted links are added to both `seen` and `article_links`:

```python
seen.add(article_url)
article_links.append(article_url)
```

---

### 6. Article Container Detection

The scraper checks several possible CSS selectors:

```python
selectors = [
    ".entry-content",
    ".post-content",
    ".article-content",
    ".single-content",
    "article .entry-content",
    "article",
    "main",
]
```

The first matching container with at least one paragraph is selected.

---

### 7. Metadata Extraction

The article title is first extracted from the `<h1>` element.

If an `<h1>` is not found, the scraper uses:

```html
<meta property="og:title">
```

The scraper looks for the author using these selectors:

```text
.author
.author-name
.post-author
.entry-author
[rel='author']
```

The publication date is first taken from a `<time>` element. If it is unavailable, the scraper checks:

```html
<meta property="article:published_time">
```

---

### 8. Article Content Extraction

Before extracting paragraphs, the scraper removes selected unwanted elements:

```python
unwanted_selectors = (
    "script, style, iframe, form, button, aside, nav, "
    ".advertisement, .ads, .related-posts, .social-share, "
    ".sharedaddy, .newsletter, .comments"
)
```

This may remove:

- Scripts
- Styles
- Iframes
- Forms
- Buttons
- Sidebars
- Navigation elements
- Advertisements
- Related-post sections
- Social-sharing sections
- Newsletters
- Comments

The scraper then extracts paragraph text:

```python
for paragraph in article_container.find_all("p"):
```

Paragraphs shorter than 20 characters are skipped:

```python
if len(text) < 20:
    continue
```

Duplicate paragraphs are also excluded.

---

### 9. Safe Filenames

Article titles are used as filenames.

Characters that are not allowed in Windows filenames are removed:

```python
name = re.sub(r'[\\/:*?"<>|]', "", text)
```

The filename is limited to 100 characters:

```python
return name[:100]
```

When an article title is missing, a fallback filename such as `article-1.md` is used.

---

### 10. Markdown Export

The extracted article is converted into Markdown and saved with UTF-8 encoding:

```python
output_file.write_text(
    "\n".join(lines),
    encoding="utf-8"
)
```

UTF-8 encoding allows Khmer text to be saved correctly.

---

## Technologies Used

- Python 3.11
- Requests
- BeautifulSoup4
- Regular expressions
- `pathlib`
- `urllib.parse`
- Type hints
- Markdown

---

## Notes

- The scraper collects up to three articles from every discovered category.
- Category pages may contain sidebar or recommended articles from other sections.
- The category-matching regular expression prevents unrelated article links from being accepted.
- The homepage may contain duplicate category links with different visible names.
- Some metadata may be missing when the website does not provide it.
- Website HTML structures may change and could require updating the CSS selectors.
- The `is_article_url()` function is currently defined but is not used by the final category-filtering logic.

---

## Disclaimer

This project is intended for educational and research purposes. Users should respect Kampuchea Thmey's terms, `robots.txt`, copyright rules, and applicable laws when collecting, storing, or redistributing website content.
