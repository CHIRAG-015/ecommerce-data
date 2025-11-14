from __future__ import annotations

import csv
import random
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

from faker import Faker


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

NUM_USERS = 200
NUM_PRODUCTS = 200
NUM_ORDERS = 200
NUM_ORDER_ITEMS = 200
NUM_PAYMENTS = 200

CATEGORIES = [
    "Electronics",
    "Home & Kitchen",
    "Fashion",
    "Beauty",
    "Sports",
    "Books",
    "Toys",
]

PAYMENT_METHODS = ["credit_card", "debit_card", "paypal", "bank_transfer"]
PAYMENT_STATUS = ["completed", "pending", "failed"]


def money(value: Decimal) -> float:
    """Round Decimal to two places and convert to float for CSV output."""
    return float(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def write_csv(path: Path, headers: list[str], rows: list[dict]):
    with path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def generate_data():
    faker = Faker()
    random.seed(42)
    faker.seed_instance(42)

    DATA_DIR.mkdir(exist_ok=True)

    users = []
    for user_id in range(1, NUM_USERS + 1):
        users.append(
            {
                "user_id": user_id,
                "name": faker.name(),
                "email": faker.unique.email(),
                "signup_date": faker.date_between(start_date="-2y", end_date="-1d"),
            }
        )

    products = []
    for product_id in range(1, NUM_PRODUCTS + 1):
        products.append(
            {
                "product_id": product_id,
                "name": faker.catch_phrase(),
                "category": random.choice(CATEGORIES),
                "price": money(
                    Decimal(str(random.uniform(5, 500))).quantize(Decimal("0.01"))
                ),
            }
        )

    orders = []
    for order_id in range(1, NUM_ORDERS + 1):
        user = random.choice(users)
        orders.append(
            {
                "order_id": order_id,
                "user_id": user["user_id"],
                "order_date": faker.date_between(start_date="-1y", end_date="today"),
                "total_amount": 0.0,  # placeholder, updated after order items
            }
        )

    order_items = []
    order_totals = defaultdict(Decimal)

    # Ensure every order has at least one item while keeping ~200 rows
    for item_id, order in zip(range(1, NUM_ORDER_ITEMS + 1), orders):
        product = random.choice(products)
        quantity = random.randint(1, 5)
        line_total = Decimal(str(product["price"])) * quantity
        order_totals[order["order_id"]] += line_total

        order_items.append(
            {
                "item_id": item_id,
                "order_id": order["order_id"],
                "product_id": product["product_id"],
                "quantity": quantity,
            }
        )

    # Update order totals based on computed item totals
    for order in orders:
        total = order_totals[order["order_id"]]
        order["total_amount"] = money(total)

    payments = []
    for payment_id, order in zip(range(1, NUM_PAYMENTS + 1), orders):
        status = random.choices(PAYMENT_STATUS, weights=[0.8, 0.15, 0.05])[0]
        amount = order["total_amount"] if status != "failed" else 0.0
        payments.append(
            {
                "payment_id": payment_id,
                "order_id": order["order_id"],
                "method": random.choice(PAYMENT_METHODS),
                "status": status,
                "amount": amount,
            }
        )

    write_csv(
        DATA_DIR / "users.csv",
        ["user_id", "name", "email", "signup_date"],
        users,
    )
    write_csv(
        DATA_DIR / "products.csv",
        ["product_id", "name", "category", "price"],
        products,
    )
    write_csv(
        DATA_DIR / "orders.csv",
        ["order_id", "user_id", "order_date", "total_amount"],
        orders,
    )
    write_csv(
        DATA_DIR / "order_items.csv",
        ["item_id", "order_id", "product_id", "quantity"],
        order_items,
    )
    write_csv(
        DATA_DIR / "payments.csv",
        ["payment_id", "order_id", "method", "status", "amount"],
        payments,
    )


if __name__ == "__main__":
    generate_data()

