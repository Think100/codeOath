from datetime import date
from decimal import Decimal
from uuid import UUID

import pytest

from expense_tracker.domain.models import Expense


def test_expense_creation() -> None:
    expense = Expense(amount=Decimal("12.50"), description="Coffee", category="food", date=date(2026, 3, 1))
    assert expense.amount == Decimal("12.50")
    assert expense.description == "Coffee"
    assert expense.category == "food"
    assert isinstance(expense.id, UUID)


def test_rejects_zero_amount() -> None:
    with pytest.raises(ValueError, match="positive"):
        Expense(amount=Decimal("0"), description="Test", category="food", date=date.today())


def test_rejects_negative_amount() -> None:
    with pytest.raises(ValueError, match="positive"):
        Expense(amount=Decimal("-5"), description="Test", category="food", date=date.today())


def test_rejects_empty_description() -> None:
    with pytest.raises(ValueError, match="Description"):
        Expense(amount=Decimal("10"), description="  ", category="food", date=date.today())


def test_rejects_empty_category() -> None:
    with pytest.raises(ValueError, match="Category"):
        Expense(amount=Decimal("10"), description="Test", category="  ", date=date.today())
