from pathlib import Path

import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = PROJECT_DIR / "data" / "ecommerce_sales.csv"

df = pd.read_csv(DATA_FILE)

print("=" * 55)
print("ORDER STATUS ANALYSIS")
print("=" * 55)

# Count orders by status.
status_counts = df["Order_Status"].value_counts()

print("\nOrders by status:")
print(status_counts)

# Calculate the percentage of orders in each status.
status_percentages = (
    df["Order_Status"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

print("\nPercentage by status:")
print(status_percentages)

# Separate delivered orders from other statuses.
delivered = df[df["Order_Status"] == "Delivered"]

cancelled = df[df["Order_Status"] == "Cancelled"]

returned = df[df["Order_Status"] == "Returned"]

print("\nFinancial summary:")
print(f"All order records: {len(df):,}")
print(f"Delivered orders: {len(delivered):,}")
print(f"Cancelled orders: {len(cancelled):,}")
print(f"Returned orders: {len(returned):,}")

print(
    "\nDelivered-order net revenue: NGN "
    f"{delivered['Net_Revenue'].sum():,.2f}"
)

print(
    "Cancelled-order recorded value: NGN "
    f"{cancelled['Net_Revenue'].sum():,.2f}"
)

print(
    "Returned-order recorded value: NGN "
    f"{returned['Net_Revenue'].sum():,.2f}"
)