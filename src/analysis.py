from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Project folders
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"
CHARTS_DIR = OUTPUT_DIR / "charts"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CHARTS_DIR.mkdir(parents=True, exist_ok=True)

# Load dataset
DATA_FILE = DATA_DIR / "sales.csv"

if not DATA_FILE.exists():
    raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

df = pd.read_csv(DATA_FILE)

print("\n========== SALES DATA ANALYSIS ==========")
print("\nFirst 5 records:")
print(df.head())

print("\nDataset shape:", df.shape)
print("\nColumn names:", df.columns.tolist())
print("\nMissing values:")
print(df.isnull().sum())

# Clean column names
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# Detect important columns
def find_column(possible_names):
    for name in possible_names:
        if name in df.columns:
            return name
    return None

product_col = find_column(["product", "product_name", "item"])
region_col = find_column(["region", "area", "location"])
sales_col = find_column(["sales", "revenue", "total_sales", "amount"])
profit_col = find_column(["profit", "net_profit", "estimated_profit"])
date_col = find_column(["date", "order_date", "sales_date"])

if sales_col is None:
    raise ValueError(
        f"Sales column not found. Available columns: {df.columns.tolist()}"
    )

df[sales_col] = pd.to_numeric(df[sales_col], errors="coerce")

if profit_col:
    df[profit_col] = pd.to_numeric(df[profit_col], errors="coerce")

# Overall business summary
total_sales = df[sales_col].sum()

total_profit = (
    df[profit_col].sum()
    if profit_col
    else np.nan
)

profit_margin = (
    (total_profit / total_sales) * 100
    if profit_col and total_sales != 0
    else np.nan
)

print("\n========== BUSINESS SUMMARY ==========")
print(f"Total Sales: ₹{total_sales:,.2f}")

if profit_col:
    print(f"Total Profit: ₹{total_profit:,.2f}")
    print(f"Profit Margin: {profit_margin:.2f}%")

# Product-wise summary
if product_col:
    product_summary = (
        df.groupby(product_col, dropna=False)
        .agg(
            total_sales=(sales_col, "sum"),
            number_of_records=(sales_col, "count"),
        )
        .reset_index()
        .sort_values("total_sales", ascending=False)
    )

    if profit_col:
        product_profit = (
            df.groupby(product_col, dropna=False)[profit_col]
            .sum()
            .reset_index(name="total_profit")
        )
        product_summary = product_summary.merge(
            product_profit, on=product_col
        )

    product_summary.to_csv(
        OUTPUT_DIR / "product_summary.csv", index=False
    )

    print("\nTop products by sales:")
    print(product_summary.head(10))

    # Sales by product chart
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=product_summary.head(10),
        x="total_sales",
        y=product_col
    )
    plt.title("Top Products by Sales")
    plt.xlabel("Total Sales (INR)")
    plt.ylabel("Product")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "sales_by_product.png", dpi=150)
    plt.close()

# Region-wise summary
if region_col:
    region_summary = (
        df.groupby(region_col, dropna=False)
        .agg(
            total_sales=(sales_col, "sum"),
            number_of_records=(sales_col, "count"),
        )
        .reset_index()
        .sort_values("total_sales", ascending=False)
    )

    if profit_col:
        region_profit = (
            df.groupby(region_col, dropna=False)[profit_col]
            .sum()
            .reset_index(name="total_profit")
        )
        region_summary = region_summary.merge(
            region_profit, on=region_col
        )

    region_summary.to_csv(
        OUTPUT_DIR / "region_summary.csv", index=False
    )

    print("\nSales by region:")
    print(region_summary)

    # Profit by region chart
    if profit_col:
        plt.figure(figsize=(9, 5))
        sns.barplot(
            data=region_summary,
            x=region_col,
            y="total_profit"
        )
        plt.title("Profit by Region")
        plt.xlabel("Region")
        plt.ylabel("Profit (INR)")
        plt.xticks(rotation=30)
        plt.tight_layout()
        plt.savefig(CHARTS_DIR / "profit_by_region.png", dpi=150)
        plt.close()

# Monthly sales trend
if date_col:
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    monthly_df = df.dropna(subset=[date_col]).copy()

    if not monthly_df.empty:
        monthly_df["month"] = (
            monthly_df[date_col].dt.to_period("M").astype(str)
        )

        monthly_sales = (
            monthly_df.groupby("month")[sales_col]
            .sum()
            .reset_index()
            .sort_values("month")
        )

        plt.figure(figsize=(11, 5))
        sns.lineplot(
            data=monthly_sales,
            x="month",
            y=sales_col,
            marker="o"
        )
        plt.title("Monthly Sales Trend")
        plt.xlabel("Month")
        plt.ylabel("Sales (INR)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(
            CHARTS_DIR / "monthly_sales_trend.png", dpi=150
        )
        plt.close()

        # Product-month heatmap
        if product_col:
            heatmap_data = monthly_df.pivot_table(
                index=product_col,
                columns="month",
                values=sales_col,
                aggfunc="sum",
                fill_value=0
            )

            plt.figure(figsize=(12, 7))
            sns.heatmap(heatmap_data, cmap="YlGnBu")
            plt.title("Product vs Month Sales Heatmap")
            plt.xlabel("Month")
            plt.ylabel("Product")
            plt.tight_layout()
            plt.savefig(
                CHARTS_DIR / "product_month_heatmap.png", dpi=150
            )
            plt.close()

print("\nAnalysis complete!")
print(f"Summary files saved in: {OUTPUT_DIR}")
print(f"Charts saved in: {CHARTS_DIR}")
