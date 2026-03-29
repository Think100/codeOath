from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4

from expense_tracker.application import use_cases
from expense_tracker.domain.models import Expense
from expense_tracker.domain.ports import ExpenseRepository


class InMemoryRepo(ExpenseRepository):
    def __init__(self) -> None:
        self._store: dict[UUID, Expense] = {}

    def save(self, expense: Expense) -> None:
        self._store[expense.id] = expense

    def get_by_id(self, expense_id: UUID) -> Expense | None:
        return self._store.get(expense_id)

    def get_all(self) -> list[Expense]:
        return list(self._store.values())

    def delete(self, expense_id: UUID) -> bool:
        if expense_id in self._store:
            del self._store[expense_id]
            return True
        return False

    def get_by_month(self, year: int, month: int) -> list[Expense]:
        return [e for e in self._store.values() if e.date.year == year and e.date.month == month]


def _repo() -> InMemoryRepo:
    return InMemoryRepo()


def test_add_expense() -> None:
    repo = _repo()
    result = use_cases.add_expense(repo, Decimal("9.99"), "Lunch", "food", date(2026, 3, 15))
    assert result.expense.amount == Decimal("9.99")
    assert len(repo.get_all()) == 1


def test_list_empty() -> None:
    assert use_cases.list_expenses(_repo()) == []


def test_list_by_category() -> None:
    repo = _repo()
    use_cases.add_expense(repo, Decimal("5"), "Coffee", "food", date(2026, 3, 1))
    use_cases.add_expense(repo, Decimal("20"), "Bus", "transport", date(2026, 3, 2))
    food = use_cases.list_expenses(repo, category="food")
    assert len(food) == 1
    assert food[0].description == "Coffee"


def test_list_by_month() -> None:
    repo = _repo()
    use_cases.add_expense(repo, Decimal("5"), "Coffee", "food", date(2026, 3, 1))
    use_cases.add_expense(repo, Decimal("20"), "Bus", "transport", date(2026, 4, 1))
    march = use_cases.list_expenses(repo, year=2026, month=3)
    assert len(march) == 1


def test_delete_expense() -> None:
    repo = _repo()
    result = use_cases.add_expense(repo, Decimal("5"), "Coffee", "food", date(2026, 3, 1))
    assert use_cases.delete_expense(repo, result.expense.id) is True
    assert repo.get_by_id(result.expense.id) is None


def test_delete_nonexistent() -> None:
    assert use_cases.delete_expense(_repo(), uuid4()) is False


def test_summarize() -> None:
    repo = _repo()
    use_cases.add_expense(repo, Decimal("10"), "Coffee", "food", date(2026, 3, 1))
    use_cases.add_expense(repo, Decimal("20"), "Bus", "transport", date(2026, 3, 2))
    use_cases.add_expense(repo, Decimal("5"), "Tea", "food", date(2026, 3, 3))
    result = use_cases.summarize_expenses(repo)
    assert result.total == Decimal("35")
    assert result.by_category["food"] == Decimal("15")
    assert result.by_category["transport"] == Decimal("20")


def test_list_sorted_by_date() -> None:
    repo = _repo()
    use_cases.add_expense(repo, Decimal("5"), "C", "food", date(2026, 3, 3))
    use_cases.add_expense(repo, Decimal("5"), "A", "food", date(2026, 3, 1))
    use_cases.add_expense(repo, Decimal("5"), "B", "food", date(2026, 3, 2))
    expenses = use_cases.list_expenses(repo)
    assert [e.description for e in expenses] == ["A", "B", "C"]
