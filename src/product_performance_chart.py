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

# Keep delivered orders.
delivered = df[
    df["Order_Status"] == "Delivered"
].copy()

# Rank products by net revenue.
product_revenue = (
    delivered.groupby("Product")["Net_Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

sns.set_theme(style="whitegrid")

plt.figure(figsize=(12, 7))

sns.barplot(
    data=product_revenue,
    x="Net_Revenue",
    y="Product"
)

plt.title(
    "Top 10 Products by Delivered Net Revenue",
    fontsize=15,
    fontweight="bold"
)

plt.xlabel("Net Revenue (₦)")
plt.ylabel("Product")

plt.ticklabel_format(
    style="plain",
    axis="x"
)

plt.tight_layout()

output_file = OUTPUT_DIR / "top_products.png"

plt.savefig(
    output_file,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Top-products chart created successfully.")
print(f"Saved to: {output_file}")

print("\nTop 10 products:")
print(product_revenue.to_string(index=False))