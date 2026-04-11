import sqlite3
from datetime import datetime, timedelta
import random

conn = sqlite3.connect("sales.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    date TEXT,
    region TEXT,
    revenue REAL,
    units INTEGER
)
""")

regions = ["North", "South", "East", "West"]

start_date = datetime(2026, 1, 1)

data = []
for i in range(31):
    date = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
    for region in regions:
        revenue = random.randint(5000, 20000)
        units = random.randint(10, 50)
        data.append((date, region, revenue, units))

cursor.executemany("INSERT INTO sales VALUES (?, ?, ?, ?)", data)

conn.commit()
conn.close()

print("✅ Database created with sample data!")