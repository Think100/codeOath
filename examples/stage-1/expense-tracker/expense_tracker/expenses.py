from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass
class Expense:
    amount: float
    category: str
    description: str
    date: str = field(default_factory=lambda: date.today().isoformat())

    def to_dict(self) -> dict:
        return {
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date,
        }

    @staticmethod
    def from_dict(data: dict) -> Expense:
        return Expense(
            amount=float(data["amount"]),
            category=data["category"],
            description=data["description"],
            date=data["date"],
        )


def add_expense(expenses: list[Expense], amount: float, category: str, description: str) -> Expense:
    expense = Expense(amount=round(amount, 2), category=category, description=description)
    expenses.append(expense)
    return expense


def summarize(expenses: list[Expense]) -> dict[str, float]:
    """Return total per category, sorted by amount descending."""
    totals: dict[str, float] = {}
    for e in expenses:
        totals[e.category] = round(totals.get(e.category, 0.0) + e.amount, 2)
    return dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))
