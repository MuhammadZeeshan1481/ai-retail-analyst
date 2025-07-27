from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
from typing import Dict
import pandas as pd
from datetime import datetime, timedelta

class InsightEngine:
    def __init__(self):
        model_id = "google/flan-t5-base"
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

        self.llm = pipeline(
            task="text2text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device=-1,  # CPU
            max_new_tokens=256
        )

    def generate_answer(self, query: str, df: pd.DataFrame) -> Dict:
        """
        Process and respond to the user's query dynamically
        """
        query = query.lower()
        answer = None
        
        # Parse the date-related queries
        date_query = self.process_date_query(query, df)
        if date_query:
            return date_query
        
        if 'revenue' in query:
            answer = self.handle_revenue_queries(query, df)
        
        elif 'sales' in query or 'units' in query:
            answer = self.handle_sales_queries(query, df)
        
        elif 'product' in query or 'category' in query:
            answer = self.handle_product_category_queries(query, df)

        if not answer:
            answer = self.general_query_processing(query, df)
        
        return answer

    def process_date_query(self, query: str, df: pd.DataFrame):
        """
        Handle date-based queries like last month, Q1, etc.
        """
        if 'Date' not in df.columns:
            return {"answer": "Date column is missing in the dataset."}
        
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        
        if 'last month' in query:
            return self.sales_last_month(df)
        if 'this year' in query:
            return self.sales_this_year(df)
        if 'q1' in query:
            return self.sales_q1(df)
        return None

    def handle_revenue_queries(self, query: str, df: pd.DataFrame):
        """
        Dynamically handle revenue-related queries.
        """
        if 'total' in query:
            return self.calculate_total_revenue(df)
        if 'by region' in query:
            return self.revenue_by_region(df)
        if 'by category' in query:
            return self.revenue_by_category(df)

    def handle_sales_queries(self, query: str, df: pd.DataFrame):
        """
        Dynamically handle sales-related queries.
        """
        if 'by region' in query:
            return self.sales_by_region(df)
        if 'top' in query or 'highest' in query:
            return self.top_selling_products(df)

    def handle_product_category_queries(self, query: str, df: pd.DataFrame):
        """
        Dynamically handle product or category-related questions
        """
        if 'category' in query:
            return self.sales_by_category(df)
        if 'product' in query:
            return self.sales_by_product(df)

    def sales_last_month(self, df: pd.DataFrame):
        last_month = (datetime.today() - timedelta(days=30)).month
        last_month_sales = df[df['Date'].dt.month == last_month]
        if last_month_sales.empty:
            return {"answer": "No sales data available for the last month."}
        top_product = last_month_sales.groupby("Product")["Units Sold"].sum().idxmax()
        return {"answer": f"The highest-selling product last month was {top_product}"}

    def sales_this_year(self, df: pd.DataFrame):
        this_year = datetime.today().year
        this_year_sales = df[df['Date'].dt.year == this_year]
        top_product = this_year_sales.groupby("Product")["Units Sold"].sum().idxmax()
        return {"answer": f"The highest-selling product this year is {top_product}"}

    def sales_q1(self, df: pd.DataFrame):
        q1_sales = df[(df['Date'].dt.month >= 1) & (df['Date'].dt.month <= 3)]
        top_product = q1_sales.groupby("Product")["Units Sold"].sum().idxmax()
        return {"answer": f"The highest-selling product in Q1 was {top_product}"}

    def calculate_total_revenue(self, df: pd.DataFrame):
        total_revenue = df["Total Revenue"].sum()
        return {"answer": f"The total revenue is {total_revenue}"}

    def revenue_by_region(self, df: pd.DataFrame):
        region_revenue = df.groupby("Region")["Total Revenue"].sum().to_dict()
        return {"answer": f"Revenue by region:\n{self.format_answer(region_revenue)}"}

    def revenue_by_category(self, df: pd.DataFrame):
        category_revenue = df.groupby("Category")["Total Revenue"].sum().to_dict()
        return {"answer": f"Revenue by category:\n{self.format_answer(category_revenue)}"}

    def sales_by_region(self, df: pd.DataFrame):
        region_sales = df.groupby("Region")["Units Sold"].sum().to_dict()
        return {"answer": f"Sales by region:\n{self.format_answer(region_sales)}"}

    def top_selling_products(self, df: pd.DataFrame):
        top_products = df.groupby("Product")["Units Sold"].sum().nlargest(5).to_dict()
        return {"answer": f"Top-selling products:\n{self.format_answer(top_products)}"}

    def sales_by_product(self, df: pd.DataFrame):
        product_sales = df.groupby("Product")["Units Sold"].sum().to_dict()
        return {"answer": f"Sales by product:\n{self.format_answer(product_sales)}"}

    def sales_by_category(self, df: pd.DataFrame):
        category_sales = df.groupby("Category")["Units Sold"].sum().to_dict()
        return {"answer": f"Sales by category:\n{self.format_answer(category_sales)}"}

    def general_query_processing(self, query: str, df: pd.DataFrame):
        """
        General logic to process any query dynamically using NLP model.
        """
        prompt = f"Analyze the following data and answer this query: {query}\n\nData: {df.head(5)}"
        result = self.llm(prompt)
        return {"answer": result[0]['generated_text']}

    def format_answer(self, answer_data: Dict) -> str:
        """
        Format the answer data into a cleaner and more readable structure.
        """
        if isinstance(answer_data, dict):
            formatted_answer = "\n".join([f"{key}: {value}" for key, value in answer_data.items()])
        else:
            formatted_answer = str(answer_data)
        
        return formatted_answer
