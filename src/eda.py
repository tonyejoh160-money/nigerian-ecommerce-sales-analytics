from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "ecommerce_sales_clean.csv"

df = pd.read_csv(DATA_FILE)
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

# Define completed sales for this project's analysis.
# This is a simplifying assumption for our synthetic dataset.
delivered = df[df["Order_Status"] == "Delivered"].copy()

print("=" * 55)
print("NIGERIAN E-COMMERCE SALES ANALYTICS")
print("EXPLORATORY DATA ANALYSIS")
print("=" * 55)

print("\n1. GENERAL DATASET INFORMATION")
print(f"Total order records: {len(df):,}")
print(f"Unique customers: {df['Customer_ID'].nunique():,}")
print(f"Unique products: {df['Product'].nunique():,}")
print(f"Number of states/territories: {df['State'].nunique():,}")

print("\n2. ORDER STATUS DISTRIBUTION")
print(df["Order_Status"].value_counts())

print("\n3. DELIVERED SALES SUMMARY")
print(f"Delivered orders: {len(delivered):,}")
print(f"Delivered net revenue: ₦{delivered['Net_Revenue'].sum():,.2f}")
print(f"Delivered product cost: ₦{delivered['Total_Cost'].sum():,.2f}")
print(f"Delivered gross profit: ₦{delivered['Gross_Profit'].sum():,.2f}")

if len(delivered) > 0:
    print(
        "Average net revenue per delivered order: "
        f"₦{delivered['Net_Revenue'].mean():,.2f}"
    )

print("\n4. TOP 10 PRODUCTS BY DELIVERED NET REVENUE")
print(
    delivered.groupby("Product")["Net_Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .to_string()
)

print("\n5. TOP 10 STATES BY DELIVERED NET REVENUE")
print(
    delivered.groupby("State")["Net_Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .to_string()
)

print("\n6. REVENUE BY PRODUCT CATEGORY")
print(
    delivered.groupby("Category")["Net_Revenue"]
    .sum()
    .sort_values(ascending=False)
    .to_string()
)

print("\n7. PAYMENT METHODS FOR DELIVERED ORDERS")
print(delivered["Payment_Method"].value_counts().to_string())

print("\nEDA completed successfully.")