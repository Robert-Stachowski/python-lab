# =========================================================
# PYTHON GOOD PRACTICES CHECKLIST
# =========================================================

# 1. Pliki
# ✅ ZAWSZE używaj konstrukcji with open(...) as f:
#    → plik zamknie się automatycznie, nawet gdy poleci wyjątek
# ❌ Nigdy nie rób open(...) bez zamykania, ani json.dump(..., open(...))

# 2. Obsługa wyjątków
# ✅ Konkretne except: except ValueError, except FileNotFoundError
# ❌ Nigdy nie używaj: except: (goły except łapie WSZYSTKO)
# ✅ W razie potrzeby: except Exception as e: → tylko gdy świadomie chcesz złapać wszystkie

# 3. Funkcje
# ✅ Nazwy parametrów OGÓLNE (np. path, data, numbers, text)
# ✅ Nazwy zmiennych w main KONKRETNE (np. user_file, note_text, random_nums)
# ❌ Nie nadpisuj parametrów wewnątrz funkcji (np. text = f.write(...))

# 4. Walidacja danych
# ✅ Zawsze sprawdzaj dane wejściowe (input, plik, config)
#    → raise ValueError albo zwróć pusty wynik z jasnym komunikatem
# ✅ Walidacja na początku funkcji, logika dopiero potem

# 5. Print / return
# ✅ Funkcje mają ZWRACAĆ wynik (return), a nie drukować
#    (print używamy w main/testach)
# ❌ Nie mieszaj printów i return w tej samej funkcji

# 6. JSON / Config
# ✅ f.read() + json.loads() → gdy musisz sprawdzić pusty plik
# ✅ json.load(f) → gdy wystarczy od razu sparsować poprawny plik
# ❌ Nie zapisuj JSON-a bez indent (indent=4 → lepsza czytelność)

# 7. Style i konwencje
# ✅ snake_case dla zmiennych i funkcji: my_variable, load_config
# ✅ Używaj 4 spacji jako wcięcia (PEP8)
# ✅ Komentarze # TODO dla zadań / brakujących fragmentów

# 8. Inne pułapki
# ❌ Nigdy nie przechowuj pustego seta jako {} (to dict!)
# ✅ Pusty set tworzysz przez set()
# ✅ Do debugowania używaj repr(), żeby zobaczyć znaki specjalne (\n)

# 9. Zasada SRP (Single Responsibility Principle)
# ✅ Funkcja powinna robić jedną rzecz dobrze
# ✅ Obsługa wyjątków (try/except) zwykle w main,
#    a funkcje mają tylko zgłaszać raise

# 10. Git / Commit
# ✅ Commit message po angielsku, w czasie teraźniejszym
#    np. Add save_note and read_notes functions with error handling
