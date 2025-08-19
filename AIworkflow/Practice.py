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

for i in range(1,21):
    if i % 2 == 0:      # % - modulo, reszta z dzielenia, if 0 print numer(i)
        print(i)
    else:
        print("nieparzysta")
        continue
print("-------------------------")


name = ["Ola","Olek","Bruno","Ala","Dupa Maryna"]
for i in name:
    print(f"Cześć {i}")

print("-------------------------")

numbers = [1,3,6,5,9,8,6,32,2,1,45,11]

print(len(numbers))     # zlicza ilość agumentów
numbers.append(44)        # dodaje na koniec listy podany w nawiasie argument  

numbers.remove(2)       # usuwa pierwsze wystąpienie podanego w nawiasie argumentu
print(numbers)

numbers.insert(1,5)             # dodaj na index 1 argument 5 i przesuń resztę w prawo
print(numbers)

print(numbers.count(1))         # policz ile razy występuję argument 1


for i in range(len(numbers)):   # pętla od  poczatku do końca listy range(len(numbers))
    print(f"nr:{i}  {numbers[i]}")

if 3 in numbers:
    print("jest trójeczka")
if 7 not in numbers:
    print("Brak siódemeczki")    

x = numbers.pop()   #usuwa ostatni argument z listy
print(x)

y = numbers.pop(0)  #usuwa  argument o podanym indexie tu nr 0
print(y)
print(numbers)

numbers[0] = 55
print(numbers)