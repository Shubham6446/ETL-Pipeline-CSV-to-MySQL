import logging
import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "sales_raw.csv"
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "etl.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

def extract(path: Path) -> pd.DataFrame:
    logging.info("Extracting CSV: %s", path)
    return pd.read_csv(path)

def transform(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Transform started; input rows=%s", len(df))
    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]

    required = {"order_id", "customer", "amount", "city"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df["customer"] = df["customer"].astype("string").str.strip()
    df["city"] = df["city"].astype("string").str.strip()
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
    df["order_id"] = pd.to_numeric(df["order_id"], errors="coerce")
    df = df.dropna(subset=["order_id"])
    df["order_id"] = df["order_id"].astype("int64")
    df = df.drop_duplicates()
    df = df.drop_duplicates(subset=["order_id"], keep="last")
    logging.info("Transform complete; output rows=%s", len(df))
    return df

def load(df: pd.DataFrame) -> None:
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "3306")
    database = os.getenv("DB_NAME", "sales_db")

    url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(url)
    logging.info("Loading %s rows into %s.sales", len(df), database)
    df.to_sql("sales", con=engine, if_exists="replace", index=False)
    logging.info("Load complete")

def main():
    try:
        raw = extract(DATA_FILE)
        cleaned = transform(raw)
        print("Preview of cleaned data:")
        print(cleaned.to_string(index=False))
        load(cleaned)
        print("\nETL completed successfully. Check MySQL table: sales")
    except Exception:
        logging.exception("ETL failed")
        raise

if __name__ == "__main__":
    main()
