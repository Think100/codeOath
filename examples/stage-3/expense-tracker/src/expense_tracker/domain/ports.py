from abc import ABC, abstractmethod
from uuid import UUID

from expense_tracker.domain.models import Expense


class ExpenseRepository(ABC):
    @abstractmethod
    def save(self, expense: Expense) -> None: ...

    @abstractmethod
    def get_by_id(self, expense_id: UUID) -> Expense | None: ...

    @abstractmethod
    def get_all(self) -> list[Expense]: ...

    @abstractmethod
    def delete(self, expense_id: UUID) -> bool: ...

    @abstractmethod
    def get_by_month(self, year: int, month: int) -> list[Expense]: ...
