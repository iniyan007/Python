import requests
from bs4 import BeautifulSoup
import sqlite3
import time
import random
import pandas as pd
from datetime import datetime
import re

BASE_URL = "https://www.scrapingcourse.com/ecommerce/page/{}"

conn = sqlite3.connect("products.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    sku TEXT PRIMARY KEY,
    name TEXT,
    price REAL,
    date TEXT
)
""")
conn.commit()

USER_AGENTS = [
    "Mozilla/5.0",
    "Chrome/91.0",
    "Safari/537.36"
]

def get_headers():
    return {"User-Agent": random.choice(USER_AGENTS)}

def fetch(url):
    for _ in range(3):
        try:
            r = requests.get(url, headers=get_headers(), timeout=10)
            if r.status_code == 200:
                return r.text
        except:
            time.sleep(2)
    return None

def parse(html):
    soup = BeautifulSoup(html, "lxml")
    items = soup.select(".product")

    products = []

    for i, item in enumerate(items):
        name = item.select_one(".product-name").text.strip()
        price_text = item.select_one(".price").text.strip()
        price = float(re.sub(r"[^\d.]", "", price_text))

        sku = f"{name[:10]}_{i}"

        products.append({
            "sku": sku,
            "name": name,
            "price": price
        })

    return products


def scrape():
    all_products = []

    print(f"[{datetime.now()}] Scraper started")

    for page in range(1, 6):
        url = BASE_URL.format(page)
        html = fetch(url)

        if not html:
            continue

        products = parse(html)
        print(f"Page {page} — {len(products)} items")

        all_products.extend(products)

        time.sleep(random.uniform(1, 3))  # rate limiting

    return all_products


def save(products):
    today = str(datetime.now().date())

    for p in products:
        cursor.execute("""
        INSERT OR REPLACE INTO products (sku, name, price, date)
        VALUES (?, ?, ?, ?)
        """, (p["sku"], p["name"], p["price"], today))

    conn.commit()

def compare():
    today = str(datetime.now().date())

    df = pd.read_sql_query("SELECT * FROM products", conn)

    if df["date"].nunique() < 2:
        print("Not enough data for comparison")
        return

    old = df[df["date"] != today]
    new = df[df["date"] == today]

    merged = old.merge(new, on="sku", suffixes=("_old", "_new"))

    changes = merged[merged["price_old"] != merged["price_new"]]

    if changes.empty:
        print("No price changes")
        return

    changes["change_%"] = (
        (changes["price_new"] - changes["price_old"]) / changes["price_old"]
    ) * 100

    filename = f"report_{today}.csv"
    changes.to_csv(filename, index=False)

    print("\n=== Price Change Report ===")
    print(changes[["name_new", "price_old", "price_new", "change_%"]])
    print(f"\nReport saved: {filename}")

if __name__ == "__main__":
    data = scrape()
    save(data)
    compare()