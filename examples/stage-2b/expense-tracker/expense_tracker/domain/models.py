from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass(frozen=True, slots=True)
class Expense:
    amount: float
    category: str
    description: str
    date: str = field(default_factory=lambda: date.today().isoformat())

    def to_dict(self) -> dict:
        return {
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date,
        }

    @staticmethod
    def from_dict(data: dict) -> Expense:
        return Expense(
            amount=float(data["amount"]),
            category=data["category"],
            description=data["description"],
            date=data["date"],
        )
