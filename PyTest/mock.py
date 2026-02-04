# payments.py
class PaymentProcessor:
    def __init__(self, gateway):
        self.gateway = gateway

    def pay(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        result = self.gateway.process_payment(amount)
        return result
