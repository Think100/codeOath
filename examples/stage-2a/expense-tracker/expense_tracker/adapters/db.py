from __future__ import annotations

import contextlib
import sqlite3
from datetime import date
from decimal import Decimal

from expense_tracker.domain.models import Expense


class SqliteExpenseRepository:
    """Implements ExpenseRepository using a local SQLite database."""

    def __init__(self, db_path: str) -> None:
        self._db_path = db_path
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_schema(self) -> None:
        with contextlib.closing(self._connect()) as conn:
            with conn:
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS expenses (
                        id          TEXT PRIMARY KEY,
                        amount      TEXT NOT NULL,
                        description TEXT NOT NULL,
                        category    TEXT NOT NULL,
                        date        TEXT NOT NULL
                    )
                    """
                )

    def save(self, expense: Expense) -> None:
        with contextlib.closing(self._connect()) as conn:
            with conn:
                conn.execute(
                    "INSERT INTO expenses (id, amount, description, category, date) VALUES (?, ?, ?, ?, ?)",
                    (
                        expense.id,
                        str(expense.amount),
                        expense.description,
                        expense.category,
                        expense.date.isoformat(),
                    ),
                )

    def list_all(self) -> list[Expense]:
        with contextlib.closing(self._connect()) as conn:
            rows = conn.execute("SELECT * FROM expenses ORDER BY date DESC").fetchall()
        return [self._row_to_expense(row) for row in rows]

    def find_by_id(self, expense_id: str) -> Expense | None:
        with contextlib.closing(self._connect()) as conn:
            row = conn.execute(
                "SELECT * FROM expenses WHERE id = ?", (expense_id,)
            ).fetchone()
        return self._row_to_expense(row) if row else None

    def delete(self, expense_id: str) -> bool:
        with contextlib.closing(self._connect()) as conn:
            with conn:
                cursor = conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
                return cursor.rowcount > 0

    def _row_to_expense(self, row: sqlite3.Row) -> Expense:
        return Expense(
            id=row["id"],
            amount=Decimal(row["amount"]),
            description=row["description"],
            category=row["category"],
            date=date.fromisoformat(row["date"]),
        )
