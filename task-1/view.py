import sqlite3
import pandas as pd
conn = sqlite3.connect("products.db")
df = pd.read_sql_query("SELECT * FROM products", conn)
print(df)
conn.close()