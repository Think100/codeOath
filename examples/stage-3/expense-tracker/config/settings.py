from pathlib import Path

# Default database location; override via EXPENSE_DB environment variable.
DEFAULT_DB_PATH = Path.home() / ".expense_tracker" / "expenses.db"
