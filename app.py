import streamlit as st
import pandas as pd
from backend.file_parser import read_file, chunk_dataframe
from backend.embedding_engine import EmbeddingEngine
from backend.vector_store import VectorStore
from backend.insight_engine import InsightEngine
from components.ui_utils import handle_upload, show_dataframe, get_filters
from components.visuals import plot_revenue_by_region, plot_revenue_by_category, plot_top_selling_products

st.set_page_config(page_title="AI Retail Analyst", layout="wide")
st.title("🧠 AI Retail Analyst")
st.markdown("Upload your sales data and ask natural language questions!")

# Handle file upload with validation
file_path = handle_upload()

if file_path:
    df = read_file(file_path)
    show_dataframe(df)

    # Filters
    filters = get_filters(df)
    
    # Apply filters if needed
    filtered_df = df
    if filters:
        filtered_df = df.loc[df[filters['column']] == filters['value']]

    # Ask a question
    st.markdown("## 🔍 Ask a question")
    user_query = st.text_input("e.g., What is the total revenue for the East region?")
    if user_query:
        engine = InsightEngine()
        response = engine.generate_answer(user_query, filtered_df)

        st.markdown("### 🤖 Answer")
        st.success(response["answer"])

        st.markdown("### 📈 Visuals")
        if 'region' in user_query.lower():
            plot_revenue_by_region(filtered_df)
        elif 'category' in user_query.lower():
            plot_revenue_by_category(filtered_df)
        elif 'top selling products' in user_query.lower():
            plot_top_selling_products(filtered_df)
else:
    st.info("👈 Upload a valid CSV file to get started.")
