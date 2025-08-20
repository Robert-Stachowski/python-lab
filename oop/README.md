# InputBankAccount.py

Opis projektu:  

Ten skrypt to moja pierwsza implementacja klasy BankAccount w Pythonie. Program umożliwia użytkownikowi wprowadzanie danych z klawiatury (input), wykonywanie operacji wpłaty i wypłaty oraz sprawdzanie aktualnego salda.

To jedno z moich pierwszych "większych" zadań w ramach mentoringu, mające na celu praktyczne zastosowanie programowania obiektowego (OOP). Bazowy plik nie zawierał żadnych inputów ani interakcji z użytkownikiem – ta część została dodana jako moja własna inwencja twórcza. Dodatkowo wprowadziłem podstawową obsługę błędów, która zapobiega wpisywaniu nieprawidłowych danych (np. liter zamiast liczb).

W nowszej wersji:
- użyto typu **`Decimal`** z modułu `decimal` do obsługi kwot pieniężnych (większa precyzja niż float),
- interfejs wiersza poleceń (CLI) uruchamiany jest tylko w bloku `if __name__ == "__main__":`.

---

Czego się tutaj uczę:

- Tworzenia klas i obiektów
- Definiowania metod (deposit, withdraw)
- Użycia pętli while do interakcji z użytkownikiem
- Obsługi danych wejściowych z klawiatury
- Warunków if/else
- Obsługi błędów i niepoprawnych danych
- Podstaw dobrej struktury kodu
- Korzystania z typu `Decimal` do finansów
- Oddzielania logiki od interfejsu użytkownika dzięki `if __name__ == "__main__":`

---

Jak uruchomić:

```bash
python InputBankAccount.py
```

Upewnij się, że masz zainstalowanego Pythona 3.10+.

---

Przykład użycia (CLI):

```text
Wpisz polecenie (wplata / wyplata / saldo / wyjscie): wplata
Podaj kwotę wpłaty: 100
Saldo po wpłacie: 1100

Wpisz polecenie (wplata / wyplata / saldo / wyjscie): saldo
Saldo: 1100

Wpisz polecenie (wplata / wyplata / saldo / wyjscie): wyplata
Podaj kwotę wypłaty (saldo: 1100): 200
Saldo po wypłacie: 900
```

---

Zawartość pliku:

- `class BankAccount:` – klasa reprezentująca konto bankowe
- `deposit(self, amount)` – metoda do wpłacania środków
- `withdraw(self, amount)` – metoda do wypłacania środków z uwzględnieniem limitów
- `get_balance(self)` – metoda zwracająca saldo
- `if __name__ == "__main__":` – uruchamia prosty interfejs konsolowy
- Obsługa błędów (np. `ValueError`, `InvalidOperation` z modułu `decimal`)

---

Znane ograniczenia:

- Brak trwałego zapisu danych (saldo nie jest zapisywane po zamknięciu programu)
- Obsługa wyłącznie w formie tekstowej (CLI)
- Brak testów jednostkowych (planowane w kolejnych etapach nauki)

---

Dodatkowo:

Ten plik powstał jako część mojego rozwoju w ramach nauki Pythona od podstaw. Początkowo był użyty również w pull requeście do repozytorium mentora. Tutaj został uporządkowany jako element osobistego portfolio i wzbogacony o własne rozszerzenia.

---

Autor:

Robert Stachowski  
Mentoring Python | Poziom: podstawy / OOP  
Repozytorium: https://github.com/Robert-Stachowski/First_step_by_Python_code
