from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DB_DIR = PROJECT_ROOT / "db"
DB_PATH = DB_DIR / "ecom.db"

TABLE_SCHEMAS = {
    "users": """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            signup_date DATE NOT NULL
        )
    """,
    "products": """
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL
        )
    """,
    "orders": """
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            order_date DATE NOT NULL,
            total_amount REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """,
    "order_items": """
        CREATE TABLE IF NOT EXISTS order_items (
            item_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    """,
    "payments": """
        CREATE TABLE IF NOT EXISTS payments (
            payment_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            method TEXT NOT NULL,
            status TEXT NOT NULL,
            amount REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id)
        )
    """,
}

CSV_CONFIG = {
    "users": {
        "filename": "users.csv",
        "parse_dates": ["signup_date"],
        "date_cols": ["signup_date"],
    },
    "products": {"filename": "products.csv"},
    "orders": {
        "filename": "orders.csv",
        "parse_dates": ["order_date"],
        "date_cols": ["order_date"],
    },
    "order_items": {"filename": "order_items.csv"},
    "payments": {"filename": "payments.csv"},
}


def load_dataframe(table: str) -> pd.DataFrame:
    config = CSV_CONFIG[table]
    csv_path = DATA_DIR / config["filename"]
    df = pd.read_csv(
        csv_path,
        parse_dates=config.get("parse_dates"),
    )

    # Ensure date columns are ISO strings for SQLite DATE storage
    for col in config.get("date_cols", []):
        df[col] = pd.to_datetime(df[col]).dt.date.astype(str)

    # Enforce integer columns (pandas may infer as floats)
    for int_col in [c for c in df.columns if c.endswith("_id") or c == "quantity"]:
        df[int_col] = df[int_col].astype(int)

    return df


def create_tables(cursor: sqlite3.Cursor):
    for ddl in TABLE_SCHEMAS.values():
        cursor.execute(ddl)


def ingest():
    DB_DIR.mkdir(exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        create_tables(cursor)
        conn.commit()

        for table in TABLE_SCHEMAS.keys():
            df = load_dataframe(table)
            df.to_sql(table, conn, if_exists="append", index=False)

        conn.commit()


if __name__ == "__main__":
    ingest()

