-- ============================================================================
-- INVENTORY OPTIMIZATION PROJECT - SQL QUERIES
-- ============================================================================
-- Author: [Your Name]
-- Database: SQLite / MySQL Compatible
-- Purpose: Retail Inventory Analysis Queries
-- ============================================================================

-- ============================================================================
-- SECTION 1: CREATE DATABASE TABLE
-- ============================================================================

-- Create the main inventory table
CREATE TABLE IF NOT EXISTS retail_inventory (
    Order_ID INTEGER PRIMARY KEY,
    Order_Date DATE NOT NULL,
    Product_ID VARCHAR(10) NOT NULL,
    Product_Name VARCHAR(100) NOT NULL,
    Category VARCHAR(50) NOT NULL,
    Unit_Price DECIMAL(10, 2) NOT NULL,
    Quantity_Sold INTEGER NOT NULL,
    Sales DECIMAL(10, 2) NOT NULL,
    Inventory_Level INTEGER NOT NULL,
    Reorder_Threshold INTEGER NOT NULL,
    Supplier_Lead_Time INTEGER NOT NULL
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_product ON retail_inventory(Product_ID);
CREATE INDEX IF NOT EXISTS idx_category ON retail_inventory(Category);
CREATE INDEX IF NOT EXISTS idx_order_date ON retail_inventory(Order_Date);

-- ============================================================================
-- SECTION 2: BASIC SALES ANALYSIS QUERIES
-- ============================================================================

-- Query 2.1: Calculate total sales per product
-- Purpose: Identify revenue contribution of each product
SELECT 
    Product_ID,
    Product_Name,
    Category,
    COUNT(*) AS Total_Orders,
    SUM(Quantity_Sold) AS Total_Quantity,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(AVG(Sales), 2) AS Avg_Sale_Value
FROM retail_inventory
GROUP BY Product_ID, Product_Name, Category
ORDER BY Total_Sales DESC;

-- Query 2.2: Find top 10 products by quantity sold
-- Purpose: Identify high-volume products for inventory prioritization
SELECT 
    Product_ID,
    Product_Name,
    SUM(Quantity_Sold) AS Total_Quantity_Sold,
    ROUND(SUM(Sales), 2) AS Total_Revenue,
    COUNT(*) AS Number_of_Orders
FROM retail_inventory
GROUP BY Product_ID, Product_Name
ORDER BY Total_Quantity_Sold DESC
LIMIT 10;

-- Query 2.3: Calculate monthly sales trends
-- Purpose: Understand seasonal patterns and growth trends
SELECT 
    strftime('%Y-%m', Order_Date) AS Month,
    COUNT(DISTINCT Order_ID) AS Total_Orders,
    SUM(Quantity_Sold) AS Total_Units_Sold,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(AVG(Sales), 2) AS Avg_Order_Value
FROM retail_inventory
GROUP BY strftime('%Y-%m', Order_Date)
ORDER BY Month;

-- ============================================================================
-- SECTION 3: INVENTORY MOVEMENT ANALYSIS
-- ============================================================================

-- Query 3.1: Identify slow-moving products
-- Purpose: Find products with low turnover for clearance decisions
SELECT 
    Product_ID,
    Product_Name,
    Category,
    SUM(Quantity_Sold) AS Total_Sold,
    MAX(Inventory_Level) AS Current_Stock,
    ROUND(CAST(SUM(Quantity_Sold) AS FLOAT) / NULLIF(MAX(Inventory_Level), 0), 2) AS Turnover_Ratio
FROM retail_inventory
GROUP BY Product_ID, Product_Name, Category
HAVING Turnover_Ratio < 2
ORDER BY Turnover_Ratio ASC;

-- Query 3.2: Identify fast-moving products
-- Purpose: Prioritize replenishment for high-demand items
SELECT 
    Product_ID,
    Product_Name,
    Category,
    SUM(Quantity_Sold) AS Total_Sold,
    MAX(Inventory_Level) AS Current_Stock,
    ROUND(CAST(SUM(Quantity_Sold) AS FLOAT) / NULLIF(MAX(Inventory_Level), 0), 2) AS Turnover_Ratio
FROM retail_inventory
GROUP BY Product_ID, Product_Name, Category
HAVING Turnover_Ratio >= 5
ORDER BY Turnover_Ratio DESC;

-- ============================================================================
-- SECTION 4: CATEGORY-WISE AGGREGATION
-- ============================================================================

-- Query 4.1: Category performance summary
-- Purpose: Strategic view of category contributions
SELECT 
    Category,
    COUNT(DISTINCT Product_ID) AS Unique_Products,
    COUNT(*) AS Total_Transactions,
    SUM(Quantity_Sold) AS Total_Units_Sold,
    ROUND(SUM(Sales), 2) AS Total_Revenue,
    ROUND(AVG(Sales), 2) AS Avg_Transaction_Value,
    ROUND(SUM(Sales) * 100.0 / (SELECT SUM(Sales) FROM retail_inventory), 2) AS Revenue_Percentage
FROM retail_inventory
GROUP BY Category
ORDER BY Total_Revenue DESC;

-- Query 4.2: Category-wise inventory health
-- Purpose: Identify category-level stock issues
SELECT 
    Category,
    SUM(Inventory_Level) AS Total_Inventory,
    SUM(Quantity_Sold) AS Total_Demand,
    ROUND(CAST(SUM(Quantity_Sold) AS FLOAT) / NULLIF(SUM(Inventory_Level), 0), 2) AS Category_Turnover,
    SUM(CASE WHEN Inventory_Level <= Reorder_Threshold THEN 1 ELSE 0 END) AS Items_Below_Reorder
FROM retail_inventory
GROUP BY Category
ORDER BY Category_Turnover DESC;

-- ============================================================================
-- SECTION 5: ADVANCED INVENTORY ANALYSIS
-- ============================================================================

-- Query 5.1: Products below reorder threshold (Stockout Risk)
-- Purpose: Immediate action items for procurement team
SELECT 
    ri.Product_ID,
    ri.Product_Name,
    ri.Category,
    ri.Inventory_Level AS Current_Stock,
    ri.Reorder_Threshold,
    ri.Supplier_Lead_Time AS Lead_Time_Days,
    (ri.Reorder_Threshold - ri.Inventory_Level) AS Units_Short
FROM retail_inventory ri
INNER JOIN (
    SELECT Product_ID, MAX(Order_Date) AS Latest_Date
    FROM retail_inventory
    GROUP BY Product_ID
) latest ON ri.Product_ID = latest.Product_ID AND ri.Order_Date = latest.Latest_Date
WHERE ri.Inventory_Level <= ri.Reorder_Threshold
ORDER BY Units_Short DESC;

-- Query 5.2: ABC Analysis using SQL
-- Purpose: Classify products by revenue contribution
WITH ProductSales AS (
    SELECT 
        Product_ID,
        Product_Name,
        ROUND(SUM(Sales), 2) AS Total_Sales
    FROM retail_inventory
    GROUP BY Product_ID, Product_Name
),
RankedProducts AS (
    SELECT 
        *,
        SUM(Total_Sales) OVER (ORDER BY Total_Sales DESC) AS Cumulative_Sales,
        SUM(Total_Sales) OVER () AS Grand_Total
    FROM ProductSales
)
SELECT 
    Product_ID,
    Product_Name,
    Total_Sales,
    ROUND(Cumulative_Sales * 100.0 / Grand_Total, 2) AS Cumulative_Percentage,
    CASE 
        WHEN Cumulative_Sales * 100.0 / Grand_Total <= 70 THEN 'A'
        WHEN Cumulative_Sales * 100.0 / Grand_Total <= 90 THEN 'B'
        ELSE 'C'
    END AS ABC_Class
FROM RankedProducts
ORDER BY Total_Sales DESC;

-- Query 5.3: Daily demand calculation for reorder planning
-- Purpose: Calculate average daily demand for each product
SELECT 
    Product_ID,
    Product_Name,
    Category,
    COUNT(DISTINCT Order_Date) AS Days_With_Sales,
    SUM(Quantity_Sold) AS Total_Quantity,
    ROUND(CAST(SUM(Quantity_Sold) AS FLOAT) / COUNT(DISTINCT Order_Date), 2) AS Avg_Daily_Demand,
    Supplier_Lead_Time,
    ROUND(CAST(SUM(Quantity_Sold) AS FLOAT) / COUNT(DISTINCT Order_Date) * Supplier_Lead_Time, 0) AS Lead_Time_Demand
FROM retail_inventory
GROUP BY Product_ID, Product_Name, Category, Supplier_Lead_Time
ORDER BY Avg_Daily_Demand DESC;

-- ============================================================================
-- SECTION 6: TIME-BASED ANALYSIS
-- ============================================================================

-- Query 6.1: Weekly sales pattern
-- Purpose: Identify day-of-week trends for staffing and promotions
SELECT 
    CASE strftime('%w', Order_Date)
        WHEN '0' THEN 'Sunday'
        WHEN '1' THEN 'Monday'
        WHEN '2' THEN 'Tuesday'
        WHEN '3' THEN 'Wednesday'
        WHEN '4' THEN 'Thursday'
        WHEN '5' THEN 'Friday'
        WHEN '6' THEN 'Saturday'
    END AS Day_of_Week,
    COUNT(*) AS Total_Orders,
    SUM(Quantity_Sold) AS Total_Units,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(AVG(Sales), 2) AS Avg_Order_Value
FROM retail_inventory
GROUP BY strftime('%w', Order_Date)
ORDER BY strftime('%w', Order_Date);

-- Query 6.2: Month-over-month growth
-- Purpose: Track sales growth for performance reporting
WITH MonthlySales AS (
    SELECT 
        strftime('%Y-%m', Order_Date) AS Month,
        ROUND(SUM(Sales), 2) AS Total_Sales
    FROM retail_inventory
    GROUP BY strftime('%Y-%m', Order_Date)
)
SELECT 
    Month,
    Total_Sales,
    LAG(Total_Sales) OVER (ORDER BY Month) AS Previous_Month_Sales,
    ROUND((Total_Sales - LAG(Total_Sales) OVER (ORDER BY Month)) * 100.0 / 
          NULLIF(LAG(Total_Sales) OVER (ORDER BY Month), 0), 2) AS Growth_Percentage
FROM MonthlySales
ORDER BY Month;

-- ============================================================================
-- SECTION 7: BUSINESS INTELLIGENCE QUERIES
-- ============================================================================

-- Query 7.1: Product performance scorecard
-- Purpose: Comprehensive view for product management decisions
SELECT 
    Product_ID,
    Product_Name,
    Category,
    SUM(Quantity_Sold) AS Total_Units,
    ROUND(SUM(Sales), 2) AS Total_Revenue,
    COUNT(DISTINCT Order_Date) AS Days_Sold,
    ROUND(AVG(Quantity_Sold), 2) AS Avg_Units_Per_Order,
    MAX(Inventory_Level) AS Last_Known_Inventory,
    MAX(Reorder_Threshold) AS Reorder_Point,
    CASE 
        WHEN MAX(Inventory_Level) <= MAX(Reorder_Threshold) THEN 'REORDER NOW'
        WHEN MAX(Inventory_Level) <= MAX(Reorder_Threshold) * 1.5 THEN 'LOW STOCK'
        ELSE 'ADEQUATE'
    END AS Stock_Status
FROM retail_inventory
GROUP BY Product_ID, Product_Name, Category
ORDER BY Total_Revenue DESC;

-- Query 7.2: Inventory value analysis
-- Purpose: Financial view of inventory holdings
SELECT 
    Category,
    COUNT(DISTINCT Product_ID) AS Product_Count,
    SUM(Inventory_Level) AS Total_Units_In_Stock,
    ROUND(SUM(Inventory_Level * Unit_Price), 2) AS Total_Inventory_Value,
    ROUND(AVG(Inventory_Level * Unit_Price), 2) AS Avg_Product_Value
FROM (
    SELECT DISTINCT Product_ID, Product_Name, Category, Unit_Price, Inventory_Level
    FROM retail_inventory ri
    WHERE Order_Date = (SELECT MAX(Order_Date) FROM retail_inventory WHERE Product_ID = ri.Product_ID)
) latest_inventory
GROUP BY Category
ORDER BY Total_Inventory_Value DESC;

-- ============================================================================
-- END OF SQL QUERIES
-- ============================================================================
