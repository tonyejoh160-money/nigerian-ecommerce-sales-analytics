from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = PROJECT_DIR / "data" / "ecommerce_sales_clean.csv"
OUTPUT_DIR = PROJECT_DIR / "reports"
VISUAL_DIR = PROJECT_DIR / "visualizations"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
VISUAL_DIR.mkdir(parents=True, exist_ok=True)

if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATA_FILE}"
    )

df = pd.read_csv(DATA_FILE)

# Calculate overall order counts by payment method.
payment_orders = (
    df.groupby("Payment_Method")
    .agg(
        Total_Orders=("Order_ID", "nunique"),
        Unique_Customers=("Customer_ID", "nunique"),
    )
    .reset_index()
)

# Calculate the delivered-order revenue by payment method.
delivered = df[
    df["Order_Status"] == "Delivered"
].copy()

payment_revenue = (
    delivered.groupby("Payment_Method")
    .agg(
        Delivered_Orders=("Order_ID", "nunique"),
        Net_Revenue=("Net_Revenue", "sum"),
        Gross_Profit=("Gross_Profit", "sum"),
    )
    .reset_index()
)

# Combine the order and revenue summaries.
payment_summary = payment_orders.merge(
    payment_revenue,
    on="Payment_Method",
    how="left"
)

payment_summary = payment_summary.fillna(0)

# Calculate each method's share of all recorded orders.
total_orders = payment_summary["Total_Orders"].sum()

payment_summary["Order_Share_Percent"] = (
    payment_summary["Total_Orders"]
    / total_orders
    * 100
).round(2)

payment_summary = payment_summary.sort_values(
    by="Total_Orders",
    ascending=False
)

# Save results.
report_file = OUTPUT_DIR / "payment_analysis.csv"

payment_summary.to_csv(
    report_file,
    index=False
)

# Create a chart of order counts.
sns.set_theme(style="whitegrid")

plt.figure(figsize=(11, 6))

sns.barplot(
    data=payment_summary,
    x="Payment_Method",
    y="Total_Orders"
)

plt.title(
    "Orders by Payment Method",
    fontsize=15,
    fontweight="bold"
)

plt.xlabel("Payment Method")
plt.ylabel("Number of Orders")

plt.xticks(rotation=25, ha="right")

plt.tight_layout()

chart_file = VISUAL_DIR / "payment_methods.png"

plt.savefig(
    chart_file,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("=" * 55)
print("PAYMENT METHOD ANALYSIS")
print("=" * 55)

print(payment_summary.to_string(index=False))

print(f"\nReport saved to: {report_file}")
print(f"Chart saved to: {chart_file}")