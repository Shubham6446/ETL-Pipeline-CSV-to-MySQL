USE sales_db;

SELECT * FROM sales;

SELECT city, SUM(amount) AS total_sales
FROM sales
GROUP BY city
ORDER BY total_sales DESC;

SELECT COUNT(*) AS total_rows FROM sales;
