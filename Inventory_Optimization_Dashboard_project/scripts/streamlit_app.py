"""
Inventory Optimization Dashboard - Streamlit App
A comprehensive dashboard for retail inventory analysis and optimization.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from io import StringIO

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Inventory Optimization Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# EMBEDDED DATA
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
# DATA LOADING AND PROCESSING
# ============================================================================
@st.cache_data
def load_data():
    """Load and preprocess the inventory data."""
    df = pd.read_csv(StringIO(DATA_CSV))
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    df['Month'] = df['Order_Date'].dt.to_period('M').astype(str)
    df['Week'] = df['Order_Date'].dt.isocalendar().week
    return df

@st.cache_data
def calculate_demand_stats(df):
    """Calculate demand statistics per product."""
    demand_stats = df.groupby(['Product_ID', 'Product_Name', 'Category']).agg({
        'Quantity_Sold': ['sum', 'mean', 'std', 'min', 'max', 'count'],
        'Sales': ['sum', 'mean'],
        'Unit_Price': 'first',
        'Inventory_Level': 'last',
        'Reorder_Threshold': 'first',
        'Supplier_Lead_Time': 'first'
    }).reset_index()
    
    demand_stats.columns = ['Product_ID', 'Product_Name', 'Category', 
                           'Total_Qty', 'Avg_Daily_Demand', 'Std_Demand', 
                           'Min_Demand', 'Max_Demand', 'Num_Transactions',
                           'Total_Sales', 'Avg_Sale', 'Unit_Price',
                           'Current_Inventory', 'Reorder_Point', 'Lead_Time']
    
    # Calculate Coefficient of Variation
    demand_stats['CV'] = (demand_stats['Std_Demand'] / demand_stats['Avg_Daily_Demand'] * 100).round(2)
    demand_stats['CV'] = demand_stats['CV'].fillna(0)
    
    return demand_stats

@st.cache_data
def perform_abc_analysis(df):
    """Perform ABC analysis on products."""
    product_sales = df.groupby(['Product_ID', 'Product_Name', 'Category'])['Sales'].sum().reset_index()
    product_sales = product_sales.sort_values('Sales', ascending=False)
    
    total_sales = product_sales['Sales'].sum()
    product_sales['Sales_Percentage'] = (product_sales['Sales'] / total_sales * 100).round(2)
    product_sales['Cumulative_Percentage'] = product_sales['Sales_Percentage'].cumsum().round(2)
    
    def assign_class(cum_pct):
        if cum_pct <= 70:
            return 'A'
        elif cum_pct <= 90:
            return 'B'
        else:
            return 'C'
    
    product_sales['ABC_Class'] = product_sales['Cumulative_Percentage'].apply(assign_class)
    
    return product_sales

@st.cache_data
def calculate_inventory_metrics(demand_stats):
    """Calculate inventory planning metrics."""
    Z_SCORE = 1.65  # 95% service level
    
    inventory_planning = demand_stats.copy()
    inventory_planning['Safety_Stock'] = np.ceil(
        Z_SCORE * inventory_planning['Std_Demand'].fillna(0) * 
        np.sqrt(inventory_planning['Lead_Time'])
    )
    
    inventory_planning['Reorder_Point_Calc'] = np.ceil(
        inventory_planning['Avg_Daily_Demand'] * inventory_planning['Lead_Time'] + 
        inventory_planning['Safety_Stock']
    )
    
    inventory_planning['Days_of_Supply'] = np.where(
        inventory_planning['Avg_Daily_Demand'] > 0,
        (inventory_planning['Current_Inventory'] / inventory_planning['Avg_Daily_Demand']).round(1),
        999
    )
    
    inventory_planning['Needs_Reorder'] = inventory_planning['Current_Inventory'] <= inventory_planning['Reorder_Point_Calc']
    
    # Inventory turnover
    inventory_planning['Turnover_Ratio'] = (
        inventory_planning['Total_Qty'] / inventory_planning['Current_Inventory'].replace(0, 1)
    ).round(2)
    
    return inventory_planning

@st.cache_data
def classify_movement(turnover):
    """Classify product movement based on turnover ratio."""
    if turnover >= 5:
        return 'Fast Moving'
    elif turnover >= 2:
        return 'Medium Moving'
    else:
        return 'Slow Moving'

# ============================================================================
# MAIN APP
# ============================================================================
def main():
    # Load data
    df = load_data()
    demand_stats = calculate_demand_stats(df)
    abc_analysis = perform_abc_analysis(df)
    inventory_metrics = calculate_inventory_metrics(demand_stats)
    inventory_metrics['Movement_Class'] = inventory_metrics['Turnover_Ratio'].apply(classify_movement)
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select Analysis",
        ["Overview", "Sales Analysis", "Demand Analysis", "ABC Analysis", 
         "Inventory Health", "Reorder Recommendations", "Raw Data"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Filters")
    
    categories = ['All'] + list(df['Category'].unique())
    selected_category = st.sidebar.selectbox("Category", categories)
    
    if selected_category != 'All':
        df_filtered = df[df['Category'] == selected_category]
    else:
        df_filtered = df
    
    # ========================================================================
    # PAGE: OVERVIEW
    # ========================================================================
    if page == "Overview":
        st.title("Inventory Optimization Dashboard")
        st.markdown("Comprehensive analysis for retail inventory management and optimization.")
        
        # KPI Cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Revenue",
                f"${df_filtered['Sales'].sum():,.2f}",
                delta=f"{len(df_filtered)} transactions"
            )
        
        with col2:
            st.metric(
                "Products",
                f"{df_filtered['Product_ID'].nunique()}",
                delta=f"{df_filtered['Category'].nunique()} categories"
            )
        
        with col3:
            needs_reorder = inventory_metrics[inventory_metrics['Needs_Reorder']].shape[0]
            st.metric(
                "Needs Reorder",
                f"{needs_reorder} products",
                delta="Action Required" if needs_reorder > 0 else "All Good",
                delta_color="inverse" if needs_reorder > 0 else "normal"
            )
        
        with col4:
            avg_turnover = inventory_metrics['Turnover_Ratio'].mean()
            st.metric(
                "Avg Turnover Ratio",
                f"{avg_turnover:.2f}x",
                delta="Inventory cycles"
            )
        
        st.markdown("---")
        
        # Quick Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Sales by Category")
            category_sales = df_filtered.groupby('Category')['Sales'].sum().reset_index()
            fig = px.pie(category_sales, values='Sales', names='Category', 
                        color_discrete_sequence=px.colors.qualitative.Set2)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Monthly Sales Trend")
            monthly_sales = df_filtered.groupby('Month')['Sales'].sum().reset_index()
            fig = px.line(monthly_sales, x='Month', y='Sales', markers=True,
                         color_discrete_sequence=['#2E86AB'])
            fig.update_layout(xaxis_title="Month", yaxis_title="Sales ($)")
            st.plotly_chart(fig, use_container_width=True)
        
        # ABC Summary
        st.subheader("ABC Classification Summary")
        abc_summary = abc_analysis.groupby('ABC_Class').agg({
            'Product_ID': 'count',
            'Sales': 'sum',
            'Sales_Percentage': 'sum'
        }).reset_index()
        abc_summary.columns = ['Class', 'Product Count', 'Total Sales', 'Sales %']
        
        col1, col2, col3 = st.columns(3)
        for i, row in abc_summary.iterrows():
            with [col1, col2, col3][i]:
                color = {'A': '#28a745', 'B': '#ffc107', 'C': '#dc3545'}[row['Class']]
                st.markdown(f"""
                <div style="background: {color}20; padding: 20px; border-radius: 10px; border-left: 5px solid {color};">
                    <h3 style="color: {color}; margin: 0;">Class {row['Class']}</h3>
                    <p style="margin: 10px 0;"><strong>{int(row['Product Count'])}</strong> products</p>
                    <p style="margin: 0;"><strong>{row['Sales %']:.1f}%</strong> of sales</p>
                </div>
                """, unsafe_allow_html=True)
    
    # ========================================================================
    # PAGE: SALES ANALYSIS
    # ========================================================================
    elif page == "Sales Analysis":
        st.title("Sales Analysis")
        
        # Top Products
        st.subheader("Top 10 Products by Revenue")
        top_products = df_filtered.groupby(['Product_ID', 'Product_Name'])['Sales'].sum().reset_index()
        top_products = top_products.nlargest(10, 'Sales')
        
        fig = px.bar(top_products, x='Sales', y='Product_Name', orientation='h',
                    color='Sales', color_continuous_scale='Blues')
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
        
        # Sales Over Time
        st.subheader("Daily Sales Trend")
        daily_sales = df_filtered.groupby('Order_Date')['Sales'].sum().reset_index()
        fig = px.area(daily_sales, x='Order_Date', y='Sales',
                     color_discrete_sequence=['#2E86AB'])
        fig.update_layout(xaxis_title="Date", yaxis_title="Sales ($)")
        st.plotly_chart(fig, use_container_width=True)
        
        # Category Performance
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Sales by Category")
            category_sales = df_filtered.groupby('Category').agg({
                'Sales': 'sum',
                'Quantity_Sold': 'sum'
            }).reset_index()
            
            fig = px.bar(category_sales, x='Category', y='Sales',
                        color='Category', color_discrete_sequence=px.colors.qualitative.Set2)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Units Sold by Category")
            fig = px.bar(category_sales, x='Category', y='Quantity_Sold',
                        color='Category', color_discrete_sequence=px.colors.qualitative.Set2)
            st.plotly_chart(fig, use_container_width=True)
    
    # ========================================================================
    # PAGE: DEMAND ANALYSIS
    # ========================================================================
    elif page == "Demand Analysis":
        st.title("Demand Analysis")
        
        st.markdown("""
        Demand analysis helps understand product sales patterns and variability. 
        The **Coefficient of Variation (CV)** measures demand volatility - higher values indicate more unpredictable demand.
        """)
        
        # Demand Statistics Table
        st.subheader("Demand Statistics by Product")
        display_cols = ['Product_Name', 'Category', 'Total_Qty', 'Avg_Daily_Demand', 
                       'Std_Demand', 'CV', 'Min_Demand', 'Max_Demand']
        
        styled_df = demand_stats[display_cols].copy()
        styled_df.columns = ['Product', 'Category', 'Total Qty', 'Avg Demand', 
                            'Std Dev', 'CV %', 'Min', 'Max']
        st.dataframe(styled_df.round(2), use_container_width=True)
        
        # Demand Variability Chart
        st.subheader("Demand Variability (Coefficient of Variation)")
        fig = px.bar(demand_stats.sort_values('CV', ascending=False), 
                    x='Product_Name', y='CV',
                    color='CV', color_continuous_scale='RdYlGn_r',
                    labels={'CV': 'CV %', 'Product_Name': 'Product'})
        fig.add_hline(y=50, line_dash="dash", line_color="red", 
                     annotation_text="High Variability Threshold")
        st.plotly_chart(fig, use_container_width=True)
        
        # Demand Distribution
        st.subheader("Demand Distribution by Product")
        selected_product = st.selectbox("Select Product", df['Product_Name'].unique())
        product_data = df[df['Product_Name'] == selected_product]
        
        fig = px.histogram(product_data, x='Quantity_Sold', nbins=10,
                          color_discrete_sequence=['#2E86AB'])
        fig.update_layout(xaxis_title="Quantity Sold", yaxis_title="Frequency")
        st.plotly_chart(fig, use_container_width=True)
    
    # ========================================================================
    # PAGE: ABC ANALYSIS
    # ========================================================================
    elif page == "ABC Analysis":
        st.title("ABC Analysis (Pareto Principle)")
        
        st.markdown("""
        ABC Analysis categorizes inventory based on value contribution:
        - **Class A**: Top ~20% of products contributing ~70% of sales (high priority)
        - **Class B**: Next ~30% contributing ~20% of sales (medium priority)  
        - **Class C**: Remaining ~50% contributing ~10% of sales (low priority)
        """)
        
        # Pareto Chart
        st.subheader("Pareto Chart")
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Bar(x=abc_analysis['Product_Name'], y=abc_analysis['Sales'],
                  name='Sales', marker_color='#2E86AB'),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(x=abc_analysis['Product_Name'], y=abc_analysis['Cumulative_Percentage'],
                      name='Cumulative %', line=dict(color='#E94F37', width=3), mode='lines+markers'),
            secondary_y=True
        )
        
        fig.add_hline(y=70, line_dash="dash", line_color="green", secondary_y=True)
        fig.add_hline(y=90, line_dash="dash", line_color="orange", secondary_y=True)
        
        fig.update_xaxes(tickangle=45)
        fig.update_yaxes(title_text="Sales ($)", secondary_y=False)
        fig.update_yaxes(title_text="Cumulative %", secondary_y=True)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # ABC Classification Table
        st.subheader("Product Classification")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            display_abc = abc_analysis[['Product_Name', 'Category', 'Sales', 
                                       'Sales_Percentage', 'Cumulative_Percentage', 'ABC_Class']]
            display_abc.columns = ['Product', 'Category', 'Sales', 'Sales %', 'Cumulative %', 'Class']
            st.dataframe(display_abc.round(2), use_container_width=True)
        
        with col2:
            class_counts = abc_analysis['ABC_Class'].value_counts().reset_index()
            class_counts.columns = ['Class', 'Count']
            fig = px.pie(class_counts, values='Count', names='Class',
                        color='Class', color_discrete_map={'A': '#28a745', 'B': '#ffc107', 'C': '#dc3545'})
            st.plotly_chart(fig, use_container_width=True)
    
    # ========================================================================
    # PAGE: INVENTORY HEALTH
    # ========================================================================
    elif page == "Inventory Health":
        st.title("Inventory Health Analysis")
        
        # Movement Classification
        st.subheader("Product Movement Classification")
        movement_counts = inventory_metrics['Movement_Class'].value_counts().reset_index()
        movement_counts.columns = ['Movement', 'Count']
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(movement_counts, values='Count', names='Movement',
                        color='Movement', 
                        color_discrete_map={'Fast Moving': '#28a745', 
                                           'Medium Moving': '#ffc107', 
                                           'Slow Moving': '#dc3545'})
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### Movement Classification Criteria")
            st.markdown("""
            | Classification | Turnover Ratio |
            |---------------|----------------|
            | Fast Moving | >= 5.0 |
            | Medium Moving | 2.0 - 4.99 |
            | Slow Moving | < 2.0 |
            """)
        
        # Inventory Turnover
        st.subheader("Inventory Turnover by Product")
        fig = px.bar(inventory_metrics.sort_values('Turnover_Ratio', ascending=False),
                    x='Product_Name', y='Turnover_Ratio',
                    color='Movement_Class',
                    color_discrete_map={'Fast Moving': '#28a745', 
                                       'Medium Moving': '#ffc107', 
                                       'Slow Moving': '#dc3545'})
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Days of Supply
        st.subheader("Days of Supply")
        dos_data = inventory_metrics[inventory_metrics['Days_of_Supply'] < 100]  # Filter out infinite
        fig = px.bar(dos_data.sort_values('Days_of_Supply'),
                    x='Product_Name', y='Days_of_Supply',
                    color='Days_of_Supply', color_continuous_scale='RdYlGn')
        fig.add_hline(y=14, line_dash="dash", line_color="red", 
                     annotation_text="2-Week Threshold")
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Heatmap
        st.subheader("Category-Product Inventory Heatmap")
        heatmap_data = inventory_metrics.pivot_table(
            values='Current_Inventory', 
            index='Category', 
            columns='Product_Name', 
            aggfunc='sum'
        ).fillna(0)
        
        fig = px.imshow(heatmap_data, 
                       color_continuous_scale='Blues',
                       labels=dict(color="Inventory Level"))
        st.plotly_chart(fig, use_container_width=True)
    
    # ========================================================================
    # PAGE: REORDER RECOMMENDATIONS
    # ========================================================================
    elif page == "Reorder Recommendations":
        st.title("Reorder Recommendations")
        
        st.markdown("""
        Based on statistical analysis using a **95% service level** (Z-score = 1.65), 
        the following products need immediate reorder attention.
        """)
        
        # Products needing reorder
        reorder_needed = inventory_metrics[inventory_metrics['Needs_Reorder']].copy()
        
        if len(reorder_needed) > 0:
            st.error(f"**{len(reorder_needed)} products need immediate reorder!**")
            
            display_reorder = reorder_needed[['Product_Name', 'Category', 'Current_Inventory',
                                              'Reorder_Point_Calc', 'Safety_Stock', 'Lead_Time', 
                                              'Days_of_Supply']].copy()
            display_reorder.columns = ['Product', 'Category', 'Current Stock', 
                                       'Reorder Point', 'Safety Stock', 'Lead Time (days)',
                                       'Days of Supply']
            
            st.dataframe(display_reorder.round(1), use_container_width=True)
            
            # Urgency Chart
            st.subheader("Stock Status Comparison")
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                name='Current Inventory',
                x=reorder_needed['Product_Name'],
                y=reorder_needed['Current_Inventory'],
                marker_color='#dc3545'
            ))
            
            fig.add_trace(go.Bar(
                name='Reorder Point',
                x=reorder_needed['Product_Name'],
                y=reorder_needed['Reorder_Point_Calc'],
                marker_color='#6c757d'
            ))
            
            fig.update_layout(barmode='group', xaxis_tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("All products are adequately stocked!")
        
        # Full Inventory Planning Table
        st.subheader("Complete Inventory Planning Table")
        display_planning = inventory_metrics[['Product_Name', 'Category', 'Current_Inventory',
                                              'Avg_Daily_Demand', 'Safety_Stock', 'Reorder_Point_Calc',
                                              'Lead_Time', 'Needs_Reorder']].copy()
        display_planning.columns = ['Product', 'Category', 'Current Stock', 'Avg Demand',
                                    'Safety Stock', 'Reorder Point', 'Lead Time', 'Needs Reorder']
        
        st.dataframe(
            display_planning.style.apply(
                lambda x: ['background-color: #ffcccc' if v else '' for v in x == True],
                subset=['Needs Reorder']
            ).format({'Avg Demand': '{:.2f}', 'Safety Stock': '{:.0f}', 'Reorder Point': '{:.0f}'}),
            use_container_width=True
        )
    
    # ========================================================================
    # PAGE: RAW DATA
    # ========================================================================
    elif page == "Raw Data":
        st.title("Raw Data Explorer")
        
        st.subheader("Transaction Data")
        st.dataframe(df_filtered, use_container_width=True)
        
        # Download button
        csv = df_filtered.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="inventory_data.csv",
            mime="text/csv"
        )
        
        # Data Summary
        st.subheader("Data Summary")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Numeric Columns**")
            st.dataframe(df_filtered.describe().round(2))
        
        with col2:
            st.markdown("**Data Info**")
            st.write(f"- Total Records: {len(df_filtered)}")
            st.write(f"- Date Range: {df_filtered['Order_Date'].min().date()} to {df_filtered['Order_Date'].max().date()}")
            st.write(f"- Categories: {df_filtered['Category'].nunique()}")
            st.write(f"- Products: {df_filtered['Product_ID'].nunique()}")

# ============================================================================
# RUN APP
# ============================================================================
if __name__ == "__main__":
    main()
