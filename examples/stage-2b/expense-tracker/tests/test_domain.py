from datetime import date

from expense_tracker.domain.models import Expense
from expense_tracker.domain.services import add_expense, summarize


def test_add_expense_appends_and_returns():
    expenses = []
    expense = add_expense(expenses, 12.5, "food", "lunch")
    assert len(expenses) == 1
    assert expenses[0] is expense
    assert expense.amount == 12.5
    assert expense.category == "food"
    assert expense.description == "lunch"


def test_add_expense_rounds_amount():
    expenses = []
    expense = add_expense(expenses, 1.005, "misc", "rounding test")
    assert expense.amount == 1.0  # round half to even


def test_add_expense_sets_today_as_date():
    expenses = []
    expense = add_expense(expenses, 5.0, "transport", "bus")
    assert expense.date == date.today().isoformat()


def test_add_expense_model_is_immutable():
    expenses = []
    expense = add_expense(expenses, 10.0, "food", "pizza")
    try:
        expense.amount = 99.0  # type: ignore[misc]
        assert False, "Should have raised FrozenInstanceError"  # noqa: B011
    except Exception:
        pass


def test_summarize_groups_by_category():
    expenses = [
        Expense(10.0, "food", "lunch", "2024-01-01"),
        Expense(5.0, "food", "coffee", "2024-01-02"),
        Expense(20.0, "transport", "taxi", "2024-01-03"),
    ]
    totals = summarize(expenses)
    assert totals["food"] == 15.0
    assert totals["transport"] == 20.0


def test_summarize_sorted_by_amount_descending():
    expenses = [
        Expense(5.0, "food", "snack", "2024-01-01"),
        Expense(50.0, "transport", "flight", "2024-01-02"),
        Expense(10.0, "misc", "book", "2024-01-03"),
    ]
    keys = list(summarize(expenses).keys())
    assert keys == ["transport", "misc", "food"]


def test_summarize_empty():
    assert summarize([]) == {}


def test_expense_roundtrip():
    original = Expense(42.0, "health", "pharmacy", "2024-06-15")
    restored = Expense.from_dict(original.to_dict())
    assert restored == original
