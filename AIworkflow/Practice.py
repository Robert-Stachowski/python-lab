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
print(x/y)
print(x//y)
print(x%y)
print(x**y)

if x > y:
    print(True)
else:
    print(False)


x = x + y
print(x)
print("-------------------------")

age = int(input("podaj wiek: "))
years_to_100 = 100 - age

print(f"Do setki zostało ci {years_to_100} lat")
print(type(years_to_100))

print("-------------------------")

password = input("Podaj hasło: ")
if password == "Python123":
    print("Haslo poprawne!")
else:
    print("Hasło niepoprawne! ")

print("-------------------------")

a = 1
while a <= 10:
    print("start!")
    print(a)
    a += 1
print("-------------------------")
"""

for i in range(1,21):
    if i % 2 == 0:
        print(i)
    else:
        print("nieparzysta")
        continue
print("-------------------------")


name = ("Ola","Olek","Bruno","Ala","Dupa Maryna")
for i in name:
    print(f"Cześć {i}")
