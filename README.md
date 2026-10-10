# Sales Data Analysis

A beginner-friendly data analytics portfolio project using Python, Pandas, Matplotlib, and Seaborn.

> **Dataset note:** `data/sales.csv` is a synthetic sample dataset generated for demonstration and learning. It is not real company/customer data. Monetary values are in Indian Rupees (INR).

## Business Questions
- What are total sales, estimated profit, and profit margin?
- Which products contribute the most sales?
- Which regions generate the most estimated profit?
- How do sales change month by month?
- How do product sales vary across months?

## Tech Stack
- Python
- Pandas and NumPy
- Matplotlib and Seaborn
- CSV data processing

## Project Structure
```text
sales-data-analysis/
├── data/sales.csv
├── src/analysis.py
├── outputs/charts/
├── outputs/product_summary.csv
├── outputs/region_summary.csv
├── requirements.txt
└── README.md
```

## Run Locally
```bash
pip install -r requirements.txt
python src/analysis.py
```

The script prints a sales summary, creates charts in `outputs/charts/`, and exports product/region summary CSVs into `outputs/`.

## Key Metrics
- Number of orders
- Units sold
- Total sales (INR)
- Estimated profit (INR)
- Average order value
- Estimated profit margin

## Important Assumptions
- One row represents one order line; an order ID is unique per row in this sample.
- Estimated cost is calculated from fixed illustrative cost ratios by product.
- Profit is an estimate based on sales minus estimated cost, not audited financial data.
- The dataset is randomly generated and should not be represented as actual business performance.

## Possible Improvements
- Add a Power BI dashboard
- Add automated data-quality checks and unit tests
- Compare sales channels and discount levels
- Build a Streamlit dashboard

- ---

## 📊 Project Visualizations

The project generates charts to explore sales performance, product contributions, regional performance, and monthly trends.

### 1. Sales by Product
![Sales by Product](outputs/charts/sales_by_product.png)

### 2. Profit by Region
![Profit by Region](outputs/charts/profit_by_region.png)

### 3. Monthly Sales Trend
![Monthly Sales Trend](outputs/charts/monthly_sales_trend.png)

### 4. Product Month Heatmap
![Product Month Heatmap ](outputs/charts/product_month_heatmap.png)

---

## 📁 Generated Reports

- [Product Summary CSV](outputs/product_summary.csv)
- [Region Summary CSV](outputs/region_summary.csv)

---
