import os
import tempfile
from datetime import date
from decimal import Decimal

from expense_tracker.adapters.db import SqliteExpenseRepository
from expense_tracker.domain.models import Expense


def _make_repo() -> tuple[SqliteExpenseRepository, str]:
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    return SqliteExpenseRepository(path), path


def _make(**kwargs) -> Expense:
    defaults: dict = {
        "amount": Decimal("12.00"),
        "description": "coffee",
        "category": "food",
        "date": date(2026, 3, 1),
    }
    defaults.update(kwargs)
    return Expense(**defaults)


def test_save_and_list() -> None:
    repo, path = _make_repo()
    try:
        expense = _make()
        repo.save(expense)
        listed = repo.list_all()
        assert len(listed) == 1
        assert listed[0].id == expense.id
        assert listed[0].amount == expense.amount
        assert listed[0].description == expense.description
    finally:
        os.unlink(path)


def test_list_empty() -> None:
    repo, path = _make_repo()
    try:
        assert repo.list_all() == []
    finally:
        os.unlink(path)


def test_find_by_id() -> None:
    repo, path = _make_repo()
    try:
        expense = _make()
        repo.save(expense)
        found = repo.find_by_id(expense.id)
        assert found is not None
        assert found.id == expense.id
        assert found.date == expense.date
    finally:
        os.unlink(path)


def test_find_by_id_missing() -> None:
    repo, path = _make_repo()
    try:
        assert repo.find_by_id("does-not-exist") is None
    finally:
        os.unlink(path)


def test_delete() -> None:
    repo, path = _make_repo()
    try:
        expense = _make()
        repo.save(expense)
        deleted = repo.delete(expense.id)
        assert deleted is True
        assert repo.find_by_id(expense.id) is None
        assert repo.list_all() == []
    finally:
        os.unlink(path)


def test_delete_missing() -> None:
    repo, path = _make_repo()
    try:
        assert repo.delete("does-not-exist") is False
    finally:
        os.unlink(path)


def test_decimal_precision_preserved() -> None:
    repo, path = _make_repo()
    try:
        expense = _make(amount=Decimal("9.99"))
        repo.save(expense)
        found = repo.find_by_id(expense.id)
        assert found is not None
        assert found.amount == Decimal("9.99")
    finally:
        os.unlink(path)
