"""
Clean and validate Nigerian e-commerce sales data.

Input:
    data/ecommerce_sales.csv

Output:
    data/ecommerce_sales_clean.csv

Financial definitions:
    Gross_Revenue = Quantity * Unit_Price
    Discount_Amount = Gross_Revenue * Discount_Rate
    Net_Revenue = Gross_Revenue - Discount_Amount
    Total_Cost = Quantity * Unit_Cost
    Profit = Net_Revenue - Total_Cost

NOTE:
    This project uses synthetic data for educational and portfolio purposes.
"""

from pathlib import Path
import sys

import numpy as np
import pandas as pd


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = PROJECT_ROOT / "data" / "ecommerce_sales.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "ecommerce_sales_clean.csv"


# ============================================================
# 2. REQUIRED COLUMNS
# ============================================================

REQUIRED_COLUMNS = [
    "Order_ID",
    "Order_Date",
    "Customer_ID",
    "Quantity",
    "Unit_Price",
    "Unit_Cost",
    "Discount_Rate",
    "Order_Status",
]


# Financial columns that this script must create or recalculate.
FINANCIAL_COLUMNS = [
    "Gross_Revenue",
    "Discount_Amount",
    "Net_Revenue",
    "Total_Cost",
    "Profit",
]


# ============================================================
# 3. HELPER FUNCTIONS
# ============================================================

def stop_with_error(message: str) -> None:
    """Display a clear error and stop execution."""
    print(f"\nERROR: {message}")
    sys.exit(1)


def validate_required_columns(df: pd.DataFrame) -> None:
    """Ensure the input dataset contains every required column."""

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        stop_with_error(
            "The input dataset is missing required columns: "
            f"{missing_columns}\n"
            f"Available columns: {df.columns.tolist()}"
        )


def convert_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Convert financial and quantity columns to numeric values."""

    numeric_columns = [
        "Quantity",
        "Unit_Price",
        "Unit_Cost",
        "Discount_Rate",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )

    return df


def calculate_financial_columns(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate all financial columns consistently."""

    # Gross revenue before discounts.
    df["Gross_Revenue"] = (
        df["Quantity"] * df["Unit_Price"]
    )

    # Discount amount in currency.
    df["Discount_Amount"] = (
        df["Gross_Revenue"] * df["Discount_Rate"]
    )

    # Revenue after discount.
    df["Net_Revenue"] = (
        df["Gross_Revenue"] - df["Discount_Amount"]
    )

    # Cost of goods sold.
    df["Total_Cost"] = (
        df["Quantity"] * df["Unit_Cost"]
    )

    # IMPORTANT: Always create the exact Profit column expected
    # by the automated tests and downstream analytics scripts.
    df["Profit"] = (
        df["Net_Revenue"] - df["Total_Cost"]
    )

    # Round monetary values to two decimal places.
    for column in FINANCIAL_COLUMNS:
        df[column] = df[column].round(2)

    return df


def validate_financial_calculations(
    df: pd.DataFrame,
) -> None:
    """Verify that the financial calculations are internally consistent."""

    expected_values = {
        "Gross_Revenue": (
            df["Quantity"] * df["Unit_Price"]
        ),
        "Discount_Amount": (
            df["Gross_Revenue"] * df["Discount_Rate"]
        ),
        "Net_Revenue": (
            df["Gross_Revenue"] - df["Discount_Amount"]
        ),
        "Total_Cost": (
            df["Quantity"] * df["Unit_Cost"]
        ),
        "Profit": (
            df["Net_Revenue"] - df["Total_Cost"]
        ),
    }

    tolerance = 0.02

    for column, expected in expected_values.items():
        actual = df[column]

        mismatch = ~np.isclose(
            actual.to_numpy(dtype=float),
            expected.to_numpy(dtype=float),
            atol=tolerance,
            rtol=0,
        )

        if mismatch.any():
            stop_with_error(
                f"Financial validation failed for '{column}'. "
                f"Number of inconsistent rows: {int(mismatch.sum())}"
            )

    print("Financial calculations: PASS")


# ============================================================
# 4. MAIN CLEANING PROCESS
# ============================================================

def main() -> None:
    print("=" * 60)
    print("NIGERIAN E-COMMERCE DATA CLEANING")
    print("=" * 60)

    # --------------------------------------------------------
    # Check input file
    # --------------------------------------------------------

    if not INPUT_FILE.exists():
        stop_with_error(
            f"Input file not found: {INPUT_FILE}\n"
            "Check that data/ecommerce_sales.csv exists."
        )

    # --------------------------------------------------------
    # Load original data
    # --------------------------------------------------------

    try:
        df = pd.read_csv(INPUT_FILE)
    except Exception as error:
        stop_with_error(
            f"Could not read the input CSV: {error}"
        )

    original_rows = len(df)

    print(f"\nInput file: {INPUT_FILE}")
    print(f"Original rows: {original_rows:,}")
    print(f"Original columns: {len(df.columns)}")

    if df.empty:
        stop_with_error("The input dataset is empty.")

    # --------------------------------------------------------
    # Standardize column names
    # --------------------------------------------------------

    # Remove accidental spaces around column names.
    df.columns = df.columns.str.strip()

    # Do not silently rename columns or guess missing fields.
    validate_required_columns(df)

    # --------------------------------------------------------
    # Remove duplicate records
    # --------------------------------------------------------

    duplicate_count = int(df.duplicated().sum())

    if duplicate_count:
        df = df.drop_duplicates().copy()

    print(f"Duplicate rows removed: {duplicate_count:,}")

    # --------------------------------------------------------
    # Convert dates
    # --------------------------------------------------------

    df["Order_Date"] = pd.to_datetime(
        df["Order_Date"],
        errors="coerce",
    )

    # --------------------------------------------------------
    # Convert numeric fields
    # --------------------------------------------------------

    df = convert_numeric_columns(df)

    # --------------------------------------------------------
    # Remove rows missing critical information
    # --------------------------------------------------------

    critical_columns = [
        "Order_ID",
        "Order_Date",
        "Customer_ID",
        "Quantity",
        "Unit_Price",
        "Unit_Cost",
        "Discount_Rate",
        "Order_Status",
    ]

    rows_before_missing = len(df)

    df = df.dropna(
        subset=critical_columns
    ).copy()

    removed_missing = rows_before_missing - len(df)

    print(
        "Rows removed for missing critical values: "
        f"{removed_missing:,}"
    )

    # --------------------------------------------------------
    # Standardize text fields
    # --------------------------------------------------------

    for column in ["Order_ID", "Customer_ID", "Order_Status"]:
        df[column] = df[column].astype(str).str.strip()

    # --------------------------------------------------------
    # Remove invalid records
    # --------------------------------------------------------

    rows_before_validation = len(df)

    valid_mask = (
        (df["Quantity"] > 0)
        & (df["Unit_Price"] >= 0)
        & (df["Unit_Cost"] >= 0)
        & (df["Discount_Rate"] >= 0)
        & (df["Discount_Rate"] <= 1)
        & (df["Order_ID"] != "")
        & (df["Customer_ID"] != "")
        & (df["Order_Status"] != "")
    )

    df = df.loc[valid_mask].copy()

    removed_invalid = rows_before_validation - len(df)

    print(
        "Rows removed for invalid values: "
        f"{removed_invalid:,}"
    )

    # --------------------------------------------------------
    # Enforce unique order IDs
    # --------------------------------------------------------

    # Duplicate full rows were already removed. If an Order_ID
    # still occurs more than once, retain the first record and
    # report the number removed.
    duplicate_order_mask = df.duplicated(
        subset=["Order_ID"],
        keep="first",
    )

    duplicate_order_count = int(duplicate_order_mask.sum())

    if duplicate_order_count:
        df = df.loc[~duplicate_order_mask].copy()

    print(
        "Duplicate order IDs removed: "
        f"{duplicate_order_count:,}"
    )

    # --------------------------------------------------------
    # Validate that usable data remains
    # --------------------------------------------------------

    if df.empty:
        stop_with_error(
            "No usable rows remain after cleaning. "
            "Review the input data and cleaning rules."
        )

    # --------------------------------------------------------
    # Recalculate ALL financial columns
    # --------------------------------------------------------

    df = calculate_financial_columns(df)

    # --------------------------------------------------------
    # Validate financial calculations
    # --------------------------------------------------------

    validate_financial_calculations(df)

    # --------------------------------------------------------
    # Validate final required output columns
    # --------------------------------------------------------

    output_required_columns = (
        REQUIRED_COLUMNS + FINANCIAL_COLUMNS
    )

    missing_output_columns = [
        column
        for column in output_required_columns
        if column not in df.columns
    ]

    if missing_output_columns:
        stop_with_error(
            "The cleaned dataset is missing required output columns: "
            f"{missing_output_columns}"
        )

    # Ensure there are no missing financial values.
    missing_financial = (
        df[FINANCIAL_COLUMNS].isna().sum()
    )

    if missing_financial.any():
        stop_with_error(
            "Missing values remain in financial columns:\n"
            f"{missing_financial[missing_financial > 0]}"
        )

    # --------------------------------------------------------
    # Sort data consistently
    # --------------------------------------------------------

    df = df.sort_values(
        by=["Order_Date", "Order_ID"]
    ).reset_index(drop=True)

    # --------------------------------------------------------
    # Save cleaned dataset
    # --------------------------------------------------------

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    try:
        df.to_csv(
            OUTPUT_FILE,
            index=False,
            encoding="utf-8",
        )
    except Exception as error:
        stop_with_error(
            f"Could not save the cleaned dataset: {error}"
        )

    # --------------------------------------------------------
    # Read saved file back to verify it
    # --------------------------------------------------------

    try:
        saved_df = pd.read_csv(OUTPUT_FILE)
    except Exception as error:
        stop_with_error(
            f"Could not verify the saved CSV: {error}"
        )

    if saved_df.empty:
        stop_with_error(
            "The saved cleaned dataset is unexpectedly empty."
        )

    if "Profit" not in saved_df.columns:
        stop_with_error(
            "The saved CSV does not contain the required 'Profit' column."
        )

    if saved_df["Profit"].isna().any():
        stop_with_error(
            "The saved CSV contains missing Profit values."
        )

    # --------------------------------------------------------
    # Final summary
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("CLEANING COMPLETED SUCCESSFULLY")
    print("=" * 60)

    print(f"Original rows: {original_rows:,}")
    print(f"Cleaned rows: {len(saved_df):,}")
    print(f"Rows removed: {original_rows - len(saved_df):,}")
    print(f"Final columns: {len(saved_df.columns)}")
    print(f"Output file: {OUTPUT_FILE}")

    print("\nFinancial columns verified:")

    for column in FINANCIAL_COLUMNS:
        print(f"  [PASS] {column}")

    print("\nFinal data preview:")
    print(
        saved_df[
            [
                "Order_ID",
                "Quantity",
                "Unit_Price",
                "Unit_Cost",
                "Gross_Revenue",
                "Net_Revenue",
                "Total_Cost",
                "Profit",
            ]
        ].head().to_string(index=False)
    )

    print("\nCleaning and financial validation: PASS")


# ============================================================
# 5. ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()