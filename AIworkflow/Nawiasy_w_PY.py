# =========================================================
# ŚCIĄGA: NAWIASY W PYTHONIE — FULL
# Data: 2025-09-16
#
# SPIS TREŚCI:
#  1. Nawiasy okrągłe () — wywołania, argumenty, grupowanie
#  2. Nawiasy kwadratowe [] — indeksowanie, slicing, listy
#  3. Nawiasy klamrowe {} — słowniki (dict) i zbiory (set)
#  4. Łączenie nawiasów (dict funkcji → wywołanie)
#  5. Comprehension: list / set / dict
#  6. Tuple (krotki) — przecinki, 1-elementowe, rozpakowywanie
#  7. *args i **kwargs — definicja i wywołanie
#  8. Generator () vs Lista [] — pamięć i „leniwość”
#  9. Pusty set: set() vs {} — częsta pułapka
# 10. Zagnieżdżone indeksowanie i łańcuchy wywołań
# 11. „Wywoływalność” (callable) i kiedy dodawać ()
# 12. operator.* jako alternatywa dla „mapy funkcji”
# 13. Dodatkowe różnice: dict.get, slicing, return krotki
#
# Skrót:
#  () → wywołania, argumenty, grupowanie, tuple/generator
#  [] → indeksowanie, slicing, listy, dostęp do klucza w dict
#  {} → dict/set (UWAGA: {} to pusty dict; pusty set = set())
# =========================================================


# ----------------------------
# 1) Nawiasy okrągłe ( )
# ----------------------------
# Używamy ich do: wywoływania funkcji/metod, tworzenia obiektów (instancji klas),
# przekazywania argumentów oraz grupowania działań.

def add(a, b):                       # definicja funkcji: argumenty też w ()
    return a + b

print(add(2, 3))                     # () → wywołanie funkcji z argumentami 2 i 3

text = "python"                      # zwykły string
print(text.upper())                  # () → wywołanie metody .upper() na obiekcie string

class Dog:                           # definicja klasy
    pass

my_dog = Dog()                       # () → wywołanie klasy = utworzenie instancji (obiekt)
x = (2 + 3) * 4                      # () → grupowanie działań arytmetycznych
print(x)                             # 20


# ----------------------------
# 2) Nawiasy kwadratowe [ ]
# ----------------------------
# Używamy ich do: indeksowania, slicing i tworzenia list (literal listy).

lista = [10, 20, 30]                 # [] → tworzenie listy
print(lista[0])                      # [] → indeks 0 → 10

print(lista[1:3])                    # [start:stop] (stop nie włącznie) → [20, 30]
print(lista[::-1])                   # [::step] z krokiem -1 → odwrócona lista

slownik = {"user": "Robert", "level": "junior"}   # {} → słownik (literal dict)
print(slownik["user"])               # [] → dostęp do wartości po kluczu "user"

napis = "python"                     # łańcuch znaków
print(napis[2])                      # [] → indeksowanie stringa → 't'


# ----------------------------
# 3) Nawiasy klamrowe { }
# ----------------------------
# Używamy ich do: tworzenia słowników (dict) oraz zbiorów (set).

slownik = {"a": 1, "b": 2}           # {} → dict z parami klucz:wartość
print(slownik["a"])                  # [] → dostęp do wartości po kluczu 'a'

zbior = {1, 2, 3, 3}                 # {} → set (zbiory usuwają duplikaty)
print(zbior)                         # {1, 2, 3}


# ----------------------------
# 4) Łączenie nawiasów (dispatch table)
# ----------------------------
# Słownik z funkcjami + natychmiastowe wywołanie pobranej funkcji.

slownik_funkcji = {                  # {} → słownik „operator” → funkcja
    "+": add,                        # wartość to referencja do funkcji (bez ())
}
wynik = slownik_funkcji["+"](5, 7)   # [] → pobranie funkcji; () → jej wywołanie
print(wynik)                         # 12


# ----------------------------
# 5) Comprehension: list / set / dict
# ----------------------------
# Jednolinijkowe tworzenie kolekcji.

lista_kwadratow = [x**2 for x in range(5)]   # [] → list comprehension
print(lista_kwadratow)                       # [0, 1, 4, 9, 16]

zbior_kwadratow = {x**2 for x in range(5)}   # {} → set comprehension
print(zbior_kwadratow)                       # {0, 1, 4, 9, 16}

slownik_kwadratow = {x: x**2 for x in range(5)}   # {} → dict comprehension
print(slownik_kwadratow)                          # {0:0, 1:1, 2:4, 3:9, 4:16}


# ----------------------------
# 6) Tuple (krotki) — przecinki są kluczowe
# ----------------------------
# Krotka to niezmienna sekwencja. Ważne: 1-elementowa krotka wymaga przecinka.

t1 = (1, 2, 3)                     # klasyczna krotka z nawiasami
print(t1)                          # (1, 2, 3)

t2 = 1, 2, 3                       # bez nawiasów też OK (liczą się przecinki)
print(t2)                          # (1, 2, 3)

t_single_wrong = (1)               # to NIE krotka — brak przecinka → zwykłe int 1
print(type(t_single_wrong))        # <class 'int'>

t_single = (1,)                    # 1-elementowa krotka → przecinek wymagany
print(type(t_single))              # <class 'tuple'>

a, b, c = t1                       # rozpakowywanie krotki pozycjami
print(a, b, c)                     # 1 2 3

x, *mid, y = (10, 20, 30, 40, 50)  # gwiazdka „zbiera resztę” do listy
print(x, mid, y)                   # 10 [20, 30, 40] 50


# ----------------------------
# 7) *args i **kwargs — definicja i wywołanie
# ----------------------------
def demo_args(*args, **kwargs):    # *args → krotka argumentów pozycyjnych; **kwargs → dict nazwanych
    print("args =", args)          # np. (1, 2, 3)
    print("kwargs =", kwargs)      # np. {'sep': ' - '}

demo_args(1, 2, 3, sep=" - ")      # () → wywołanie; mieszamy pozycyjne i nazwane

def add2(a, b):                    # prosta funkcja do pokazania rozpakowywania
    return a + b

pair = (5, 7)                      # krotka z dwoma liczbami
print(add2(*pair))                 # *pair rozpakowuje do add2(5, 7) → 12

params = {"a": 2, "b": 9}          # dict odpowiadający nazwom parametrów
print(add2(**params))              # **params → add2(a=2, b=9) → 11


# ----------------------------
# 8) Generator () vs Lista []
# ----------------------------
# Generator „produkuje” wartości na żądanie (oszczędza pamięć).
# Lista tworzy wszystkie wartości od razu.

lst = [x * x for x in range(5)]    # [] → lista
print(lst)                         # [0, 1, 4, 9, 16]

gen = (x * x for x in range(5))    # () → generator expression
print(gen)                         # <generator object ...>
print(sum(gen))                    # zużywamy generator (po tym jest „pusty”) → 30


# ----------------------------
# 9) Pusty set — uwaga na {}
# ----------------------------
empty_curly = {}                   # {} → to PUSTY DICT, nie set!
print(type(empty_curly))           # <class 'dict'>

empty_set = set()                  # pusty set tworzymy przez set()
print(type(empty_set))             # <class 'set'>

non_empty_set = {1, 2, 2, 3}       # set usuwa duplikaty
print(non_empty_set)               # {1, 2, 3}


# ----------------------------
# 10) Zagnieżdżone indeksowanie i łańcuchy wywołań
# ----------------------------
data = {
    "users": [
        {"name": "Robert", "skills": ["Python", "Git"]},
        {"name": "Ala",    "skills": ["SQL", "Django"]}
    ]
}                                  # {} + [] na zmianę: dict z listą dictów i listami w środku

skill = data["users"][0]["skills"][1]  # [] → klucz „users” → indeks 0 → klucz „skills” → indeks 1
print(skill)                        # Git

text2 = "  hello, world  "          # string z nadmiarowymi spacjami
clean = text2.strip().upper().split(",")  # () łańcuch wywołań metod; split → zwraca listę
print(clean)                        # ['HELLO', ' WORLD']
first_part = clean[0]               # [] → indeks 0 listy
print(first_part)                   # HELLO


# ----------------------------
# 11) „Wywoływalne” i nawiasy ()
# ----------------------------
def foo():                          # zwykła funkcja
    return "OK"

print(foo)                          # bez () → sama referencja do funkcji (nie wywołujemy)
print(foo())                        # z () → wynik wywołania → "OK"

print(callable(foo))                # True → obiekt da się wywołać
print(callable(123))                # False → liczba nie jest wywoływalna


# ----------------------------
# 12) operator.* jako alternatywa dla „mapy funkcji”
# ----------------------------
import operator                     # moduł z funkcyjnymi odpowiednikami operatorów

op_map = {                          # {} → dict symbol → funkcja
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "**": operator.pow,
}
print(op_map["+"](3, 4))            # [] pobiera funkcję, () ją wywołuje → 7
print(op_map["**"](2, 5))           # 32


# ----------------------------
# 13) Dodatkowe różnice i pułapki
# ----------------------------
# a) dict.get vs indeksowanie — zachowanie, gdy klucza brak
user = {"name": "Robert"}           # słownik z jednym kluczem
# print(user["age"])                # KeyError (brak klucza)
print(user.get("age"))              # None (bez wyjątku)
print(user.get("age", 0))           # 0 (wartość domyślna, jeśli „age” nie istnieje)

# b) Slicing na stringu i liście
s = "abcdef"
print(s[1:4])                       # 'bcd' (indeksy 1..3)
print(s[:3])                        # 'abc'  (od początku)
print(s[3:])                        # 'def'  (do końca)
print(s[::-1])                      # 'fedcba' (odwrócony string)

nums = [10, 20, 30, 40, 50]
print(nums[::2])                    # [10, 30, 50] (co drugi element)

# c) Return krotki: przecinki decydują, nie nawiasy
def pair():
    return 1, 2                     # krotka dzięki przecinkowi
print(pair())                       # (1, 2)

def pair2():
    return (1, 2)                   # jawne nawiasy, efekt identyczny
print(pair2())                      # (1, 2)


# =========================================================
# PODSUMOWANIE KOŃCOWE:
#  • () używaj do WYWOŁAWANIA (funkcji/metod/klas), przekazywania argumentów i grupowania działań.
#  • [] używaj do INDEKSOWANIA i SLICINGU oraz tworzenia LIST.
#  • {} używaj do tworzenia DICT i SET (pusty set → set()).
#  • Tuple: decydują PRZECINKI (1-elementowa: (x,)).
#  • * / **: rozpakowywanie przy wywołaniu; w definicji *args/**kwargs „zbierają” argumenty.
#  • Generator ( ) jest „leniwy” (oszczędza pamięć) w odróżnieniu od listy [ ].
# =========================================================
