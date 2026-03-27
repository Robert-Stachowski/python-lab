class Calculator:
    def __init__(self) -> None:
        self.history: list[str] = []

    def add(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, a: float, b: float) -> float:
        return a - b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("Błąd: Nie można dzielić przez zero.")
        return a / b

    def power(self, a: float, b: float) -> float:
        return a ** b

    def calculate(self, a: float, b: float, operation: str) -> float:
        operation_map: dict[str, object] = {
            "+": self.add,
            "-": self.subtract,
            "*": self.multiply,
            "/": self.divide,
            "^": self.power,
        }
        func = operation_map.get(operation)
        if func is None:
            raise ValueError(f"Nieznana operacja: '{operation}'")
        result = func(a, b)
        self.history.append(f"{a} {operation} {b} = {result}")
        return result

    def show_history(self) -> None:
        if not self.history:
            print("Historia operacji jest pusta.")
        else:
            print("\n--- Historia operacji ---")
            for entry in self.history:
                print(entry)
            print("-------------------------\n")


if __name__ == "__main__":
    calc = Calculator()
    print()
    print("Prosty kalkulator.")
    print()

    while True:
        operation = input("Podaj operację (+, -, *, /, ^) lub 'exit' aby zakończyć: ")

        if operation == "exit":
            calc.show_history()
            break

        if operation not in ("+", "-", "*", "/", "^"):
            print("Nieznana operacja. Spróbuj ponownie.")
            continue

        try:
            a = float(input("Podaj pierwszą liczbę: "))
            b = float(input("Podaj drugą liczbę: "))
            result = calc.calculate(a, b, operation)
            print(f"Wynik: {result}")
        except ValueError:
            print("Błąd: Podano nieprawidłową liczbę. Spróbuj jeszcze raz.")
        except ZeroDivisionError as e:
            print(e)
        except Exception as e:
            print(f"Wystąpił nieoczekiwany błąd: {e}")
