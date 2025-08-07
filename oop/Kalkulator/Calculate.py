class Calculator:
    def __init__(self):
        self.history = []

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    # ZMIANA: Usunięto pętlę i interakcję z użytkownikiem.
    # Metoda teraz zgłasza błąd ZeroDivisionError, jeśli b jest zerem.
    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Błąd: Nie można dzielić przez zero.")
        return a / b

    # ZMIANA: Zastąpiono pętlę wbudowanym operatorem potęgowania (**).
    # Jest wydajniejszy i obsługuje wszystkie przypadki (wykładniki ujemne, zerowe, ułamkowe).
    # Pierwotny projekt nie zakładał użycia operatora ** tylko pętlę for.
    def power(self, a, b):
        return a ** b

    def show_history(self):
        if not self.history:
            print("Historia operacji jest pusta.")
        else:
            print("\n--- Historia operacji ---")
            # ZMIANA: Użycie bardziej opisowej nazwy zmiennej w pętli.
            for entry in self.history:
                print(entry)
            print("-------------------------\n")


    def calculate(self, a, b, operation):
        operation_map = {
            "+": self.add,
            "-": self.subtract,
            "*": self.multiply,
            "/": self.divide,
            "^": self.power
        }
        func = operation_map[operation]
        result = func(a, b)
        self.history.append(f"{a} {operation} {b} = {result}")
        return result

if __name__ == "__main__":
    calc = Calculator()
    print()
    print("Prosty kalkulator. ")
    print()

    while True:
        operation = input("Podaj operację (+, -, *, /, ^) lub 'exit' aby zakończyć: ")
        allowed_operations = ["+", "-", "/", "*", "^", "exit"]

        if operation == "exit":
            calc.show_history()
            break

        if operation not in allowed_operations:
            print("Nieznana operacja. Spróbuj ponownie.")
            
        try: 
            #UWAGA:
            # Nie jest to może najlepsza forma, ale na tym poziomie zupełnie wystarczająca, 
            # można ten fragment wydzielić do oddzielnej metody i wywołać ją w pętli while.
            a = float(input("Podaj pierwszą liczbę: "))
            b = float(input("Podaj drugą liczbę: "))

            result = calc.calculate(a, b, operation)
            print(f"Wynik: {result}")

        # ZMIANA: Rozszerzono obsługę błędów o ZeroDivisionError.
        except ValueError:
            print("Błąd: Podano nieprawidłową liczbę. Spróbuj jeszcze raz.")
        except ZeroDivisionError as e:
            # Wyświetlamy komunikat błędu zdefiniowany w metodzie divide.
            print(e)
        except Exception as e:
            # Ogólna obsługa innych, nieprzewidzianych błędów.
            print(f"Wystąpił nieoczekiwany błąd: {e}")