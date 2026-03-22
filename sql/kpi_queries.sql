-- Total Sales
SELECT SUM(Sales) AS Total_Sales
FROM read_parquet('../data/processed/cleaned_superstore.parquet');

-- Total Profit
SELECT SUM(Profit) AS Total_Profit
FROM read_parquet('../data/processed/cleaned_superstore.parquet');

-- Sales by Category
SELECT Category, SUM(Sales) AS Total_Sales
FROM read_parquet('../data/processed/cleaned_superstore.parquet')
GROUP BY Category
ORDER BY Total_Sales DESC;

-- Monthly Revenue
SELECT 
    strftime("Order Date", '%Y-%m') AS month,
    SUM(Sales) AS revenue
FROM read_parquet('../data/processed/cleaned_superstore.parquet')
GROUP BY month
ORDER BY month;

-- Top Customers
SELECT 
    "Customer ID",
    SUM(Sales) AS Total_Spent
FROM read_parquet('../data/processed/cleaned_superstore.parquet')
GROUP BY "Customer ID"
ORDER BY Total_Spent DESC
LIMIT 10;