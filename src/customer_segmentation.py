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

df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    errors="coerce"
)

# Keep delivered orders with valid dates.
delivered = df[
    (df["Order_Status"] == "Delivered")
    & df["Order_Date"].notna()
].copy()

if delivered.empty:
    raise ValueError(
        "No valid delivered orders are available for RFM analysis."
    )

# Use the day after the latest observed order as the reference date.
reference_date = (
    delivered["Order_Date"].max().normalize()
    + pd.Timedelta(days=1)
)

# Calculate RFM metrics per customer.
rfm = (
    delivered.groupby("Customer_ID")
    .agg(
        Last_Purchase=("Order_Date", "max"),
        Frequency=("Order_ID", "nunique"),
        Monetary=("Net_Revenue", "sum"),
    )
    .reset_index()
)

rfm["Recency"] = (
    reference_date - rfm["Last_Purchase"]
).dt.days

# Score each metric from 1 to 5.
# Higher recency scores mean more recent purchases.
rfm["R_Score"] = pd.qcut(
    rfm["Recency"].rank(method="first", ascending=False),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

rfm["M_Score"] = pd.qcut(
    rfm["Monetary"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

rfm["RFM_Score"] = (
    rfm["R_Score"].astype(str)
    + rfm["F_Score"].astype(str)
    + rfm["M_Score"].astype(str)
)

# Assign understandable customer segments.
def assign_segment(row):
    if row["R_Score"] >= 4 and row["F_Score"] >= 4:
        return "Loyal / Recent"

    if row["R_Score"] >= 4 and row["M_Score"] >= 4:
        return "Recent High Spenders"

    if row["R_Score"] <= 2 and row["F_Score"] >= 4:
        return "Previously Loyal / Inactive"

    if row["R_Score"] <= 2:
        return "At Risk / Inactive"

    if row["F_Score"] <= 2 and row["R_Score"] >= 3:
        return "New or Occasional"

    return "Regular Customers"


rfm["Customer_Segment"] = rfm.apply(
    assign_segment,
    axis=1
)

# Save customer-level RFM results.
report_file = REPORT_DIR / "customer_rfm_segments.csv"

rfm.to_csv(report_file, index=False)

# Summarize the segments.
segment_summary = (
    rfm.groupby("Customer_Segment")
    .agg(
        Customers=("Customer_ID", "nunique"),
        Total_Revenue=("Monetary", "sum"),
        Average_Recency_Days=("Recency", "mean"),
        Average_Frequency=("Frequency", "mean"),
    )
    .reset_index()
)

segment_summary["Revenue_Percent"] = (
    segment_summary["Total_Revenue"]
    / segment_summary["Total_Revenue"].sum()
    * 100
).round(2)

segment_summary.to_csv(
    REPORT_DIR / "customer_segment_summary.csv",
    index=False
)

print("=" * 60)
print("CUSTOMER RFM SEGMENTATION")
print("=" * 60)

print(f"Reference date: {reference_date.date()}")

print("\nSegment summary:")
print(segment_summary.to_string(index=False))

# Visualize customer counts by segment.
sns.set_theme(style="whitegrid")

plt.figure(figsize=(12, 7))

sns.barplot(
    data=segment_summary.sort_values("Customers", ascending=False),
    x="Customers",
    y="Customer_Segment"
)

plt.title(
    "Customer Segments by Number of Customers",
    fontsize=15,
    fontweight="bold"
)

plt.xlabel("Number of Customers")
plt.ylabel("Customer Segment")

plt.tight_layout()

chart_file = VISUAL_DIR / "customer_segments.png"

plt.savefig(
    chart_file,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(f"\nCustomer report saved to: {report_file}")
print(
    "Segment summary saved to: "
    f"{REPORT_DIR / 'customer_segment_summary.csv'}"
)
print(f"Chart saved to: {chart_file}")