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

# Load the dataset.
df = pd.read_csv(DATA_FILE)

df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    errors="coerce"
)

# Use delivered orders for sales analysis.
delivered = df[
    (df["Order_Status"] == "Delivered")
    & df["Order_Date"].notna()
].copy()

# Aggregate monthly sales.
delivered["Month"] = (
    delivered["Order_Date"]
    .dt.to_period("M")
    .dt.to_timestamp()
)

monthly = (
    delivered.groupby("Month")
    .agg(
        Delivered_Orders=("Order_ID", "nunique"),
        Net_Revenue=("Net_Revenue", "sum"),
        Gross_Profit=("Gross_Profit", "sum"),
    )
    .reset_index()
    .sort_values("Month")
)

# Calculate month-over-month revenue change.
monthly["Previous_Month_Revenue"] = (
    monthly["Net_Revenue"].shift(1)
)

monthly["Revenue_Change"] = (
    monthly["Net_Revenue"]
    - monthly["Previous_Month_Revenue"]
)

monthly["Revenue_Growth_Percent"] = (
    monthly["Revenue_Change"]
    / monthly["Previous_Month_Revenue"].where(
        monthly["Previous_Month_Revenue"] != 0
    )
    * 100
).round(2)

# Save results.
report_file = REPORT_DIR / "revenue_growth_analysis.csv"

monthly.to_csv(report_file, index=False)

# Identify the highest- and lowest-revenue months.
highest_month = monthly.loc[
    monthly["Net_Revenue"].idxmax()
]

lowest_month = monthly.loc[
    monthly["Net_Revenue"].idxmin()
]

print("=" * 60)
print("MONTHLY REVENUE GROWTH ANALYSIS")
print("=" * 60)

print(monthly.to_string(index=False))

print("\nHighest-revenue month:")
print(
    f"{highest_month['Month'].strftime('%Y-%m')}: "
    f"NGN {highest_month['Net_Revenue']:,.2f}"
)

print("\nLowest-revenue month:")
print(
    f"{lowest_month['Month'].strftime('%Y-%m')}: "
    f"NGN {lowest_month['Net_Revenue']:,.2f}"
)

# Create a revenue trend chart.
sns.set_theme(style="whitegrid")

plt.figure(figsize=(13, 7))

sns.lineplot(
    data=monthly,
    x="Month",
    y="Net_Revenue",
    marker="o",
    linewidth=2.5
)

plt.title(
    "Monthly Delivered Net Revenue Trend",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Month")
plt.ylabel("Net Revenue (NGN)")

plt.xticks(rotation=45)

plt.ticklabel_format(
    style="plain",
    axis="y"
)

plt.tight_layout()

chart_file = VISUAL_DIR / "revenue_growth_trend.png"

plt.savefig(
    chart_file,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(f"\nReport saved to: {report_file}")
print(f"Chart saved to: {chart_file}")