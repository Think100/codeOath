from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class Expense:
    amount: Decimal
    description: str
    category: str
    date: date
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self) -> None:
        if self.amount <= 0:
            raise ValueError(f"Amount must be positive, got {self.amount}")
        if not self.description.strip():
            raise ValueError("Description cannot be empty")
        if not self.category.strip():
            raise ValueError("Category cannot be empty")


def summarize_by_category(expenses: list[Expense]) -> dict[str, Decimal]:
    totals: dict[str, Decimal] = {}
    for expense in expenses:
        totals[expense.category] = totals.get(expense.category, Decimal(0)) + expense.amount
    return totals
