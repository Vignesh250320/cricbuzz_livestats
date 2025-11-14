"""Run all SQL practice queries from pages/sql_queries.py and report row counts."""
from __future__ import annotations

import ast
import pathlib

import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "cb_user",
    "password": "vicky@123",
    "database": "cricbuzz_livestats",
}

QUERIES_PATH = pathlib.Path("pages/sql_queries.py")


def load_queries() -> list[tuple[str, str]]:
    source = QUERIES_PATH.read_text(encoding="utf-8")
    module = ast.parse(source)
    for node in module.body:
        if isinstance(node, ast.FunctionDef) and node.name == "get_queries":
            for stmt in node.body:
                if isinstance(stmt, ast.Return):
                    queries_dict = ast.literal_eval(stmt.value)
                    return list(queries_dict.items())
    raise RuntimeError("get_queries function not found")


def run_queries():
    queries = load_queries()
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor(dictionary=True)

    results: list[tuple[int, str, int | str]] = []
    for idx, (title, sql) in enumerate(queries, start=1):
        try:
            cur.execute(sql)
            rows = cur.fetchall()
            results.append((idx, title, len(rows)))
        except Exception as exc:
            results.append((idx, title, f"ERROR: {exc}"))

    cur.close()
    conn.close()
    return results


def main():
    results = run_queries()
    for idx, title, status in results:
        print(f"Query {idx:02d} - {title}: {status}")


if __name__ == "__main__":
    main()
