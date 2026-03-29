from __future__ import annotations

import argparse
import sys
from datetime import date
from decimal import Decimal, InvalidOperation

from expense_tracker.domain.models import Expense, summarize_by_category
from expense_tracker.domain.ports import ExpenseRepository


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Track your expenses from the terminal.")
    sub = parser.add_subparsers(dest="command")

    add_cmd = sub.add_parser("add", help="Add a new expense")
    add_cmd.add_argument("--amount", required=True, help="Amount (e.g. 12.50)")
    add_cmd.add_argument("--category", required=True, help="Category (e.g. food, transport)")
    add_cmd.add_argument("--description", required=True, help="Short description")
    add_cmd.add_argument("--date", default=None, help="Date as YYYY-MM-DD (default: today)")

    list_cmd = sub.add_parser("list", help="List all expenses")
    list_cmd.add_argument("--category", default=None, help="Filter by category")

    sub.add_parser("summary", help="Show totals per category")

    delete_cmd = sub.add_parser("delete", help="Delete an expense by ID")
    delete_cmd.add_argument("id", help="Expense ID (or ID prefix)")

    return parser


def run(repo: ExpenseRepository, argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "add":
        try:
            amount = Decimal(args.amount)
        except InvalidOperation:
            print(f"Invalid amount: {args.amount!r}", file=sys.stderr)
            return 1

        expense_date = date.fromisoformat(args.date) if args.date else date.today()

        try:
            expense = Expense(
                amount=amount,
                description=args.description,
                category=args.category.lower(),
                date=expense_date,
            )
        except ValueError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1

        repo.save(expense)
        print(
            f"Added  {expense.id[:8]}  {expense.date}  "
            f"{expense.category:<15} {expense.amount:>8}  {expense.description}"
        )
        return 0

    if args.command == "list":
        expenses = repo.list_all()
        if args.category:
            expenses = [e for e in expenses if e.category == args.category.lower()]
        if not expenses:
            print("No expenses found.")
            return 0
        print(f"{'ID':<10} {'Date':<12} {'Category':<15} {'Amount':>10}  Description")
        print("-" * 62)
        for e in expenses:
            print(
                f"{e.id[:8]:<10} {str(e.date):<12} {e.category:<15} "
                f"{str(e.amount):>10}  {e.description}"
            )
        return 0

    if args.command == "summary":
        expenses = repo.list_all()
        if not expenses:
            print("No expenses found.")
            return 0
        totals = summarize_by_category(expenses)
        grand_total = sum(totals.values(), Decimal(0))
        print(f"{'Category':<20} {'Total':>10}")
        print("-" * 32)
        for category, total in sorted(totals.items()):
            print(f"{category:<20} {str(total):>10}")
        print("-" * 32)
        print(f"{'TOTAL':<20} {str(grand_total):>10}")
        return 0

    if args.command == "delete":
        # Support both full UUID and short prefix
        all_expenses = repo.list_all()
        matches = [e for e in all_expenses if e.id.startswith(args.id)]
        if len(matches) == 0:
            print(f"No expense found with ID: {args.id}", file=sys.stderr)
            return 1
        if len(matches) > 1:
            print(f"Ambiguous ID prefix {args.id!r} matches {len(matches)} expenses.", file=sys.stderr)
            return 1
        repo.delete(matches[0].id)
        print(f"Deleted {matches[0].id[:8]}  {matches[0].description}")
        return 0

    parser.print_help()
    return 0
