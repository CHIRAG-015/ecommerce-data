# Synthetic E-commerce Data Pipeline

## Overview
- `scripts/generate_data.py` fabricates 200 rows for each CSV in `data/` using Faker.
- `scripts/ingest_data.py` rebuilds `db/ecom.db`, creates the required tables, and bulk-loads the CSVs with pandas + sqlite3.
- `query.sql` joins `users → orders → order_items → products → payments`, selecting key order details.

## How to Reproduce
1. `python scripts/generate_data.py`
2. `python scripts/ingest_data.py`
3. `python -m pip install pandas faker` (if not already installed)
4. `python -c "import sqlite3, pandas as pd, pathlib; root=pathlib.Path('.'); query=(root/'query.sql').read_text(); conn=sqlite3.connect(root/'db/ecom.db'); df=pd.read_sql_query(query, conn); conn.close(); (root/'result').mkdir(exist_ok=True); (root/'result'/'joined_output.csv').write_text(df.to_csv(index=False))"`

Step 4 is already automated for you and produced `result/joined_output.csv`.

## Query Output (first 5 rows)
| user_name        | order_id | product_name                             | quantity | total_amount | payment_method | payment_status |
|------------------|----------|------------------------------------------|----------|--------------|----------------|----------------|
| Matthew Mitchell | 1        | Cross-group systemic functionalities     | 4        | 1382.56      | paypal         | pending        |
| Amanda Logan     | 2        | Reactive executive archive               | 3        | 708.54       | credit_card    | completed      |
| Isaiah Avila     | 3        | Re-engineered discrete monitoring        | 2        | 45.66        | credit_card    | completed      |
| Brian Gregory    | 4        | Innovative directional framework         | 3        | 1497.69      | paypal         | failed         |
| David Fowler     | 5        | Proactive contextually-based synergy     | 5        | 2431.20      | debit_card     | completed      |

| user_name        | order_id | product_name                             | quantity | total_amount | payment_method | payment_status |
The complete joined dataset (20 rows ordered by `order_id`) lives in `result/joined_output.csv`.
