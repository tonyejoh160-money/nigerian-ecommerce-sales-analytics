from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Locate the project folders.
PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = PROJECT_DIR / "data" / "ecommerce_sales_clean.csv"
OUTPUT_DIR = PROJECT_DIR / "visualizations"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Check that the dataset exists.
if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATA_FILE}\n"
        "Run python src/clean_data.py first."
    )

# Load and prepare the data.
df = pd.read_csv(DATA_FILE)

df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    errors="coerce"
)

# Only delivered orders are included in sales.
delivered = df[
    (df["Order_Status"] == "Delivered")
    & df["Order_Date"].notna()
].copy()

# Calculate monthly net revenue.
delivered["Month"] = (
    delivered["Order_Date"].dt.to_period("M").astype(str)
)

monthly_revenue = (
    delivered.groupby("Month")["Net_Revenue"]
    .sum()
    .reset_index()
)

# Configure chart appearance.
sns.set_theme(style="whitegrid")

plt.figure(figsize=(14, 7))

sns.lineplot(
    data=monthly_revenue,
    x="Month",
    y="Net_Revenue",
    marker="o",
    linewidth=2.5
)

plt.title(
    "Monthly Delivered Net Revenue",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Month", fontsize=12)
plt.ylabel("Net Revenue (₦)", fontsize=12)

plt.xticks(rotation=45)
plt.ticklabel_format(
    style="plain",
    axis="y"
)

plt.tight_layout()

# Save the chart.
output_file = OUTPUT_DIR / "monthly_revenue.png"

plt.savefig(
    output_file,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Monthly revenue chart created successfully.")
print(f"Saved to: {output_file}")