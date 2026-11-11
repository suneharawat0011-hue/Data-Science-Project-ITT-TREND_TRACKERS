"""
Trend Trackers interactive dashboard.
Run from the project root: streamlit run src/dashboard.py
"""
from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "sales_data.csv"

st.set_page_config(page_title="Trend Trackers | Sales Analytics", page_icon="📈", layout="wide")
st.title("📈 Trend Trackers")
st.caption("Sales Trend Analysis & Business Intelligence Dashboard • Demonstration dataset")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA)
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    for c in ["Sales", "Profit", "Quantity", "Discount"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.drop_duplicates().dropna(subset=["Order Date", "Sales", "Profit"])
    df["Year"] = df["Order Date"].dt.year
    df["Month Start"] = df["Order Date"].dt.to_period("M").dt.to_timestamp()
    return df

df = load_data()
with st.sidebar:
    st.header("Filter the data")
    years = sorted(df["Year"].dropna().unique().tolist())
    selected_years = st.multiselect("Year", years, default=years)
    regions = sorted(df["Region"].dropna().unique().tolist())
    selected_regions = st.multiselect("Region", regions, default=regions)
    categories = sorted(df["Category"].dropna().unique().tolist())
    selected_categories = st.multiselect("Category", categories, default=categories)
    st.info("The included dataset is synthetic sample data. Replace it with real data before drawing business conclusions.")

filtered = df[
    df["Year"].isin(selected_years)
    & df["Region"].isin(selected_regions)
    & df["Category"].isin(selected_categories)
].copy()

if filtered.empty:
    st.warning("No records match these filters. Select at least one year, region, and category.")
    st.stop()

total_sales = filtered["Sales"].sum()
total_profit = filtered["Profit"].sum()
orders = filtered["Order ID"].nunique()
units = filtered["Quantity"].sum()
margin = total_profit / total_sales * 100 if total_sales else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Sales", f"${total_sales:,.0f}")
c2.metric("Total Profit", f"${total_profit:,.0f}")
c3.metric("Orders", f"{orders:,}")
c4.metric("Profit Margin", f"{margin:.1f}%")

monthly = filtered.groupby("Month Start", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
category = filtered.groupby("Category", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
region = filtered.groupby("Region", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
product = filtered.groupby("Product Name", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Quantity=("Quantity", "sum"))

left, right = st.columns(2)
with left:
    st.subheader("Monthly sales trend")
    fig = px.line(monthly, x="Month Start", y="Sales", markers=True, template="plotly_white")
    fig.update_layout(xaxis_title="Month", yaxis_title="Sales ($)")
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Sales by category")
    fig = px.bar(category.sort_values("Sales", ascending=False), x="Category", y="Sales", color="Category", template="plotly_white")
    fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Sales ($)")
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Profit by region")
    fig = px.bar(region.sort_values("Profit"), x="Profit", y="Region", orientation="h", template="plotly_white")
    fig.update_layout(xaxis_title="Profit ($)", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Top 10 products by sales")
    fig = px.bar(product.nlargest(10, "Sales").sort_values("Sales"), x="Sales", y="Product Name", orientation="h", template="plotly_white")
    fig.update_layout(xaxis_title="Sales ($)", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Filtered records")
st.dataframe(filtered, use_container_width=True, hide_index=True)
st.download_button(
    "Download filtered data as CSV",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="trend_trackers_filtered_sales.csv",
    mime="text/csv"
)
st.caption("Trend Trackers • Python + Pandas + Plotly + Streamlit. Source files are editable.")
