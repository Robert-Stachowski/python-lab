# savings_premium.py
from datetime import date
from bank_account import BankAccount


class SavingsAccount(BankAccount):
    """
    ROR oszczędnościowy:
      - 3 darmowe wypłaty/miesiąc (upraszczamy do licznika)
      - 4-ta i kolejne wypłaty: prowizja 5.0 (pobierana po udanej wypłacie)
      - hasła/kwoty waliduje logika bazowa (użyj super().withdraw)
    """
    FEE = 5.0

    def __init__(self, owner: str, initial_balance: float, password: str):
        super().__init__(owner, initial_balance, password)
        # licznik wypłat (reset miesięczny pomijamy w tym zadaniu)
        self._withdrawals_count = 0

    def withdraw(self, amount: float, pwd: str) -> None:
        super().withdraw(amount,pwd)
        self._withdrawals_count += 1
        if self._withdrawals_count >= 4:
            fee = 5.0
            if self.balance < fee:
                raise ValueError("insufficient funds for fee")
            self._BankAccount__balance -= fee
# Uwaga: obecna logika nie jest w pełni idealna z punktu widzenia systemu finansowego.
# Sprawdzenie, czy wystarczy środków na pobranie prowizji (fee),
# następuje dopiero PO wykonaniu właściwej wypłaty (super().withdraw).
# W praktyce system bankowy powinien zweryfikować, czy saldo >= amount + fee
# jeszcze przed realizacją operacji, aby transakcja mogła być w całości zatwierdzona.

        
class PremiumAccount(BankAccount):
    """
    Rachunek premium:
      - dzienny limit sumy wypłat: domyślnie 10_000
      - próba przekroczenia: ValueError("daily limit exceeded")
      - datę bierzemy z metody _today() (łatwe do „podmiany” w testach)
    """

    def __init__(self, owner: str, initial_balance: float, password: str, daily_limit: float = 10_000.0):
        super().__init__(owner, initial_balance, password)
        self._daily_limit = float(daily_limit)
        self._spent_today = 0.0
        self._last_withdraw_day = self._today()

    def _today(self) -> date:
        """Osobna metoda na dzisiejszą datę (testy ją podmieniają)."""
        return date.today()

    def _reset_if_new_day(self) -> None:
        today = self._today()
        if today != self._last_withdraw_day:
            self._last_withdraw_day = today
            self._spent_today = 0.0

    def withdraw(self, amount: float, pwd: str) -> None:
        self._reset_if_new_day()
        if pwd != self._password:
            raise PermissionError("invalid password")
        if amount <= 0:
            raise ValueError("amount must be > 0")
        if (amount+self._spent_today) > self._daily_limit:
            raise ValueError("daily limit exceeded")
        super().withdraw(amount,pwd)
        self._spent_today += amount
        
accounts = [
    BankAccount("Robert", 2000, "tajne"),
    SavingsAccount("Basia", 3000, "tajne"),
    PremiumAccount("Zenek", 50000, "tajne")
]

for acc in accounts:
    acc.withdraw(100, "tajne")
    print(acc.balance)
