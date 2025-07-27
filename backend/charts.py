import pandas as pd
import plotly.express as px

def load_uploaded_file(path: str) -> pd.DataFrame:
    ext = path.split('.')[-1].lower()
    if ext == "csv":
        return pd.read_csv(path)
    elif ext in ["xlsx", "xls"]:
        return pd.read_excel(path)
    else:
        raise ValueError("Unsupported file format")

def plot_revenue_by_region(df: pd.DataFrame):
    fig = px.bar(df, x="Region", y="Total Revenue", color="Region", title="Revenue by Region", text="Total Revenue")
    return fig

def plot_units_by_product(df: pd.DataFrame):
    fig = px.pie(df, names="Product", values="Units Sold", title="Units Sold per Product")
    return fig
