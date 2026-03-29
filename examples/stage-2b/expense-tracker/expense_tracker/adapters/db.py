from __future__ import annotations

import json
from pathlib import Path

from expense_tracker.domain.models import Expense

DEFAULT_PATH = Path.home() / ".expense-tracker.json"


class JsonExpenseRepository:
    """Implements ExpenseRepository: loads and saves expenses as JSON."""

    def __init__(self, path: Path = DEFAULT_PATH) -> None:
        self.path = path

    def load(self) -> list[Expense]:
        if not self.path.exists():
            return []
        with self.path.open(encoding="utf-8") as f:
            data = json.load(f)
        return [Expense.from_dict(item) for item in data]

    def save(self, expenses: list[Expense]) -> None:
        with self.path.open("w", encoding="utf-8") as f:
            json.dump([e.to_dict() for e in expenses], f, indent=2, ensure_ascii=False)
