import pandas as pd
import streamlit as st
import altair as alt

def plot_revenue_by_region(df: pd.DataFrame):
    if "Region" not in df.columns or "Total Revenue" not in df.columns:
        st.warning("Data must contain 'Region' and 'Total Revenue' columns.")
        return
    
    chart = alt.Chart(df).mark_bar().encode(
        x="Region:N",
        y="Total Revenue:Q",
        color="Region:N"
    ).properties(title=" Revenue by Region")
    
    st.altair_chart(chart, use_container_width=True)

def plot_revenue_by_category(df: pd.DataFrame):
    if "Category" not in df.columns or "Total Revenue" not in df.columns:
        st.warning("Data must contain 'Category' and 'Total Revenue' columns.")
        return
    
    chart = alt.Chart(df).mark_bar().encode(
        x="Category:N",
        y="Total Revenue:Q",
        color="Category:N"
    ).properties(title=" Revenue by Category")
    
    st.altair_chart(chart, use_container_width=True)

def plot_top_selling_products(df: pd.DataFrame):
    if "Product" not in df.columns or "Units Sold" not in df.columns:
        st.warning("Data must contain 'Product' and 'Units Sold' columns.")
        return
    
    chart = alt.Chart(df).mark_bar().encode(
        x="Product:N",
        y="Units Sold:Q",
        color="Product:N"
    ).properties(title="Top Selling Products")
    
    st.altair_chart(chart, use_container_width=True)
