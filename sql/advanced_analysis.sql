-- =====================================================
-- ADVANCED SQL ANALYSIS
-- =====================================================


-- QUERY 1:
-- Calculate delivered revenue and profit by state.

SELECT
    State,
    COUNT(*) AS Delivered_Orders,
    ROUND(SUM(Net_Revenue), 2) AS Total_Net_Revenue,
    ROUND(SUM(Gross_Profit), 2) AS Total_Gross_Profit,
    ROUND(
        100.0 * SUM(Gross_Profit)
        / NULLIF(SUM(Net_Revenue), 0),
        2
    ) AS Gross_Profit_Margin_Percent
FROM sales
WHERE Order_Status = 'Delivered'
GROUP BY State
ORDER BY Total_Net_Revenue DESC;


-- QUERY 2:
-- Find customers with at least three delivered orders.

SELECT
    Customer_ID,
    COUNT(DISTINCT Order_ID) AS Delivered_Orders,
    ROUND(SUM(Net_Revenue), 2) AS Total_Net_Revenue
FROM sales
WHERE Order_Status = 'Delivered'
GROUP BY Customer_ID
HAVING COUNT(DISTINCT Order_ID) >= 3
ORDER BY Total_Net_Revenue DESC;


-- QUERY 3:
-- Join customer records to delivered sales.

SELECT
    c.Customer_ID,
    c.Customer_Name,
    COUNT(DISTINCT s.Order_ID) AS Delivered_Orders,
    ROUND(SUM(s.Net_Revenue), 2) AS Total_Net_Revenue
FROM customers AS c
INNER JOIN sales AS s
    ON c.Customer_ID = s.Customer_ID
WHERE s.Order_Status = 'Delivered'
GROUP BY
    c.Customer_ID,
    c.Customer_Name
ORDER BY Total_Net_Revenue DESC
LIMIT 20;


-- QUERY 4:
-- Compare delivered and cancelled order counts.

SELECT
    State,
    SUM(
        CASE
            WHEN Order_Status = 'Delivered' THEN 1
            ELSE 0
        END
    ) AS Delivered_Orders,
    SUM(
        CASE
            WHEN Order_Status = 'Cancelled' THEN 1
            ELSE 0
        END
    ) AS Cancelled_Orders,
    COUNT(*) AS Total_Orders
FROM sales
GROUP BY State
ORDER BY Cancelled_Orders DESC;


-- QUERY 5:
-- Calculate each month's revenue and month-over-month change.

WITH monthly_sales AS (
    SELECT
        SUBSTR(Order_Date, 1, 7) AS Sales_Month,
        SUM(Net_Revenue) AS Monthly_Revenue
    FROM sales
    WHERE Order_Status = 'Delivered'
    GROUP BY SUBSTR(Order_Date, 1, 7)
),
revenue_comparison AS (
    SELECT
        Sales_Month,
        Monthly_Revenue,
        LAG(Monthly_Revenue) OVER (
            ORDER BY Sales_Month
        ) AS Previous_Month_Revenue
    FROM monthly_sales
)
SELECT
    Sales_Month,
    ROUND(Monthly_Revenue, 2) AS Monthly_Revenue,
    ROUND(Previous_Month_Revenue, 2)
        AS Previous_Month_Revenue,
    ROUND(
        100.0 * (
            Monthly_Revenue - Previous_Month_Revenue
        ) / NULLIF(Previous_Month_Revenue, 0),
        2
    ) AS Revenue_Change_Percent
FROM revenue_comparison
ORDER BY Sales_Month;