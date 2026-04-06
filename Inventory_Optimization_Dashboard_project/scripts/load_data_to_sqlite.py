"""
================================================================================
INVENTORY OPTIMIZATION PROJECT - SQLite Data Loader
================================================================================
Purpose: Load CSV data into SQLite database and execute SQL queries
================================================================================
"""

import sqlite3
import pandas as pd
import os

# Database file path
DB_PATH = 'data/retail_inventory.db'

def create_database():
    """Create SQLite database and load data from CSV."""
    
    print("=" * 60)
    print("LOADING DATA INTO SQLITE DATABASE")
    print("=" * 60)
    
    # Create database connection
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Read CSV data
    df = pd.read_csv('data/retail_inventory_data.csv')
    print(f"\n✓ Loaded {len(df)} records from CSV")
    
    # Create table
    cursor.execute('''
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
        )
    ''')
    
    # Load data into table
    df.to_sql('retail_inventory', conn, if_exists='replace', index=False)
    print(f"✓ Data loaded into 'retail_inventory' table")
    
    # Create indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_product ON retail_inventory(Product_ID)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_category ON retail_inventory(Category)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_order_date ON retail_inventory(Order_Date)')
    print("✓ Indexes created")
    
    conn.commit()
    return conn

def run_sample_queries(conn):
    """Execute and display sample SQL queries."""
    
    print("\n" + "=" * 60)
    print("EXECUTING SQL QUERIES")
    print("=" * 60)
    
    queries = {
        "Total Sales per Product": """
            SELECT 
                Product_ID,
                Product_Name,
                Category,
                COUNT(*) AS Total_Orders,
                SUM(Quantity_Sold) AS Total_Quantity,
                ROUND(SUM(Sales), 2) AS Total_Sales
            FROM retail_inventory
            GROUP BY Product_ID, Product_Name, Category
            ORDER BY Total_Sales DESC
            LIMIT 10
        """,
        
        "Top 10 Products by Quantity Sold": """
            SELECT 
                Product_Name,
                SUM(Quantity_Sold) AS Total_Quantity_Sold,
                ROUND(SUM(Sales), 2) AS Total_Revenue
            FROM retail_inventory
            GROUP BY Product_ID, Product_Name
            ORDER BY Total_Quantity_Sold DESC
            LIMIT 10
        """,
        
        "Monthly Sales Trends": """
            SELECT 
                strftime('%Y-%m', Order_Date) AS Month,
                COUNT(DISTINCT Order_ID) AS Total_Orders,
                SUM(Quantity_Sold) AS Total_Units_Sold,
                ROUND(SUM(Sales), 2) AS Total_Sales
            FROM retail_inventory
            GROUP BY strftime('%Y-%m', Order_Date)
            ORDER BY Month
        """,
        
        "Slow-Moving Products": """
            SELECT 
                Product_Name,
                Category,
                SUM(Quantity_Sold) AS Total_Sold,
                MAX(Inventory_Level) AS Current_Stock,
                ROUND(CAST(SUM(Quantity_Sold) AS FLOAT) / NULLIF(MAX(Inventory_Level), 0), 2) AS Turnover_Ratio
            FROM retail_inventory
            GROUP BY Product_ID, Product_Name, Category
            HAVING Turnover_Ratio < 3
            ORDER BY Turnover_Ratio ASC
        """,
        
        "Category Performance": """
            SELECT 
                Category,
                COUNT(DISTINCT Product_ID) AS Unique_Products,
                SUM(Quantity_Sold) AS Total_Units_Sold,
                ROUND(SUM(Sales), 2) AS Total_Revenue,
                ROUND(SUM(Sales) * 100.0 / (SELECT SUM(Sales) FROM retail_inventory), 2) AS Revenue_Percentage
            FROM retail_inventory
            GROUP BY Category
            ORDER BY Total_Revenue DESC
        """
    }
    
    for query_name, query in queries.items():
        print(f"\n📊 {query_name}:")
        print("-" * 50)
        result = pd.read_sql_query(query, conn)
        print(result.to_string(index=False))
    
    return queries

def main():
    """Main execution function."""
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Create database and load data
    conn = create_database()
    
    # Run sample queries
    run_sample_queries(conn)
    
    # Close connection
    conn.close()
    
    print("\n" + "=" * 60)
    print("DATABASE OPERATIONS COMPLETE!")
    print("=" * 60)
    print(f"\nDatabase saved to: {DB_PATH}")
    print("You can now run additional queries using any SQLite client.")

if __name__ == "__main__":
    main()
