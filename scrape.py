import re
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://www.kampucheathmey.com"

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


session = requests.Session()
session.headers.update(HEADERS)


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def get_soup(url: str) -> BeautifulSoup:
    response = session.get(url, timeout=30)
    response.raise_for_status()

    return BeautifulSoup(response.content, "html.parser")


def get_main_categories() -> dict[str, str]:
    """
    Automatically collect all category links from the homepage.

    Example:
    {
        "ព័ត៌មានជាតិ": ".../category/local-news",
        "ព័ត៌មានអន្ដរជាតិ": ".../category/global-news"
    }
    """
    soup = get_soup(BASE_URL)

    categories = {}

    for link in soup.find_all("a", href=True):
        category_name = clean_text(link.get_text(" ", strip=True))
        category_url = urljoin(BASE_URL, link["href"])

        parsed = urlparse(category_url)
        path = parsed.path.rstrip("/")

        if not path.startswith("/category/"):
            continue

        # Ignore pagination and category feeds.
        if "/page/" in path or path.endswith("/feed"):
            continue

        if not category_name:
            category_name = path.split("/")[-1]

        categories[category_name] = category_url.rstrip("/")

    return categories


def is_article_url(url: str) -> bool:
    parsed = urlparse(url)

    if parsed.netloc not in {
        "kampucheathmey.com",
        "www.kampucheathmey.com"
    }:
        return False

    path = parsed.path.rstrip("/")

    # Kampuchea Thmey article URLs normally end with a numeric ID.
    return bool(re.search(r"/\d+$", path))


def collect_article_links(
    category_url: str,
    limit: int = 3
) -> list[str]:

    soup = get_soup(category_url)

    category_slug = category_url.rstrip("/").split("/")[-1]

    article_links = []
    seen = set()

    for link in soup.find_all("a", href=True):
        article_url = urljoin(category_url, link["href"])
        article_url = article_url.split("#")[0].split("?")[0]
        article_url = article_url.rstrip("/")

        parsed = urlparse(article_url)
        path = parsed.path.rstrip("/")


        pattern = rf"^/{re.escape(category_slug)}/\d+$"

        if not re.match(pattern, path):
            continue

        if article_url in seen:
            continue

        seen.add(article_url)
        article_links.append(article_url)

        if len(article_links) >= limit:
            break

    return article_links


def find_article_container(soup: BeautifulSoup):
    selectors = [
        ".entry-content",
        ".post-content",
        ".article-content",
        ".single-content",
        "article .entry-content",
        "article",
        "main",
    ]

    for selector in selectors:
        container = soup.select_one(selector)

        if container and container.find("p"):
            return container

    return None


def get_meta_content(
    soup: BeautifulSoup,
    property_name: str
) -> str:

    meta = soup.find(
        "meta",
        attrs={"property": property_name}
    )

    if meta:
        return clean_text(meta.get("content", ""))

    return ""


def extract_article(url: str) -> dict:
    soup = get_soup(url)

    title = ""

    heading = soup.find("h1")

    if heading:
        title = clean_text(
            heading.get_text(" ", strip=True)
        )

    if not title:
        title = get_meta_content(soup, "og:title")

    author = ""

    author_element = soup.select_one(
        ".author, "
        ".author-name, "
        ".post-author, "
        ".entry-author, "
        "[rel='author']"
    )

    if author_element:
        author = clean_text(
            author_element.get_text(" ", strip=True)
        )

    published_date = ""

    time_element = soup.find("time")

    if time_element:
        published_date = (
            time_element.get("datetime")
            or clean_text(
                time_element.get_text(" ", strip=True)
            )
        )

    if not published_date:
        date_meta = soup.find(
            "meta",
            attrs={"property": "article:published_time"}
        )

        if date_meta:
            published_date = date_meta.get("content", "")

    article_container = find_article_container(soup)

    paragraphs = []

    if article_container:
        unwanted_selectors = (
            "script, style, iframe, form, button, aside, nav, "
            ".advertisement, .ads, .related-posts, .social-share, "
            ".sharedaddy, .newsletter, .comments"
        )

        for unwanted in article_container.select(
            unwanted_selectors
        ):
            unwanted.decompose()

        for paragraph in article_container.find_all("p"):
            text = clean_text(
                paragraph.get_text(" ", strip=True)
            )

            if len(text) < 20:
                continue

            if text not in paragraphs:
                paragraphs.append(text)

    return {
        "title": title,
        "url": url,
        "date": published_date,
        "author": author,
        "content": paragraphs,
    }


def safe_name(text: str, fallback: str) -> str:
    name = re.sub(r'[\\/:*?"<>|]', "", text)
    name = re.sub(r"\s+", " ", name).strip()

    if not name:
        name = fallback

    return name[:100]


def save_article(
    article: dict,
    output_directory: Path,
    number: int
):
    lines = [
        f"# {article['title']}",
        "",
        f"URL: {article['url']}",
    ]

    if article["date"]:
        lines.append(f"Date: {article['date']}")

    if article["author"]:
        lines.append(f"Author: {article['author']}")

    lines.extend(["", "---", ""])

    for paragraph in article["content"]:
        lines.append(paragraph)
        lines.append("")

    filename = safe_name(
        article["title"],
        f"article-{number}"
    )

    output_file = output_directory / f"{filename}.md"

    output_file.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )

    print(f"Saved: {output_file}")


def scrape_all_categories(
    output_directory: str = "kampucheathmey_articles",
    articles_per_category: int = 10,
    delay: float = 2.0
):
    root_output = Path(output_directory)
    root_output.mkdir(parents=True, exist_ok=True)

    categories = get_main_categories()

    print(f"Found {len(categories)} categories.\n")

    for category_number, (
        category_name,
        category_url
    ) in enumerate(categories.items(), start=1):

        category_slug = urlparse(
            category_url
        ).path.rstrip("/").split("/")[-1]

        category_folder = (
            root_output
            / safe_name(category_slug, f"category-{category_number}")
        )

        category_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        print("=" * 60)
        print(f"Category: {category_name}")
        print(f"URL: {category_url}")

        try:
            article_links = collect_article_links(
                category_url,
                limit=articles_per_category
            )

            print(
                f"Found {len(article_links)} articles."
            )

            for article_number, article_url in enumerate(
                article_links,
                start=1
            ):
                try:
                    print(
                        f"[{article_number}/"
                        f"{len(article_links)}] "
                        f"{article_url}"
                    )

                    article = extract_article(article_url)

                    save_article(
                        article,
                        category_folder,
                        article_number
                    )

                except requests.RequestException as error:
                    print(
                        f"Article request failed: {error}"
                    )

                except Exception as error:
                    print(
                        f"Article scraping failed: {error}"
                    )

                time.sleep(delay)

        except requests.RequestException as error:
            print(
                f"Category request failed: {error}"
            )

        except Exception as error:
            print(
                f"Category scraping failed: {error}"
            )

        time.sleep(delay)


if __name__ == "__main__":
    scrape_all_categories(
        output_directory="kampucheathmey_articles",
        articles_per_category=3,
        delay=2
    )