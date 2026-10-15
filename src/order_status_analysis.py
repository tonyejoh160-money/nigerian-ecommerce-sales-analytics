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

# Summarize all recorded orders by status.
status_summary = (
    df.groupby("Order_Status")
    .agg(
        Total_Orders=("Order_ID", "nunique"),
        Net_Revenue_Recorded=("Net_Revenue", "sum"),
    )
    .reset_index()
)

total_orders = status_summary["Total_Orders"].sum()

status_summary["Percentage"] = (
    status_summary["Total_Orders"]
    / total_orders
    * 100
).round(2)

status_summary = status_summary.sort_values(
    by="Total_Orders",
    ascending=False
)

# Save the report.
report_file = OUTPUT_DIR / "order_status_analysis.csv"

status_summary.to_csv(
    report_file,
    index=False
)

# Visualize order counts.
sns.set_theme(style="whitegrid")

plt.figure(figsize=(10, 6))

sns.barplot(
    data=status_summary,
    x="Order_Status",
    y="Total_Orders"
)

plt.title(
    "Order Status Distribution",
    fontsize=15,
    fontweight="bold"
)

plt.xlabel("Order Status")
plt.ylabel("Number of Orders")

plt.xticks(rotation=20)

plt.tight_layout()

chart_file = VISUAL_DIR / "order_status_distribution.png"

plt.savefig(
    chart_file,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# Display results.
print("=" * 55)
print("ORDER STATUS ANALYSIS")
print("=" * 55)

print(status_summary.to_string(index=False))

print(f"\nTotal recorded orders: {total_orders:,}")

print(
    "\nDelivered order percentage:",
    f"{status_summary.loc[status_summary['Order_Status'] == 'Delivered', 'Percentage'].sum():.2f}%"
)

print(
    "Cancelled order percentage:",
    f"{status_summary.loc[status_summary['Order_Status'] == 'Cancelled', 'Percentage'].sum():.2f}%"
)

print(
    "Returned order percentage:",
    f"{status_summary.loc[status_summary['Order_Status'] == 'Returned', 'Percentage'].sum():.2f}%"
)

print(f"\nReport saved to: {report_file}")
print(f"Chart saved to: {chart_file}")