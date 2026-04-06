"""
================================================================================
INVENTORY OPTIMIZATION PROJECT - MR DIY RETAIL ANALYSIS
================================================================================
Author: [Your Name]
Date: 2024
Purpose: End-to-end inventory analysis for retail optimization
Tools: Python (Pandas, Matplotlib, Seaborn)
================================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
from io import StringIO

# Set visualization style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# Output directory
OUTPUT_DIR = '/tmp/inventory_output'
os.makedirs(f'{OUTPUT_DIR}/charts', exist_ok=True)

# ============================================================================
# EMBEDDED DATA - Retail Inventory Dataset
# ============================================================================
DATA_CSV = """Order_ID,Order_Date,Product_ID,Product_Name,Category,Unit_Price,Quantity_Sold,Sales,Inventory_Level,Reorder_Threshold,Supplier_Lead_Time
1001,2024-01-05,P001,Power Drill,Tools,89.99,3,269.97,45,20,7
1002,2024-01-05,P002,LED Bulb Pack,Electrical,12.99,15,194.85,200,50,5
1003,2024-01-06,P003,Paint Brush Set,Paint,24.99,8,199.92,120,30,4
1004,2024-01-07,P004,Garden Hose,Garden,34.99,5,174.95,35,15,6
1005,2024-01-08,P005,Screwdriver Set,Tools,29.99,12,359.88,80,25,5
1006,2024-01-09,P006,Wall Paint 5L,Paint,45.99,20,919.80,150,40,7
1007,2024-01-10,P007,Extension Cord,Electrical,18.99,25,474.75,180,45,5
1008,2024-01-11,P008,Hammer,Tools,19.99,10,199.90,60,20,4
1009,2024-01-12,P009,Plant Pot Large,Garden,15.99,18,287.82,90,25,6
1010,2024-01-13,P010,Masking Tape,Paint,6.99,40,279.60,250,60,3
1011,2024-01-14,P001,Power Drill,Tools,89.99,4,359.96,41,20,7
1012,2024-01-15,P002,LED Bulb Pack,Electrical,12.99,20,259.80,180,50,5
1013,2024-01-16,P003,Paint Brush Set,Paint,24.99,6,149.94,114,30,4
1014,2024-01-17,P004,Garden Hose,Garden,34.99,3,104.97,32,15,6
1015,2024-01-18,P005,Screwdriver Set,Tools,29.99,8,239.92,72,25,5
1016,2024-01-19,P006,Wall Paint 5L,Paint,45.99,25,1149.75,125,40,7
1017,2024-01-20,P007,Extension Cord,Electrical,18.99,30,569.70,150,45,5
1018,2024-01-21,P008,Hammer,Tools,19.99,7,139.93,53,20,4
1019,2024-01-22,P009,Plant Pot Large,Garden,15.99,12,191.88,78,25,6
1020,2024-01-23,P010,Masking Tape,Paint,6.99,35,244.65,215,60,3
1021,2024-01-24,P011,Wire Cutter,Tools,22.99,5,114.95,40,15,5
1022,2024-01-25,P012,Solar Light Set,Garden,49.99,8,399.92,25,10,8
1023,2024-01-26,P013,Spray Paint,Paint,8.99,30,269.70,180,50,4
1024,2024-01-27,P014,USB Charger,Electrical,14.99,45,674.55,220,60,5
1025,2024-01-28,P015,Wrench Set,Tools,39.99,6,239.94,35,12,6
1026,2024-01-29,P001,Power Drill,Tools,89.99,5,449.95,36,20,7
1027,2024-01-30,P002,LED Bulb Pack,Electrical,12.99,18,233.82,162,50,5
1028,2024-01-31,P003,Paint Brush Set,Paint,24.99,10,249.90,104,30,4
1029,2024-02-01,P004,Garden Hose,Garden,34.99,7,244.93,25,15,6
1030,2024-02-02,P005,Screwdriver Set,Tools,29.99,15,449.85,57,25,5
1031,2024-02-03,P006,Wall Paint 5L,Paint,45.99,18,827.82,107,40,7
1032,2024-02-04,P007,Extension Cord,Electrical,18.99,22,417.78,128,45,5
1033,2024-02-05,P008,Hammer,Tools,19.99,9,179.91,44,20,4
1034,2024-02-06,P009,Plant Pot Large,Garden,15.99,15,239.85,63,25,6
1035,2024-02-07,P010,Masking Tape,Paint,6.99,50,349.50,165,60,3
1036,2024-02-08,P011,Wire Cutter,Tools,22.99,4,91.96,36,15,5
1037,2024-02-09,P012,Solar Light Set,Garden,49.99,6,299.94,19,10,8
1038,2024-02-10,P013,Spray Paint,Paint,8.99,25,224.75,155,50,4
1039,2024-02-11,P014,USB Charger,Electrical,14.99,50,749.50,170,60,5
1040,2024-02-12,P015,Wrench Set,Tools,39.99,4,159.96,31,12,6
1041,2024-02-13,P001,Power Drill,Tools,89.99,6,539.94,30,20,7
1042,2024-02-14,P002,LED Bulb Pack,Electrical,12.99,22,285.78,140,50,5
1043,2024-02-15,P003,Paint Brush Set,Paint,24.99,9,224.91,95,30,4
1044,2024-02-16,P004,Garden Hose,Garden,34.99,8,279.92,17,15,6
1045,2024-02-17,P005,Screwdriver Set,Tools,29.99,11,329.89,46,25,5
1046,2024-02-18,P006,Wall Paint 5L,Paint,45.99,22,1011.78,85,40,7
1047,2024-02-19,P007,Extension Cord,Electrical,18.99,28,531.72,100,45,5
1048,2024-02-20,P008,Hammer,Tools,19.99,8,159.92,36,20,4
1049,2024-02-21,P009,Plant Pot Large,Garden,15.99,10,159.90,53,25,6
1050,2024-02-22,P010,Masking Tape,Paint,6.99,45,314.55,120,60,3
1051,2024-02-23,P011,Wire Cutter,Tools,22.99,6,137.94,30,15,5
1052,2024-02-24,P012,Solar Light Set,Garden,49.99,10,499.90,9,10,8
1053,2024-02-25,P013,Spray Paint,Paint,8.99,35,314.65,120,50,4
1054,2024-02-26,P014,USB Charger,Electrical,14.99,40,599.60,130,60,5
1055,2024-02-27,P015,Wrench Set,Tools,39.99,5,199.95,26,12,6
1056,2024-02-28,P016,Ceiling Fan,Electrical,129.99,3,389.97,15,8,10
1057,2024-02-29,P017,Lawn Mower,Garden,299.99,2,599.98,8,5,14
1058,2024-03-01,P018,Wood Stain,Paint,35.99,12,431.88,45,15,6
1059,2024-03-02,P019,Measuring Tape,Tools,9.99,20,199.80,100,30,3
1060,2024-03-03,P020,Battery Pack,Electrical,24.99,35,874.65,150,40,5
1061,2024-03-04,P001,Power Drill,Tools,89.99,7,629.93,23,20,7
1062,2024-03-05,P002,LED Bulb Pack,Electrical,12.99,25,324.75,115,50,5
1063,2024-03-06,P003,Paint Brush Set,Paint,24.99,11,274.89,84,30,4
1064,2024-03-07,P004,Garden Hose,Garden,34.99,10,349.90,7,15,6
1065,2024-03-08,P005,Screwdriver Set,Tools,29.99,14,419.86,32,25,5
1066,2024-03-09,P006,Wall Paint 5L,Paint,45.99,30,1379.70,55,40,7
1067,2024-03-10,P007,Extension Cord,Electrical,18.99,35,664.65,65,45,5
1068,2024-03-11,P008,Hammer,Tools,19.99,12,239.88,24,20,4
1069,2024-03-12,P009,Plant Pot Large,Garden,15.99,14,223.86,39,25,6
1070,2024-03-13,P010,Masking Tape,Paint,6.99,55,384.45,65,60,3
1071,2024-03-14,P011,Wire Cutter,Tools,22.99,8,183.92,22,15,5
1072,2024-03-15,P012,Solar Light Set,Garden,49.99,12,599.88,0,10,8
1073,2024-03-16,P013,Spray Paint,Paint,8.99,40,359.60,80,50,4
1074,2024-03-17,P014,USB Charger,Electrical,14.99,55,824.45,75,60,5
1075,2024-03-18,P015,Wrench Set,Tools,39.99,7,279.93,19,12,6
1076,2024-03-19,P016,Ceiling Fan,Electrical,129.99,4,519.96,11,8,10
1077,2024-03-20,P017,Lawn Mower,Garden,299.99,3,899.97,5,5,14
1078,2024-03-21,P018,Wood Stain,Paint,35.99,15,539.85,30,15,6
1079,2024-03-22,P019,Measuring Tape,Tools,9.99,25,249.75,75,30,3
1080,2024-03-23,P020,Battery Pack,Electrical,24.99,42,1049.58,108,40,5
1081,2024-03-24,P001,Power Drill,Tools,89.99,8,719.92,15,20,7
1082,2024-03-25,P002,LED Bulb Pack,Electrical,12.99,30,389.70,85,50,5
1083,2024-03-26,P003,Paint Brush Set,Paint,24.99,13,324.87,71,30,4
1084,2024-03-27,P004,Garden Hose,Garden,34.99,12,419.88,0,15,6
1085,2024-03-28,P005,Screwdriver Set,Tools,29.99,16,479.84,16,25,5
1086,2024-03-29,P006,Wall Paint 5L,Paint,45.99,28,1287.72,27,40,7
1087,2024-03-30,P007,Extension Cord,Electrical,18.99,32,607.68,33,45,5
1088,2024-03-31,P008,Hammer,Tools,19.99,11,219.89,13,20,4
1089,2024-04-01,P009,Plant Pot Large,Garden,15.99,16,255.84,23,25,6
1090,2024-04-02,P010,Masking Tape,Paint,6.99,60,419.40,5,60,3
1091,2024-04-03,P011,Wire Cutter,Tools,22.99,10,229.90,12,15,5
1092,2024-04-04,P012,Solar Light Set,Garden,49.99,15,749.85,0,10,8
1093,2024-04-05,P013,Spray Paint,Paint,8.99,45,404.55,35,50,4
1094,2024-04-06,P014,USB Charger,Electrical,14.99,60,899.40,15,60,5
1095,2024-04-07,P015,Wrench Set,Tools,39.99,9,359.91,10,12,6
1096,2024-04-08,P016,Ceiling Fan,Electrical,129.99,5,649.95,6,8,10
1097,2024-04-09,P017,Lawn Mower,Garden,299.99,4,1199.96,1,5,14
1098,2024-04-10,P018,Wood Stain,Paint,35.99,18,647.82,12,15,6
1099,2024-04-11,P019,Measuring Tape,Tools,9.99,30,299.70,45,30,3
1100,2024-04-12,P020,Battery Pack,Electrical,24.99,48,1199.52,60,40,5"""

# ============================================================================
# SECTION 1: DATA LOADING
# ============================================================================
print("=" * 60)
print("SECTION 1: DATA LOADING")
print("=" * 60)

# Load the retail inventory dataset from embedded data
df = pd.read_csv(StringIO(DATA_CSV))

# Display basic information
print(f"\n✓ Dataset loaded successfully!")
print(f"  - Total Records: {len(df)}")
print(f"  - Total Columns: {len(df.columns)}")
print(f"\nColumn Names:")
for col in df.columns:
    print(f"  • {col}")

print(f"\nFirst 5 rows of data:")
print(df.head().to_string())

print(f"\nData Types:")
print(df.dtypes)

# ============================================================================
# SECTION 2: DATA CLEANING
# ============================================================================
print("\n" + "=" * 60)
print("SECTION 2: DATA CLEANING")
print("=" * 60)

# 2.1 Check for missing values
print("\n2.1 Missing Values Analysis:")
missing_values = df.isnull().sum()
print(missing_values[missing_values > 0] if missing_values.sum() > 0 else "  ✓ No missing values found!")

# 2.2 Check for duplicates
print("\n2.2 Duplicate Records:")
duplicates = df.duplicated().sum()
print(f"  • Duplicate rows found: {duplicates}")
if duplicates > 0:
    df = df.drop_duplicates()
    print(f"  ✓ Duplicates removed. New record count: {len(df)}")

# 2.3 Convert date column to datetime format
print("\n2.3 Date Formatting:")
df['Order_Date'] = pd.to_datetime(df['Order_Date'])
print(f"  ✓ Order_Date converted to datetime")
print(f"  • Date Range: {df['Order_Date'].min().date()} to {df['Order_Date'].max().date()}")

# 2.4 Add derived columns for analysis
df['Month'] = df['Order_Date'].dt.month
df['Month_Name'] = df['Order_Date'].dt.strftime('%B')
df['Week'] = df['Order_Date'].dt.isocalendar().week
df['Day_of_Week'] = df['Order_Date'].dt.day_name()

print("\n2.4 Derived Columns Added:")
print("  • Month, Month_Name, Week, Day_of_Week")

# 2.5 Data validation
print("\n2.5 Data Validation:")
print(f"  • Negative Sales: {(df['Sales'] < 0).sum()}")
print(f"  • Negative Quantities: {(df['Quantity_Sold'] < 0).sum()}")
print(f"  • Zero Inventory Items: {(df['Inventory_Level'] == 0).sum()}")

# ============================================================================
# SECTION 3: DEMAND ANALYSIS
# ============================================================================
print("\n" + "=" * 60)
print("SECTION 3: DEMAND ANALYSIS")
print("=" * 60)

# 3.1 Product-level demand statistics
demand_stats = df.groupby(['Product_ID', 'Product_Name', 'Category']).agg({
    'Quantity_Sold': ['sum', 'mean', 'max', 'min', 'std'],
    'Sales': ['sum', 'mean'],
    'Order_ID': 'count'
}).round(2)

demand_stats.columns = ['Total_Qty', 'Avg_Qty', 'Max_Qty', 'Min_Qty', 'Std_Qty', 
                        'Total_Sales', 'Avg_Sales', 'Order_Count']
demand_stats = demand_stats.reset_index()

print("\n3.1 Product Demand Statistics:")
print(demand_stats.to_string())

# 3.2 Demand variability (Coefficient of Variation)
demand_stats['CV'] = (demand_stats['Std_Qty'] / demand_stats['Avg_Qty'] * 100).round(2)
demand_stats['Demand_Pattern'] = demand_stats['CV'].apply(
    lambda x: 'Stable' if x < 30 else ('Moderate' if x < 60 else 'Volatile')
)

print("\n3.2 Demand Variability Analysis:")
print(demand_stats[['Product_Name', 'Avg_Qty', 'Std_Qty', 'CV', 'Demand_Pattern']].to_string())

# ============================================================================
# SECTION 4: FAST-MOVING vs SLOW-MOVING PRODUCTS
# ============================================================================
print("\n" + "=" * 60)
print("SECTION 4: FAST-MOVING vs SLOW-MOVING PRODUCTS")
print("=" * 60)

# Calculate inventory turnover ratio
latest_inventory = df.groupby('Product_ID')['Inventory_Level'].last().reset_index()
latest_inventory.columns = ['Product_ID', 'Current_Inventory']

product_movement = demand_stats.merge(latest_inventory, on='Product_ID')
product_movement['Turnover_Ratio'] = (product_movement['Total_Qty'] / 
                                       product_movement['Current_Inventory'].replace(0, 1)).round(2)

# Classify products based on turnover
turnover_threshold_fast = product_movement['Turnover_Ratio'].quantile(0.75)
turnover_threshold_slow = product_movement['Turnover_Ratio'].quantile(0.25)

product_movement['Movement_Category'] = product_movement['Turnover_Ratio'].apply(
    lambda x: 'Fast-Moving' if x >= turnover_threshold_fast else 
              ('Slow-Moving' if x <= turnover_threshold_slow else 'Medium-Moving')
)

print("\n4.1 Product Movement Classification:")
print(f"  • Fast-Moving Threshold (75th percentile): {turnover_threshold_fast:.2f}")
print(f"  • Slow-Moving Threshold (25th percentile): {turnover_threshold_slow:.2f}")

print("\n4.2 Fast-Moving Products (High Demand):")
fast_moving = product_movement[product_movement['Movement_Category'] == 'Fast-Moving']
print(fast_moving[['Product_Name', 'Total_Qty', 'Current_Inventory', 'Turnover_Ratio']].to_string())

print("\n4.3 Slow-Moving Products (Low Demand):")
slow_moving = product_movement[product_movement['Movement_Category'] == 'Slow-Moving']
print(slow_moving[['Product_Name', 'Total_Qty', 'Current_Inventory', 'Turnover_Ratio']].to_string())

print("\n4.4 Movement Summary:")
print(product_movement['Movement_Category'].value_counts())

# ============================================================================
# SECTION 5: ABC ANALYSIS
# ============================================================================
print("\n" + "=" * 60)
print("SECTION 5: ABC ANALYSIS (Pareto Principle)")
print("=" * 60)

# Sort products by total sales (descending)
abc_analysis = product_movement[['Product_ID', 'Product_Name', 'Category', 'Total_Sales']].copy()
abc_analysis = abc_analysis.sort_values('Total_Sales', ascending=False)

# Calculate cumulative percentage
abc_analysis['Cumulative_Sales'] = abc_analysis['Total_Sales'].cumsum()
abc_analysis['Cumulative_Percentage'] = (abc_analysis['Cumulative_Sales'] / 
                                          abc_analysis['Total_Sales'].sum() * 100).round(2)

# Classify into A, B, C categories
def classify_abc(cum_pct):
    if cum_pct <= 70:
        return 'A'  # Top 70% of sales
    elif cum_pct <= 90:
        return 'B'  # Next 20% of sales
    else:
        return 'C'  # Bottom 10% of sales

abc_analysis['ABC_Class'] = abc_analysis['Cumulative_Percentage'].apply(classify_abc)

print("\n5.1 ABC Classification Results:")
print(abc_analysis[['Product_Name', 'Total_Sales', 'Cumulative_Percentage', 'ABC_Class']].to_string())

print("\n5.2 ABC Summary:")
abc_summary = abc_analysis.groupby('ABC_Class').agg({
    'Product_ID': 'count',
    'Total_Sales': 'sum'
}).rename(columns={'Product_ID': 'Product_Count'})
abc_summary['Sales_Percentage'] = (abc_summary['Total_Sales'] / abc_summary['Total_Sales'].sum() * 100).round(2)
print(abc_summary)

print("\n5.3 ABC Analysis Interpretation:")
print("  • Class A: High-value items - Require tight inventory control")
print("  • Class B: Moderate-value items - Normal inventory control")
print("  • Class C: Low-value items - Simple inventory control")

# ============================================================================
# SECTION 6: REORDER POINT & SAFETY STOCK CALCULATION
# ============================================================================
print("\n" + "=" * 60)
print("SECTION 6: REORDER POINT & SAFETY STOCK")
print("=" * 60)

# Get lead time data
lead_time_data = df.groupby('Product_ID')['Supplier_Lead_Time'].first().reset_index()

# Merge with demand stats
inventory_planning = demand_stats.merge(lead_time_data, on='Product_ID')

# Calculate daily demand (assuming 90 days of data)
days_in_period = (df['Order_Date'].max() - df['Order_Date'].min()).days + 1
inventory_planning['Daily_Demand'] = (inventory_planning['Total_Qty'] / days_in_period).round(2)
inventory_planning['Daily_Std'] = (inventory_planning['Std_Qty'] / np.sqrt(inventory_planning['Order_Count'])).round(2)

# Safety Stock = Z-score × Standard Deviation of Demand × √Lead Time
# Using Z = 1.65 for 95% service level
Z_SCORE = 1.65

inventory_planning['Safety_Stock'] = (
    Z_SCORE * inventory_planning['Daily_Std'] * 
    np.sqrt(inventory_planning['Supplier_Lead_Time'])
).round(0)

# Reorder Point = (Daily Demand × Lead Time) + Safety Stock
inventory_planning['Reorder_Point'] = (
    inventory_planning['Daily_Demand'] * inventory_planning['Supplier_Lead_Time'] + 
    inventory_planning['Safety_Stock']
).round(0)

print("\n6.1 Inventory Planning Parameters:")
print(f"  • Service Level: 95% (Z-score = {Z_SCORE})")
print(f"  • Analysis Period: {days_in_period} days")

print("\n6.2 Reorder Point & Safety Stock by Product:")
inventory_output = inventory_planning[['Product_Name', 'Daily_Demand', 'Supplier_Lead_Time', 
                                        'Safety_Stock', 'Reorder_Point']]
print(inventory_output.to_string())

# Merge with current inventory to identify items needing reorder
inventory_planning = inventory_planning.merge(latest_inventory, on='Product_ID')
inventory_planning['Needs_Reorder'] = inventory_planning['Current_Inventory'] <= inventory_planning['Reorder_Point']

print("\n6.3 Products Needing Immediate Reorder:")
reorder_needed = inventory_planning[inventory_planning['Needs_Reorder']]
if len(reorder_needed) > 0:
    print(reorder_needed[['Product_Name', 'Current_Inventory', 'Reorder_Point', 'Safety_Stock']].to_string())
else:
    print("  ✓ No products currently need reordering")

# ============================================================================
# SECTION 7: VISUALIZATIONS
# ============================================================================
print("\n" + "=" * 60)
print("SECTION 7: GENERATING VISUALIZATIONS")
print("=" * 60)

# 7.1 Monthly Sales Trend
fig, ax = plt.subplots(figsize=(12, 6))
monthly_sales = df.groupby(df['Order_Date'].dt.to_period('M'))['Sales'].sum()
monthly_sales.index = monthly_sales.index.astype(str)
ax.plot(monthly_sales.index, monthly_sales.values, marker='o', linewidth=2, markersize=8)
ax.fill_between(monthly_sales.index, monthly_sales.values, alpha=0.3)
ax.set_title('Monthly Sales Trend', fontsize=14, fontweight='bold')
ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Total Sales ($)', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'charts/01_monthly_sales_trend.png'), dpi=150)
plt.close()
print("  ✓ Chart saved: 01_monthly_sales_trend.png")

# 7.2 Top 10 Products by Sales
fig, ax = plt.subplots(figsize=(12, 6))
top_products = demand_stats.nlargest(10, 'Total_Sales')[['Product_Name', 'Total_Sales']]
colors = sns.color_palette("viridis", 10)
bars = ax.barh(top_products['Product_Name'], top_products['Total_Sales'], color=colors)
ax.set_title('Top 10 Products by Total Sales', fontsize=14, fontweight='bold')
ax.set_xlabel('Total Sales ($)', fontsize=12)
ax.invert_yaxis()
for bar, value in zip(bars, top_products['Total_Sales']):
    ax.text(value + 50, bar.get_y() + bar.get_height()/2, f'${value:,.0f}', 
            va='center', fontsize=10)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'charts/02_top_products_sales.png'), dpi=150)
plt.close()
print("  ✓ Chart saved: 02_top_products_sales.png")

# 7.3 Category Performance
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Sales by Category
category_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
colors = sns.color_palette("Set2", len(category_sales))
axes[0].pie(category_sales, labels=category_sales.index, autopct='%1.1f%%', 
            colors=colors, startangle=90, explode=[0.05]*len(category_sales))
axes[0].set_title('Sales Distribution by Category', fontsize=12, fontweight='bold')

# Quantity by Category
category_qty = df.groupby('Category')['Quantity_Sold'].sum().sort_values(ascending=False)
axes[1].bar(category_qty.index, category_qty.values, color=colors)
axes[1].set_title('Quantity Sold by Category', fontsize=12, fontweight='bold')
axes[1].set_xlabel('Category', fontsize=10)
axes[1].set_ylabel('Total Quantity', fontsize=10)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'charts/03_category_performance.png'), dpi=150)
plt.close()
print("  ✓ Chart saved: 03_category_performance.png")

# 7.4 ABC Analysis Pareto Chart
fig, ax1 = plt.subplots(figsize=(14, 7))

# Bar chart for individual sales
colors_abc = ['#2ecc71' if c == 'A' else '#f39c12' if c == 'B' else '#e74c3c' 
              for c in abc_analysis['ABC_Class']]
bars = ax1.bar(range(len(abc_analysis)), abc_analysis['Total_Sales'], color=colors_abc, alpha=0.8)
ax1.set_ylabel('Total Sales ($)', fontsize=12)
ax1.set_xlabel('Products (Ranked by Sales)', fontsize=12)
ax1.set_xticks(range(len(abc_analysis)))
ax1.set_xticklabels(abc_analysis['Product_Name'], rotation=45, ha='right', fontsize=9)

# Line chart for cumulative percentage
ax2 = ax1.twinx()
ax2.plot(range(len(abc_analysis)), abc_analysis['Cumulative_Percentage'], 
         color='#3498db', marker='o', linewidth=2, markersize=6)
ax2.axhline(y=70, color='green', linestyle='--', alpha=0.7, label='70% (A cutoff)')
ax2.axhline(y=90, color='orange', linestyle='--', alpha=0.7, label='90% (B cutoff)')
ax2.set_ylabel('Cumulative Percentage (%)', fontsize=12)
ax2.legend(loc='center right')

plt.title('ABC Analysis - Pareto Chart', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'charts/04_abc_pareto_chart.png'), dpi=150)
plt.close()
print("  ✓ Chart saved: 04_abc_pareto_chart.png")

# 7.5 Inventory Status Heatmap
fig, ax = plt.subplots(figsize=(12, 8))
inventory_status = inventory_planning[['Product_Name', 'Current_Inventory', 'Reorder_Point', 
                                        'Safety_Stock', 'Daily_Demand']].set_index('Product_Name')
sns.heatmap(inventory_status, annot=True, fmt='.0f', cmap='RdYlGn', 
            linewidths=0.5, ax=ax)
ax.set_title('Inventory Status Dashboard', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'charts/05_inventory_heatmap.png'), dpi=150)
plt.close()
print("  ✓ Chart saved: 05_inventory_heatmap.png")

# 7.6 Product Movement Distribution
fig, ax = plt.subplots(figsize=(10, 6))
movement_counts = product_movement['Movement_Category'].value_counts()
colors = {'Fast-Moving': '#27ae60', 'Medium-Moving': '#f39c12', 'Slow-Moving': '#e74c3c'}
bars = ax.bar(movement_counts.index, movement_counts.values, 
              color=[colors[x] for x in movement_counts.index])
ax.set_title('Product Movement Distribution', fontsize=14, fontweight='bold')
ax.set_xlabel('Movement Category', fontsize=12)
ax.set_ylabel('Number of Products', fontsize=12)
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height, f'{int(height)}',
            ha='center', va='bottom', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'charts/06_movement_distribution.png'), dpi=150)
plt.close()
print("  ✓ Chart saved: 06_movement_distribution.png")

# ============================================================================
# SECTION 8: BUSINESS INSIGHTS & RECOMMENDATIONS
# ============================================================================
print("\n" + "=" * 60)
print("SECTION 8: BUSINESS INSIGHTS & RECOMMENDATIONS")
print("=" * 60)

print("\n" + "-" * 60)
print("8.1 KEY FINDINGS")
print("-" * 60)

# Finding 1: Top Revenue Drivers
top_3_products = demand_stats.nlargest(3, 'Total_Sales')['Product_Name'].tolist()
print(f"\n🔹 TOP REVENUE DRIVERS:")
print(f"   The top 3 products by sales are: {', '.join(top_3_products)}")
print(f"   These products should have priority stock management.")

# Finding 2: Stockout Risk
stockout_risk = inventory_planning[inventory_planning['Current_Inventory'] <= inventory_planning['Safety_Stock']]
print(f"\n🔹 STOCKOUT RISK ALERT:")
print(f"   {len(stockout_risk)} product(s) have inventory below safety stock levels.")
if len(stockout_risk) > 0:
    print(f"   Products at risk: {', '.join(stockout_risk['Product_Name'].tolist())}")

# Finding 3: Overstock Situation
avg_inventory = inventory_planning['Current_Inventory'].mean()
overstocked = inventory_planning[inventory_planning['Current_Inventory'] > avg_inventory * 2]
print(f"\n🔹 OVERSTOCK ANALYSIS:")
print(f"   {len(overstocked)} product(s) may be overstocked (>2x average inventory).")
if len(overstocked) > 0:
    print(f"   Consider promotions for: {', '.join(overstocked['Product_Name'].tolist())}")

# Finding 4: Category Insights
best_category = df.groupby('Category')['Sales'].sum().idxmax()
worst_category = df.groupby('Category')['Sales'].sum().idxmin()
print(f"\n🔹 CATEGORY PERFORMANCE:")
print(f"   Best performing category: {best_category}")
print(f"   Lowest performing category: {worst_category}")

# Finding 5: Demand Patterns
volatile_products = demand_stats[demand_stats['Demand_Pattern'] == 'Volatile']
print(f"\n🔹 DEMAND VOLATILITY:")
print(f"   {len(volatile_products)} product(s) show volatile demand patterns.")
print(f"   These require higher safety stock levels.")

print("\n" + "-" * 60)
print("8.2 ACTIONABLE RECOMMENDATIONS")
print("-" * 60)

print("""
📋 IMMEDIATE ACTIONS (This Week):
   1. Place urgent orders for products below reorder point
   2. Review safety stock levels for volatile demand products
   3. Implement daily inventory checks for Class A items

📋 SHORT-TERM ACTIONS (This Month):
   1. Set up automated reorder alerts in inventory system
   2. Negotiate better lead times with suppliers for fast-moving items
   3. Plan promotional activities for slow-moving products
   4. Review and adjust reorder points based on seasonal trends

📋 LONG-TERM STRATEGY (This Quarter):
   1. Implement ABC-based inventory policies
   2. Develop supplier scorecards based on lead time reliability
   3. Consider demand forecasting tools for better planning
   4. Evaluate EOQ (Economic Order Quantity) for cost optimization
""")

# ============================================================================
# SECTION 9: EXPORT RESULTS
# ============================================================================
print("\n" + "=" * 60)
print("SECTION 9: EXPORTING ANALYSIS RESULTS")
print("=" * 60)

# Export key dataframes to CSV
demand_stats.to_csv(os.path.join(OUTPUT_DIR, 'demand_analysis.csv'), index=False)
print("  ✓ Exported: demand_analysis.csv")

abc_analysis.to_csv(os.path.join(OUTPUT_DIR, 'abc_analysis.csv'), index=False)
print("  ✓ Exported: abc_analysis.csv")

inventory_planning.to_csv(os.path.join(OUTPUT_DIR, 'inventory_planning.csv'), index=False)
print("  ✓ Exported: inventory_planning.csv")

product_movement.to_csv(os.path.join(OUTPUT_DIR, 'product_movement.csv'), index=False)
print("  ✓ Exported: product_movement.csv")

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE!")
print("=" * 60)
print(f"""
Summary:
  • Total Products Analyzed: {len(demand_stats)}
  • Products Needing Reorder: {len(reorder_needed)}
  • Class A Products: {len(abc_analysis[abc_analysis['ABC_Class'] == 'A'])}
  • Fast-Moving Products: {len(fast_moving)}
  • Slow-Moving Products: {len(slow_moving)}
  
Output Files:
  • Charts: output/charts/
  • Data: output/*.csv
""")
