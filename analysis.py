"""
Trend Trackers — Sales Trend Analysis
Uses the included sample dataset. Replace data/sales_data.csv with your own
dataset after matching the required column names.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "sales_data.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

def load_and_clean(path=DATA):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    for col in ["Sales", "Profit", "Quantity", "Unit Price", "Discount"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.drop_duplicates()
    df = df.dropna(subset=["Order Date", "Sales", "Profit"])
    df = df[df["Sales"] >= 0].copy()
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month
    df["Month Start"] = df["Order Date"].dt.to_period("M").dt.to_timestamp()
    df["Profit Margin %"] = (df["Profit"] / df["Sales"].replace(0, pd.NA) * 100).fillna(0)
    return df

def main():
    df = load_and_clean()
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_orders = df["Order ID"].nunique() if "Order ID" in df.columns else len(df)
    total_units = df["Quantity"].sum() if "Quantity" in df.columns else 0
    print("\\n=== TREND TRACKERS: KPI SUMMARY ===")
    print(f"Rows analyzed: {len(df):,}")
    print(f"Total sales: ${total_sales:,.2f}")
    print(f"Total profit: ${total_profit:,.2f}")
    print(f"Total orders: {total_orders:,}")
    print(f"Units sold: {total_units:,}")
    print(f"Profit margin: {(total_profit / total_sales * 100 if total_sales else 0):.2f}%")

    monthly = df.groupby("Month Start", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    category = df.groupby("Category", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    region = df.groupby("Region", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    product = df.groupby("Product Name", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Quantity=("Quantity", "sum"))
    monthly.to_csv(OUT / "monthly_summary.csv", index=False)
    category.to_csv(OUT / "category_summary.csv", index=False)
    region.to_csv(OUT / "region_summary.csv", index=False)
    product.to_csv(OUT / "product_summary.csv", index=False)
    df.to_csv(OUT / "cleaned_sales_data.csv", index=False)

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(monthly["Month Start"], monthly["Sales"], marker="o", linewidth=2)
    ax.set_title("Monthly Sales Trend", fontsize=16)
    ax.set_xlabel("Month"); ax.set_ylabel("Sales ($)")
    fig.tight_layout(); fig.savefig(OUT / "monthly_sales_trend.png", dpi=160); plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    cat_sorted = category.sort_values("Sales", ascending=True)
    ax.barh(cat_sorted["Category"], cat_sorted["Sales"])
    ax.set_title("Sales by Category", fontsize=16)
    ax.set_xlabel("Sales ($)")
    fig.tight_layout(); fig.savefig(OUT / "sales_by_category.png", dpi=160); plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    reg_sorted = region.sort_values("Profit", ascending=True)
    ax.barh(reg_sorted["Region"], reg_sorted["Profit"])
    ax.set_title("Profit by Region", fontsize=16)
    ax.set_xlabel("Profit ($)")
    fig.tight_layout(); fig.savefig(OUT / "profit_by_region.png", dpi=160); plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 6))
    top = product.nlargest(10, "Sales").sort_values("Sales")
    ax.barh(top["Product Name"], top["Sales"])
    ax.set_title("Top 10 Products by Sales", fontsize=16)
    ax.set_xlabel("Sales ($)")
    fig.tight_layout(); fig.savefig(OUT / "top_products.png", dpi=160); plt.close(fig)

    print("\\nTop categories by sales:")
    print(category.sort_values("Sales", ascending=False).to_string(index=False))
    print("\\nTop 5 products by sales:")
    print(product.nlargest(5, "Sales").to_string(index=False))
    print(f"\\nOutputs saved to: {OUT}")

if __name__ == "__main__":
    main()
