from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "sales_data.csv"
DB = ROOT / "data" / "sales_database.db"

df = pd.read_csv(DATA)
with sqlite3.connect(DB) as conn:
    df.to_sql("sales", conn, if_exists="replace", index=False)
print(f"Loaded {len(df):,} rows into {DB}")
print("Example category summary:")
with sqlite3.connect(DB) as conn:
    print(pd.read_sql_query("""
        SELECT Category, ROUND(SUM(Sales), 2) AS total_sales,
               ROUND(SUM(Profit), 2) AS total_profit
        FROM sales GROUP BY Category ORDER BY total_sales DESC
    """, conn).to_string(index=False))
