from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Locate project folders.
PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = PROJECT_DIR / "data" / "ecommerce_sales_clean.csv"
OUTPUT_DIR = PROJECT_DIR / "reports"
VISUAL_DIR = PROJECT_DIR / "visualizations"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
VISUAL_DIR.mkdir(parents=True, exist_ok=True)

# Check the dataset.
if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATA_FILE}"
    )

# Load data.
df = pd.read_csv(DATA_FILE)

# Analyze delivered orders only.
delivered = df[
    df["Order_Status"] == "Delivered"
].copy()

# Summarize product profitability.
profitability = (
    delivered.groupby("Product")
    .agg(
        Units_Sold=("Quantity", "sum"),
        Net_Revenue=("Net_Revenue", "sum"),
        Total_Cost=("Total_Cost", "sum"),
        Gross_Profit=("Gross_Profit", "sum"),
    )
    .reset_index()
)

# Calculate gross profit margin.
profitability["Profit_Margin_Percent"] = (
    profitability["Gross_Profit"]
    / profitability["Net_Revenue"].where(
        profitability["Net_Revenue"] != 0
    )
    * 100
).round(2)

# Rank products by gross profit.
profitability = profitability.sort_values(
    by="Gross_Profit",
    ascending=False
)

# Save the report.
report_file = OUTPUT_DIR / "product_profitability.csv"

profitability.to_csv(
    report_file,
    index=False
)

# Visualize the top 10 products.
top_products = profitability.head(10)

sns.set_theme(style="whitegrid")

plt.figure(figsize=(12, 7))

sns.barplot(
    data=top_products,
    x="Gross_Profit",
    y="Product"
)

plt.title(
    "Top 10 Products by Gross Profit",
    fontsize=15,
    fontweight="bold"
)

plt.xlabel("Gross Profit (₦)")
plt.ylabel("Product")

plt.ticklabel_format(
    style="plain",
    axis="x"
)

plt.tight_layout()

chart_file = VISUAL_DIR / "top_products_by_profit.png"

plt.savefig(
    chart_file,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# Display results.
print("=" * 55)
print("PRODUCT PROFITABILITY ANALYSIS")
print("=" * 55)

print(
    profitability.head(10).to_string(index=False)
)

print(f"\nReport saved to: {report_file}")
print(f"Chart saved to: {chart_file}")