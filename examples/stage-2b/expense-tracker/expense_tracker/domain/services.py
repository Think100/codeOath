from __future__ import annotations

from expense_tracker.domain.models import Expense


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
