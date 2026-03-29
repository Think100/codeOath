from __future__ import annotations

from typing import Protocol

from expense_tracker.domain.models import Expense


class ExpenseRepository(Protocol):
    def load(self) -> list[Expense]: ...
    def save(self, expenses: list[Expense]) -> None: ...
