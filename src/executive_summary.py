from pathlib import Path

import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = PROJECT_DIR / "data" / "ecommerce_sales_clean.csv"
OUTPUT_DIR = PROJECT_DIR / "reports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATA_FILE}"
    )

df = pd.read_csv(DATA_FILE)

df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    errors="coerce"
)

# Select delivered orders for the main sales metrics.
delivered = df[
    df["Order_Status"] == "Delivered"
].copy()

# Calculate business metrics.
total_records = len(df)
delivered_orders = delivered["Order_ID"].nunique()

unique_customers = df["Customer_ID"].nunique()
delivered_customers = delivered["Customer_ID"].nunique()

total_units = delivered["Quantity"].sum()

total_revenue = delivered["Net_Revenue"].sum()
total_cost = delivered["Total_Cost"].sum()
total_profit = delivered["Gross_Profit"].sum()

if total_revenue != 0:
    profit_margin = total_profit / total_revenue * 100
else:
    profit_margin = 0

if delivered_orders > 0:
    average_order_value = total_revenue / delivered_orders
else:
    average_order_value = 0

# Identify the top state.
if not delivered.empty:
    state_revenue = (
        delivered.groupby("State")["Net_Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    top_state = state_revenue.index[0]
    top_state_revenue = state_revenue.iloc[0]

    # Identify the top product.
    product_revenue = (
        delivered.groupby("Product")["Net_Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    top_product = product_revenue.index[0]
    top_product_revenue = product_revenue.iloc[0]

    # Identify the top category.
    category_revenue = (
        delivered.groupby("Category")["Net_Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    top_category = category_revenue.index[0]
    top_category_revenue = category_revenue.iloc[0]

else:
    top_state = "N/A"
    top_state_revenue = 0

    top_product = "N/A"
    top_product_revenue = 0

    top_category = "N/A"
    top_category_revenue = 0

# Count order statuses.
status_counts = df["Order_Status"].value_counts()

# Calculate percentages using all recorded order records.
status_percentages = (
    df["Order_Status"]
    .value_counts(normalize=True)
    .mul(100)
)

delivered_percentage = status_percentages.get("Delivered", 0)
cancelled_percentage = status_percentages.get("Cancelled", 0)
returned_percentage = status_percentages.get("Returned", 0)

# Create the report.
report = f"""
===========================================================
NIGERIAN E-COMMERCE SALES ANALYTICS
EXECUTIVE SUMMARY
===========================================================

DATASET OVERVIEW
----------------
Total order records: {total_records:,}
Unique customers: {unique_customers:,}
Customers with delivered orders: {delivered_customers:,}
Total delivered units sold: {total_units:,}

DELIVERED SALES PERFORMANCE
---------------------------
Delivered orders: {delivered_orders:,}
Delivered net revenue: NGN {total_revenue:,.2f}
Delivered product cost: NGN {total_cost:,.2f}
Delivered gross profit: NGN {total_profit:,.2f}
Gross profit margin: {profit_margin:.2f}%
Average net revenue per delivered order: NGN {average_order_value:,.2f}

TOP PERFORMERS
--------------
Top state by delivered net revenue:
{top_state} — NGN {top_state_revenue:,.2f}

Top product by delivered net revenue:
{top_product} — NGN {top_product_revenue:,.2f}

Top category by delivered net revenue:
{top_category} — NGN {top_category_revenue:,.2f}

ORDER STATUS
------------
Delivered: {status_counts.get("Delivered", 0):,} ({delivered_percentage:.2f}%)
Cancelled: {status_counts.get("Cancelled", 0):,} ({cancelled_percentage:.2f}%)
Returned: {status_counts.get("Returned", 0):,} ({returned_percentage:.2f}%)

METHODOLOGY AND LIMITATIONS
---------------------------
1. The dataset is synthetically generated for educational purposes.
2. Sales metrics in this report use delivered orders only.
3. Gross profit is net revenue minus recorded product cost.
4. Profit margin is gross profit divided by net revenue.
5. The dataset does not establish actual Nigerian market performance.
6. The results are not a substitute for audited financial statements.

===========================================================
END OF REPORT
===========================================================
"""

# Save report.
report_file = OUTPUT_DIR / "executive_summary.txt"

with open(report_file, "w", encoding="utf-8") as file:
    file.write(report)

print(report)
print(f"\nExecutive summary saved to: {report_file}")