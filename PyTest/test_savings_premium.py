# test_savings_premium.py
import unittest
from datetime import date, timedelta

from bank_account import BankAccount
from savings_premium import SavingsAccount, PremiumAccount


class TestInheritance(unittest.TestCase):
    def test_is_subclass(self):
        self.assertTrue(issubclass(SavingsAccount, BankAccount))
        self.assertTrue(issubclass(PremiumAccount, BankAccount))

    def test_is_instance(self):
        s = SavingsAccount("R", 1000, "tajne")
        p = PremiumAccount("R", 1000, "tajne")
        self.assertIsInstance(s, BankAccount)
        self.assertIsInstance(p, BankAccount)


class TestSavingsAccount(unittest.TestCase):
    def setUp(self):
        self.acc = SavingsAccount("Robert", 1000.0, "tajne")

    def test_three_withdrawals_free_then_fee(self):
        # 3 darmowe
        self.acc.withdraw(100.0, "tajne")
        self.acc.withdraw(100.0, "tajne")
        self.acc.withdraw(100.0, "tajne")
        self.assertEqual(self.acc.balance, 700.0)

        # 4-ta z prowizją 5.0 (700 - 100 - 5)
        self.acc.withdraw(100.0, "tajne")
        self.assertEqual(self.acc.balance, 595.0)

    def test_wrong_password_still_raises(self):
        with self.assertRaises(PermissionError):
            self.acc.withdraw(50.0, "zle")

    def test_non_positive_amount_raises(self):
        for bad in (0, -1.0, -5.5):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    self.acc.withdraw(bad, "tajne")


class TestPremiumAccount(unittest.TestCase):
    def setUp(self):
        self.p = PremiumAccount("Robert", 20_000.0, "tajne", daily_limit=10_000.0)

        # Podmieniamy „dziś”, by kontrolować upływ dni:
        self.today = date(2025, 1, 1)
        self.next_day = self.today + timedelta(days=1)
        self.p._today = lambda: self.today  # monkeypatch metody

    def test_daily_limit_respected_same_day(self):
        # 4000 + 6000 = 10000 (max)
        self.p.withdraw(4000.0, "tajne")
        self.p.withdraw(6000.0, "tajne")
        self.assertEqual(self.p.balance, 10_000.0)

        # kolejna wypłata tego samego dnia → błąd
        with self.assertRaisesRegex(ValueError, "daily limit exceeded"):
            self.p.withdraw(1.0, "tajne")

    def test_next_day_resets_counter(self):
        self.p.withdraw(6000.0, "tajne")
        self.assertEqual(self.p.balance, 14_000.0)

        # nowy dzień — reset licznika
        self.p._today = lambda: self.next_day
        self.p.withdraw(6000.0, "tajne")  # znowu wolno
        self.assertEqual(self.p.balance, 8_000.0)

    def test_password_and_amount_validation_inherited(self):
        with self.assertRaises(PermissionError):
            self.p.withdraw(100.0, "zle")
        with self.assertRaises(ValueError):
            self.p.withdraw(0.0, "tajne")


if __name__ == "__main__":
    unittest.main()
