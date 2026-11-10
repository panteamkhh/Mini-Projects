"""Unit tests for SQLAnalyzer (Day 15 - SQL for Analysts)."""

import sqlite3

import pandas as pd
import pytest

from main import SQLAnalyzer


@pytest.fixture
def analyzer(tmp_path):
    """A SQLAnalyzer over a small, hand-built database with a known shape."""
    db_path = tmp_path / "sales.db"
    conn = sqlite3.connect(db_path)

    customers = pd.DataFrame({
        "customer_id": [1, 2, 3],
        "name": ["Alice", "Bob", "Cara"],
        "region": ["North", "South", "North"],
        "segment": ["Consumer", "Corporate", "Consumer"],
    })
    products = pd.DataFrame({
        "product_id": [1, 2],
        "product_name": ["Widget", "Gadget"],
        "category": ["Tools", "Electronics"],
        "unit_price": [10.0, 20.0],
    })
    orders = pd.DataFrame({
        "order_id": [1, 2],
        "customer_id": [1, 1],  # Bob (2) and Cara (3) never order
        "order_date": ["2024-01-05", "2024-02-10"],
    })
    order_items = pd.DataFrame({
        "order_item_id": [1, 2, 3],
        "order_id": [1, 1, 2],
        "product_id": [1, 2, 1],
        "quantity": [2, 1, 3],
        "discount": [0.0, 0.0, 0.1],
    })

    customers.to_sql("customers", conn, index=False)
    products.to_sql("products", conn, index=False)
    orders.to_sql("orders", conn, index=False)
    order_items.to_sql("order_items", conn, index=False)
    conn.close()

    instance = SQLAnalyzer(db_path=db_path)
    yield instance
    instance.close()


def test_missing_db_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        SQLAnalyzer(db_path=tmp_path / "nope.db")


def test_run_query_arbitrary_sql(analyzer):
    result = analyzer.run_query("SELECT COUNT(*) AS n FROM customers")
    assert result.loc[0, "n"] == 3


def test_top_customers_by_revenue(analyzer):
    # Order 1: 2*10 + 1*20 = 40; Order 2: 3*10*0.9 = 27 -> Alice total = 67
    result = analyzer.top_customers_by_revenue(n=5)
    assert len(result) == 1  # only Alice has ever ordered
    assert result.loc[0, "name"] == "Alice"
    assert result.loc[0, "total_revenue"] == 67.0


def test_top_customers_respects_n(analyzer):
    result = analyzer.top_customers_by_revenue(n=1)
    assert len(result) <= 1


def test_revenue_by_category_sums_correctly(analyzer):
    result = analyzer.revenue_by_category().set_index("category")
    # Tools (Widget): qty 2 + qty 3*0.9 discount => 20 + 27 = 47
    assert result.loc["Tools", "total_revenue"] == 47.0
    # Electronics (Gadget): qty 1 * 20 = 20
    assert result.loc["Electronics", "total_revenue"] == 20.0


def test_monthly_revenue_trend_chronological(analyzer):
    trend = analyzer.monthly_revenue_trend()
    assert list(trend["month"]) == ["2024-01", "2024-02"]


def test_customers_without_orders(analyzer):
    result = analyzer.customers_without_orders()
    names = set(result["name"])
    assert names == {"Bob", "Cara"}


def test_average_order_value_by_region(analyzer):
    result = analyzer.average_order_value_by_region()
    # Only North (Alice) has orders in this fixture
    assert set(result["region"]) == {"North"}
    assert result.loc[0, "avg_order_value"] > 0
