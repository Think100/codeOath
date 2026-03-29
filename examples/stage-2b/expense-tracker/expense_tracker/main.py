from __future__ import annotations

from expense_tracker.adapters.cli import run
from expense_tracker.adapters.db import DEFAULT_PATH, JsonExpenseRepository


def main() -> None:
    repo = JsonExpenseRepository(DEFAULT_PATH)
    run(repo)


if __name__ == "__main__":
    main()
