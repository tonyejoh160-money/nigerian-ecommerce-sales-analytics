from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = PROJECT_DIR / "data" / "ecommerce_sales.csv"

df = pd.read_csv(DATA_FILE)

# Recalculate the financial values.
expected_gross = df["Quantity"] * df["Unit_Price"]

expected_discount = (
    expected_gross * df["Discount_Rate"]
).round(2)

expected_net = expected_gross - expected_discount

expected_cost = df["Quantity"] * df["Unit_Cost"]

expected_profit = expected_net - expected_cost

# Compare calculated values with stored values.
checks = {
    "Gross_Revenue": expected_gross,
    "Discount_Amount": expected_discount,
    "Net_Revenue": expected_net,
    "Total_Cost": expected_cost,
    "Gross_Profit": expected_profit,
}

print("=" * 55)
print("FINANCIAL VALIDATION REPORT")
print("=" * 55)

for column, expected in checks.items():

    actual = df[column]

    matches = np.isclose(
        actual.to_numpy(dtype=float),
        expected.to_numpy(dtype=float),
        atol=0.01
    )

    errors = int((~matches).sum())

    print(f"{column}: {errors} calculation errors")

    if errors == 0:
        print("  PASS")
    else:
        print("  FAIL")

print("\nValidation complete.")