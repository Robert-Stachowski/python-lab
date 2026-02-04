# payments.py
from abc import ABC, abstractmethod


class PaymentMethod(ABC):
    """
    Klasa abstrakcyjna (szablon interfejsu płatności).
    Każda metoda płatności MUSI mieć metodę pay(amount).
    """
    def __init__(self, balance: float):
        self.balance = balance

    @abstractmethod
    def pay(self, amount: float) -> str:
        """Abstrakcyjna metoda płatności."""
        pass


class CreditCard(PaymentMethod):
    """Płatność kartą — prowizja 2%."""
    FEE_RATE = 0.02

    def pay(self, amount: float) -> str:
        fee = amount * self.FEE_RATE
        total = amount + fee
        if total > self.balance:
            raise ValueError("Insufficient funds on card.")
        self.balance -= total
        return f"Paid {amount} by CreditCard (fee: {fee:.2f})"


class PayPal(PaymentMethod):
    """Płatność PayPal — prowizja stała 1.5."""
    FEE = 1.5

    def pay(self, amount: float) -> str:
        total = amount + self.FEE
        if total > self.balance:
            raise ValueError("Insufficient PayPal balance.")
        self.balance -= total
        return f"Paid {amount} via PayPal (fee: {self.FEE})"


class Crypto(PaymentMethod):
    """Płatność kryptowalutą — brak prowizji, ale ryzyko (kurs) -5% wartości."""
    def pay(self, amount: float) -> str:
        value_loss = amount * 0.05
        total = amount + value_loss
        if total > self.balance:
            raise ValueError("Insufficient crypto balance.")
        self.balance -= total
        return f"Paid {amount} in Crypto (loss: {value_loss:.2f})"


class Blik(PaymentMethod):
    """Płatność Blikiem — brak prowizji, ale ograniczenie, max 500zł."""
    def pay(self, amount: float) -> str:               
        if amount > 500:
            raise ValueError("Insufficient balance.")
        if amount >self.balance:
            raise ValueError("Insufficient Blik balance.")
        self.balance -= amount
        return f"Paid {amount} via Blik (fee: free) "
        
