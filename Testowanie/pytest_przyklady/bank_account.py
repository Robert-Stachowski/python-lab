# bank_account.py

class BankAccount:
    """
    Prosty rachunek bankowy z enkapsulacją salda i kontrolą dostępu.
    Wymagania:
      - saldo trzymamy prywatnie w __balance
      - hasło trzymamy w _password (chronione — konwencja)
      - wpłata > 0, inaczej ValueError
      - wypłata wymaga poprawnego hasła; przy braku środków -> ValueError("insufficient funds")
      - metoda read_balance(pwd) zwraca saldo po poprawnym haśle; w innym wypadku PermissionError
      - property `balance` (tylko getter) zwraca bieżące saldo (do użytku wewnętrznego/testów)
    """

    def __init__(self, owner: str, initial_balance: float, password: str):
        if initial_balance <= 0:
            raise ValueError("Initial balance must be positive")
        self.owner = owner
        self.__balance = float(initial_balance)
        self._password = password
        


    @property
    def balance(self) -> float:
        return self.__balance    

        

    def read_balance(self, pwd: str) -> float:        
        if pwd != self._password:
            raise PermissionError("Invalid password")
        return self.__balance



    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Zbyt mala kwota")
        self.__balance += amount



    def withdraw(self, amount: float, pwd: str) -> None:
        if pwd != self._password:
            raise PermissionError("Invalid password")
        if amount > self.__balance:
            raise ValueError("insufficient funds")
        if amount <= 0:
            raise ValueError("Wypłata nie może być ujemna/zerowa!")
        self.__balance -= amount
        


    def change_password(self, old_pwd: str, new_pwd: str) -> None:
        if old_pwd != self._password:
            raise PermissionError("Wrong password")
        if len(new_pwd) < 4:
            raise ValueError("To short password")
        self._password = new_pwd
        #
        