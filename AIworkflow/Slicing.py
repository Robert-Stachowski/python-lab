print("-----------------------")    # SLICE ASSIGNMENT
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


# SET COMPREHENSION

numbers = [1,22,3,4,4,5,5,6,8,9,9,9,2,2,2,31,31,36,36]
unq_numbers = {x for x in numbers}
print(unq_numbers)
# "x fox in numbers" - pętla przechodząca po elemantach numbers
# {} - zapis tworzący zbiór (set)










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
