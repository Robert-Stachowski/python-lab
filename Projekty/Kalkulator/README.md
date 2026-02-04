# Calculator

## Opis projektu

To prosty kalkulator napisany w języku Python w podejściu obiektowym. Program umożliwia wykonywanie podstawowych operacji matematycznych: dodawanie, odejmowanie, mnożenie, dzielenie oraz potęgowanie. Kalkulator działa w trybie interaktywnym z użytkownikiem i przechowuje historię wszystkich działań.

Projekt bazuje na pierwotnym zadaniu z kursu DevMentor, jednak został znacznie rozszerzony i zrefaktoryzowany w celu poprawy jakości kodu, zgodności z zasadami czystej architektury i dobrych praktyk OOP.

---

## Czego się nauczyłem

- Tworzenia i organizowania klas w Pythonie zgodnie z zasadą SRP (Single Responsibility Principle)
- Obsługi wyjątków za pomocą `try-except`, w tym własnych komunikatów błędów (`ZeroDivisionError`)
- Rozdzielania logiki biznesowej od interakcji z użytkownikiem (I/O)
- Stosowania mapowania funkcji (`operation_map`) dla czytelniejszego zarządzania operacjami
- Tworzenia historii działań i refaktoryzacji kodu do bardziej czytelnej i skalowalnej postaci

---

## Jak uruchomić

1. Upewnij się, że masz zainstalowanego Pythona (min. wersja 3.10+)
2. Uruchom plik `Calculate.py` (np. w terminalu: `python Calculate.py`)
3. Wprowadź wybraną operację oraz liczby zgodnie z komunikatami w terminalu
4. Wpisz `exit`, aby zakończyć działanie programu i zobaczyć historię

---

## Zawartość pliku

- **Klasa `Calculator`**:
  - `add(a, b)`, `subtract(a, b)`, `multiply(a, b)`, `divide(a, b)`, `power(a, b)` – operacje matematyczne
  - `calculate(a, b, operation)` – obsługa żądania i zapis historii
  - `show_history()` – wypisuje historię operacji

- **Tryb interaktywny**:
  - w bloku `if __name__ == "__main__"` – obsługuje komunikację z użytkownikiem i kontroluje logikę pętli `while`

---

## Na co warto zwrócić uwagę

- W odróżnieniu od pierwotnych założeń (potęgowanie pętlą `for`), projekt został usprawniony i wykorzystuje operator `**`, co pozwala obsłużyć potęgowanie ujemne, ułamkowe i zerowe
- W CLI `^` oznacza potęgowanie (**)
- Zrezygnowano z pobierania danych wewnątrz metod logicznych (`divide`, `power`) – metody zgłaszają wyjątki, a dane wejściowe obsługiwane są centralnie
- Blok `try-except` obsługuje różne rodzaje błędów (`ValueError`, `ZeroDivisionError`, `Exception`) i wyświetla odpowiednie komunikaty
- Program można łatwo rozszerzyć o kolejne operacje matematyczne bez modyfikacji logiki głównej pętli

---

## Autor

Robert Stachowski  
Mentoring Python | Poziom: podstawy / OOP  
Repozytorium: https://github.com/Robert-Stachowski/First_step_by_Python_code
