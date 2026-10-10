from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Sales Analytics Dashboard", page_icon="📊", layout="wide")
st.title("📊 Sales Analytics Dashboard")
st.caption("Interactive analysis of a synthetic sales dataset • Python, Pandas, Plotly & Streamlit")

DATA_PATH = Path(__file__).parent / "data" / "sales.csv"

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df.columns = [str(c).strip() for c in df.columns]
    required = {"Order_Date", "Product", "Region", "Sales_INR", "Profit_INR"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(sorted(missing)))
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    for col in ["Sales_INR", "Profit_INR"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.dropna(subset=["Order_Date", "Product", "Region", "Sales_INR", "Profit_INR"])

if not DATA_PATH.exists():
    st.error("Dataset not found. Ensure data/sales.csv exists in the GitHub repository.")
    st.stop()

try:
    data = load_data(str(DATA_PATH))
except Exception as exc:
    st.error(f"Could not load dataset: {exc}")
    st.stop()

st.sidebar.header("🔎 Filters")
products = sorted(data["Product"].astype(str).unique())
regions = sorted(data["Region"].astype(str).unique())
selected_products = st.sidebar.multiselect("Product", products, default=products)
selected_regions = st.sidebar.multiselect("Region", regions, default=regions)
min_date, max_date = data["Order_Date"].min().date(), data["Order_Date"].max().date()
date_range = st.sidebar.date_input("Order date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

filtered = data[
    data["Product"].astype(str).isin(selected_products)
    & data["Region"].astype(str).isin(selected_regions)
].copy()
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    filtered = filtered[filtered["Order_Date"].dt.date.between(date_range[0], date_range[1])]
elif isinstance(date_range, (tuple, list)) and len(date_range) == 1:
    filtered = filtered[filtered["Order_Date"].dt.date == date_range[0]]

if filtered.empty:
    st.warning("No records match these filters. Select more products/regions or a wider date range.")
    st.stop()

sales = filtered["Sales_INR"].sum()
profit = filtered["Profit_INR"].sum()
orders = len(filtered)
margin = profit / sales * 100 if sales else 0
c1, c2, c3, c4 = st.columns(4)
c1.metric("💰 Total Sales", f"₹{sales:,.0f}")
c2.metric("📈 Estimated Profit", f"₹{profit:,.0f}")
c3.metric("📦 Orders Analyzed", f"{orders:,}")
c4.metric("🎯 Estimated Profit Margin", f"{margin:.2f}%")

st.divider()
left, right = st.columns(2)
with left:
    product_sales = filtered.groupby("Product", as_index=False)["Sales_INR"].sum().sort_values("Sales_INR", ascending=False)
    fig = px.bar(product_sales, x="Product", y="Sales_INR", title="Sales by Product", text_auto=".2s",
                 labels={"Sales_INR": "Sales (INR)", "Product": "Product"})
    fig.update_layout(xaxis_title="", yaxis_tickprefix="₹", yaxis_tickformat=",.0f")
    st.plotly_chart(fig, use_container_width=True)
with right:
    region_profit = filtered.groupby("Region", as_index=False)["Profit_INR"].sum().sort_values("Profit_INR", ascending=False)
    fig = px.bar(region_profit, x="Region", y="Profit_INR", title="Estimated Profit by Region", text_auto=".2s",
                 labels={"Profit_INR": "Estimated Profit (INR)", "Region": "Region"})
    fig.update_layout(xaxis_title="", yaxis_tickprefix="₹", yaxis_tickformat=",.0f")
    st.plotly_chart(fig, use_container_width=True)

monthly = filtered.assign(Month=filtered["Order_Date"].dt.to_period("M").astype(str))
monthly_sales = monthly.groupby("Month", as_index=False)["Sales_INR"].sum()
fig = px.line(monthly_sales, x="Month", y="Sales_INR", title="Monthly Sales Trend", markers=True,
              labels={"Sales_INR": "Sales (INR)", "Month": "Month"})
fig.update_layout(yaxis_tickprefix="₹", yaxis_tickformat=",.0f")
st.plotly_chart(fig, use_container_width=True)

st.subheader("📋 Filtered Data Preview")
st.dataframe(filtered.head(100), use_container_width=True, hide_index=True)
st.download_button("⬇️ Download filtered data as CSV", data=filtered.to_csv(index=False).encode("utf-8"),
                   file_name="filtered_sales_data.csv", mime="text/csv")
st.caption("Disclaimer: This project uses synthetic sample data for learning and demonstration. Figures do not represent a real company.")
