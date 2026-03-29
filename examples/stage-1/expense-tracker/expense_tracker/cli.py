from __future__ import annotations

import argparse
import sys
from pathlib import Path

from expense_tracker import expenses as exp_module
from expense_tracker.storage import DEFAULT_PATH, load, save


def cmd_add(args: argparse.Namespace, path: Path) -> None:
    data = load(path)
    expense = exp_module.add_expense(data, args.amount, args.category, args.description)
    save(data, path)
    print(f"Added: {expense.date}  {expense.category}  {expense.amount:.2f}  {expense.description}")


def cmd_list(args: argparse.Namespace, path: Path) -> None:  # noqa: ARG001
    data = load(path)
    if not data:
        print("No expenses yet.")
        return
    print(f"{'Date':<12} {'Category':<16} {'Amount':>8}  Description")
    print("-" * 60)
    for e in data:
        print(f"{e.date:<12} {e.category:<16} {e.amount:>8.2f}  {e.description}")


def cmd_summary(args: argparse.Namespace, path: Path) -> None:  # noqa: ARG001
    data = load(path)
    if not data:
        print("No expenses yet.")
        return
    totals = exp_module.summarize(data)
    grand_total = sum(totals.values())
    print(f"{'Category':<20} {'Total':>10}")
    print("-" * 32)
    for category, total in totals.items():
        print(f"{category:<20} {total:>10.2f}")
    print("-" * 32)
    print(f"{'TOTAL':<20} {grand_total:>10.2f}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="expense-tracker",
        description="Track personal expenses from the terminal.",
    )
    parser.add_argument(
        "--file",
        type=Path,
        default=DEFAULT_PATH,
        metavar="PATH",
        help=f"Data file (default: {DEFAULT_PATH})",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add an expense")
    add_parser.add_argument("amount", type=float, help="Amount (e.g. 12.50)")
    add_parser.add_argument("category", help="Category (e.g. food, transport)")
    add_parser.add_argument("description", help="Short description")

    subparsers.add_parser("list", help="List all expenses")
    subparsers.add_parser("summary", help="Show totals per category")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    path: Path = args.file

    dispatch = {
        "add": cmd_add,
        "list": cmd_list,
        "summary": cmd_summary,
    }
    handler = dispatch.get(args.command)
    if handler is None:
        parser.print_help()
        sys.exit(1)
    handler(args, path)


if __name__ == "__main__":
    main()
