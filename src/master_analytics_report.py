from pathlib import Path

import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = PROJECT_DIR / "data" / "ecommerce_sales_clean.csv"
REPORT_DIR = PROJECT_DIR / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATA_FILE}"
    )

df = pd.read_csv(DATA_FILE)

df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    errors="coerce"
)

# Use delivered orders for sales metrics.
delivered = df[
    (df["Order_Status"] == "Delivered")
    & df["Order_Date"].notna()
].copy()

total_records = len(df)

total_customers = df["Customer_ID"].nunique()

delivered_orders = delivered["Order_ID"].nunique()

delivered_customers = delivered["Customer_ID"].nunique()

total_revenue = delivered["Net_Revenue"].sum()

total_cost = delivered["Total_Cost"].sum()

total_profit = delivered["Gross_Profit"].sum()

total_units = delivered["Quantity"].sum()

if total_revenue > 0:
    profit_margin = total_profit / total_revenue * 100
else:
    profit_margin = 0

if delivered_orders > 0:
    average_order_value = total_revenue / delivered_orders
else:
    average_order_value = 0

# Calculate repeat purchase rate.
customer_frequency = (
    delivered.groupby("Customer_ID")["Order_ID"]
    .nunique()
)

repeat_customers = int(
    (customer_frequency >= 2).sum()
)

if delivered_customers > 0:
    repeat_purchase_rate = (
        repeat_customers / delivered_customers * 100
    )
else:
    repeat_purchase_rate = 0

# Identify top-performing products and states.
if not delivered.empty:
    product_revenue = (
        delivered.groupby("Product")["Net_Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    state_revenue = (
        delivered.groupby("State")["Net_Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    category_revenue = (
        delivered.groupby("Category")["Net_Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    top_product = product_revenue.index[0]
    top_product_revenue = product_revenue.iloc[0]

    top_state = state_revenue.index[0]
    top_state_revenue = state_revenue.iloc[0]

    top_category = category_revenue.index[0]
    top_category_revenue = category_revenue.iloc[0]

else:
    top_product = "N/A"
    top_product_revenue = 0

    top_state = "N/A"
    top_state_revenue = 0

    top_category = "N/A"
    top_category_revenue = 0

# Calculate order status percentages.
status_counts = df["Order_Status"].value_counts()

if total_records > 0:
    delivered_percentage = (
        status_counts.get("Delivered", 0)
        / total_records
        * 100
    )

    cancelled_percentage = (
        status_counts.get("Cancelled", 0)
        / total_records
        * 100
    )

    returned_percentage = (
        status_counts.get("Returned", 0)
        / total_records
        * 100
    )
else:
    delivered_percentage = 0
    cancelled_percentage = 0
    returned_percentage = 0

# Build a single metrics table.
metrics = [
    ("Total_Order_Records", total_records),
    ("Unique_Customers", total_customers),
    ("Delivered_Orders", delivered_orders),
    ("Customers_With_Delivered_Orders", delivered_customers),
    ("Delivered_Units_Sold", total_units),
    ("Delivered_Net_Revenue_NGN", round(total_revenue, 2)),
    ("Delivered_Product_Cost_NGN", round(total_cost, 2)),
    ("Delivered_Gross_Profit_NGN", round(total_profit, 2)),
    ("Gross_Profit_Margin_Percent", round(profit_margin, 2)),
    ("Average_Order_Value_NGN", round(average_order_value, 2)),
    ("Repeat_Purchase_Rate_Percent", round(repeat_purchase_rate, 2)),
    ("Delivered_Order_Percent", round(delivered_percentage, 2)),
    ("Cancelled_Order_Percent", round(cancelled_percentage, 2)),
    ("Returned_Order_Percent", round(returned_percentage, 2)),
    ("Top_Product", top_product),
    ("Top_Product_Net_Revenue_NGN", round(top_product_revenue, 2)),
    ("Top_State", top_state),
    ("Top_State_Net_Revenue_NGN", round(top_state_revenue, 2)),
    ("Top_Category", top_category),
    ("Top_Category_Net_Revenue_NGN", round(top_category_revenue, 2)),
]

master_report = pd.DataFrame(
    metrics,
    columns=["Metric", "Value"]
)

report_file = REPORT_DIR / "master_analytics_report.csv"

master_report.to_csv(
    report_file,
    index=False
)

print("=" * 60)
print("MASTER ANALYTICS REPORT")
print("=" * 60)

print(master_report.to_string(index=False))

print(f"\nReport saved to: {report_file}")

print(
    "\nNote: The dataset is synthetic. "
    "Delivered-order financial metrics use a simplifying "
    "analytical assumption and are not audited accounting figures."
)