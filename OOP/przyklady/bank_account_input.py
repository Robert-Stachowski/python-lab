from decimal import Decimal, InvalidOperation


class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            return True
        else:
            return False

    def withdraw(self, amount):
        if amount <= self.__balance and amount > 0:
            self.__balance -= amount
            return True
        else:
            return False

    def get_balance(self):
        return self.__balance


if __name__ == "__main__":
    account = BankAccount("Jan Nowak", Decimal("1000"))
    
    while True:
        choice = input("Wpisz polecenie (wplata / wyplata / saldo / wyjscie): ").strip().lower()
        if choice == "wyjscie":
            break

        elif choice == "saldo":
             print(f"Saldo wynosi: {account.get_balance()}")

        elif choice == "wyplata":
            try:
                input_amount = Decimal(input(f"Podaj kwotę wypłaty, mniejszą niż saldo( {account.get_balance()} ): "))
                result = account.withdraw(input_amount)
            except InvalidOperation:
                print("Wprowadź poprawną liczbę: ")

            if result is True:
                print(f"Saldo po wypłacie wynosi: {account.get_balance()} ")
            else:
                print("---")
                print("Poucinam paluszki ;P ")
                print("---")

            
        elif choice == "wplata":
            try:
                input_amount = Decimal(input("Podaj kwotę wpłaty : "))
                result = account.deposit(input_amount)
            except ValueError:
                print("Wprowadź poprawna liczbę: ")

            if result is True:
                print(f"Saldo po wpłacie: {account.get_balance()}")
            else:
                print("Nie można wpłacać ujemnych kwot, zera również...")
            

        else:
            print("Halo, halo co tu się dzieje?")
        continue
