# 📦 Inventory Optimization Project - MR DIY Retail Analysis

## 🎯 Project Overview

This end-to-end inventory optimization project demonstrates practical business analysis skills using Python and SQL. It simulates a real-world retail scenario for a company like MR DIY, analyzing sales patterns, inventory levels, and demand forecasting.

---

## 📁 Project Structure

```
scripts/
├── data/
│   └── retail_inventory_data.csv    # Sample dataset (100 records)
├── output/
│   ├── charts/                      # Generated visualizations
│   ├── demand_analysis.csv          # Demand statistics export
│   ├── abc_analysis.csv             # ABC classification export
│   ├── inventory_planning.csv       # Reorder points export
│   └── product_movement.csv         # Movement analysis export
├── inventory_analysis.py            # Main Python analysis script
├── inventory_queries.sql            # SQL queries reference
├── load_data_to_sqlite.py           # SQLite database loader
└── PROJECT_GUIDE.md                 # This documentation
```

---

## 🚀 How to Run the Project

### Prerequisites
```bash
# Install required Python packages
pip install pandas numpy matplotlib seaborn
```

### Step 1: Run Python Analysis
```bash
cd scripts
python inventory_analysis.py
```

### Step 2: Load Data into SQLite (Optional)
```bash
python load_data_to_sqlite.py
```

### Step 3: Run SQL Queries
- Open `inventory_queries.sql` in any SQL client
- Connect to `data/retail_inventory.db`
- Execute queries individually

---

## 📊 Key Analysis Components

### 1. Data Cleaning
- Null value handling
- Duplicate removal
- Date formatting
- Data validation

### 2. Demand Analysis
- Average/Max/Min demand per product
- Demand variability (Coefficient of Variation)
- Demand pattern classification (Stable/Moderate/Volatile)

### 3. Product Movement Classification
- **Fast-Moving**: High turnover ratio (≥75th percentile)
- **Medium-Moving**: Normal turnover
- **Slow-Moving**: Low turnover ratio (≤25th percentile)

### 4. ABC Analysis
- **Class A**: Top ~70% of revenue (tight control needed)
- **Class B**: Next ~20% of revenue (normal control)
- **Class C**: Bottom ~10% of revenue (simple control)

### 5. Inventory Planning
- **Safety Stock** = Z × σ × √Lead Time (95% service level)
- **Reorder Point** = (Daily Demand × Lead Time) + Safety Stock

### 6. Visualizations Generated
1. Monthly Sales Trend
2. Top 10 Products by Sales
3. Category Performance (Pie + Bar)
4. ABC Pareto Chart
5. Inventory Status Heatmap
6. Product Movement Distribution

---

## 💡 Business Insights Delivered

### Products Requiring Action
- Items below reorder point
- Overstocked products for clearance
- Volatile demand products needing higher safety stock

### Category Performance
- Best/worst performing categories
- Revenue contribution analysis

### Recommendations
- Immediate restocking priorities
- Promotional opportunities for slow movers
- Supplier negotiation targets

---

## 🎤 Interview Presentation Tips

### Opening (30 seconds)
> "I built an end-to-end inventory optimization solution for a retail company similar to MR DIY, analyzing 100 transactions across 20 products to identify restocking priorities and cost-saving opportunities."

### Key Talking Points

1. **Business Problem**
   - Retail companies face stockouts and overstock situations
   - Manual inventory management leads to lost sales and excess costs

2. **My Approach**
   - Used Python for data analysis and visualization
   - Implemented SQL for scalable querying
   - Applied industry-standard frameworks (ABC Analysis, Safety Stock)

3. **Technical Skills Demonstrated**
   - Data cleaning and transformation (Pandas)
   - Statistical analysis (demand variability, standard deviation)
   - Data visualization (Matplotlib, Seaborn)
   - Database management (SQL/SQLite)

4. **Business Impact**
   - Identified X products needing immediate reorder
   - Found Y products suitable for clearance promotions
   - Provided category-level strategic recommendations

### Questions to Anticipate

- "How would you handle missing data?"
- "What assumptions did you make for safety stock?"
- "How would this scale to thousands of products?"
- "How would you automate this process?"

---

## 📈 Dashboard Conversion Guide

### Power BI Implementation
1. Import CSV files from `output/` folder
2. Create relationships between tables
3. Build visuals:
   - Card visuals for KPIs (Total Sales, Stockout Count)
   - Bar chart for Top Products
   - Pie chart for Category Distribution
   - Matrix for ABC Analysis
   - Conditional formatting for stock alerts

### Excel Dashboard
1. Use Power Query to load CSV files
2. Create PivotTables for aggregations
3. Build charts using PivotChart
4. Add slicers for Category/Movement filters
5. Use Conditional Formatting for alerts

### Tableau Alternative
1. Connect to SQLite database
2. Create calculated fields for Turnover Ratio, ABC Class
3. Build interactive dashboard with filters
4. Publish to Tableau Public for portfolio

---

## 🔧 Customization Options

### Using Your Own Dataset
Replace `data/retail_inventory_data.csv` with your data. Required columns:
- Order_ID, Order_Date, Product_ID, Product_Name
- Category, Unit_Price, Quantity_Sold, Sales
- Inventory_Level, Reorder_Threshold, Supplier_Lead_Time

### Adjusting Parameters
In `inventory_analysis.py`:
```python
Z_SCORE = 1.65  # Change for different service levels
# 1.28 = 90%, 1.65 = 95%, 2.33 = 99%
```

### Adding More Products
Extend the CSV file with additional product records following the same format.

---

## ✅ Skills Demonstrated

| Skill Area | Technologies |
|------------|--------------|
| Data Analysis | Python, Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Database | SQL, SQLite |
| Business Analysis | ABC Analysis, Demand Forecasting |
| Inventory Management | Safety Stock, Reorder Points |
| Documentation | Markdown, Code Comments |

---

## 📞 Contact

**Portfolio Project by:** [Your Name]  
**LinkedIn:** [Your LinkedIn]  
**GitHub:** [Your GitHub]

---

*This project is designed for educational and portfolio purposes, simulating real-world retail inventory optimization scenarios.*
