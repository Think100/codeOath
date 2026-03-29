import sqlite3
from contextlib import contextmanager
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Generator
from uuid import UUID

from expense_tracker.domain.models import Expense
from expense_tracker.domain.ports import ExpenseRepository


class SQLiteExpenseRepository(ExpenseRepository):
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    @contextmanager
    def _connect(self) -> Generator[sqlite3.Connection, None, None]:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id TEXT PRIMARY KEY,
                    amount TEXT NOT NULL,
                    description TEXT NOT NULL,
                    category TEXT NOT NULL,
                    date TEXT NOT NULL
                )
            """)

    def save(self, expense: Expense) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO expenses (id, amount, description, category, date) VALUES (?, ?, ?, ?, ?)",
                (str(expense.id), str(expense.amount), expense.description, expense.category, expense.date.isoformat()),
            )

    def get_by_id(self, expense_id: UUID) -> Expense | None:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM expenses WHERE id = ?", (str(expense_id),)).fetchone()
        return self._row_to_expense(row) if row else None

    def get_all(self) -> list[Expense]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM expenses ORDER BY date").fetchall()
        return [self._row_to_expense(row) for row in rows]

    def delete(self, expense_id: UUID) -> bool:
        with self._connect() as conn:
            cursor = conn.execute("DELETE FROM expenses WHERE id = ?", (str(expense_id),))
        return cursor.rowcount > 0

    def get_by_month(self, year: int, month: int) -> list[Expense]:
        month_prefix = f"{year:04d}-{month:02d}-"
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM expenses WHERE date LIKE ? ORDER BY date",
                (f"{month_prefix}%",),
            ).fetchall()
        return [self._row_to_expense(row) for row in rows]

    @staticmethod
    def _row_to_expense(row: sqlite3.Row) -> Expense:
        return Expense(
            id=UUID(row["id"]),
            amount=Decimal(row["amount"]),
            description=row["description"],
            category=row["category"],
            date=date.fromisoformat(row["date"]),
        )
