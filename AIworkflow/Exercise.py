lista = []                  # pustą listę
lista.append(1)             # dodaj 1 na koniec -> [1]
lista.extend([2, 3])        # dodaj kilka elementów -> [1, 2, 3]
lista.insert(1, 5)          # wstaw 5 na indeks 1 -> [1, 5, 2, 3]
lista.remove(5)             # usuń pierwsze wystąpienie 5 -> [1, 2, 3]
lista.pop()                 # usuń i zwróć ostatni (3) -> [1, 2]
del lista[0]                # usuń element na indeksie 0 -> [2]
lista.clear()               # usuń wszystko -> []


zbior = set()               # pusty zbiór
zbior.add(5)                # dodaj 5 -> {5}
zbior.update([6, 7])        # dodaj kilka elementów -> {5, 6, 7}
zbior.discard(8)            # usuń 8, jeśli istnieje (bez błędu)
zbior.remove(5)             # usuń 5 (błąd, jeśli nie ma)
zbior.pop()                 # usuń i zwróć losowy element
zbior.clear()               # usuń wszystko -> set()


slownik = {}                # pusty słownik
slownik['a'] = 1            # dodaj klucz 'a' -> {'a': 1}
slownik.update({'b': 2})    # dodaj/zmień kilka par -> {'a': 1, 'b': 2}
wartosc = slownik.pop('a')  # usuń 'a' i zwróć 1 -> {'b': 2}
del slownik['b']            # usuń klucz 'b' -> {}
slownik.clear()             # usuń wszystko -> {}


krotka = ()                 # pusta krotka
krotka = (1, 2)             # krotka z elementami
krotka = krotka + (3,)      # dodanie = nowa krotka (1, 2, 3)
# brak metod dodawania/usuwania – niemutowalna





# Exercise




num22 = [1,2,2,3,4,4,5]
uniqe_num22 = {x for x in num22} # Utworzenie unikalnego zbioru {set}
print(uniqe_num22)
print("-----------------------")

# Wynik: {1, 2, 3, 4, 5}


aa = { x for x in range(20) if x % 2 == 0 }
print(aa)
print("-----------------------")

# Używamy set comprehension - dla każdego x z zakresu (range) sprawdź czy jest parzysta i dodaj do zbioru.
# Wynik: {0, 2, 4, 6, 8, 10, 12, 14, 16, 18}

x = set()
for i in range(20):
    if i % 2 == 0:
        x.add(i)

print(x)
print("-----------------------")

# Tu to samo co ćwiczenie wyżej, ale bez comprehension, tworzymy pusty zbiór set=(), 
# dla każdego i z zakresu range sprawdź czy jest parzysta, jeżeli tak dodaj x.add(i) do zbioru.
# Wynik: {0, 2, 4, 6, 8, 10, 12, 14, 16, 18}


words = ["pythonik", "javusia", "cpluplusik", "turbopisklak"]
words_dict = {word : len(word) for word in words}
print(words_dict)
print("-----------------------")


# Zrób słownik, gdzie kluczem jest słowo, wartością długośc słowa (word:len(word)) dla każdego słowa w liście słów...
# Wynik: {'pythonik': 8, 'javusia': 7, 'cpluplusik': 10, 'turbopisklak': 12}


xx = [1,2,3,4,5]
xx_dict = {i : i**3 for i in xx if i>2}
print(xx_dict)
print("-----------------------")


# Utwórz słownik, w którym kluczem jest liczba, 
# a wartością jest jej sześcian (liczba do potęgi 3), 
# tylko dla liczb większych od 2
# # Wynik: {3: 27, 4: 64, 5: 125}


s = {"a": 1, "b": 2, "c": 3}
k = {val: key for key, val in s.items()}
print(k)
print("-----------------------")


# Metoda s.items() zwraca widok par (klucz, wartość) w postaci krotek [("a",1),("b",2),("c",3)]
# Dzięki temu możemy po nich iterować i w każdej iteracji dostać key i val.
# { stary_klucz: nowa_wartość for stary_klucz, stara_wartość in s.items() }
# nowym kluczem jest val (czyli stara wartość)
# starą wartością jest key (czyli stary klucz)
# Klucze i wartości zostały zamienione miejscami:
# Wynik: {1: 'a', 2: 'b', 3: 'c'}
















"""
name = "Robert"
age = 43
height = 1.83
print(type(name), type(age), type(height))
print("-----------------------")


w = int(input("Podaj liczbę "))
print(w+5)
print("-----------------------")


i = int(input("podaj liczbę "))
if i > 0:
    print("Dodatnia")
elif i < 0:
    print("ujemna")
elif i == 0:
    print("zero")


for i in range(1,11):
    print(i)


password = "python1234"
while True:
    inn = input("podaj hasło ")
    if inn != password:                 # Tak ma być, ćwiczenie nakazuje zapętlenie dopóki inn = true
        print("Incorect!")
    
    else:
        print("Zalogowano!")
        break
"""



menu_d = ["zrazy", "gołąbki", "żurek", "burger", "karkówka"]
print(menu_d[0])                        # Pierwszy element listy, bez użycia slicingu który zwraca podlisty
print(menu_d[-1])                       # Pierwszy od końca, czyli ostatni ;), bez użycia slicingu, który zwraca podlisty.



lista = [1,2,3,4,5,6,7,8,9,10]
print(lista[:3])                        # Sliing - pierwsze 3 elementy
print(lista[-3:])                       # Ostatnie 3 elementy
print(lista[::2])                       # Co drugi element


ll = [1,2,3,4,5]
print(ll)

ll[1:3] = [20,30,40]                    # Zmiana indexów od 1 do 3 na inna listę.
print(ll)                               # Wynik: [1, 20, 30, 40, 4, 5]


q = [x**2 for x in range(1,6)]
print(q)


w = [x for x in range(1,21) if x % 2 ==0]
print(w)

ss = ["Python","java", "javascript", "php"]
s = {char[0] for char in ss }            # char[0] zwróci pierwszy znak z każdego słowa (for char in ss)
print(s)                                 # dlaczego nie char[1:]? slicing zwróci nie znak tylko łańcuch jednoznakowy.
                                         # Wynik {'p', 'P', 'j'} - znaki zdublowanie nie są wyświetlane.


l = [1,2,3,4]
square = {x: x**2 for x in l}            # Kluczem jest liczba, wartością kwadrat tej liczby
print(square)                            # Wynik: {1: 1, 2: 4, 3: 9, 4: 16}





suma = 0 
x = [int(x.strip()) for x in input("podaj 5 cyfr oddzielonych przecinkami :").split(",")]
# srednia = sum(x) /len(x)   # tu bez pętli możemy obliczyć średnią, korzystając z wbudowanych funkcji sum() i len()               
for i in x:
    suma += i

y = len(x)
srednia = suma / y
print(srednia)

#  Program liczy średnią arytmetyczną z liczb podanych przez użytkownika w jednej linii.
# Krok po kroku:
# 1. Tworzymy zmienną suma = 0 (akumulator do dodawania liczb).
# 2. Pobieramy od użytkownika dane: np. "10, 20, 30, 40, 50".
#    - input() zwraca tekst, split(",") rozdziela go po przecinkach -> ["10", " 20", ...].
#    - x.strip() usuwa spacje, int(...) zamienia tekst na liczbę.
#    - List comprehension [int(x.strip()) for x in ...] tworzy listę liczb całkowitych.
# 3. W pętli for dodajemy każdą liczbę do zmiennej suma.
# 4. Funkcja len(x) liczy, ile liczb podał użytkownik (y).
# 5. srednia = suma / y oblicza średnią.
# 6. print(srednia) wyświetla wynik.



words_one = ["kot", "pies", "koń", "kot", "pies"]
uniq_words = set(words_one)                 # Wynik: {'kot', 'pies', 'koń'}
print(uniq_words)
s_one = {x : len(x) for x in words_one}     # Wynik: {'kot': 3, 'pies': 4, 'koń': 3}
print(s_one)

# Program pokazuje pracę ze zbiorami (set) i słownikami (dict) w Pythonie.
# Krok po kroku:
# 1. Tworzymy listę words_one z kilkoma słowami, niektóre się powtarzają.
# 2. uniq_words = set(words_one)
#    - set() tworzy zbiór: usuwa duplikaty i zwraca unikalne elementy -> {'kot', 'pies', 'koń'}.
# 3. print(uniq_words) wyświetla zbiór.
# 4. s_one = {x: len(x) for x in words_one}
#    - To tzw. dict comprehension: dla każdego słowa (x) twórz parę klucz:wartość,
#      gdzie klucz to słowo, a wartość to długość słowa (len(x)).
#    - Wynik: {'kot': 3, 'pies': 4, 'koń': 3}.
# 5. print(s_one) wyświetla słownik.
