import pytest


def calculate_financial_metrics(
    quantity,
    unit_price,
    unit_cost,
    discount_rate,
):
    """Calculate basic order-level financial metrics."""

    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero.")

    if unit_price < 0 or unit_cost < 0:
        raise ValueError("Prices and costs cannot be negative.")

    if not 0 <= discount_rate <= 1:
        raise ValueError(
            "Discount rate must be between zero and one."
        )

    gross_revenue = quantity * unit_price

    discount_amount = gross_revenue * discount_rate

    net_revenue = gross_revenue - discount_amount

    total_cost = quantity * unit_cost

    profit = net_revenue - total_cost

    profit_margin = (
        profit / net_revenue * 100
        if net_revenue != 0
        else None
    )

    return {
        "gross_revenue": round(gross_revenue, 2),
        "discount_amount": round(discount_amount, 2),
        "net_revenue": round(net_revenue, 2),
        "total_cost": round(total_cost, 2),
        "profit": round(profit, 2),
        "profit_margin": (
            round(profit_margin, 2)
            if profit_margin is not None
            else None
        ),
    }


def test_standard_order_calculation():
    result = calculate_financial_metrics(
        quantity=2,
        unit_price=5000,
        unit_cost=3000,
        discount_rate=0.10,
    )

    assert result["gross_revenue"] == 10000
    assert result["discount_amount"] == 1000
    assert result["net_revenue"] == 9000
    assert result["total_cost"] == 6000
    assert result["profit"] == 3000
    assert result["profit_margin"] == pytest.approx(33.33, abs=0.01)


def test_zero_discount():
    result = calculate_financial_metrics(
        quantity=1,
        unit_price=1000,
        unit_cost=600,
        discount_rate=0,
    )

    assert result["gross_revenue"] == 1000
    assert result["discount_amount"] == 0
    assert result["net_revenue"] == 1000
    assert result["profit"] == 400
    assert result["profit_margin"] == 40


def test_full_discount():
    result = calculate_financial_metrics(
        quantity=1,
        unit_price=1000,
        unit_cost=600,
        discount_rate=1,
    )

    assert result["gross_revenue"] == 1000
    assert result["discount_amount"] == 1000
    assert result["net_revenue"] == 0
    assert result["profit"] == -600
    assert result["profit_margin"] is None


def test_negative_quantity_is_rejected():
    with pytest.raises(ValueError):
        calculate_financial_metrics(
            quantity=-1,
            unit_price=1000,
            unit_cost=600,
            discount_rate=0,
        )


def test_negative_price_is_rejected():
    with pytest.raises(ValueError):
        calculate_financial_metrics(
            quantity=1,
            unit_price=-1000,
            unit_cost=600,
            discount_rate=0,
        )


def test_invalid_discount_is_rejected():
    with pytest.raises(ValueError):
        calculate_financial_metrics(
            quantity=1,
            unit_price=1000,
            unit_cost=600,
            discount_rate=1.5,
        )


def test_loss_making_order():
    result = calculate_financial_metrics(
        quantity=1,
        unit_price=500,
        unit_cost=700,
        discount_rate=0,
    )

    assert result["profit"] == -200
    assert result["profit_margin"] == -40