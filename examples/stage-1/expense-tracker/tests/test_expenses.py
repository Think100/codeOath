from expense_tracker.expenses import Expense, add_expense, summarize


def test_add_expense_appends_and_returns():
    data = []
    expense = add_expense(data, 12.5, "food", "lunch")
    assert len(data) == 1
    assert data[0] is expense
    assert expense.amount == 12.5
    assert expense.category == "food"
    assert expense.description == "lunch"


def test_add_expense_rounds_amount():
    data = []
    expense = add_expense(data, 1.005, "misc", "rounding test")
    assert expense.amount == 1.0  # round half to even


def test_add_expense_sets_today_as_date():
    from datetime import date
    data = []
    expense = add_expense(data, 5.0, "transport", "bus")
    assert expense.date == date.today().isoformat()


def test_summarize_groups_by_category():
    data = [
        Expense(10.0, "food", "lunch", "2024-01-01"),
        Expense(5.0, "food", "coffee", "2024-01-02"),
        Expense(20.0, "transport", "taxi", "2024-01-03"),
    ]
    totals = summarize(data)
    assert totals["food"] == 15.0
    assert totals["transport"] == 20.0


def test_summarize_sorted_by_amount_descending():
    data = [
        Expense(5.0, "food", "snack", "2024-01-01"),
        Expense(50.0, "transport", "flight", "2024-01-02"),
        Expense(10.0, "misc", "book", "2024-01-03"),
    ]
    keys = list(summarize(data).keys())
    assert keys == ["transport", "misc", "food"]


def test_summarize_empty():
    assert summarize([]) == {}


def test_expense_roundtrip():
    original = Expense(42.0, "health", "pharmacy", "2024-06-15")
    restored = Expense.from_dict(original.to_dict())
    assert restored.amount == original.amount
    assert restored.category == original.category
    assert restored.description == original.description
    assert restored.date == original.date
