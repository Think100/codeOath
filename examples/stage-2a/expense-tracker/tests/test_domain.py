from datetime import date
from decimal import Decimal

import pytest

from expense_tracker.domain.models import Expense, summarize_by_category


def _make(**kwargs) -> Expense:
    defaults: dict = {
        "amount": Decimal("10.00"),
        "description": "lunch",
        "category": "food",
        "date": date(2026, 1, 1),
    }
    defaults.update(kwargs)
    return Expense(**defaults)


def test_expense_has_auto_id() -> None:
    e = _make()
    assert e.id
    assert len(e.id) == 36  # UUID format


def test_two_expenses_have_different_ids() -> None:
    assert _make().id != _make().id


def test_expense_is_immutable() -> None:
    e = _make()
    with pytest.raises(Exception):
        e.amount = Decimal("99.00")  # type: ignore[misc]


def test_negative_amount_raises() -> None:
    with pytest.raises(ValueError, match="positive"):
        _make(amount=Decimal("-1.00"))


def test_zero_amount_raises() -> None:
    with pytest.raises(ValueError, match="positive"):
        _make(amount=Decimal("0"))


def test_blank_description_raises() -> None:
    with pytest.raises(ValueError, match="Description"):
        _make(description="   ")


def test_blank_category_raises() -> None:
    with pytest.raises(ValueError, match="Category"):
        _make(category="")


def test_summarize_groups_by_category() -> None:
    expenses = [
        _make(amount=Decimal("10.00"), category="food"),
        _make(amount=Decimal("5.50"), category="food"),
        _make(amount=Decimal("20.00"), category="transport"),
    ]
    totals = summarize_by_category(expenses)
    assert totals["food"] == Decimal("15.50")
    assert totals["transport"] == Decimal("20.00")


def test_summarize_empty_list() -> None:
    assert summarize_by_category([]) == {}
