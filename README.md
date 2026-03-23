# RetailPulse: Sales & Profit Intelligence Dashboard

RetailPulse is an interactive e-commerce analytics dashboard built to analyze revenue, profit, customer behavior, product performance, and regional business trends.

It simulates a real-world data analyst workflow: loading raw retail data, cleaning and transforming it, validating metrics using Python and SQL, and building an interactive dashboard for business users.

---

## Project Objective

The goal of this project is to create a recruiter-ready data analytics portfolio project that demonstrates:

- data cleaning and preprocessing
- exploratory data analysis
- KPI design and business analysis
- SQL and Python validation
- dashboard building with Streamlit
- business storytelling through insights

---

## Dashboard Preview

Add your screenshots here after running the app.

### Overview
![Overview](outputs/screenshots/overview.png)

### Trends
![Trends](outputs/screenshots/trends.png)

### Customers
![Customers](outputs/screenshots/customers.png)

### Products
![Products](outputs/screenshots/products.png)

---

## Tools & Technologies Used

- Python
- Pandas
- Streamlit
- Plotly
- DuckDB
- Jupyter Notebook

---

## Key Features

- Revenue, Profit, Orders, Average Order Value, and Profit Margin KPIs
- Sales by Category
- Regional Revenue Contribution
- Monthly Sales Trend
- Monthly Profit Trend
- Top 10 Products by Sales
- Top 10 Products by Profit
- Customer Analysis with repeat customer tracking
- Sales by Customer Segment
- Profit Margin by Category
- Business insight cards
- Downloadable filtered dataset

---

## Dashboard Sections

### 1. Overview
Displays:
- category-wise sales
- regional revenue mix
- profit margin by category

### 2. Trends
Displays:
- monthly sales trend
- monthly profit trend

### 3. Products
Displays:
- top 10 products by sales
- top 10 products by profit

### 4. Customers
Displays:
- total customers
- repeat customers
- customer segment sales
- top customers by sales

### 5. Data & Insights
Displays:
- dataset preview
- key business insights
- downloadable filtered data

---

## Business Questions Answered

This project helps answer questions like:

- Which category generates the highest revenue?
- Which region contributes the most sales?
- Which products drive the most revenue and profit?
- Are high-sales categories also high-profit categories?
- Which customer segments contribute the most?
- How do sales and profit change over time?
- Which category has the best profit margin?
- Which category may need pricing or discount review?

---

## Project Structure

```bash
RetailPulse/
│
├── app/
│   └── streamlit_app.py
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   └── 01_data_cleaning.ipynb
├── sql/
│   └── kpi_queries.sql
├── outputs/
│   └── screenshots/
├── README.md
└── requirements.txt5