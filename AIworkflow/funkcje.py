# FUNKCJE UŻYTKOWNIKA

def przywitaj_sie():
    print("Hello!")

przywitaj_sie()
print("----------------------------")


def przedstaw_sie(a,b):
    return f"Cześć {a} , masz {b} lata?!"

x = przedstaw_sie("Robert", 43)
print(x)
print("----------------------------")


def pole_kwadratu(a):
    return a*a

x = pole_kwadratu(5)
print(x)
print("----------------------------")


def czy_parzysta(liczba):
    return liczba % 2==0

liczba = int(input("Podaj liczbę: "))
if czy_parzysta(liczba):
    print("Parzysta")
else:
    print("Nieparzysta")
print("----------------------------")



