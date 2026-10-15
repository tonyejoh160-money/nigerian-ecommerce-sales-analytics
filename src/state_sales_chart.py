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

# Calculate revenue by state.
state_revenue = (
    delivered.groupby("State")["Net_Revenue"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

sns.set_theme(style="whitegrid")

plt.figure(figsize=(12, 8))

sns.barplot(
    data=state_revenue,
    x="Net_Revenue",
    y="State"
)

plt.title(
    "Delivered Net Revenue by State",
    fontsize=15,
    fontweight="bold"
)

plt.xlabel("Net Revenue (₦)")
plt.ylabel("State / Territory")

plt.ticklabel_format(
    style="plain",
    axis="x"
)

plt.tight_layout()

output_file = OUTPUT_DIR / "state_sales.png"

plt.savefig(
    output_file,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("State sales chart created successfully.")
print(f"Saved to: {output_file}")

print("\nRevenue by state:")
print(state_revenue.to_string(index=False))