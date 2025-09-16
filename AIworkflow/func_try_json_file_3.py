# =========================================================
# MIX 5 ZADAŃ: funkcje, pliki (txt/json), obsługa błędów
# Zasady:
# - Każde zadanie ma własną funkcję/funkcje.
# - W miejscach na kod używaj # TODO (bez rozwiązań).
# - Nie używamy OOP w tych zadaniach.
# =========================================================

# ---------------------------------------------------------
# 1) NOTATNIK Z DATĄ (TXT)
# Opis:
# - Napisz funkcję save_note(path, text), która:
#   * jeśli 'text' jest pusty → raise ValueError,
#   * dopisuje (append) do pliku linię: "YYYY-MM-DD HH:MM | text".
# - Napisz funkcję read_notes(path), która zwróci listę wszystkich linii z pliku.
# - W main:
#   * poproś użytkownika o tekst,
#   * zapisz go, odczytaj cały plik i wypisz ostatnie 3 wpisy (jeśli są).
# - Obsłuż błędy: FileNotFoundError (gdy ścieżka katalogu nie istnieje), ValueError.
# TODO: uzupełnij ciało funkcji i logikę główną.

from datetime import datetime

def save_note(path, text):
    # TODO: sprawdź pusty tekst i dopisz linię z timestampem do pliku (append)
    if not text:
        raise ValueError("Brak treści")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    line = f"{timestamp} | {text}\n"
    with open(path, "a", encoding="utf-8") as f:
        f.write(line)


def read_notes(path):
    # TODO: odczytaj plik i zwróć listę linii (bez znaków końca linii)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().splitlines()
        if not content:
            raise ValueError("Brak danych")
        return content
        

if __name__ == "__main__":
    notes_path = r"Files_samples\notes.txt"  # możesz zmienić ścieżkę
    try:
        # TODO: pobierz tekst od użytkownika (input), zapisz i wypisz 3 ostatnie wpisy
        note_text = input("Podaj dane do zapisu: ")
        save_note(notes_path, note_text)
        print("Dane zapisano: \n")
        print(read_notes(notes_path))
        print("\nTrzy ostatnie wpisy: \n")
        for line in read_notes(notes_path)[-3:]:
            print(line)

    except FileNotFoundError:
        # TODO: wypisz komunikat, że katalog/plik nie istnieje
        print("Katalog/plik nie istnieje")
    except ValueError as e:
        # TODO: wypisz błąd walidacji
        print(f"Wystąpił błąd: {e}")

print("=" * 60)

# ---------------------------------------------------------
# 2) KONFIGURACJA JSON (LOAD/UPDATE)
# Opis:
# - Napisz funkcję load_config(path), która:
#   * wczytuje plik JSON do dict,
#   * jeśli plik nie istnieje → tworzy domyślny config (np. {"user":"Robert","level":"junior"}) i zapisuje go,
#   * jeśli plik istnieje ale jest pusty → raise ValueError,
#   * jeśli JSON błędny → przechwyć JSONDecodeError i podnieś ValueError z opisem.
# - Napisz funkcję update_config(path, key, value), która:
#   * wczytuje config, aktualizuje klucz i nadpisuje plik.
# - W main:
#   * wczytaj config, zapytaj użytkownika o klucz i wartość, zaktualizuj i pokaż wynik.
# TODO: uzupełnij ciało funkcji i logikę.
import json

def load_config(path):
    # TODO: wczytaj/utwórz domyślny config; obsłuż puste/błędne dane
    pass

def update_config(path, key, value):
    # TODO: wczytaj, zaktualizuj klucz i zapisz z powrotem
    pass

if __name__ == "__main__":
    cfg_path = r"Files_samples\config.json"
    try:
        # TODO: pobierz/utwórz config, poproś użytkownika o parę (key, value), zaktualizuj, wypisz efekt
        pass
    except ValueError as e:
        # TODO: obsłuż błędy walidacji
        pass
    except FileNotFoundError:
        # TODO: obsłuż brak ścieżki katalogu
        pass

print("=" * 60)

# ---------------------------------------------------------
# 3) STATYSTYKI LICZB Z LINII CSV (TXT)
# Opis:
# - Użytkownik wpisuje liczby całkowite oddzielone przecinkami (np. "10, -3, 7").
# - Napisz funkcję parse_ints(csv_text) → list[int].
#   * Jeśli którakolwiek wartość nie jest int → raise ValueError.
#   * Jeśli po przetworzeniu lista pusta → raise ValueError.
# - Napisz funkcję save_stats(path, numbers), która zapisze do pliku:
#   * sumę, średnią, min, max (każde w osobnej linii).
# - W main:
#   * pobierz wejście, sparsuj, zapisz statystyki do "stats.txt", potem odczytaj i wypisz zawartość na ekran.
# - Obsłuż błędy: ValueError (parsing/empty), FileNotFoundError (ścieżka).
# TODO: uzupełnij implementację.
def parse_ints(csv_text):
    # TODO: zamień csv_text na listę intów z walidacją
    pass

def save_stats(path, numbers):
    # TODO: zapisz sumę/średnią/min/max do pliku (po jednej wartości na linię)
    pass

def read_text(path):
    # TODO: odczytaj i zwróć zawartość pliku jako string
    pass

if __name__ == "__main__":
    stats_path = r"Files_samples\stats.txt"
    try:
        # TODO: pobierz surowe dane (input), sparsuj, zapisz statystyki, odczytaj i wypisz
        pass
    except ValueError as e:
        # TODO: wypisz info o błędnych danych
        pass
    except FileNotFoundError:
        # TODO: wypisz info o braku ścieżki
        pass

print("=" * 60)

# ---------------------------------------------------------
# 4) MERGE DWÓCH PLIKÓW TXT → UNIKALNE LINIE
# Opis:
# - Użytkownik podaje DWIE ścieżki do plików .txt (po przecinku).
# - Napisz funkcję read_lines(path) → list[str], zwracającą linie bez \n.
# - Napisz funkcję merge_unique(path_a, path_b, out_path), która:
#   * wczytuje linie z obu plików,
#   * łączy je w zbiór unikalnych, usuwa puste linie/spacje brzegowe,
#   * sortuje alfabetycznie i zapisuje do out_path (jedna linia = jeden wpis).
# - W main:
#   * pobierz ścieżki od użytkownika i wykonaj merge do "merged.txt", a następnie wczytaj i wypisz wynik.
# - Obsłuż błędy: FileNotFoundError (którykolwiek plik), ValueError (np. brak dwóch ścieżek).
# TODO: uzupełnij implementację.
def read_lines(path):
    # TODO: odczytaj linie i zwróć listę bez znaków końca linii
    pass

def merge_unique(path_a, path_b, out_path):
    # TODO: wczytaj, oczyść, złącz unikalnie, posortuj i zapisz do out_path
    pass

if __name__ == "__main__":
    out_path = r"Files_samples\merged.txt"
    try:
        # TODO: pobierz dwie ścieżki (input, rozdzielone przecinkiem), wykonaj merge i wypisz wynik
        pass
    except FileNotFoundError:
        # TODO: wypisz komunikat o braku któregoś z plików
        pass
    except ValueError as e:
        # TODO: wypisz komunikat o błędnych danych wejściowych
        pass

print("=" * 60)

# ---------------------------------------------------------
# 5) GENERATOR HASEŁ + ZAPIS/ODCZYT (TXT)
# Opis:
# - Napisz funkcję make_password(length, use_digits=True, use_letters=True, use_special=False), która:
#   * zwróci losowe hasło o długości 'length' korzystając z wybranych zestawów znaków,
#   * jeśli length < 4 → raise ValueError,
#   * jeśli wszystkie flagi False → raise ValueError.
# - Napisz funkcję save_password(path, password), która zapisze hasło do pliku (nadpisz).
# - Napisz funkcję read_password(path), która odczyta hasło jako string.
# - W main:
#   * pobierz długość i opcje od użytkownika (np. "12, digits, letters"),
#   * wygeneruj hasło, zapisz do "password.txt", odczytaj i pokaż (UWAGA: to tylko ćw. — normalnie haseł nie drukujemy!).
# - Obsłuż błędy: ValueError (walidacja), FileNotFoundError (ścieżka).
# TODO: uzupełnij implementację.
import random
import string

def make_password(length, use_digits=True, use_letters=True, use_special=False):
    # TODO: zbuduj pulę znaków na podstawie flag i zwróć losowy string o zadanej długości
    pass

def save_password(path, password):
    # TODO: zapisz hasło do pliku (w try/except jeśli chcesz)
    pass

def read_password(path):
    # TODO: odczytaj hasło z pliku i zwróć string
    pass

if __name__ == "__main__":
    pwd_path = r"Files_samples\password.txt"
    try:
        # TODO: pobierz od użytkownika parametry (długość + opcje), wygeneruj, zapisz, odczytaj i wypisz
        pass
    except ValueError as e:
        # TODO: wypisz błąd walidacji
        pass
    except FileNotFoundError:
        # TODO: wypisz błąd ścieżki
        pass

print("=" * 60)
# KONIEC PLIKU
