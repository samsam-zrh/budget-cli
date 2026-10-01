import tempfile
import unittest
from datetime import date
from decimal import Decimal
from pathlib import Path

from budget import Expense, add_expense, filter_by_month, parse_amount, read_expenses, summarize


class BudgetTest(unittest.TestCase):
    def test_parse_amount_accepts_decimal_comma(self) -> None:
        self.assertEqual(parse_amount("12,5"), Decimal("12.50"))

    def test_parse_amount_rejects_non_positive_values(self) -> None:
        for value in ("0", "-2"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_amount(value)

    def test_expenses_are_saved_and_loaded(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "expenses.csv"
            expense = Expense(date(2026, 10, 1), Decimal("8.40"), "transport", "Bus")

            add_expense(path, expense)

            self.assertEqual(read_expenses(path), [expense])

    def test_summary_can_be_filtered_by_month(self) -> None:
        expenses = [
            Expense(date(2026, 10, 1), Decimal("8.40"), "transport"),
            Expense(date(2026, 10, 2), Decimal("12.60"), "courses"),
            Expense(date(2026, 9, 30), Decimal("4.00"), "transport"),
        ]

        october = filter_by_month(expenses, "2026-10")
        total, categories = summarize(october)

        self.assertEqual(total, Decimal("21.00"))
        self.assertEqual(categories["transport"], Decimal("8.40"))
        self.assertEqual(categories["courses"], Decimal("12.60"))


if __name__ == "__main__":
    unittest.main()
