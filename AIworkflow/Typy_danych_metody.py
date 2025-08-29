# ====================================
# PYTHON – PODSTAWOWE TYPY DANYCH I ICH METODY
# ====================================

# ==============================
# LISTA (LIST)
# ==============================
lista = []                  # pustą listę
lista.append(1)             # dodaj 1 na koniec -> [1]
lista.extend([2, 3])        # dodaj kilka elementów -> [1, 2, 3]
lista.insert(1, 5)          # wstaw 5 na indeks 1 -> [1, 5, 2, 3]
lista.remove(5)             # usuń pierwsze wystąpienie 5 -> [1, 2, 3]
lista.pop()                 # usuń i zwróć ostatni (3) -> [1, 2]
del lista[0]                # usuń element na indeksie 0 -> [2]
lista.clear()               # usuń wszystko -> []


# ==============================
# ZBIÓR (SET)
# ==============================
zbior = set()               # pusty zbiór
zbior.add(5)                # dodaj 5 -> {5}
zbior.update([6, 7])        # dodaj kilka elementów -> {5, 6, 7}
zbior.discard(8)            # usuń 8, jeśli istnieje (bez błędu)
zbior.remove(5)             # usuń 5 (błąd, jeśli nie ma)
zbior.pop()                 # usuń i zwróć losowy element
zbior.clear()               # usuń wszystko -> set()


# ==============================
# SŁOWNIK (DICT)
# ==============================
slownik = {}                        # pusty słownik
slownik['a'] = 1                    # dodaj klucz 'a' -> {'a': 1}
slownik.update({'b': 2})            # dodaj/zmień kilka par -> {'a': 1, 'b': 2}
wartosc = slownik.pop('a')          # usuń 'a' i zwróć 1 -> {'b': 2}
del slownik['b']                    # usuń klucz 'b' -> {}
slownik.clear()                     # usuń wszystko -> {}

# --- dodatkowe metody MUST-HAVE ---
slownik = {"a": 1, "b": 2}
print(slownik.get("a"))             # bezpieczne pobranie -> 1
print(slownik.get("c"))             # brak klucza -> None (bez błędu)
print(slownik.get("c", 0))          # brak klucza -> zwraca wartość domyślną 0

print(slownik.keys())               # dict_keys(['a', 'b']) -> lista kluczy
print(slownik.values())             # dict_values([1, 2]) -> lista wartości
print(slownik.items())              # dict_items([('a', 1), ('b', 2)]) -> pary (klucz, wartość)

for k, v in slownik.items():        # typowa pętla po parach
    print(k, v)                     # a 1 / b 2

slownik2 = slownik.copy()           # płytka kopia słownika
print("a" in slownik)               # sprawdzenie, czy klucz istnieje -> True


# ==============================
# KROTKA (TUPLE)
# ==============================
krotka = ()                         # pusta krotka
krotka = (1, 2)                     # krotka z elementami
krotka = krotka + (3,)              # dodanie = nowa krotka (1, 2, 3)
# brak metod dodawania/usuwania – niemutowalna


# ==============================
# STRING (STR)
# ==============================
tekst = "  Hello Python  "

print(tekst.upper())        # HELLO PYTHON -> wszystkie litery na wielkie
print(tekst.lower())        # hello python -> wszystkie litery na małe
print(tekst.strip())        # "Hello Python" -> usuwa spacje z początku i końca
print(tekst.lstrip())       # "Hello Python  " -> usuwa tylko z lewej
print(tekst.rstrip())       # "  Hello Python" -> usuwa tylko z prawej

print(tekst.replace("Python", "World"))  # "  Hello World  " -> zamiana fragmentu tekstu

print(tekst.split())        # ['Hello', 'Python'] -> domyślnie dzieli po spacji
print("a,b,c".split(","))   # ['a', 'b', 'c'] -> dzielenie po przecinku

lista = ["a", "b", "c"]
print("-".join(lista))      # "a-b-c" -> łączenie listy w string

print(tekst.startswith("  He"))   # True -> sprawdza początek stringa
print(tekst.endswith("on  "))     # True -> sprawdza koniec stringa

print("Python".find("th"))  # 2 -> indeks pierwszego wystąpienia
print("Python".find("zz"))  # -1 -> jeśli nie znajdzie

print(len(tekst))           # długość stringa -> 15
print("y" in "Python")      # True -> sprawdza, czy znak występuje
print("z" not in "Python")  # True -> sprawdza brak znaku
