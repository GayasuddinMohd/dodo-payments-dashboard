import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Load data
df = pd.read_csv('SaaS-Sales_B8E9E49F6C.csv')
df['Order Date'] = pd.to_datetime(df['Order Date'])

st.set_page_config(page_title="SaaS Sales Dashboard", layout="wide")

# Sidebar filters
st.sidebar.title("Filters")
date_range = st.sidebar.date_input("Date Range", 
    [df['Order Date'].min(), df['Order Date'].max()])
selected_region = st.sidebar.multiselect("Region", df['Region'].unique())
selected_industry = st.sidebar.multiselect("Industry", df['Industry'].unique())

# KPI Cards
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Revenue", f"${df['Sales'].sum():,.0f}")
with col2:
    st.metric("Total Profit", f"${df['Profit'].sum():,.0f}")
with col3:
    margin = (df['Profit'].sum() / df['Sales'].sum()) * 100
    st.metric("Profit Margin", f"{margin:.1f}%")

# Charts
col1, col2 = st.columns(2)

with col1:
    # Monthly Revenue Trend
    monthly_data = df.groupby([pd.Grouper(key='Order Date', freq='M'), 'Product'])['Sales'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    for product in monthly_data['Product'].unique()[:5]:  # Top 5 products
        product_data = monthly_data[monthly_data['Product'] == product]
        ax.plot(product_data['Order Date'], product_data['Sales'], label=product, marker='o')
    ax.set_title('Monthly Revenue Trend by Product')
    ax.legend()
    st.pyplot(fig)

with col2:
    # Revenue by Country & Segment
    country_segment = df.groupby(['Country', 'Segment'])['Sales'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=country_segment, x='Sales', y='Country', hue='Segment', ax=ax)
    ax.set_title('Revenue by Country & Segment')
    st.pyplot(fig)

col3, col4 = st.columns(2)

with col3:
    # Top 5 Products
    top_products = df.groupby('Product')['Sales'].sum().nlargest(5)
    fig, ax = plt.subplots(figsize=(10, 6))
    top_products.plot(kind='barh', ax=ax)
    ax.set_title('Top 5 Products by Revenue')
    st.pyplot(fig)

with col4:
    # Customer Retention (Quarterly active customers)
    quarterly_customers = df.groupby(pd.Grouper(key='Order Date', freq='Q'))['Customer ID'].nunique()
    fig, ax = plt.subplots(figsize=(10, 6))
    quarterly_customers.plot(ax=ax, marker='o')
    ax.set_title('Quarterly Active Customers')
    st.pyplot(fig)
