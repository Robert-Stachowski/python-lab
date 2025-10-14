# test_bank_account.py
import unittest
from bank_account import BankAccount


class TestBankAccount(unittest.TestCase):
    def setUp(self):
        self.acc = BankAccount(owner="Robert", initial_balance=1000.0, password="tajne")

    # --- Konstruktor / enkapsulacja ---
    def test_initial_state(self):
        self.assertEqual(self.acc.owner, "Robert")
        self.assertEqual(self.acc.balance, 1000.0)  # property getter

    def test_private_balance_not_directly_visible(self):
        # Python nie wystawi __balance jako atrybutu publicznego
        self.assertFalse(hasattr(self.acc, "__balance"))
        # (Uwaga: name mangling istnieje: _BankAccount__balance, ale NIE używamy tego w praktyce.)

    def test_initial_balance_must_be_non_negative(self):
        with self.assertRaises(ValueError):
            BankAccount(owner="X", initial_balance=-1, password="p")

    # --- Odczyt salda z hasłem ---
    def test_read_balance_with_correct_password(self):
        self.assertEqual(self.acc.read_balance("tajne"), 1000.0)

    def test_read_balance_with_wrong_password_raises(self):
        with self.assertRaises(PermissionError):
            self.acc.read_balance("zle")

    # --- Wpłata ---
    def test_deposit_positive_amount(self):
        self.acc.deposit(250.0)
        self.assertEqual(self.acc.balance, 1250.0)

    def test_deposit_non_positive_raises(self):
        for bad in (0, -1, -10.5):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    self.acc.deposit(bad)

    # --- Wypłata ---
    def test_withdraw_with_correct_password(self):
        self.acc.withdraw(300.0, "tajne")
        self.assertEqual(self.acc.balance, 700.0)

    def test_withdraw_with_wrong_password_raises(self):
        with self.assertRaises(PermissionError):
            self.acc.withdraw(100.0, "zle")

    def test_withdraw_insufficient_funds_raises(self):
        with self.assertRaisesRegex(ValueError, "insufficient funds"):
            self.acc.withdraw(5000.0, "tajne")

    def test_withdraw_non_positive_amount_raises(self):
        for bad in (0, -1, -5.5):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    self.acc.withdraw(bad, "tajne")

    # --- Zmiana hasła ---
    def test_change_password_happy_path(self):
        self.acc.change_password("tajne", "nowe")
        # nowe hasło powinno działać:
        self.assertEqual(self.acc.read_balance("nowe"), 1000.0)
        # stare już nie:
        with self.assertRaises(PermissionError):
            self.acc.read_balance("tajne")

    def test_change_password_wrong_old_raises(self):
        with self.assertRaises(PermissionError):
            self.acc.change_password("zle", "inne")

    def test_change_password_too_short_raises(self):
        with self.assertRaises(ValueError):
            self.acc.change_password("tajne", "abc")  # < 4 znaki


if __name__ == "__main__":
    unittest.main()
