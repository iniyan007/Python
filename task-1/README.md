# 🕸️ Web Scraper with Anti-Bot Bypass

## 📌 Overview

This project is a **Python-based web scraper** designed to extract product data from an e-commerce website while handling basic anti-bot mechanisms. It supports pagination, retry logic, user-agent rotation, and stores data in a SQLite database.

Additionally, it tracks **price changes over time** and generates a **daily CSV report**.

---

## 🚀 Features

- 🔄 Pagination handling (multiple pages)
- 🧠 Anti-bot techniques:
  - Rotating User-Agents
  - Request retries
  - Random delays (rate limiting)
- 🗄️ SQLite database storage
- 📊 Price comparison between days
- 📁 CSV report generation
- 🧹 Data cleaning using regex

---

## 🛠️ Tech Stack

- Python
- `requests` – HTTP requests
- `BeautifulSoup (bs4)` – HTML parsing
- `lxml` – Fast parser
- `sqlite3` – Database
- `pandas` – Data analysis & reporting
- `re` – Regex for text cleaning

## ⚙️ How It Works

### 1. Scraping Data

- Iterates through multiple pages:

```

[https://www.scrapingcourse.com/ecommerce/page/{page_number}](https://www.scrapingcourse.com/ecommerce/page/{page_number})

````

- Extracts:
- Product Name
- Price
- SKU (generated)

---

### 2. Anti-Bot Handling

- Rotates User-Agent headers:

```python
random.choice(USER_AGENTS)
````

* Retry mechanism (3 attempts)
* Random delay:

  ```python
  time.sleep(random.uniform(1, 3))
  ```

---

### 3. Data Storage

* Uses SQLite database: `products.db`
* Table schema:

```sql
CREATE TABLE products (
    sku TEXT PRIMARY KEY,
    name TEXT,
    price REAL,
    date TEXT
);
```

* Stores data with current date

---

### 4. Price Comparison

* Loads all data into Pandas
* Compares:

  * Today's prices vs previous data
* Identifies price differences

---

### 5. Report Generation

* Calculates percentage change:

```python
(price_new - price_old) / price_old * 100
```

* Saves output:

```
report_YYYY-MM-DD.csv
```

* Displays summary in console

---

## ▶️ Execution

Run the script:

```bash
python scraper.py
```

---

## 🧪 Sample Output

```
[2026-04-03 10:00:00] Scraper started
Page 1 — 20 items
Page 2 — 20 items
...

=== Price Change Report ===
Product Name | Old Price | New Price | Change %
------------------------------------------------
Item A       | 100       | 120       | +20%
```

---

## 📚 Prerequisites

Before running, ensure you understand:

* HTTP basics (methods, headers, status codes)
* HTML & CSS selectors
* Python libraries:

  * requests / httpx
  * BeautifulSoup
* Regex basics
* Optional (for advanced scraping):

  * Selenium / Playwright
  * asyncio for concurrency

---

## 📌 Use Case

* Daily e-commerce monitoring
* Price tracking system
* Competitive analysis
* Automated reporting pipelines
