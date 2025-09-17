# =========================================================
# PYTHON CHEAT SHEET: CO ZWRACA FUNKCJA / METODA
# Junior Ready – najważniejsze rzeczy
# =========================================================

# -------------------------------
# Wbudowane funkcje (built-ins)
# -------------------------------
print(type(len([1,2,3])))       # int
print(type(sum([1,2,3])))       # int (lub float, zależy od danych)
print(type(max([1,2,3])))       # element z kolekcji (np. int)
print(type(min([1,2,3])))       # element z kolekcji
print(type(range(5)))           # range (iterowalny obiekt)
print(type(list(range(5))))     # list
print(type(sorted([3,1,2])))    # list
print(type(any([0, 1, 0])))     # bool
print(type(all([1, 2, 3])))     # bool
print(type(zip([1,2], [3,4])))  # zip object (iterowalny) → można list(zip(...)) = lista tupli
print(type(map(str, [1,2,3])))  # map object (iterowalny)
print(type(filter(None, [0,1])))# filter object (iterowalny)

# Konwersje typów
print(type(int("123")))         # int
print(type(float("12.3")))      # float
print(type(str(123)))           # str
print(type(list("abc")))        # list (['a','b','c'])
print(type(set([1,2,2])))       # set
print(type(dict([("a",1),("b",2)]))) # dict

# -------------------------------
# Stringi (str)
# -------------------------------
s = "Ala ma kota"
print(type(s.split()))          # list[str]
print(type(s.strip()))          # str
print(type(s.lower()))          # str
print(type(s.upper()))          # str
print(type(s.replace("Ala","Ola"))) # str
print(type(s.find("ma")))       # int (-1 jeśli nie znajdzie)
print(type(s.startswith("Ala")))# bool
print(type(s.endswith("kot")))  # bool
print(type(s.join(["a","b"])))  # str → "aXb" jeśli X to separator
print(type(s.format(x=5)))      # str

# -------------------------------
# Listy (list)
# -------------------------------
lst = [1,2,3]
print(type(lst.append(4)))      # None (uwaga: modyfikuje w miejscu!)
print(type(lst.extend([5,6])))  # None (modyfikuje w miejscu)
print(type(lst.insert(0, 10)))  # None
print(type(lst.pop()))          # element (np. int)
print(type(lst.remove(2)))      # None (usuwa pierwszy znaleziony element)
print(type(lst.index(3)))       # int (pozycja elementu)
print(type(lst.count(3)))       # int
print(type(lst.sort()))         # None (sortuje w miejscu)
print(type(sorted(lst)))        # list (nowa posortowana lista)
print(type(lst.reverse()))      # None
print(type(lst.copy()))         # list (płytka kopia)

# -------------------------------
# Sety (set)
# -------------------------------
a = {1,2,3}
b = {3,4,5}
print(type(a.union(b)))         # set
print(type(a.intersection(b)))  # set
print(type(a.difference(b)))    # set
print(type(a.add(10)))          # None (modyfikuje w miejscu)
print(type(a.remove(1)))        # None (błąd jeśli brak elementu)
print(type(a.discard(1)))       # None (bez błędu)
print(type(a.pop()))            # element (np. int)
print(type(a.copy()))           # set

# -------------------------------
# Dictionary (dict)
# -------------------------------
d = {"a":1,"b":2}
print(type(d.keys()))           # dict_keys (iterowalny)
print(type(list(d.keys())))     # list
print(type(d.values()))         # dict_values (iterowalny)
print(type(list(d.values())))   # list
print(type(d.items()))          # dict_items (iterowalny)
print(type(list(d.items())))    # list[tuple]
print(type(d.get("a")))         # wartość lub None
print(type(d.update({"c":3})))  # None (modyfikuje w miejscu)
print(type(d.pop("a")))         # element (np. int)
print(type(d.popitem()))        # tuple (klucz,wartość)
print(type(d.copy()))           # dict

# -------------------------------
# Pliki (file objects)
# -------------------------------
with open("plik.txt","w",encoding="utf-8") as f:
    print(type(f.write("ala"))) # int (liczba zapisanych znaków)

with open("plik.txt","r",encoding="utf-8") as f:
    print(type(f.read()))       # str (cała zawartość)
with open("plik.txt","r",encoding="utf-8") as f:
    print(type(f.readlines()))  # list[str] (linie ze znakiem \n)
with open("plik.txt","r",encoding="utf-8") as f:
    print(type(f.read().splitlines())) # list[str] (linie bez \n)

# -------------------------------
# JSON
# -------------------------------
import json
cfg = {"user":"Robert"}
with open("config.json","w",encoding="utf-8") as f:
    json.dump(cfg,f)            # None (zapis do pliku)

with open("config.json","r",encoding="utf-8") as f:
    print(type(json.load(f)))   # dict (wczytuje z pliku)

raw = '{"user":"Robert"}'
print(type(json.loads(raw)))    # dict (wczytuje ze stringa)
print(type(json.dumps(cfg)))    # str (konwertuje dict → JSON string)

# =========================================================
# TIPY:
# - Wszystko co modyfikuje w miejscu (append, sort, update, add) → zwraca None.
# - Funkcje typu "get, find, index, count" → zwracają konkretną wartość (int, bool, str).
# - Wbudowane konwersje (int(), str(), list(), set(), dict()) → zwracają nowy obiekt.
# - Plik.write() zawsze zwraca int (ile znaków zapisano).
# - JSON: load/load*s* → dict lub list, dump/dump*s* → None lub str.
# =========================================================
