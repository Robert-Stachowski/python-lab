# test_payments.py
import unittest
from unittest.mock import Mock
from payments import PaymentProcessor

class TestPaymentProcessor(unittest.TestCase):
    def setUp(self):
        # Tworzymy mock "na sztywno", bez patchowania
        self.gateway = Mock()
        self.processor = PaymentProcessor(self.gateway)

    def test_payment_calls_gateway(self):
        # konfigurujemy mocka
        self.gateway.process_payment.return_value = "OK"

        # wywołanie testowanej metody
        result = self.processor.pay(100)

        # sprawdzenie, czy mock został wywołany
        self.gateway.process_payment.assert_called_once_with(100)
        self.assertEqual(result, "OK")

    def test_invalid_amount_raises_error(self):
        with self.assertRaises(ValueError):
            self.processor.pay(0)
