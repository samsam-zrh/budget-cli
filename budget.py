from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path


DEFAULT_FILE = Path.home() / ".budget-cli" / "expenses.csv"
FIELDS = ("date", "amount", "category", "note")


@dataclass(frozen=True)
class Expense:
    day: date
    amount: Decimal
    category: str
    note: str = ""


def parse_amount(value: str) -> Decimal:
    try:
        amount = Decimal(value.replace(",", ".")).quantize(Decimal("0.01"))
    except InvalidOperation as error:
        raise ValueError("Le montant doit être un nombre.") from error

    if amount <= 0:
        raise ValueError("Le montant doit être supérieur à zéro.")
    return amount


def parse_day(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise ValueError("La date doit respecter le format AAAA-MM-JJ.") from error


def add_expense(path: Path, expense: Expense) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    is_new_file = not path.exists()

    with path.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        if is_new_file:
            writer.writeheader()
        writer.writerow(
            {
                "date": expense.day.isoformat(),
                "amount": str(expense.amount),
                "category": expense.category,
                "note": expense.note,
            }
        )


def read_expenses(path: Path) -> list[Expense]:
    if not path.exists():
        return []

    with path.open(newline="", encoding="utf-8") as file:
        return [
            Expense(
                day=parse_day(row["date"]),
                amount=parse_amount(row["amount"]),
                category=row["category"],
                note=row["note"],
            )
            for row in csv.DictReader(file)
        ]


def filter_by_month(expenses: list[Expense], month: str | None) -> list[Expense]:
    if month is None:
        return expenses
    return [expense for expense in expenses if expense.day.strftime("%Y-%m") == month]


def summarize(expenses: list[Expense]) -> tuple[Decimal, dict[str, Decimal]]:
    by_category: dict[str, Decimal] = defaultdict(lambda: Decimal("0.00"))
    for expense in expenses:
        by_category[expense.category] += expense.amount
    return sum(by_category.values(), Decimal("0.00")), dict(by_category)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Suivre simplement ses dépenses.")
    parser.add_argument("--file", type=Path, default=DEFAULT_FILE, help="Fichier CSV à utiliser")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Ajouter une dépense")
    add_parser.add_argument("amount", help="Montant dépensé")
    add_parser.add_argument("category", help="Catégorie, par exemple courses")
    add_parser.add_argument("note", nargs="?", default="", help="Note facultative")
    add_parser.add_argument("--date", default=date.today().isoformat(), help="Date au format AAAA-MM-JJ")

    for command in ("list", "summary"):
        command_parser = subparsers.add_parser(command)
        command_parser.add_argument("--month", help="Mois au format AAAA-MM")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "add":
            expense = Expense(
                day=parse_day(args.date),
                amount=parse_amount(args.amount),
                category=args.category.strip().lower(),
                note=args.note.strip(),
            )
            add_expense(args.file, expense)
            print(f"Ajouté : {expense.amount:.2f} € · {expense.category}")
            return

        expenses = filter_by_month(read_expenses(args.file), args.month)
        if not expenses:
            print("Aucune dépense enregistrée pour cette période.")
            return

        if args.command == "list":
            for expense in sorted(expenses, key=lambda item: item.day):
                note = f" · {expense.note}" if expense.note else ""
                print(f"{expense.day} · {expense.amount:>8.2f} € · {expense.category}{note}")
            return

        total, categories = summarize(expenses)
        print(f"Total : {total:.2f} €")
        for category, amount in sorted(categories.items(), key=lambda item: item[1], reverse=True):
            print(f"- {category:<16} {amount:>8.2f} €")
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
