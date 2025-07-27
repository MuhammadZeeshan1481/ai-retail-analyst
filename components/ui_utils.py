import os
import pandas as pd
import streamlit as st

UPLOAD_FOLDER = "data/uploads"

def handle_upload():
    st.sidebar.header(" Upload CSV")
    uploaded_file = st.sidebar.file_uploader("Upload your sales CSV", type=["csv"])
    
    if uploaded_file is not None:
        # Validate if the file is a CSV
        if not uploaded_file.name.endswith('.csv'):
            st.error("Please upload a CSV file.")
            return None

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    return None

def show_dataframe(df: pd.DataFrame):
    st.subheader(" Uploaded Sales Data")
    st.dataframe(df, use_container_width=True)

def get_filters(df: pd.DataFrame):
    filters = {}
    st.sidebar.header("Filter Data")

    # Add filter options here
    region_filter = st.sidebar.selectbox("Select Region", options=["All"] + list(df["Region"].unique()))
    if region_filter != "All":
        filters['column'] = "Region"
        filters['value'] = region_filter

    return filters
