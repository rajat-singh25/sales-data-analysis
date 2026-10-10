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
    plt
