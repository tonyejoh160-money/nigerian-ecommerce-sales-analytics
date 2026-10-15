# Data Dictionary — Nigerian E-Commerce Sales Analytics

## 1. Project Overview

This project analyzes a synthetic Nigerian e-commerce dataset for educational and portfolio purposes.

The dataset does not represent verified transactions from a real Nigerian e-commerce company.

The analysis explores sales performance, product profitability, customer behavior, regional performance, payment methods, and order statuses.

## 2. Dataset Files

* `data/ecommerce_sales.csv` — Original synthetic sales dataset.
* `data/ecommerce_sales_clean.csv` — Cleaned sales dataset.
* `data/customers.csv` — Synthetic customer information.

## 3. Main Dataset Fields

| Field           | Description                            |
| --------------- | -------------------------------------- |
| Order_ID        | Unique order identifier                |
| Order_Date      | Date the order was recorded            |
| Customer_ID     | Identifier for the customer            |
| State           | State or FCT associated with the order |
| City            | City associated with the order         |
| Product         | Product purchased                      |
| Category        | Product category                       |
| Quantity        | Number of units ordered                |
| Unit_Price      | Selling price per unit before discount |
| Unit_Cost       | Product cost per unit                  |
| Discount_Rate   | Discount expressed as a decimal        |
| Discount_Amount | Total discount applied to the order    |
| Gross_Revenue   | Revenue before discount                |
| Net_Revenue     | Revenue after discount                 |
| Total_Cost      | Total product cost                     |
| Profit          | Net revenue minus total product cost   |
| Payment_Method  | Recorded payment method                |
| Payment_Status  | Recorded payment status                |
| Order_Status    | Recorded order or fulfillment status   |

**Important:** Verify the exact column names against the CSV headers before using them in analysis. Column names may differ in capitalization or spelling.

## 4. Financial Calculations

### Gross Revenue

Quantity × Unit Price

### Discount Amount

Gross Revenue × Discount Rate

### Net Revenue

Gross Revenue − Discount Amount

### Total Cost

Quantity × Unit Cost

### Profit

Net Revenue − Total Cost

### Profit Margin

(Profit ÷ Net Revenue) × 100

Profit margin is undefined when net revenue is zero.

## 5. Analytical Assumptions

For the primary sales analysis, orders with `Order_Status = Delivered` are used as a simplified proxy for completed sales.

This is an educational analytical assumption, not a complete accounting or revenue-recognition policy.

Cancelled, processing, and shipped orders are excluded from the primary delivered-sales calculations.

Returned orders and refunds are not modeled as a complete accounting process. Consequently, calculated profit should not be interpreted as audited business profit.

## 6. Customer Analysis

Customer-level analysis aggregates order records by `Customer_ID`.

Repeat customers are identified using the number of delivered orders.

RFM analysis measures:

* **Recency:** Days since the customer's most recent delivered order.
* **Frequency:** Number of delivered orders.
* **Monetary:** Total net revenue from delivered orders.

The RFM reference date is one day after the latest delivered order date.

Customers without delivered orders are excluded from the RFM segments unless a particular analysis explicitly includes them.

## 7. Data Quality

The project checks for:

* Missing values.
* Duplicate records.
* Invalid dates.
* Invalid quantities.
* Invalid prices and costs.
* Invalid discount rates.
* Unexpected order statuses.
* Inconsistent financial calculations.

## 8. Limitations

1. The dataset is synthetic.
2. Customer and transaction patterns are generated rather than observed.
3. Results do not establish actual Nigerian e-commerce market trends.
4. Profit calculations exclude operating expenses, logistics costs, taxes, and other costs not represented in the dataset.
5. Returns and refunds are not modeled as a complete accounting process.
6. Results depend on the filters and assumptions used in each analysis.

## 9. Responsible Interpretation

Use this project to demonstrate data cleaning, Python programming, SQL, visualization, reporting, and analytical reasoning.

Do not present synthetic results as verified market statistics.
