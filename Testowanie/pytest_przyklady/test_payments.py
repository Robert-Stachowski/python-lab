# test_payments.py
"""
test_payments.py — polimorfizm + klasa abstrakcyjna + kiedy używać setUp()

DLACZEGO setUp()?
- setUp() uruchamia się PRZED KAŻDYM testem (test_*), więc daje ZA KAŻDYM RAZEM świeży stan.
- Dzięki temu testy są niezależne (jeden test nie psuje stanu dla drugiego).

KIEDY używać obiektów z self.methods (stworzonych w setUp)?
- Gdy testujesz ZACHOWANIE WSPÓLNE dla wszystkich klas (polimorfizm),
  np. „każda metoda płatności ma .pay() i zmniejsza saldo”.

KIEDY tworzyć nową instancję w teście?
- Gdy testujesz ZACHOWANIE SPECYFICZNE dla JEDNEJ KLASY (np. limit BLIK=500).
  Wtedy robimy b = Blik(1000.0) w samym teście, aby mieć pełną kontrolę nad stanem.

Zasada:
- Polimorfizm / wspólne cechy → self.methods (z setUp)
- Specyficzne zachowanie klasy → własna świeża instancja w teście
"""

import unittest
from payments import PaymentMethod, CreditCard, PayPal, Crypto, Blik


class TestPaymentPolymorphism(unittest.TestCase):
    def setUp(self):
        # Zestaw metod płatności do testów POLIMORFICZNYCH
        # (każdy test dostaje świeże obiekty)
        self.methods = [
            CreditCard(1000.0),
            PayPal(1000.0),
            Crypto(1000.0),
            Blik(1000.0),
        ]

    # --- Testy „wspólne” dla wszystkich klas (polimorfizm) ---

    def test_is_subclass_of_paymentmethod(self):
        # Każdy obiekt powinien być instancją klasy pochodnej od PaymentMethod
        for m in self.methods:
            self.assertIsInstance(m, PaymentMethod)

    def test_all_have_pay_method(self):
        # Każda klasa powinna mieć tę samą „twarz” API: metodę .pay(amount)
        for m in self.methods:
            self.assertTrue(callable(m.pay))

    def test_pay_reduces_balance(self):
        # Jeden test obsługuje WIELE klas — to właśnie polimorfizm
        for m in self.methods:
            with self.subTest(cls=m.__class__.__name__):
                start = m.balance
                msg = m.pay(100.0)
                # Każda implementacja zwraca komunikat zaczynający się od "Paid ..."
                self.assertIn("Paid", msg)
                # Saldo musi się zmniejszyć
                self.assertLess(m.balance, start)

    def test_insufficient_funds_raises(self):
        # Wspólny test: zbyt duża kwota powinna skończyć się ValueError
        for m in self.methods:
            with self.subTest(cls=m.__class__.__name__):
                with self.assertRaises(ValueError):
                    m.pay(10_000.0)

    # --- Testy SPECYFICZNE dla jednej klasy (tu: BLIK) ---

    def test_blik_payment_behavior(self):
        """
        Dlaczego NIE używamy tu self.methods?
        - Bo testujemy coś specyficznego dla BLIK (treść komunikatu, brak prowizji).
        - Tworzymy świeżą instancję, by mieć pełną kontrolę nad stanem początkowym,
          niezależnie od tego, co robią inne testy.
        """
        b = Blik(1000.0)
        msg = b.pay(100.0)
        self.assertIn("Blik", msg)           # komunikat zawiera nazwę metody
        self.assertEqual(b.balance, 900.0)   # brak prowizji → 1000 - 100 = 900

    def test_blik_limit_exceeded(self):
        """
        BLIK ma limit pojedynczej transakcji 500. Testujemy to na świeżym obiekcie.
        """
        b = Blik(1000.0)
        with self.assertRaises(ValueError):
            b.pay(600.0)  # powyżej limitu 500 → ValueError


if __name__ == "__main__":
    unittest.main()
