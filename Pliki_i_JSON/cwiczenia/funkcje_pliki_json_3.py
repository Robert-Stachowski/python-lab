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
    notes_path = r"../pliki_przykladowe/notes.txt"  # możesz zmienić ścieżkę
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
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
        if not raw:
            raise ValueError("Brak danych")
        return json.loads(raw)
    except FileNotFoundError:
        config_data = {"user":"Robert","level":"junior"} # tu jest ta sama nazwa co w try: ze wzgledu na to, ze jeżeli plik pusty, to ma podstawić dict z tej zmiennej
        with open(path, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=4)
        return config_data
    except json.JSONDecodeError as e:
        raise ValueError(f"Błędny plik JSON: {e}")


def update_config(path, key, value):
    # TODO: wczytaj, zaktualizuj klucz i zapisz z powrotem
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    data[key] = value
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    return data

if __name__ == "__main__":
    config_path = r"../pliki_przykladowe/config_3.json"
    try:
        # TODO: pobierz/utwórz config, poproś użytkownika o parę (key, value), zaktualizuj, wypisz efekt
        config_data = load_config(config_path)
        user_key = input("Podaj nowy klucz: ")
        user_value = input("Podaj nową wartość klucza: ")
        updated_config = update_config(config_path, user_key, user_value)
        print(updated_config)

    except ValueError as e:
        # TODO: obsłuż błędy walidacji
        print(f"Bład: {e}")
# =========================================================
# KOMENTARZ WYJAŚNIAJĄCY – DLACZEGO TAK Z `config_data`
#
# Funkcja load_config próbuje wczytać dane z pliku JSON.
# - Jeśli plik istnieje i ma poprawne dane → zwraca dict z pliku.
# - Jeśli plik nie istnieje → tworzymy domyślny słownik i zapisujemy go do pliku.
# - Jeśli plik jest pusty albo ma błędny JSON → zgłaszamy ValueError.
#
# Zmienna `config_data` zawsze ma trzymać "aktualny config",
# niezależnie od tego, czy pochodzi z pliku, czy z fallbacka.
# Dzięki temu w dalszej części programu odwołujemy się zawsze do jednej nazwy.
#
# W skrócie:
# - `config_path` = ścieżka do pliku (string)
# - `config_data` = dane konfiguracyjne (dict) – z pliku albo domyślne
#
# To wzorzec tzw. fallback/default config.
# =========================================================
# =========================================================
# KOMENTARZE DO PLIKU (LINIA PO LINII)
# =========================================================
# import json → potrzebny do pracy z plikami JSON.
#
# def load_config(path): → funkcja do wczytania konfiguracji.
# try: → próbujemy otworzyć i przetworzyć plik.
# with open(path, "r", ...) as f: → otwieramy plik w trybie odczytu.
# raw = f.read() → wczytujemy całą zawartość jako string.
# if not raw: raise ValueError(...) → jeśli plik pusty, zgłaszamy błąd.
# return json.loads(raw) → parsujemy string do dict i zwracamy.
#
# except FileNotFoundError: → plik nie istnieje.
# config_data = {...} → przygotowujemy domyślne dane.
# with open(config_path, "w", ...) → otwieramy plik do zapisu (nadpisuje całość).
# json.dump(config_data, f, indent=4) → zapisujemy domyślny config do pliku.
# return config_data → zwracamy fallback, żeby program mógł działać dalej.
#
# except json.JSONDecodeError → JSON jest błędny.
# raise ValueError(...) → zamieniamy na ValueError z opisem.
#
# def update_config(path, key, value): → funkcja aktualizująca config.
# with open(path, "r", ...) as f: → otwieramy plik do odczytu.
# data = json.load(f) → ładujemy plik JSON do dict.
# data[key] = value → dodajemy/aktualizujemy klucz.
# with open(path, "w", ...) → otwieramy plik do zapisu (nadpisuje całość).
# json.dump(data, f, indent=4) → zapisujemy zaktualizowany dict.
# return data → zwracamy zaktualizowany config.
#
# if __name__ == "__main__": → kod uruchomi się tylko jeśli plik działa jako główny.
# config_path = ... → ścieżka do pliku config.
# config_data = load_config(config_path) → wczytujemy albo tworzymy domyślny config.
# user_key / user_value = input(...) → pytamy użytkownika o dane.
# updated_config = update_config(...) → aktualizujemy config.
# print(updated_config) → drukujemy efekt.
#
# except ValueError as e: → jeśli plik pusty lub błędny JSON.
# print(...) → pokazujemy komunikat błędu zamiast crasha.
# =========================================================
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
    stats_path = r"../pliki_przykladowe/stats.txt"
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
import os


def read_lines(path):
    # TODO: odczytaj linie i zwróć listę bez znaków końca linii
    with open(path, "r", encoding="utf-8") as f:
        read_data = f.read().splitlines()
        if not read_data:
            raise ValueError("Plik pusty")
        return read_data

def merge_unique(path_a, path_b, out_path):
    # TODO: wczytaj, oczyść, złącz unikalnie, posortuj i zapisz do out_path
    lines_a = read_lines(path_a)
    lines_b = read_lines(path_b)
    unique = set(lines_a + lines_b)
    cleaned = [x for x in unique if x]
    sorted_lines = sorted(cleaned)

    if not sorted_lines:
            raise ValueError("Brak danych")
    
    with open(out_path, "w", encoding="utf-8") as f:
        for line in sorted_lines:
            f.write(line + "\n")
        
    return sorted_lines


if __name__ == "__main__":
    out_path = r"../pliki_przykladowe/merged.txt"
    try:
        # TODO: pobierz dwie ścieżki (input, rozdzielone przecinkiem), wykonaj merge i wypisz wynik
        raw = input("Podaj dwie ścieżki, oddzielone przecinkiem: \n")
        parts = [p.strip() for p in raw.split(",") if p.strip()]

        if len(parts) != 2:
            raise ValueError("Podaj dokładnie dwie ścieżki")
        
        path_a = os.path.abspath(parts[0])
        path_b = os.path.abspath(parts[1])

        merge_unique(path_a, path_b, out_path)

        for line in read_lines(out_path):
            print(line)
        # print(read_lines(out_path))

    except FileNotFoundError as e:
        # TODO: wypisz komunikat o braku któregoś z plików
        print(f"Bład nie znaleziono pliku: {e}")
    except ValueError as e:
        # TODO: wypisz komunikat o błędnych danych wejściowych
        print(f"Bład: {e}")
# =========================================================
# KOMENTARZE DO ZADANIA 4 – MERGE DWÓCH PLIKÓW TXT
# =========================================================
# Funkcja read_lines(path):
# - Otwiera plik w trybie odczytu ("r").
# - f.read().splitlines() → zwraca listę linii BEZ znaków końca linii \n.
# - Jeśli plik jest pusty → ValueError("Plik pusty").
# - Zwraca listę stringów (list[str]) z zawartością pliku.

# Funkcja merge_unique(path_a, path_b, out_path):
# - Wczytuje zawartość obu plików (listy stringów).
# - Łączy je w jeden zbiór (set), dzięki temu usuwane są duplikaty.
# - Czyści zbiór: [x for x in unique if x] → usuwa puste stringi "".
# - Sortuje alfabetycznie (sorted).
# - Jeśli po czyszczeniu nic nie zostanie → ValueError("Brak danych").
# - Otwiera plik wynikowy w trybie zapisu ("w").
# - Zapisuje każdą linię osobno + "\n" na końcu.
# - Zwraca posortowaną listę unikalnych linii (list[str]).

# Blok main:
# - out_path = ścieżka docelowa, tu: "../pliki_przykladowe/merged.txt".
# - Pobiera od użytkownika input: dwie ścieżki oddzielone przecinkiem.
# - parts = lista ścieżek (po split i strip).
# - Jeśli liczba ścieżek != 2 → ValueError.
# - path_a, path_b → zamieniane na pełne ścieżki absolutne (os.path.abspath).
# - Wywołuje merge_unique(path_a, path_b, out_path).
# - Następnie czyta gotowy plik wynikowy i wypisuje każdą linię.
#   (dla czytelności zamiast print(list) → wypis w pętli po liniach).

# Obsługa wyjątków:
# - FileNotFoundError as e → jeśli któregoś pliku nie ma → komunikat "nie znaleziono pliku".
# - ValueError as e → np. pusty plik, brak dwóch ścieżek → komunikat "Błąd: ...".

# Najważniejsze koncepcje w tym zadaniu:
# - Operacje na plikach: open/read/write, splitlines().
# - Usuwanie duplikatów przez set().
# - List comprehension do filtrowania pustych linii.
# - Sortowanie listy (sorted()).
# - Obsługa wyjątków (FileNotFoundError, ValueError).
# - os.path.abspath() → zamiana ścieżek względnych na absolutne.
# =========================================================
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
    if length < 4:
        raise ValueError("Zbyt krótkie hasło!")

    pool = ""
    if use_digits:
        pool += string.digits
    if use_letters:
        pool += string.ascii_letters
    if use_special:
        pool += "!@#$%^&*"
    if not pool:
        raise ValueError("Musisz wybrać co najmniej jeden rodzaj znaków")
    
    password = ""
    for i in range(length):
        password += random.choice(pool)
    return password


def save_password(path, password):
    # TODO: zapisz hasło do pliku (w try/except jeśli chcesz)
    try:
        if not password:
            raise ValueError("Brak hasła do zapisania!")
        with open(path, "w", encoding="utf-8") as f:
            f.write(password)        
        return True
    except Exception as e:
        print(f"Błąd przy zapisie {e}")
        return False


def read_password(path):
    # TODO: odczytaj hasło z pliku i zwróć string
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if not content:
        raise ValueError("Plik z hasłem jest pusty.")
    return content


if __name__ == "__main__":
    pwd_path = r"../pliki_przykladowe/password.txt"
    try:
        # TODO: pobierz od użytkownika parametry (długość + opcje), wygeneruj, zapisz, odczytaj i wypisz
        raw_choice_data = input(
        "Podaj długość hasła(>=4 znaki) " \
        "oraz z jakiego zakresu symboli ma się składać(l-litery,c-cyfry,s-specjalne)" \
        ", oddziel od siebie przecinkami: "
        )
        choice_data = [p.strip() for p in raw_choice_data.split(",") if p.strip()]

        choice_length = int(choice_data[0])
        choice_digits = choice_data[2]
        choice_letters = choice_data[1]
        choice_special = choice_data[3]
        choice_password = make_password(choice_length,choice_digits,choice_letters,choice_special)
        save_password(pwd_path, choice_password)
        print(read_password(pwd_path))


    except ValueError as e:
        # TODO: wypisz błąd walidacji
        print(f"Błąd walidacji: {e}")
    except FileNotFoundError:
        # TODO: wypisz błąd ścieżki
        print(f"Błąd ścieżki/plików: {e}")
    except PermissionError as e:
        print(f"Brak uprawnień do zapisu/odczytu: {e}")
        

print("=" * 60)
# KONIEC PLIKU
