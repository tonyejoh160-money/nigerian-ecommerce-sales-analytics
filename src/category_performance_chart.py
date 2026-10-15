from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = PROJECT_DIR / "data" / "ecommerce_sales_clean.csv"
OUTPUT_DIR = PROJECT_DIR / "visualizations"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATA_FILE}"
    )

df = pd.read_csv(DATA_FILE)

# Analyze delivered orders only.
delivered = df[
    df["Order_Status"] == "Delivered"
].copy()

# Calculate revenue by category.
category_revenue = (
    delivered.groupby("Category")["Net_Revenue"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

sns.set_theme(style="whitegrid")

plt.figure(figsize=(11, 7))

sns.barplot(
    data=category_revenue,
    x="Category",
    y="Net_Revenue"
)

plt.title(
    "Delivered Net Revenue by Product Category",
    fontsize=15,
    fontweight="bold"
)

plt.xlabel("Product Category")
plt.ylabel("Net Revenue (₦)")

plt.xticks(
    rotation=30,
    ha="right"
)

plt.ticklabel_format(
    style="plain",
    axis="y"
)

plt.tight_layout()

output_file = OUTPUT_DIR / "category_performance.png"

plt.savefig(
    output_file,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Category performance chart created successfully.")
print(f"Saved to: {output_file}")

print("\nRevenue by category:")
print(category_revenue.to_string(index=False))