from pathlib import Path

import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = PROJECT_DIR / "data" / "ecommerce_sales_clean.csv"
REPORT_DIR = PROJECT_DIR / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATA_FILE}"
    )

df = pd.read_csv(DATA_FILE)

# Convert dates for validation.
df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    errors="coerce"
)

# Store data-quality checks.
checks = []

def add_check(name, failed_rows, total_rows, details):
    failed_rows = int(failed_rows)

    if total_rows > 0:
        failure_percent = failed_rows / total_rows * 100
    else:
        failure_percent = 0

    checks.append(
        {
            "Check": name,
            "Failed_Rows": failed_rows,
            "Total_Rows": int(total_rows),
            "Failure_Percent": round(failure_percent, 2),
            "Details": details,
            "Status": (
                "PASS"
                if failed_rows == 0
                else "REVIEW"
            ),
        }
    )


# 1. Duplicate records.
add_check(
    "Duplicate rows",
    df.duplicated().sum(),
    len(df),
    "Entire row should be unique."
)

# 2. Duplicate order IDs.
add_check(
    "Duplicate Order_ID",
    df["Order_ID"].duplicated().sum(),
    len(df),
    "Each order should have a unique ID."
)

# 3. Missing required values.
required_columns = [
    "Order_ID",
    "Order_Date",
    "Customer_ID",
    "Product",
    "Category",
    "Quantity",
    "Unit_Price",
    "Unit_Cost",
    "Discount_Rate",
    "Order_Status",
]

existing_required = [
    column
    for column in required_columns
    if column in df.columns
]

for column in existing_required:
    add_check(
        f"Missing values: {column}",
        df[column].isna().sum(),
        len(df),
        f"{column} should not contain missing values."
    )

# 4. Invalid dates.
add_check(
    "Invalid order dates",
    df["Order_Date"].isna().sum(),
    len(df),
    "Order_Date must be a valid date."
)

# 5. Invalid quantity.
add_check(
    "Non-positive quantity",
    (df["Quantity"] <= 0).sum(),
    len(df),
    "Quantity must be greater than zero."
)

# 6. Invalid unit prices.
add_check(
    "Non-positive unit price",
    (df["Unit_Price"] <= 0).sum(),
    len(df),
    "Unit_Price must be greater than zero."
)

# 7. Invalid unit costs.
add_check(
    "Negative unit cost",
    (df["Unit_Cost"] < 0).sum(),
    len(df),
    "Unit_Cost must not be negative."
)

# 8. Invalid discounts.
invalid_discount = (
    (df["Discount_Rate"] < 0)
    | (df["Discount_Rate"] > 1)
)

add_check(
    "Invalid discount rate",
    invalid_discount.sum(),
    len(df),
    "Discount_Rate must be between 0 and 1."
)

# 9. Invalid order statuses.
allowed_statuses = {
    "Delivered",
    "Shipped",
    "Processing",
    "Cancelled",
    "Returned",
}

add_check(
    "Invalid order status",
    (~df["Order_Status"].isin(allowed_statuses)).sum(),
    len(df),
    "Order status must be in the approved list."
)

# 10. Incorrect financial calculations.
expected_gross = (
    df["Quantity"] * df["Unit_Price"]
).round(2)

expected_discount = (
    expected_gross * df["Discount_Rate"]
).round(2)

expected_net = (
    expected_gross - expected_discount
).round(2)

expected_cost = (
    df["Quantity"] * df["Unit_Cost"]
).round(2)

expected_profit = (
    expected_net - expected_cost
).round(2)

add_check(
    "Incorrect gross revenue",
    (~df["Gross_Revenue"].round(2).eq(expected_gross)).sum(),
    len(df),
    "Gross_Revenue must equal quantity multiplied by unit price."
)

add_check(
    "Incorrect discount amount",
    (~df["Discount_Amount"].round(2).eq(expected_discount)).sum(),
    len(df),
    "Discount_Amount must match gross revenue multiplied by discount rate."
)

add_check(
    "Incorrect net revenue",
    (~df["Net_Revenue"].round(2).eq(expected_net)).sum(),
    len(df),
    "Net_Revenue must equal gross revenue minus discount."
)

add_check(
    "Incorrect total cost",
    (~df["Total_Cost"].round(2).eq(expected_cost)).sum(),
    len(df),
    "Total_Cost must equal quantity multiplied by unit cost."
)

add_check(
    "Incorrect gross profit",
    (~df["Gross_Profit"].round(2).eq(expected_profit)).sum(),
    len(df),
    "Gross_Profit must equal net revenue minus total cost."
)

# Create report.
quality_report = pd.DataFrame(checks)

report_file = REPORT_DIR / "data_quality_report.csv"

quality_report.to_csv(
    report_file,
    index=False
)

print("=" * 65)
print("DATA QUALITY REPORT")
print("=" * 65)

print(f"Dataset rows: {len(df):,}")
print(f"Dataset columns: {len(df.columns)}")

print("\nValidation results:")
print(quality_report.to_string(index=False))

passed = (quality_report["Status"] == "PASS").sum()
review = (quality_report["Status"] == "REVIEW").sum()

print("\nSUMMARY")
print(f"Checks passed: {passed}")
print(f"Checks requiring review: {review}")

print(f"\nReport saved to: {report_file}")