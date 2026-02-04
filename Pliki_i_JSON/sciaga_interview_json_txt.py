# =========================================================
# PYTHON INTERVIEW CHEATS
# =========================================================
# Zawiera szkielety i gotowe wzorce dla:
# 1. JSON: load z fallbackiem (domyślne dane, obsługa błędów)
# 2. JSON: update (wczytaj → zmień → zapisz)
# 3. TXT: notatnik (z timestampem, dopisywanie, odczyt)
# 4. Main: dwa warianty — config i notatnik
# 5. Komentarze i tipy do rekrutacji
# =========================================================

import json
from datetime import datetime

# ---------------------------------------------------------
# 1) JSON: load z fallbackiem
# ---------------------------------------------------------
def load_config(path):
    """
    Wczytaj plik JSON do dict.
    - Jeśli plik istnieje i jest poprawny → zwróć dict.
    - Jeśli plik nie istnieje → utwórz domyślny config i zapisz go.
    - Jeśli plik istnieje, ale pusty → ValueError.
    - Jeśli JSON błędny → ValueError z opisem.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
        if not raw:
            raise ValueError("Empty config file")
        return json.loads(raw)
    except FileNotFoundError:
        default_data = {"user": "Robert", "level": "junior"}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=4)
        return default_data
    except json.JSONDecodeError as e:
        raise ValueError(f"Bad JSON: {e}")

# ---------------------------------------------------------
# 2) JSON: update (read → change → write)
# ---------------------------------------------------------
def update_config(path, key, value):
    """
    Wczytaj config, zaktualizuj/dodaj klucz i nadpisz plik.
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    data[key] = value
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    return data

# ---------------------------------------------------------
# 3) TXT: notatnik (dopisz z timestampem + odczyt)
# ---------------------------------------------------------
def save_note(path, text):
    """
    Dopisz linię do pliku w formacie:
    YYYY-MM-DD HH:MM | treść
    """
    t = text.strip()
    if not t:
        raise ValueError("No content")
    line = f"{datetime.now().strftime('%Y-%m-%d %H:%M')} | {t}\n"
    with open(path, "a", encoding="utf-8") as f:
        f.write(line)

def read_notes(path):
    """
    Wczytaj wszystkie linie z pliku i zwróć listę (bez \n).
    """
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    if not lines:
        raise ValueError("No data")
    return lines

# ---------------------------------------------------------
# 4) Main – dwa warianty (wybierz w zależności od zadania)
# ---------------------------------------------------------
if __name__ == "__main__":
    # --- Wariant A: Config ---
    cfg_path = r"pliki_przykladowe/config.json"
    try:
        cfg = load_config(cfg_path)
        k = input("Key: ")
        v = input("Value: ")
        print(update_config(cfg_path, k, v))
    except ValueError as e:
        print(f"Error: {e}")

    # --- Wariant B: Notatnik ---
    notes_path = r"pliki_przykladowe/notes.txt"
    try:
        save_note(notes_path, input("Note: "))
        all_notes = read_notes(notes_path)
        print("\nLAST 3 ENTRIES:")
        for line in all_notes[-3:]:
            print(line)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")

# =========================================================
# 5) TIPY REKRUTACYJNE:
# - Aktualizacja JSON = read → modify dict → write full file
# - load_config zawsze zwraca dict (z pliku albo fallback)
# - update_config dodaje lub nadpisuje klucze
# - Notatnik: append + timestamp, read().splitlines() dla listy
# - Używaj with open(...) as f: → zawsze zamknie plik
# - Raise ValueError gdy dane puste/złe
# - FileNotFoundError obsługuj przez fallback albo komunikat
# =========================================================
