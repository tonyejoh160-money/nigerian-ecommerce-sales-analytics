from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "ecommerce_sales_clean.csv"
OUTPUT_DIR = PROJECT_DIR / "reports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATA_FILE}\n"
        "Run your data-cleaning script first."
    )

df = pd.read_csv(DATA_FILE)
df["Order_Date"] = pd.to_datetime(
    df["Order_Date"], errors="coerce"
)

# Analyze delivered orders only.
delivered = df[df["Order_Status"] == "Delivered"].copy()

# Group delivered orders by month.
delivered["Month"] = (
    delivered["Order_Date"].dt.to_period("M").astype(str)
)

monthly_sales = (
    delivered.groupby("Month")
    .agg(
        Delivered_Orders=("Order_ID", "nunique"),
        Unique_Customers=("Customer_ID", "nunique"),
        Units_Sold=("Quantity", "sum"),
        Net_Revenue=("Net_Revenue", "sum"),
        Total_Cost=("Total_Cost", "sum"),
        Gross_Profit=("Gross_Profit", "sum"),
    )
    .reset_index()
)

monthly_sales["Profit_Margin_Percent"] = (
    monthly_sales["Gross_Profit"]
    / monthly_sales["Net_Revenue"].where(
        monthly_sales["Net_Revenue"] != 0
    )
    * 100
).round(2)

output_file = OUTPUT_DIR / "monthly_sales_summary.csv"
monthly_sales.to_csv(output_file, index=False)

print("=" * 50)
print("MONTHLY DELIVERED SALES ANALYSIS")
print("=" * 50)

print(monthly_sales.to_string(index=False))
print(f"\nReport saved to: {output_file}")