import json
from pathlib import Path

import pytest

from expense_tracker.adapters.db import JsonExpenseRepository
from expense_tracker.domain.models import Expense


@pytest.fixture
def tmp_repo(tmp_path: Path) -> JsonExpenseRepository:
    return JsonExpenseRepository(tmp_path / "expenses.json")


def test_load_returns_empty_when_file_missing(tmp_repo: JsonExpenseRepository):
    assert tmp_repo.load() == []


def test_save_and_load_roundtrip(tmp_repo: JsonExpenseRepository):
    expenses = [Expense(12.5, "food", "lunch", "2024-01-01")]
    tmp_repo.save(expenses)
    loaded = tmp_repo.load()
    assert len(loaded) == 1
    assert loaded[0] == expenses[0]


def test_save_multiple_expenses(tmp_repo: JsonExpenseRepository):
    expenses = [
        Expense(10.0, "food", "breakfast", "2024-01-01"),
        Expense(5.50, "transport", "bus", "2024-01-02"),
    ]
    tmp_repo.save(expenses)
    loaded = tmp_repo.load()
    assert len(loaded) == 2
    assert loaded[1].category == "transport"


def test_save_writes_valid_json(tmp_repo: JsonExpenseRepository):
    tmp_repo.save([Expense(9.99, "misc", "test", "2024-01-01")])
    raw = json.loads(tmp_repo.path.read_text(encoding="utf-8"))
    assert isinstance(raw, list)
    assert raw[0]["amount"] == 9.99


def test_overwrite_replaces_existing(tmp_repo: JsonExpenseRepository):
    tmp_repo.save([Expense(1.0, "food", "snack", "2024-01-01")])
    tmp_repo.save([Expense(2.0, "misc", "book", "2024-01-02")])
    loaded = tmp_repo.load()
    assert len(loaded) == 1
    assert loaded[0].category == "misc"
