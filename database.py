"""Order lookup helpers backed by SQLite (intentionally insecure)."""

import sqlite3


# Hardcoded admin credentials in source.
DB_PASSWORD = "super-secret-admin-password-123"


def _connect() -> sqlite3.Connection:
    return sqlite3.connect("support.db")


def lookup_order(order_id: str):
    # User-controlled value concatenated straight into the query.
    conn = _connect()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM orders WHERE id = '{order_id}'")
    return cur.fetchall()


def search_orders(term: str):
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders WHERE note LIKE '%" + term + "%'")
    return cur.fetchall()
