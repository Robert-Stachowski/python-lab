class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance
        
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount            
            return True
        else:
            return None   
   
    def withdraw(self, amount):
        if amount <= self.__balance:
            self.__balance -= amount                        
            return True          
        else:            
            return None            

    def get_balance(self):
        return self.__balance
    
account = BankAccount("Jan Nowak", 1000)

while True:
    menu_amount = input("Wpisz polecenie (wplata / wyplata / wyjscie): ")
    if menu_amount == "wyjscie" :
        break

    elif menu_amount == "wyplata" :
        try:        
            input_amount = float(input(f"Podaj kwotę wypłaty, mniejszą niż saldo( {account.get_balance()} ): "))       
            result = account.withdraw(input_amount)
            
            if result is True:
                print(f"Saldo po wypłacie wynosi: {account.get_balance()} ")
                
            else:
                print("---")
                print("Poucinam paluszki ;P ")
                print("---")     

        except ValueError:
            print("Wprowadź poprawną liczbę: ")

    elif menu_amount == "wplata":  
        try:      
            input_amount = float(input("Podaj kwotę wpłaty : "))
            result = account.deposit(input_amount)

            if result is True:
                print(f"Saldo po wpłacie: {account.get_balance()}")
                
            else:
               print("Nie można wpłacać ujemnych kwot, zera również...")
        except ValueError:
            print("Wprowadź poprawna liczbę: ")

    else: 
        print("Halo, halo co tu się dzieje?")
        break
