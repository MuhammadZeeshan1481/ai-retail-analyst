# AI Retail Analyst

## Overview
AI Retail Analyst is a web-based application built with **Streamlit** and **NLP** models. It helps users analyze sales data and generate insights based on natural language queries. The app allows users to upload a CSV file containing sales data, and it can respond to a wide variety of questions related to sales, revenue, product performance, and more.

## Features
- Upload sales data in CSV format.
- Get answers to various business-related questions (e.g., highest-selling products, revenue by region, etc.).
- Dynamic data visualizations based on user queries.
- NLP-based query processing to understand user questions.

## Technologies Used
- **Streamlit**: Web framework for building the user interface.
- **Pandas**: For data manipulation.
- **Altair**: For data visualization.
- **Transformers**: Pretrained language models for NLP-based queries.
- **PyTorch**: Backend for Transformers.

## Installation
To run this project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ai-retail-analyst.git
   cd ai-retail-analyst


### Install dependencies:
pip install -r requirements.txt

### Run the app:
streamlit run app.py