import sqlite3
from pathlib import Path


SQL_FILES = [
    "schema.sql",
    "data_products.sql",
    "data_customers.sql",
    "data_orders.sql",
    "data_order_items.sql",
]


def load_sql(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise FileNotFoundError(f"SQL file not found: {path}") from None


def ingest(database_path: Path, sql_paths: list[Path]) -> None:
    if database_path.exists():
        database_path.unlink()

    with sqlite3.connect(database_path) as conn:
        for sql_file in sql_paths:
            script = load_sql(sql_file)
            conn.executescript(script)


def main() -> None:
    workspace = Path(__file__).parent
    database_path = workspace / "ecom.db"
    sql_paths = [workspace / name for name in SQL_FILES]

    ingest(database_path, sql_paths)
    print(f"Ingested SQL files into {database_path}")


if __name__ == "__main__":
    main()

