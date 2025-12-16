import randfacts
#instal pip randfacts

# random facts :)

print("--- Infinite Fact Generator ---")

while True:
    input("Press Enter to get a new fact... ")
    fact = randfacts.get_fact(filter_enabled = True)

    print(f"\nDid you know? {fact}\n")
    print("-"*30)