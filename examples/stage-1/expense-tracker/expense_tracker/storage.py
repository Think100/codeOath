from __future__ import annotations

import json
from pathlib import Path

from expense_tracker.expenses import Expense

DEFAULT_PATH = Path.home() / ".expense-tracker.json"


def load(path: Path = DEFAULT_PATH) -> list[Expense]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    return [Expense.from_dict(item) for item in data]


def save(expenses: list[Expense], path: Path = DEFAULT_PATH) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump([e.to_dict() for e in expenses], f, indent=2, ensure_ascii=False)
