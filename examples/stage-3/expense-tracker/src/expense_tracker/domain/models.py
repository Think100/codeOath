from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4


@dataclass
class Expense:
    amount: Decimal
    description: str
    category: str
    date: date
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        if self.amount <= 0:
            raise ValueError(f"Amount must be positive, got {self.amount}")
        if not self.description.strip():
            raise ValueError("Description must not be empty")
        if not self.category.strip():
            raise ValueError("Category must not be empty")
