import sqlite3
from pathlib import Path


QUERY = """
SELECT
    c.first_name || ' ' || c.last_name AS customer_name,
    p.name AS product_name,
    oi.quantity
FROM customers AS c
JOIN orders AS o ON o.customer_id = c.id
JOIN order_items AS oi ON oi.order_id = o.id
JOIN products AS p ON p.id = oi.product_id
ORDER BY c.last_name, o.id, p.name;
"""


def main() -> None:
    db_path = Path(__file__).with_name("ecom.db")
    if not db_path.exists():
        raise FileNotFoundError("Database file ecom.db not found. Run ingest_data.py first.")

    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute(QUERY)
        rows = cursor.fetchall()

    if not rows:
        print("No order data found.")
        return

    print(f"{'Customer':25} {'Product':35} Quantity")
    print("-" * 70)
    for customer_name, product_name, quantity in rows:
        print(f"{customer_name:25} {product_name:35} {quantity}")


if __name__ == "__main__":
    main()

