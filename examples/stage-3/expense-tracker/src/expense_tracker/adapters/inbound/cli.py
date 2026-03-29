from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
from uuid import UUID

import click

from expense_tracker.adapters.outbound.sqlite_repo import SQLiteExpenseRepository
from expense_tracker.application import use_cases


def _make_repo(db_path: Path) -> SQLiteExpenseRepository:
    return SQLiteExpenseRepository(db_path)


@click.group()
@click.option(
    "--db",
    default=str(Path.home() / ".expense_tracker" / "expenses.db"),
    envvar="EXPENSE_DB",
    show_default=True,
    help="Path to the SQLite database file.",
)
@click.pass_context
def cli(ctx: click.Context, db: str) -> None:
    """Expense tracker -- manage your expenses from the terminal."""
    ctx.ensure_object(dict)
    ctx.obj["repo"] = _make_repo(Path(db))


@cli.command()
@click.argument("amount")
@click.argument("description")
@click.option("--category", "-c", default="general", show_default=True, help="Expense category.")
@click.option("--date", "-d", "expense_date", default=None, help="Date as YYYY-MM-DD (default: today).")
@click.pass_context
def add(ctx: click.Context, amount: str, description: str, category: str, expense_date: str | None) -> None:
    """Add a new expense: AMOUNT DESCRIPTION."""
    try:
        parsed_amount = Decimal(amount)
    except InvalidOperation:
        raise click.BadParameter(f"'{amount}' is not a valid number", param_hint="AMOUNT")

    parsed_date = date.today()
    if expense_date:
        try:
            parsed_date = date.fromisoformat(expense_date)
        except ValueError:
            raise click.BadParameter(f"'{expense_date}' is not valid (use YYYY-MM-DD)", param_hint="--date")

    try:
        result = use_cases.add_expense(
            repo=ctx.obj["repo"],
            amount=parsed_amount,
            description=description,
            category=category,
            expense_date=parsed_date,
        )
    except ValueError as exc:
        raise click.ClickException(str(exc))

    e = result.expense
    click.echo(f"Added {e.id}  {e.date}  {e.amount:>10.2f}  [{e.category}]  {e.description}")


@cli.command("list")
@click.option("--category", "-c", default=None, help="Filter by category.")
@click.option("--month", "-m", default=None, help="Filter by month as YYYY-MM.")
@click.pass_context
def list_cmd(ctx: click.Context, category: str | None, month: str | None) -> None:
    """List expenses."""
    year, mon = _parse_month(month)
    expenses = use_cases.list_expenses(repo=ctx.obj["repo"], category=category, year=year, month=mon)

    if not expenses:
        click.echo("No expenses found.")
        return

    click.echo(f"{'ID':<36}  {'Date':<10}  {'Amount':>10}  {'Category':<15}  Description")
    click.echo("-" * 92)
    for e in expenses:
        click.echo(f"{str(e.id):<36}  {e.date.isoformat():<10}  {e.amount:>10.2f}  {e.category:<15}  {e.description}")


@cli.command()
@click.argument("expense_id")
@click.pass_context
def delete(ctx: click.Context, expense_id: str) -> None:
    """Delete an expense by ID."""
    try:
        uid = UUID(expense_id)
    except ValueError:
        raise click.BadParameter(f"'{expense_id}' is not a valid UUID", param_hint="EXPENSE_ID")

    if use_cases.delete_expense(repo=ctx.obj["repo"], expense_id=uid):
        click.echo(f"Deleted {expense_id}")
    else:
        raise click.ClickException(f"Expense {expense_id} not found")


@cli.command()
@click.option("--month", "-m", default=None, help="Summarize by month as YYYY-MM.")
@click.pass_context
def summary(ctx: click.Context, month: str | None) -> None:
    """Show a spending summary."""
    year, mon = _parse_month(month)
    result = use_cases.summarize_expenses(repo=ctx.obj["repo"], year=year, month=mon)

    if not result.expenses:
        click.echo("No expenses found.")
        return

    click.echo("By category:")
    for cat, total in sorted(result.by_category.items()):
        click.echo(f"  {cat:<20}  {total:>10.2f}")
    click.echo("-" * 35)
    click.echo(f"  {'TOTAL':<20}  {result.total:>10.2f}")


def _parse_month(month: str | None) -> tuple[int | None, int | None]:
    if not month:
        return None, None
    try:
        year, mon = map(int, month.split("-"))
        return year, mon
    except (ValueError, AttributeError):
        raise click.BadParameter(f"'{month}' is not valid (use YYYY-MM)", param_hint="--month")
