from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID

from expense_tracker.domain.models import Expense
from expense_tracker.domain.ports import ExpenseRepository


@dataclass
class AddExpenseResult:
    expense: Expense


@dataclass
class SummaryResult:
    expenses: list[Expense]
    total: Decimal
    by_category: dict[str, Decimal]


def add_expense(
    repo: ExpenseRepository,
    amount: Decimal,
    description: str,
    category: str,
    expense_date: date,
) -> AddExpenseResult:
    expense = Expense(amount=amount, description=description, category=category, date=expense_date)
    repo.save(expense)
    return AddExpenseResult(expense=expense)


def list_expenses(
    repo: ExpenseRepository,
    category: str | None = None,
    year: int | None = None,
    month: int | None = None,
) -> list[Expense]:
    if year is not None and month is not None:
        expenses = repo.get_by_month(year, month)
    else:
        expenses = repo.get_all()

    if category:
        expenses = [e for e in expenses if e.category.lower() == category.lower()]

    return sorted(expenses, key=lambda e: e.date)


def delete_expense(repo: ExpenseRepository, expense_id: UUID) -> bool:
    return repo.delete(expense_id)


def summarize_expenses(
    repo: ExpenseRepository,
    year: int | None = None,
    month: int | None = None,
) -> SummaryResult:
    expenses = list_expenses(repo, year=year, month=month)
    total = sum((e.amount for e in expenses), Decimal("0"))
    by_category: dict[str, Decimal] = {}
    for expense in expenses:
        by_category[expense.category] = by_category.get(expense.category, Decimal("0")) + expense.amount
    return SummaryResult(expenses=expenses, total=total, by_category=by_category)
