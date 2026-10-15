from pathlib import Path

import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "ecommerce_sales_clean.csv"


def load_data():
    """Load the cleaned dataset."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Cleaned dataset not found: {DATA_FILE}. "
            "Run the data generation and cleaning scripts first."
        )

    return pd.read_csv(DATA_FILE)


def test_cleaned_dataset_exists():
    """The cleaned CSV must exist."""
    assert DATA_FILE.exists(), (
        f"Dataset does not exist: {DATA_FILE}"
    )


def test_dataset_is_not_empty():
    """The cleaned dataset must contain records."""
    df = load_data()

    assert not df.empty, "The cleaned dataset is empty."


def test_required_columns_exist():
    """Required analytical columns must be present."""
    df = load_data()

    required_columns = [
        "Order_ID",
        "Order_Date",
        "Customer_ID",
        "Quantity",
        "Unit_Price",
        "Unit_Cost",
        "Discount_Rate",
        "Gross_Revenue",
        "Net_Revenue",
        "Total_Cost",
        "Profit",
        "Order_Status",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    assert not missing_columns, (
        f"Missing required columns: {missing_columns}"
    )


def test_order_ids_are_not_missing():
    """Order IDs must be populated."""
    df = load_data()

    assert df["Order_ID"].notna().all(), (
        "Some order IDs are missing."
    )


def test_order_ids_are_unique():
    """Each order record should have a unique order ID."""
    df = load_data()

    duplicates = df["Order_ID"].duplicated().sum()

    assert duplicates == 0, (
        f"Found {duplicates} duplicate order IDs."
    )


def test_quantities_are_positive():
    """Quantity must be greater than zero."""
    df = load_data()

    assert (df["Quantity"] > 0).all(), (
        "Found quantities that are zero or negative."
    )


def test_prices_and_costs_are_non_negative():
    """Prices and costs must not be negative."""
    df = load_data()

    assert (df["Unit_Price"] >= 0).all(), (
        "Found negative unit prices."
    )

    assert (df["Unit_Cost"] >= 0).all(), (
        "Found negative unit costs."
    )


def test_discount_rates_are_valid():
    """Discount rates must be between zero and one."""
    df = load_data()

    assert df["Discount_Rate"].between(0, 1).all(), (
        "Found discount rates outside the range 0 to 1."
    )


def test_financial_columns_are_not_missing():
    """Required financial fields must be populated."""
    df = load_data()

    financial_columns = [
        "Gross_Revenue",
        "Net_Revenue",
        "Total_Cost",
        "Profit",
    ]

    assert df[financial_columns].notna().all().all(), (
        "Missing values found in financial columns."
    )


def test_financial_calculations_are_consistent():
    """Financial values should match their formulas."""
    df = load_data()

    expected_gross = df["Quantity"] * df["Unit_Price"]

    expected_discount = (
        expected_gross * df["Discount_Rate"]
    )

    expected_net = expected_gross - expected_discount

    expected_cost = df["Quantity"] * df["Unit_Cost"]

    expected_profit = expected_net - expected_cost

    tolerance = 0.02

    assert (
        (df["Gross_Revenue"] - expected_gross).abs()
        <= tolerance
    ).all(), "Gross revenue calculation is inconsistent."

    if "Discount_Amount" in df.columns:
        assert (
            (df["Discount_Amount"] - expected_discount).abs()
            <= tolerance
        ).all(), "Discount amount calculation is inconsistent."

    assert (
        (df["Net_Revenue"] - expected_net).abs()
        <= tolerance
    ).all(), "Net revenue calculation is inconsistent."

    assert (
        (df["Total_Cost"] - expected_cost).abs()
        <= tolerance
    ).all(), "Total cost calculation is inconsistent."

    assert (
        (df["Profit"] - expected_profit).abs()
        <= tolerance
    ).all(), "Profit calculation is inconsistent."


def test_order_status_values_are_valid():
    """Order statuses should belong to the expected categories."""
    df = load_data()

    allowed_statuses = {
        "Delivered",
        "Shipped",
        "Processing",
        "Cancelled",
        "Returned",
    }

    actual_statuses = set(
        df["Order_Status"].dropna().unique()
    )

    unexpected_statuses = actual_statuses - allowed_statuses

    assert not unexpected_statuses, (
        f"Unexpected order statuses: {unexpected_statuses}"
    )