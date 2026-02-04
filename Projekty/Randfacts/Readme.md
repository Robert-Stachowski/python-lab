# 🧠 Infinite Random Facts CLI

Mały, prosty skrypt CLI w Pythonie, który po każdym naciśnięciu **Entera** wyświetla losowy ciekawy fakt.

Projekt wrzucony **jako ciekawostka** – szybkie demo użycia zewnętrznej biblioteki i interakcji w terminalu. Bez przerostu formy nad treścią.

---

## 🔧 Wymagania

- Python 3.8+
- Biblioteka `randfacts`

Instalacja zależności:

    pip install randfacts

---

## ▶️ Uruchomienie

    python main.py

Po starcie:
- naciśnij **Enter** → dostajesz nowy losowy fakt
- **Ctrl + C** → kończysz program

---

## 📦 Co robi skrypt?

- działa w **pętli nieskończonej**
- czeka na interakcję użytkownika (`input`)
- pobiera losowy fakt z biblioteki `randfacts`
- filtruje treści (`filter_enabled=True`)
- wypisuje wynik w czytelnej formie CLI

Zero konfiguracji. Zero stanu. Zero komplikacji.

---

## 🎯 Po co to repo?

- przykład użycia **zewnętrznego modułu (pip)**
- prosty **CLI input/output**
- luźny projekt pokazujący, że nawet mała rzecz może być schludnie opisana

Idealne jako:
- ciekawostka w portfolio
- sandbox do eksperymentów
- punkt wyjścia do dalszej rozbudowy (argparse, flags, tryby pracy)

---

## ⚠️ Świadome uproszczenia

- brak testów
- brak argumentów CLI
- brak struktury pakietowej

To **feature**, nie bug.

---

## 📜 Licencja

Rób co chcesz. Używaj, modyfikuj, kasuj, śmiej się. :) 
