"""
Day 15 - SQL for Analysts
Generates a reproducible relational dataset and loads it into a
SQLite database (data/sales.db) with four related tables:

    customers(customer_id, name, region, segment)
    products(product_id, product_name, category, unit_price)
    orders(order_id, customer_id, order_date)
    order_items(order_item_id, order_id, product_id, quantity, discount)

This mirrors a realistic normalized schema (rather than one flat
CSV), so main.py has genuine joins, aggregations, and a
left-join-for-missing-data case to work with.
"""

import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

RANDOM_SEED = 30
N_CUSTOMERS = 40
N_ORDERS = 350
N_ORDER_ITEMS_MAX_PER_ORDER = 4

REGIONS = ["North", "South", "East", "West"]
SEGMENTS = ["Consumer", "Corporate", "Small Business"]

PRODUCTS = [
    ("Wireless Mouse", "Electronics", 18.0),
    ("Bluetooth Speaker", "Electronics", 45.0),
    ("USB-C Hub", "Electronics", 32.0),
    ("Webcam", "Electronics", 55.0),
    ("Notebook Pack", "Office Supplies", 6.5),
    ("Printer Paper", "Office Supplies", 8.0),
    ("Stapler", "Office Supplies", 5.0),
    ("Office Chair", "Furniture", 120.0),
    ("Standing Desk", "Furniture", 260.0),
    ("Bookshelf", "Furniture", 95.0),
    ("T-Shirt", "Apparel", 15.0),
    ("Hoodie", "Apparel", 35.0),
]

FIRST_NAMES = ["Ali", "Sara", "Reza", "Mina", "Amir", "Nazanin", "Kian", "Leila", "Omid", "Parisa"]
LAST_NAMES = ["Ahmadi", "Karimi", "Hosseini", "Moradi", "Rostami", "Jafari"]


def _build_customers(rng: np.random.Generator) -> pd.DataFrame:
    first = rng.choice(FIRST_NAMES, size=N_CUSTOMERS)
    last = rng.choice(LAST_NAMES, size=N_CUSTOMERS)
    names = [f"{f} {l}" for f, l in zip(first, last)]

    return pd.DataFrame({
        "customer_id": range(1, N_CUSTOMERS + 1),
        "name": names,
        "region": rng.choice(REGIONS, size=N_CUSTOMERS),
        "segment": rng.choice(SEGMENTS, size=N_CUSTOMERS, p=[0.5, 0.3, 0.2]),
    })


def _build_products() -> pd.DataFrame:
    return pd.DataFrame({
        "product_id": range(1, len(PRODUCTS) + 1),
        "product_name": [p[0] for p in PRODUCTS],
        "category": [p[1] for p in PRODUCTS],
        "unit_price": [p[2] for p in PRODUCTS],
    })


def _build_orders_and_items(
    rng: np.random.Generator, customers: pd.DataFrame, products: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    # Leave a handful of customers with zero orders on purpose, so
    # "customers without orders" (a LEFT JOIN case) has real rows to find.
    ordering_customer_ids = customers["customer_id"].sample(
        n=N_CUSTOMERS - 5, random_state=int(rng.integers(0, 1_000_000))
    )

    order_dates = pd.to_datetime("2024-01-01") + pd.to_timedelta(
        rng.integers(0, 365, size=N_ORDERS), unit="D"
    )
    order_customer_ids = rng.choice(ordering_customer_ids, size=N_ORDERS)

    orders = pd.DataFrame({
        "order_id": range(1, N_ORDERS + 1),
        "customer_id": order_customer_ids,
        "order_date": order_dates.strftime("%Y-%m-%d"),
    })

    items_rows = []
    item_id = 1
    for order_id in orders["order_id"]:
        n_items = rng.integers(1, N_ORDER_ITEMS_MAX_PER_ORDER + 1)
        chosen_products = rng.choice(products["product_id"], size=n_items, replace=False)
        for product_id in chosen_products:
            items_rows.append({
                "order_item_id": item_id,
                "order_id": order_id,
                "product_id": product_id,
                "quantity": int(rng.integers(1, 6)),
                "discount": float(rng.choice([0.0, 0.05, 0.1, 0.15])),
            })
            item_id += 1

    return orders, pd.DataFrame(items_rows)


def build_database(db_path: str | Path = "data/sales.db", seed: int = RANDOM_SEED) -> None:
    """Generate all four tables and write them into a fresh SQLite database."""
    rng = np.random.default_rng(seed)

    customers = _build_customers(rng)
    products = _build_products()
    orders, order_items = _build_orders_and_items(rng, customers, products)

    db_path = Path(db_path)
    if db_path.exists():
        db_path.unlink()

    with sqlite3.connect(db_path) as conn:
        customers.to_sql("customers", conn, index=False)
        products.to_sql("products", conn, index=False)
        orders.to_sql("orders", conn, index=False)
        order_items.to_sql("order_items", conn, index=False)


if __name__ == "__main__":
    build_database()
    print("Wrote data/sales.db with tables: customers, products, orders, order_items")
