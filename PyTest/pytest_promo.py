def is_valid_promo(code):
    if not isinstance(code, str):
        return False
    if len(code) != 10:
        return False
    if not all(char.isupper() or char.isdigit() for char in code):
        return False
    if sum (char.isdigit() for char in code) <2 :
        return False
    return True

# skrócona wersja tego co powyżej    
def is_valid_promo_and(code):
    return (
        isinstance(code,str)
        and len(code) == 10
        and all(char.isupper() or char.isdigit() for char in code)
        and sum(char.isdigit() for char in code) >= 2
    )