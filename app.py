import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np

# Set page config
st.set_page_config(page_title="SaaS Sales Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('SaaS-Sales_B8E9E49F6C.csv')
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    return df

df = load_data()

# Sidebar filters
st.sidebar.title("Filters")
date_range = st.sidebar.date_input("Date Range", 
    [df['Order Date'].min(), df['Order Date'].max()])
selected_region = st.sidebar.multiselect("Region", df['Region'].unique(), default=df['Region'].unique())
selected_industry = st.sidebar.multiselect("Industry", df['Industry'].unique(), default=df['Industry'].unique())

# Apply filters
filtered_df = df[
    (df['Order Date'] >= pd.to_datetime(date_range[0])) & 
    (df['Order Date'] <= pd.to_datetime(date_range[1])) &
    (df['Region'].isin(selected_region)) &
    (df['Industry'].isin(selected_industry))
]

# KPI Cards
st.title("SaaS Sales Dashboard")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Revenue", f"${filtered_df['Sales'].sum():,.0f}")
with col2:
    st.metric("Total Profit", f"${filtered_df['Profit'].sum():,.0f}")
with col3:
    margin = (filtered_df['Profit'].sum() / filtered_df['Sales'].sum()) * 100
    st.metric("Profit Margin", f"{margin:.1f}%")
with col4:
    st.metric("Active Customers", f"{filtered_df['Customer ID'].nunique():,}")

# Charts - First Row
col1, col2 = st.columns(2)

with col1:
    # Monthly Revenue Trend by Product (Matching the first image)
    st.subheader("Monthly Revenue Trend by Product")
    
    # Define the specific products from the image
    products_to_plot = ['ChatBot Plugin', 'ContactMatcher', 'Data Smasher', 'FinanceHub', 'Marketing Suite']
    
    # Filter data for these specific products
    monthly_data = filtered_df[filtered_df['Product'].isin(products_to_plot)].copy()
    monthly_data = monthly_data.groupby([pd.Grouper(key='Order Date', freq='M'), 'Product'])['Sales'].sum().reset_index()
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Color palette matching the image style
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    for i, product in enumerate(products_to_plot):
        product_data = monthly_data[monthly_data['Product'] == product]
        if not product_data.empty:
            ax.plot(product_data['Order Date'], product_data['Sales'], 
                   label=product, marker='o', linewidth=2.5, color=colors[i])
    
    ax.set_title('Monthly Revenue Trend by Product', fontsize=16, fontweight='bold')
    ax.set_ylabel('Revenue ($)')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, alpha=0.3)
    ax.set_ylim(bottom=0)
    
    # Format y-axis with commas
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    # Revenue by Country & Segment (Matching the second image)
    st.subheader("Revenue by Country & Segment")
    
    # Get top countries by revenue
    top_countries = filtered_df.groupby('Country')['Sales'].sum().nlargest(15).index
    
    country_segment = filtered_df[filtered_df['Country'].isin(top_countries)].groupby(
        ['Country', 'Segment'])['Sales'].sum().reset_index()
    
    # Create horizontal bar plot
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Pivot data for plotting
    pivot_data = country_segment.pivot(index='Country', columns='Segment', values='Sales').fillna(0)
    
    # Plot stacked bar chart
    pivot_data.plot(kind='barh', stacked=True, ax=ax, 
                   color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    
    ax.set_title('Revenue by Country & Segment', fontsize=16, fontweight='bold')
    ax.set_xlabel('Revenue ($)')
    ax.set_ylabel('Country')
    ax.legend(title='Segment')
    ax.grid(True, alpha=0.3, axis='x')
    
    # Format x-axis with commas
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
    
    plt.tight_layout()
    st.pyplot(fig)

# Charts - Second Row
col3, col4 = st.columns(2)

with col3:
    # Top 5 Products by Revenue (Matching the third image)
    st.subheader("Top 5 Products by Revenue")
    
    top_products = filtered_df.groupby('Product')['Sales'].sum().nlargest(5)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create horizontal bar chart
    bars = ax.barh(range(len(top_products)), top_products.values, 
                  color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
    
    ax.set_yticks(range(len(top_products)))
    ax.set_yticklabels(top_products.index)
    ax.set_title('Top 5 Products by Revenue', fontsize=16, fontweight='bold')
    ax.set_xlabel('Revenue ($)')
    
    # Add value labels on bars
    for i, v in enumerate(top_products.values):
        ax.text(v + 0.01 * max(top_products.values), i, f'${v:,.0f}', 
               va='center', fontweight='bold')
    
    ax.grid(True, alpha=0.3, axis='x')
    ax.set_xlim(0, max(top_products.values) * 1.1)
    
    # Format x-axis with commas
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
    
    plt.tight_layout()
    st.pyplot(fig)

with col4:
    # Quarterly Active Customers (Matching the fourth image)
    st.subheader("Quarterly Active Customers")
    
    # Calculate quarterly active customers
    quarterly_customers = filtered_df.groupby(
        pd.Grouper(key='Order Date', freq='Q'))['Customer ID'].nunique()
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Plot line chart
    ax.plot(quarterly_customers.index, quarterly_customers.values, 
           marker='o', linewidth=2.5, color='#1f77b4', markersize=8)
    
    ax.set_title('Quarterly Active Customers', fontsize=16, fontweight='bold')
    ax.set_ylabel('Number of Active Customers')
    ax.set_xlabel('Quarter')
    ax.grid(True, alpha=0.3)
    
    # Format y-axis
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

# Additional insights section
st.markdown("---")
st.subheader("Key Insights")

col_insight1, col_insight2, col_insight3 = st.columns(3)

with col_insight1:
    st.metric("Average Deal Size", 
             f"${filtered_df['Sales'].mean():,.0f}",
             help="Average revenue per transaction")

with col_insight2:
    repeat_customers = filtered_df.groupby('Customer ID').size()
    repeat_rate = (repeat_customers > 1).sum() / len(repeat_customers) * 100
    st.metric("Customer Repeat Rate", 
             f"{repeat_rate:.1f}%",
             help="Percentage of customers with multiple purchases")

with col_insight3:
    latest_month = filtered_df['Order Date'].max()
    monthly_growth = filtered_df[filtered_df['Order Date'].dt.to_period('M') == latest_month.to_period('M')]['Sales'].sum()
    prev_month = filtered_df[filtered_df['Order Date'].dt.to_period('M') == (latest_month - pd.DateOffset(months=1)).to_period('M')]['Sales'].sum()
    growth_pct = ((monthly_growth - prev_month) / prev_month * 100) if prev_month > 0 else 0
    st.metric("Monthly Growth", 
             f"{growth_pct:.1f}%",
             help="Revenue growth compared to previous month")

# Data summary
with st.expander("Data Summary"):
    st.write(f"**Time Period:** {filtered_df['Order Date'].min().strftime('%Y-%m-%d')} to {filtered_df['Order Date'].max().strftime('%Y-%m-%d')}")
    st.write(f"**Total Transactions:** {len(filtered_df):,}")
    st.write(f"**Products Analyzed:** {filtered_df['Product'].nunique()}")
    st.write(f"**Countries:** {filtered_df['Country'].nunique()}")
