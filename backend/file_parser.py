import pandas as pd
import os
from typing import List, Dict

def read_file(file_path: str) -> pd.DataFrame:
    """Reads a CSV or Excel file and returns a clean DataFrame."""
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".csv":
        df = pd.read_csv(file_path)
    elif ext in [".xlsx", ".xls"]:
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format: must be .csv or .xlsx")

    df = df.dropna(how="all")
    df = df.drop_duplicates()
    return df

def chunk_dataframe(df: pd.DataFrame) -> List[Dict]:
    """Convert each row into a string chunk for embedding."""
    chunks = []
    for i, row in df.iterrows():
        text = " | ".join([f"{col}: {row[col]}" for col in df.columns])
        chunks.append({
            "chunk_id": f"row_{i}",
            "text": text,
            "metadata": row.to_dict()
        })
    return chunks
