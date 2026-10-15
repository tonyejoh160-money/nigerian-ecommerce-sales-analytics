from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "ecommerce_sales_clean.csv"

df = pd.read_csv(DATA_FILE)
df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")

print("=" * 55)
print("COMPREHENSIVE DATA VALIDATION")
print("=" * 55)

# 1. Dataset size
print("\n1. Dataset size:")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")

# 2. Missing values
print("\n2. Missing values:")
missing = df.isnull().sum()
print(missing[missing > 0] if missing.any() else "No missing values found.")

# 3. Duplicate records
print("\n3. Duplicate records:")
print(f"Duplicate rows: {df.duplicated().sum()}")
print(f"Duplicate Order_IDs: {df['Order_ID'].duplicated().sum()}")

# 4. Invalid quantities and prices
print("\n4. Invalid numerical values:")
print(f"Quantity <= 0: {(df['Quantity'] <= 0).sum()}")
print(f"Unit price <= 0: {(df['Unit_Price'] <= 0).sum()}")
print(f"Unit cost < 0: {(df['Unit_Cost'] < 0).sum()}")

# 5. Discount validation
print("\n5. Discount validation:")
invalid_discount = (
    (df["Discount_Rate"] < 0)
    | (df["Discount_Rate"] > 1)
)
print(f"Invalid discount rates: {invalid_discount.sum()}")

# 6. Order status validation
print("\n6. Order statuses:")
print(df["Order_Status"].value_counts(dropna=False))

allowed_statuses = {
    "Delivered",
    "Shipped",
    "Processing",
    "Cancelled",
    "Returned",
}

invalid_statuses = ~df["Order_Status"].isin(allowed_statuses)
print(f"Invalid order statuses: {invalid_statuses.sum()}")

# 7. Date validation
print("\n7. Order dates:")
print(f"Invalid dates: {df['Order_Date'].isna().sum()}")

if df["Order_Date"].notna().any():
    print(f"Earliest date: {df['Order_Date'].min().date()}")
    print(f"Latest date: {df['Order_Date'].max().date()}")

# 8. Financial validation
print("\n8. Financial validation:")

expected_gross = (df["Quantity"] * df["Unit_Price"]).round(2)
expected_discount = (
    expected_gross * df["Discount_Rate"]
).round(2)
expected_net = (expected_gross - expected_discount).round(2)
expected_cost = (df["Quantity"] * df["Unit_Cost"]).round(2)
expected_profit = (expected_net - expected_cost).round(2)

print(
    "Incorrect gross revenue:",
    (~(df["Gross_Revenue"].round(2) == expected_gross)).sum(),
)
print(
    "Incorrect discount amount:",
    (~(df["Discount_Amount"].round(2) == expected_discount)).sum(),
)
print(
    "Incorrect net revenue:",
    (~(df["Net_Revenue"].round(2) == expected_net)).sum(),
)
print(
    "Incorrect total cost:",
    (~(df["Total_Cost"].round(2) == expected_cost)).sum(),
)
print(
    "Incorrect gross profit:",
    (~(df["Gross_Profit"].round(2) == expected_profit)).sum(),
)

print("\nValidation completed.")