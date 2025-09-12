# ============================================
# 1. Suma liczb dodatnich
# Napisz funkcję, która przyjmuje listę liczb.
# Zwróć sumę tylko tych liczb, które są dodatnie.
# Użyj list comprehension.
# TODO

def positive_sum(numbers):
    if not numbers:
        return ValueError("Pusta lista")
    return sum(x for x in numbers if x >= 0)


numbers = [1,2,3,-5,-6,-2,4,5]
print(positive_sum(numbers))

print("="*40)


# ============================================

# ============================================
# 2. Parzysta czy nieparzysta
# Funkcja przyjmuje liczbę. Jeśli jest ujemna → raise ValueError.
# Jeśli >= 0, zwróć napis "parzysta" albo "nieparzysta".
# TODO

def wtf_numer(a):
    if a is None:
        raise ValueError("Brak liczby")
    elif a < 0:
        raise ValueError("liczba ujemna")
    elif a % 2 == 0:
        return ("Parzysta")
    else:
        return ("Nieparzysta")

try:
    print(wtf_numer(0))
except ValueError as e:
    print(f"Błąd: {e}")

print("="*40)


# ============================================

# ============================================
# 3. Zapis do pliku TXT
# Funkcja przyjmuje string i zapisuje go do pliku "output.txt".
# Jeśli string pusty → raise ValueError.
# TODO


def write_to_file(path, line):
    if not line:
        raise ValueError("Pusty tekst")
    with open(path, "w", encoding="utf-8") as f:
        f.write(line)
try:
    line = "Przykładowy tekst\n"
    write_to_file("Files_samples/output.txt", line)
    print("Zapis do pliku udany.")
except ValueError as e:
    print(f"Bład: {e}")



print("="*40)



# ============================================

# ============================================
# 4. Odczyt z pliku TXT
# Funkcja wczytuje zawartość pliku "output.txt".
# Jeśli plik nie istnieje → obsłuż wyjątek.
# Jeśli plik pusty → raise ValueError.
# TODO

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

        if not content:
            raise ValueError("plik pusty")
        return content
    
try:
    print(read_file("Files_samples/output.txt"))
except FileNotFoundError:
    print("Brak pliku")
except ValueError as e:
    print(f"Błąd: {e}")


print("="*40)





# ============================================

# ============================================
# 5. JSON – zapis konfiguracji
# Funkcja zapisuje słownik {"user": ..., "lang": ...} do pliku config.json.
# Jeśli słownik nie ma klucza "user" → raise KeyError.
# TODO
import json

def write_dict(path, data):
    if "user" not in data:
        raise KeyError("Brak klucza 'user' ")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
data = {"user": "Robert", "lang": "PL", "age": 43}
try:
    write_dict("Files_samples\config.json", data)
    print("Zapisano config.json")
except (KeyError, ValueError) as e:
    print(f"Błąd: {e}")
except FileNotFoundError as e:
    print(f"Brak pliku, wystąpił błąd: {e}")













print("="*40)

# ============================================

# ============================================
# 6. JSON – odczyt konfiguracji
# Funkcja otwiera plik config.json i wczytuje dane do słownika.
# Obsłuż: brak pliku, pusty plik, błędny JSON.
# TODO
import json

def read_json_file(path):
    with open(path, "r", encoding="utf-8") as f:
        raw_content = f.read()
        if not raw_content:
            raise ValueError("Plik pusty")
        try:
            parsed_data = json.loads(raw_content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Błędne dane w pliku, bład: {e}")
        return parsed_data
    
try:
    print("Plik wczytano poprawnnie: ")
    print(read_json_file(r"Files_samples\config.json"))
except FileNotFoundError:
    print("Pliku nie zanleziono")
except ValueError as e:
    print(f"Błąd: {e}")





print("="*40)

# ============================================

# ============================================
# 7. Najdłuższe słowo
# Funkcja przyjmuje listę stringów i zwraca najdłuższy element.
# Jeśli lista pusta → raise ValueError.
# Wykorzystaj wbudowaną funkcję max() z parametrem key=len.
# TODO





print("="*40)

# ============================================

# ============================================
# 8. Funkcja anonimowa (lambda)
# Utwórz lambdę, która przyjmuje liczbę i zwraca jej kwadrat.
# Przetestuj ją na kilku liczbach za pomocą map().
# TODO





print("="*40)

# ============================================

# ============================================
# 9. Filtrowanie liczb
# Funkcja przyjmuje listę liczb i zwraca nową listę z tylko parzystymi.
# Użyj funkcji filter() + lambdy.
# TODO






print("="*40)

# ============================================

# ============================================
# 10. Generator haseł
# Funkcja tworzy losowe hasło o zadanej długości.
# Użyj modułu random.choice i string.ascii_letters + digits.
# Jeśli długość < 4 → raise ValueError.
# Zapisz wygenerowane hasło do pliku "password.txt".
# TODO








print("="*40)

# ============================================
