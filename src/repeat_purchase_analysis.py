from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = PROJECT_DIR / "data" / "ecommerce_sales_clean.csv"
REPORT_DIR = PROJECT_DIR / "reports"
VISUAL_DIR = PROJECT_DIR / "visualizations"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
VISUAL_DIR.mkdir(parents=True, exist_ok=True)

if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATA_FILE}"
    )

df = pd.read_csv(DATA_FILE)

# Keep delivered orders only.
delivered = df[
    df["Order_Status"] == "Delivered"
].copy()

# Count delivered orders per customer.
customer_orders = (
    delivered.groupby("Customer_ID")
    .agg(
        Delivered_Orders=("Order_ID", "nunique"),
        Total_Net_Revenue=("Net_Revenue", "sum"),
    )
    .reset_index()
)

# Classify purchase frequency.
customer_orders["Purchase_Type"] = customer_orders[
    "Delivered_Orders"
].apply(
    lambda count: (
        "Repeat Customer"
        if count >= 2
        else "One-Time Customer"
    )
)

# Summarize customer purchasing behaviour.
purchase_summary = (
    customer_orders.groupby("Purchase_Type")
    .agg(
        Customers=("Customer_ID", "nunique"),
        Delivered_Orders=("Delivered_Orders", "sum"),
        Total_Net_Revenue=("Total_Net_Revenue", "sum"),
    )
    .reset_index()
)

total_customers_with_delivered_orders = (
    customer_orders["Customer_ID"].nunique()
)

purchase_summary["Customer_Percent"] = (
    purchase_summary["Customers"]
    / total_customers_with_delivered_orders
    * 100
).round(2)

# Save customer-level data.
customer_orders.to_csv(
    REPORT_DIR / "customer_purchase_frequency.csv",
    index=False
)

# Save summary.
purchase_summary.to_csv(
    REPORT_DIR / "repeat_purchase_summary.csv",
    index=False
)

print("=" * 60)
print("REPEAT PURCHASE ANALYSIS")
print("=" * 60)

print("\nCustomer purchase summary:")
print(purchase_summary.to_string(index=False))

repeat_customers = customer_orders[
    customer_orders["Delivered_Orders"] >= 2
]["Customer_ID"].nunique()

if total_customers_with_delivered_orders > 0:
    repeat_rate = (
        repeat_customers
        / total_customers_with_delivered_orders
        * 100
    )
else:
    repeat_rate = 0

print(
    "\nCustomers with delivered orders:",
    total_customers_with_delivered_orders
)

print(
    "Customers with multiple delivered orders:",
    repeat_customers
)

print(f"Repeat customer rate: {repeat_rate:.2f}%")

# Create a customer-count chart.
sns.set_theme(style="whitegrid")

plt.figure(figsize=(9, 6))

sns.barplot(
    data=purchase_summary,
    x="Purchase_Type",
    y="Customers"
)

plt.title(
    "One-Time vs Repeat Customers",
    fontsize=15,
    fontweight="bold"
)

plt.xlabel("Customer Type")
plt.ylabel("Number of Customers")

plt.tight_layout()

chart_file = VISUAL_DIR / "repeat_customers.png"

plt.savefig(
    chart_file,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    "\nCustomer frequency report saved to: "
    f"{REPORT_DIR / 'customer_purchase_frequency.csv'}"
)
print(
    "Summary saved to: "
    f"{REPORT_DIR / 'repeat_purchase_summary.csv'}"
)
print(f"Chart saved to: {chart_file}")