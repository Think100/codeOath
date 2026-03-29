import tempfile
from datetime import date
from decimal import Decimal
from pathlib import Path
from uuid import uuid4

import pytest

from expense_tracker.adapters.outbound.sqlite_repo import SQLiteExpenseRepository
from expense_tracker.domain.models import Expense


@pytest.fixture
def repo():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield SQLiteExpenseRepository(Path(tmpdir) / "test.db")


def _expense(**kwargs) -> Expense:
    defaults: dict = dict(amount=Decimal("9.99"), description="Test", category="general", date=date(2026, 3, 1))
    return Expense(**{**defaults, **kwargs})


def test_save_and_get(repo) -> None:
    expense = _expense()
    repo.save(expense)
    loaded = repo.get_by_id(expense.id)
    assert loaded is not None
    assert loaded.id == expense.id
    assert loaded.amount == expense.amount
    assert loaded.description == expense.description
    assert loaded.date == expense.date


def test_get_all(repo) -> None:
    repo.save(_expense(description="A"))
    repo.save(_expense(description="B"))
    assert len(repo.get_all()) == 2


def test_delete(repo) -> None:
    expense = _expense()
    repo.save(expense)
    assert repo.delete(expense.id) is True
    assert repo.get_by_id(expense.id) is None


def test_delete_nonexistent(repo) -> None:
    assert repo.delete(uuid4()) is False


def test_get_by_month(repo) -> None:
    repo.save(_expense(date=date(2026, 3, 1)))
    repo.save(_expense(date=date(2026, 3, 15)))
    repo.save(_expense(date=date(2026, 4, 1)))
    assert len(repo.get_by_month(2026, 3)) == 2
    assert len(repo.get_by_month(2026, 4)) == 1


def test_decimal_precision(repo) -> None:
    expense = _expense(amount=Decimal("12.345"))
    repo.save(expense)
    loaded = repo.get_by_id(expense.id)
    assert loaded.amount == Decimal("12.345")
