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





# SLICE ASSIGNMENT




print("-----------------------")    
nums = [10,20,30,40,50,60,70]
nums[1:1] = [1,2,3]                 # Dodawanie dokładnie miedzy index 0 a 1 nowej listy
print(nums)
print("-----------------------")
nums[3:4] = [5,5,5,5]               # Podmień index nr 3 i wstaw listę, przesuwając resztę w prawo
print(nums)
print("-----------------------")
nums[0:7] = []                      # Podmień indexy od 0 do 6! na pustą liste, czyli wykasuj ;P
print(nums)
print("-----------------------")
nums = [10,20,30,40,50,60,70]
nums2 = nums[:]                     # Płytka kopia(SHALLOW COPY), UWAGA tworzy nową listę, ale zawartość patrzy na starą listę!
print(nums2)                        # Jeżeli płytka kopia listy zawiera zagnieżdżone elementy typu lista w liscie, słowniki w liście 
                                    # to operacje na tych zmiennych dotyczą także oryginału, to jest b. ważne!!!




# LIST COMPREHENSION




x = [1,2,3,4,5]
squares = [i**2 for i in x]         # potęga i pętla w jednym wyrażeniu, dla każdego elementu i w kolekcji x wykonaj potęgowanie i dodaj do listy.
print(squares)
print("-----------------------")
even_num = [i for i in x if i % 2==0]   # Przejdź po każdym elemencie i w kolekcji x i wybierz tylko te elementy (i) które są parzyste
print(even_num)
print("-----------------------")
print("-----------------------")

nums = list(range(10))
three = [ i for i in nums if i % 3 == 0] # Przejdź po kązdym elemnie z listy nums i wybierz tylko nieparzyste (i%3==0)
print(three)
print("-----------------------")
print("-----------------------")

test = "abrakadabra"
no_a = [char for char in test if char != "a" ] # Przechodzimy po każdym znaku ze stringa, 
print(no_a)                                    # sprawdzamy czy znak nie jest "a",
                                               # jeżeli warunek spełniony, zapisujemy do listy.
print("-----------------------")
print("-----------------------")


temperatures_c = [0, 10, 20, 30]
temperatures_f = [ (i * 9/5) +32 for i in temperatures_c] # Dla każdego elementu z listy temperatures_c 
print(temperatures_f)                                     # wykonaj przeliczenie na Fahrenheita (według wzoru C * 9/5 + 32) i utwórz z tego nową listę.
print("-----------------------")
print("-----------------------")

matrix = [[1,2],[3,4],[5,6],[7,8]]
flat_matrix = [num for row in matrix for num in row]
print(flat_matrix)
print("-----------------------")
print("-----------------------")

# "for row in matrix" - weź kolejny wiersz (listę liczb)
# "for num i row" - weź każdy element z tego wiersza
# "num" dodaj do nowej list
# Dla każdego wiersza w macierzy, a w każdym wierszu dla każdego elementu, dodaj ten element do listy flat_matrix 
# Wynik: [1, 2, 3, 4, 5, 6, 7, 8]




# SET COMPREHENSION





numbers = [1,22,3,4,4,5,5,6,8,9,9,9,2,2,2,31,31,36,36]
unq_numbers = {x for x in numbers}
print(unq_numbers)
print("-----------------------")
print("-----------------------")

# "x for x in numbers" - pętla przechodząca po elemantach numbers
# {} - zapis tworzący zbiór (set)
# Wynik: {1, 2, 3, 4, 5, 6, 36, 8, 9, 22, 31}




# DICTIONARY COMPREHENSION




numbers_1 = [1,2,3,4,5,6,6,6]
square_num = {x: x**2 for x in numbers_1}
print(square_num)
print("-----------------------")
print("-----------------------")

# {x : x**2 for x in numbers_1} klucz to liczba x, wartość to jej kwadrat
# Wynik: {1: 1, 2: 4, 3: 9, 4: 16, 5: 25, 6: 36}


qq = [0,1,2,3,2,5,4,1,3,6,7]
filtered_qq = {x: x**2 for x in qq if x > 2}
print(filtered_qq)
print("-----------------------")
print("-----------------------")

# {x:x**2 for x in qq if x>2} Filtr, który zakłada kwadrat tylko dla liczb większych od 2
# Wynik: {3: 9, 5: 25, 4: 16, 6: 36, 7: 49}




# ODWRACANIE WARTOŚCI W SŁOWNIKU




original = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
reversed_dict = {value: key for key, value in original.items()}
print(reversed_dict)
print("-----------------------")
print("-----------------------")

# value: key - zamiana miejscami
# original.items() - metoda zwracająca pary (klucz: wartość) słownika
# Wynik: {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'}





# FIBONACCI SEQUENCE

x = 1                                   # Ustawiamy x, y początkowe. Y będziemy dodawać do listy 
y = 0
fib_list = []
n = range(0,10)
for _ in n:
    fib_list.append(y)                  # Dokładam bieżący element ciagu do listy
    tmp = x + y                         # Policz następną liczbę: suma dwóch poprzednich 
    x = y                               # Przesuń okno: poprzednie x staje sie nowym y
    y = tmp                             # Nowe y to wyliczona suma
    
print(fib_list)
print("-----------------------")




# Excercise


num22 = [1,2,2,3,4,4,5]
uniqe_num22 = {x for x in num22} # Utworzenie unikalnego zbioru {set}
print(uniqe_num22)
print("-----------------------")




aa = { x for x in list(range(20)) if x % 2 == 0 }
print(aa)

x = set()
for i in range(20):
    if i % 2 == 0:
        x.add(i)

print(x)