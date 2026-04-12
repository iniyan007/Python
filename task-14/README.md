# 🕸️ Concurrent Web Crawler with Depth Control

An asynchronous web crawler built using Python that performs **BFS-based crawling with concurrency**, respects `robots.txt`, avoids duplicate URLs, and generates SEO insights like broken links, redirects, and orphan pages.

---

## 🚀 Features

* ⚡ Async crawling using `asyncio` and `aiohttp`
* 🌐 BFS traversal with configurable depth
* 🔁 URL deduplication using sets
* 🤖 `robots.txt` compliance
* 📊 Crawl graph generation (JSON)
* 🗺️ Sitemap generation (XML)
* 🔍 SEO audit:

  * Broken links (404)
  * Redirect tracking (301/302)
  * Orphan pages detection

---

## 🛠️ Tech Stack

* Python 3
* `asyncio`
* `aiohttp`
* `BeautifulSoup`
* `urllib.parse`
* `RobotFileParser`

---

## 📦 Installation

```bash
pip install aiohttp beautifulsoup4 lxml
```

---

## ▶️ Usage

```bash
python crawler.py --seed https://books.toscrape.com --depth 2 --concurrency 20
```

---

## 📌 Parameters

| Argument        | Description                   |
| --------------- | ----------------------------- |
| `--seed`        | Starting URL                  |
| `--depth`       | Maximum crawl depth           |
| `--concurrency` | Number of concurrent requests |

---

## 🧠 How It Works

### 1. BFS Traversal

* Uses a queue (`deque`)
* Crawls **level by level**
* Ensures depth control

---

### 2. Async Crawling

* Uses `aiohttp` for non-blocking HTTP requests
* Multiple pages fetched simultaneously

---

### 3. URL Deduplication

* `visited` set prevents revisiting URLs

---

### 4. robots.txt Compliance

* Fetches `/robots.txt`
* Skips disallowed URLs

---

### 5. Graph Construction

* `graph` → adjacency list (who links to whom)
* `inbound_links` → reverse mapping

---

## 📊 Sample Output

```txt
=== Crawl Started ===
[INFO] Seed: https://books.toscrape.com
[INFO] Max depth: 2 | Concurrency: 20

=== Crawl Complete (209.87s) ===
Pages crawled: 586
Unique URLs found: 800

=== SEO Audit Report ===

Broken Links (404):

Redirects:

Orphan Pages:
- https://books.toscrape.com
```

---

## 📁 Output Files

| File               | Description                          |
| ------------------ | ------------------------------------ |
| `crawl_graph.json` | Link relationships (graph structure) |
| `sitemap.xml`      | XML sitemap for crawled URLs         |

---

## 🔍 Code Structure

| Function              | Purpose                               |
| --------------------- | ------------------------------------- |
| `normalize_url()`     | Converts relative → absolute URLs     |
| `init_robot_parser()` | Loads robots.txt rules                |
| `fetch()`             | Fetches page and handles status codes |
| `extract_links()`     | Extracts links from HTML              |
| `crawl()`             | Core BFS + async crawler              |
| `generate_sitemap()`  | Creates XML sitemap                   |
| `save_graph()`        | Saves crawl graph                     |
| `seo_report()`        | Prints SEO insights                   |

---

## 🎯 Learning Outcomes

* Asynchronous programming in Python
* Graph traversal (BFS)
* Web scraping and parsing
* System design for scalable crawlers
