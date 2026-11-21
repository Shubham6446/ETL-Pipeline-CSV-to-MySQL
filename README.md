# ETL Pipeline: CSV to MySQL

## What this project does
1. Extracts rows from `data/sales_raw.csv`.
2. Transforms data: trims text, converts amount to numeric, handles missing amounts, removes duplicate rows.
3. Loads cleaned rows into a MySQL table using SQLAlchemy.
4. Writes run messages to `logs/etl.log`.

## Setup
1. Install Python 3.10+ and MySQL.
2. Create a database:
   ```sql
   CREATE DATABASE sales_db;
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set your MySQL connection in environment variables (recommended):
   - `DB_HOST` (default: localhost)
   - `DB_PORT` (default: 3306)
   - `DB_USER` (default: root)
   - `DB_PASSWORD` (your MySQL password)
   - `DB_NAME` (default: sales_db)
5. Run:
   ```bash
   python etl_pipeline.py
   ```

The script creates/replaces the `sales` table. For a real production pipeline, change `if_exists='replace'` to an incremental/upsert strategy and validate business rules before loading.

## Verify
```sql
USE sales_db;
SELECT * FROM sales;
SELECT city, SUM(amount) AS total_sales FROM sales GROUP BY city;
```
