"""

print("-------------------------")
first_name = "Robert"
last_name = "Stachowski"
age = 43
try_to_learn_python = True

print(f"{first_name} {last_name}, {age}, try to learn python: {try_to_learn_python}")
age = str(age)
print(first_name + age)
print("-------------------------")

x = 15
y = 4

print(x+y)
print(x-y)
print(x/y)      # dzielenie normalne z resztą
print(x//y)     # dzielenie całkowite
print(x%y)      # reszta z dzielenia
print(x**y)

if x > y:
    print(True)
else:
    print(False)


x = x + y
print(x)
print("-------------------------")

age = int(input("podaj wiek: "))        # input i od razu zamiana na liczbę całkowitą integer
years_to_100 = 100 - age

print(f"Do setki zostało ci {years_to_100} lat")
print(type(years_to_100))

print("-------------------------")

password = input("Podaj hasło: ")
if password == "Python123":     # == porównanie!
    print("Haslo poprawne!")
else:
    print("Hasło niepoprawne! ")

print("-------------------------")

a = 1
while a <= 10:
    print("start!")     #zliczanie od 1 do 10
    print(a)
    a += 1
print("-------------------------")
"""
"""
for i in range(1,21):
    if i % 2 == 0:      # % - modulo, reszta z dzielenia, if 0 print numer(i)
        print(i)
    else:
        print("nieparzysta")
        continue
print("-------------------------")


name = ["Ola","Olek","Bruno","Ala","Dupa Maryna"]
for i in name:              # pętla iteruje po elemntach (i) z listy name
    print(f"Cześć {i}")

print("-------------------------")

numbers = [1,3,6,5,9,8,6,32,2,1,45,11]

print(len(numbers))     # zlicza ilość elementów
numbers.append(44)        # dodaje na koniec listy podany w nawiasie element  
print("-------------------------")

numbers.remove(2)       # usuwa pierwsze wystąpienie podanego w nawiasie elementu
print(numbers)
print("-------------------------")

numbers.insert(1,5)             # dodaj na index 1 element 5 i przesuń resztę w prawo
print(numbers)
print("-------------------------")

print(numbers.count(1))         # policz ile razy występuję element 1


for i in range(len(numbers)):   # pętla od  poczatku do końca listy range(len(numbers)), 
                                    # ale UWAGA iteruje po indexach, nie po elementach!
    print(f"nr:{i}  {numbers[i]}")
print("-------------------------")

if 3 in numbers:
    print("jest trójeczka")
if 7 not in numbers:
    print("Brak siódemeczki")    
print("-------------------------")


for i, numer in enumerate(numbers):
    print(i , numer)
print("funkcja Enumerate")
print("-------------------------")

x = numbers.pop()   #usuwa ostatni element z listy
print(x)
print("-------------------------")

y = numbers.pop(0)  #usuwa  element o podanym indexie tu nr 0
print(y)
print(numbers)
print("-------------------------")

numbers[0] = 55         # podmienia pod podany index[0] nową wartość 55
print(numbers)
print("-------------------------")

tasks = ["email","deploy","backup"]
tasks[1] = "test"
print(tasks)

print(tasks.pop())
print("-------------------------")

words = ["python", "java", "go", "rust"]
word = input("wpisz nazwę języka programowania: ")
if word in words:
    print("Brawo Ty!")
if word not in words:
    print("Może kiedy indziej...")
print("-------------------------")

nums = [2,4,4,6,4,8]
print(nums.count(4))

nums.remove(4)
print(nums)
print("-------------------------")
"""
"""
print("-------------------------")
colors = ["green" , "pink", "red", "yellow", "blue"]
for i , n in enumerate(colors):         # Funkcja Enumerate, liczy indexy i od razu elementy
    print(i , n)
print("-------------------------")

for i in range(len(colors)):            # Tu liczymy po indexach
    print(f"nr {i}, dł {len(colors[i])}")       # tu musimy wywołać colors[i] żeby wywołać dany element
print("-------------------------")

for i , color in enumerate(colors):
    print(f"Nr. {i} kolor: {color}, długość: {len(color)} ")  # tu łączymy wszystko razem, 
                                                                #wywołujemy index (i), kolor czyli element (color) i długość elementu (len(color))

print("-------------------------")

"""
"""
nums = [2,4,6,8,10,12,14]
print(nums[:3])                 # pierwsze 3
print("-------------------------")
print(nums[2:5])                # od indexu 2 do 5, bez 5 :)
print("-------------------------")
print(nums[::2])                # co drugi index 
print("-------------------------")

text = "Programowanie"
print(text[::-1])               # odwrócenie listy /textu
print("-------------------------")
print(text[3:9])                   # od 3 indexu do 8 włącznie. czyli do 9 bez 9 :D

data = ["H","T","T","P","","2",".","0"]
print(data[:4])
print("-------------------------")
print(data[5:])
print("-------------------------")

base = [0,1,2,3,4,5,6,7,8,9]
n = int(input("Podaj cyfrę z zakresu 0-9: "))
print(f"Pierwsze {n} elementów: {base[:n]}")        # pierwsze n elementów listy
print("-------------------------")
print(f"Ostatnie {n} elementów: {base[-n:]}")       # ostatnie n elementów listy
print("-------------------------")

y = []                              # tworzymy pustą listę na potrzeby zapisu z pętli, zeby utworzyć listę wyników
for nums1 in list(range(1, 21)):    # wypisz liczbę z zakresu podanego w nawiasach
        if nums1 % 3 == 0:          # sprawdź czy jest podzielna przez 3
            y.append(nums1)         # dodaj wynik do pustej listy y=[]
print(y[1::2])                      # wyświetl listę od drugiego elementu, co drugi element.

print("-------------------------")


mums = [1,2,3]
mums.append([4,5])                  # append() dodaje tylko jeden element, 
print(mums)                         # w tym wypadku doda  [4,5] jako jeden element (lista w liście)
print("-------------------------")
mums += [6,7]                       # += dodaje wiele elementów pojedynczo
print(mums)
            
result = []
for i in range(1, 6):               # tu przykład kiedy append wygląda porządnie, kwadrat liczb z zakresu range
      result.append([i ,i**2])      # wynik wyświetlany parami zakres i i kwadrat [1,1] [2,4] [3,9] itp
print(result)                       # czytelnie, ładnie
print("-------------------------")

x = []
y = []
nums = list(range(1,21))
for i in nums:
    if i % 2 == 0:
        #x.append(i)                 # tu z append wyciąga każde i podzielne przez 2 (bez reszty)
        x += [i]                     # tu za pomocą += robi to samo, natomiast += sprawdza sie tylko przy płaskich listach
    if i % 5 == 0:
        y.append([i])                 # lista oddzielnych list czyli podlista w liście: [[5]],[[10]],[[15]],[[20]]      
print(nums[::3])        
print("-------------------------")        
print(x)
print("-------------------------")        
print(y)
print("-------------------------")        
print(x[1::2])
print("-------------------------")    
print("-------------------------")
print("-------------------------")



x = []
y = []
nums = list(range(1,31))
for i in nums:
    if i % 3 == 0:
        x.append([i])        
    if i % 4 == 0:        
        y += [i] 
print(y[1::2])        
print("-------------------------")        
print([x]+y)
"""

"""
x = []
y = []
nums = list(range(1,60))
for i in nums:                                                         # UWAGA!
    if (i % 4 == 0 or i % 6 == 0) and not (i % 4 == 0 and i % 6 == 0): # warunek XOR (A or B) and not (A and B)
        x += [i]                                                       # skrócony zapis: Symetryczna różnica warunków: 
        #x.append([i])                                                 # (i % 4 == 0) != (i % 6 == 0)    
    if i % 1 == 0 and i % i == 0:        
        y.append([i])
        #y += [i] 

print("-------------------------")   
print(x)        
print("-------------------------")        
print(y)
print("-------------------------")        
print(x[1::3] + y[5::-1])
"""

x = []
nums = list(range(1,61))
for i in nums:
    
    if i <= 1:
        is_prime = False
        continue
    elif i == 2 or i==3:
        x.append(i)
        continue
    elif i % 2 == 0 or i % 3 == 0:
        is_prime = False
        continue
    else:
        d = 5
        while d*d <= i:
    
            d2 = d + 2
            if i % d == 0 or i % d2 == 0:
                is_prime = False
                break
            d += 6
        else:
            x.append(i)
g1 = 0
g2 = 0
for i, val in enumerate(x):
    if val > 20:
        g1 = i
        break
    else:
        g1= len(x)

for i , val in enumerate(x[g1:]):
        if val > 40:
            g2 = g1 + i
            break
        else:
            g2 = len(x)

print(g1)
print(g2)


#print(x.index(2))

print(x)
"""
print(x[1:21])
print(x[21:41])
print(x[::2])
print(x[3:-1])
wynik = x[1:21]+x[21:41]+x[::2]+x[3:-1]
print(wynik)

    
"""