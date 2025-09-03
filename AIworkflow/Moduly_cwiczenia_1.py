# ===========================================
# Ćwiczenia utrwalające
# ===========================================

# 1. Użyj math do policzenia 5! (silnia).
# 2. Użyj random do wylosowania hasła z listy ["Python", "Django", "Backend"].
# 3. Sprawdź status strony https://google.com i wypisz czy jest OK.
# 4. Stwórz plik requirements.txt i zapisz w nim nazwę modułu requests.

# 1

try:
    x = int(input("podaj liczbę: "))

    if x < 0:
        raise ValueError("Silnia jest zdefiniowana tylko dla liczb >= 0")
    if x > 50:
        raise ValueError("Za duża liczba - ogranicz do max 50!")

    silnia = 1
    for i in range(1, x + 1):    
            silnia *= i
        
    print(f"{x}! = {silnia}")


except ValueError as e:
     print(f"Błąd! {e}")


# 2






