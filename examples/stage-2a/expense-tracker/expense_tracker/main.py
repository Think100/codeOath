from __future__ import annotations

import os
import sys

from expense_tracker.adapters.cli import run
from expense_tracker.adapters.db import SqliteExpenseRepository

DB_PATH = os.environ.get("EXPENSE_DB", "expenses.db")


def main() -> None:
    repo = SqliteExpenseRepository(DB_PATH)
    sys.exit(run(repo))
