from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

PROJECT_DIR = Path(__file__).resolve().parent.parent

SALES_FILE = PROJECT_DIR / "data" / "ecommerce_sales_clean.csv"
CUSTOMERS_FILE = PROJECT_DIR / "data" / "customers.csv"

OUTPUT_DIR = PROJECT_DIR / "reports"
VISUAL_DIR = PROJECT_DIR / "visualizations"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
VISUAL_DIR.mkdir(parents=True, exist_ok=True)

if not SALES_FILE.exists():
    raise FileNotFoundError(
        f"Sales dataset not found: {SALES_FILE}"
    )

if not CUSTOMERS_FILE.exists():
    raise FileNotFoundError(
        f"Customer dataset not found: {CUSTOMERS_FILE}"
    )

# Load datasets.
sales = pd.read_csv(SALES_FILE)
customers = pd.read_csv(CUSTOMERS_FILE)

# Keep delivered orders.
delivered = sales[
    sales["Order_Status"] == "Delivered"
].copy()

# Calculate customer purchasing metrics.
customer_summary = (
    delivered.groupby("Customer_ID")
    .agg(
        Delivered_Orders=("Order_ID", "nunique"),
        Units_Purchased=("Quantity", "sum"),
        Total_Net_Revenue=("Net_Revenue", "sum"),
        Total_Gross_Profit=("Gross_Profit", "sum"),
    )
    .reset_index()
)

# Calculate average revenue per delivered order.
customer_summary["Average_Order_Value"] = (
    customer_summary["Total_Net_Revenue"]
    / customer_summary["Delivered_Orders"]
).round(2)

# Add customer names.
customer_summary = customer_summary.merge(
    customers,
    on="Customer_ID",
    how="left"
)

# Rank customers by delivered net revenue.
customer_summary = customer_summary.sort_values(
    by="Total_Net_Revenue",
    ascending=False
)

# Save customer-level results.
report_file = OUTPUT_DIR / "customer_analysis.csv"

customer_summary.to_csv(
    report_file,
    index=False
)

# Prepare the top 10 customers for a chart.
top_customers = customer_summary.head(10).copy()

# Use customer IDs on the chart to keep labels readable.
sns.set_theme(style="whitegrid")

plt.figure(figsize=(12, 7))

sns.barplot(
    data=top_customers,
    x="Total_Net_Revenue",
    y="Customer_ID"
)

plt.title(
    "Top 10 Customers by Delivered Net Revenue",
    fontsize=15,
    fontweight="bold"
)

plt.xlabel("Delivered Net Revenue (₦)")
plt.ylabel("Customer ID")

plt.ticklabel_format(
    style="plain",
    axis="x"
)

plt.tight_layout()

chart_file = VISUAL_DIR / "top_customers.png"

plt.savefig(
    chart_file,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# Print results.
print("=" * 55)
print("CUSTOMER PURCHASING ANALYSIS")
print("=" * 55)

print(
    customer_summary.head(10).to_string(index=False)
)

print(
    "\nCustomers with at least one delivered order:",
    customer_summary["Customer_ID"].nunique()
)

print(f"\nReport saved to: {report_file}")
print(f"Chart saved to: {chart_file}")