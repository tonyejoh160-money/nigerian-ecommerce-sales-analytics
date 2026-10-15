-- =====================================================
-- NIGERIAN E-COMMERCE SALES ANALYTICS
-- BASIC BUSINESS QUERIES
-- =====================================================


-- QUERY 1:
-- Count all order records.

SELECT
    COUNT(*) AS Total_Order_Records
FROM sales;


-- QUERY 2:
-- Count unique customers who appear in the sales table.

SELECT
    COUNT(DISTINCT Customer_ID) AS Unique_Customers
FROM sales;


-- QUERY 3:
-- Calculate order counts by status.

SELECT
    Order_Status,
    COUNT(*) AS Number_Of_Orders
FROM sales
GROUP BY Order_Status
ORDER BY Number_Of_Orders DESC;


-- QUERY 4:
-- Calculate delivered net revenue.

SELECT
    ROUND(SUM(Net_Revenue), 2) AS Delivered_Net_Revenue
FROM sales
WHERE Order_Status = 'Delivered';


-- QUERY 5:
-- Calculate delivered gross profit.

SELECT
    ROUND(SUM(Gross_Profit), 2) AS Delivered_Gross_Profit
FROM sales
WHERE Order_Status = 'Delivered';


-- QUERY 6:
-- Identify the ten highest-revenue products.

SELECT
    Product,
    ROUND(SUM(Net_Revenue), 2) AS Total_Net_Revenue
FROM sales
WHERE Order_Status = 'Delivered'
GROUP BY Product
ORDER BY Total_Net_Revenue DESC
LIMIT 10;


-- QUERY 7:
-- Calculate delivered revenue by state.

SELECT
    State,
    ROUND(SUM(Net_Revenue), 2) AS Total_Net_Revenue
FROM sales
WHERE Order_Status = 'Delivered'
GROUP BY State
ORDER BY Total_Net_Revenue DESC;


-- QUERY 8:
-- Compare revenue across product categories.

SELECT
    Category,
    ROUND(SUM(Net_Revenue), 2) AS Total_Net_Revenue
FROM sales
WHERE Order_Status = 'Delivered'
GROUP BY Category
ORDER BY Total_Net_Revenue DESC;


-- QUERY 9:
-- Compare payment methods by delivered revenue.

SELECT
    Payment_Method,
    COUNT(*) AS Delivered_Orders,
    ROUND(SUM(Net_Revenue), 2) AS Total_Net_Revenue
FROM sales
WHERE Order_Status = 'Delivered'
GROUP BY Payment_Method
ORDER BY Total_Net_Revenue DESC;


-- QUERY 10:
-- Calculate monthly delivered revenue.

SELECT
    SUBSTR(Order_Date, 1, 7) AS Sales_Month,
    COUNT(*) AS Delivered_Orders,
    ROUND(SUM(Net_Revenue), 2) AS Monthly_Net_Revenue
FROM sales
WHERE Order_Status = 'Delivered'
GROUP BY SUBSTR(Order_Date, 1, 7)
ORDER BY Sales_Month;