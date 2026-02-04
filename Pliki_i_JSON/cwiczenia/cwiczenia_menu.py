#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Complete exercises file (1..10) — executable with comments inline.

How to use:
- Run this file. A menu will appear.
- Enter the number of the exercise you want to run (1..10).
- Follow on-screen prompts for interactive exercises.

This keeps functions/classes reusable and demonstrations isolated.
"""

import json               # used in JSON exercises
import random             # used in random-number exercise
from collections import Counter  # optional, shown in exercises
from typing import List, Tuple

# ---------------------------------------------------------------------
# 1) Save / read note
# ---------------------------------------------------------------------
def save_note(path: str, data: str) -> None:
    """Save a string `data` to file at `path`. Validate before writing."""
    if not data:                                # do not create/overwrite empty files
        raise ValueError("Brak treści")
    with open(path, "w", encoding="utf-8") as f: # open file safely
        f.write(data)                           # write string to file

def read_note(path: str) -> str:
    """Read entire file and return its content. Raise if file empty."""
    with open(path, "r", encoding="utf-8") as f: # open for reading
        content = f.read()                      # read whole file as string
    if not content:                             # if file empty -> treat as error
        raise ValueError("Błąd, brak treści")
    return content

# ---------------------------------------------------------------------
# 2) Try/except on input (get_input + add/avg)
# ---------------------------------------------------------------------
def get_two_ints_from_input(prompt: str = "Podaj dwie liczby oddzielone przecinkami: ") -> List[int]:
    """Ask user until they provide exactly two integers separated by comma."""
    while True:
        try:
            parts = input(prompt).split(",")                 # raw split by comma
            nums = [int(x.strip()) for x in parts]           # strip whitespace, convert to int
            if len(nums) != 2:
                raise ValueError("Podaj dokładnie dwie liczby")
            return nums                                      # valid list of two ints
        except ValueError as e:
            print(f"Błąd: {e}")                              # explain what went wrong and repeat

def add(a: int, b: int) -> int:
    return a + b

def avg_list(nums: List[int]) -> float:
    """Return average of numbers in list; longer-term useful form."""
    if not nums:
        raise ValueError("Brak liczb do uśrednienia")
    return sum(nums) / len(nums)

# ---------------------------------------------------------------------
# 3) Class with history (History_calc)
# ---------------------------------------------------------------------
class HistoryCalc:
    """Calculator that stores history of operations in-memory."""
    def __init__(self):
        self.history: List[str] = []               # list of strings like "2 + 3 = 5"

    def show_history(self) -> None:
        if not self.history:                       # nothing to show
            print("Historia pusta")
            return
        print("Historia operacji:")
        for entry in self.history:
            print(entry)

    def calc_sum(self, a: int, b: int) -> int:
        result = a + b
        self.history.append(f"{a} + {b} = {result}") # store readable record
        return result

# ---------------------------------------------------------------------
# 4) List comprehension — squares of even numbers
# ---------------------------------------------------------------------
def squares_of_even(numbers: List[int]) -> List[int]:
    """Return squares of even numbers from the input list."""
    return [x**2 for x in numbers if x % 2 == 0]  # comprehension with filter

# ---------------------------------------------------------------------
# 5) Slicing examples
# ---------------------------------------------------------------------
def slicing_examples() -> Tuple[List[int], List[int], List[int]]:
    data = list(range(10))                          # [0..9]
    slice_2_6 = data[2:7]                           # indices 2..6 inclusive
    every_second_from_start = data[::2]             # indices 0,2,4,...
    reversed_list = data[::-1]                      # reversed
    return slice_2_6, every_second_from_start, reversed_list

# ---------------------------------------------------------------------
# 6) Random numbers: write and read, compute average
# ---------------------------------------------------------------------
def write_random_nums(path: str, length: int) -> List[int]:
    """Generate `length` random ints in 1..100, write as CSV line to `path`, return list."""
    nums = [random.randint(1, 100) for _ in range(length)]   # generate numbers
    with open(path, "w", encoding="utf-8") as f:
        # join int->str and write single line like "12, 34, 56"
        f.write(", ".join(str(x) for x in nums))
    return nums

def read_random_nums(path: str) -> List[int]:
    """Read CSV line from `path`, convert to list[int]. Raise if empty."""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if not content:
        raise ValueError("Pusty plik")
    return [int(x.strip()) for x in content.split(",")]

# ---------------------------------------------------------------------
# 7) divide with validation
# ---------------------------------------------------------------------
def divide(a: float, b: float) -> float:
    """Divide a by b; raise ValueError for division by zero (per exercise)."""
    if b == 0:
        raise ValueError("Błąd, dzielenie przez zero")
    return a / b

# ---------------------------------------------------------------------
# 8) dict comprehension counting words (exercise demands dict comprehension)
# ---------------------------------------------------------------------
def count_words_dict(words: List[str]) -> dict:
    """Return {word: count} using dict comprehension over set(words)."""
    return {word: words.count(word) for word in set(words)}

# alternative: Counter(words) is more efficient in real projects

# ---------------------------------------------------------------------
# 9) JSON write/read utilities with validation
# ---------------------------------------------------------------------
def json_write_data(path: str, data) -> None:
    """Write Python object (dict/list) as pretty JSON into file `path`."""
    if not data:
        raise ValueError("Brak danych do zapisu")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)  # pretty-printed JSON

def json_read_data(path: str):
    """Read JSON from `path` and return Python object; raise if empty."""
    with open(path, "r", encoding="utf-8") as f:
        content = json.load(f)        # parse JSON to Python object
    if not content:
        raise ValueError("Plik pusty")
    return content

# ---------------------------------------------------------------------
# 10) Mini project: calculator with history and file append
# ---------------------------------------------------------------------
class Calculate:
    """Calculator class with memory history and automatic append to history file."""
    def __init__(self, history_file: str = "../pliki_przykladowe/history.txt"):
        self.history: List[str] = []
        self.history_file = history_file

    def show_history(self) -> None:
        if not self.history:
            print("Historia pusta")
            return
        print("Historia operacji:")
        for entry in self.history:
            print(entry)

    # basic operations — return numeric results
    def add(self, a: int, b: int) -> int: return a + b
    def subtract(self, a: int, b: int) -> int: return a - b
    def multiply(self, a: int, b: int) -> int: return a * b
    def power(self, a: int, b: int): return a ** b
    def divide(self, a: int, b: int):
        if b == 0:
            raise ZeroDivisionError("Nie można dzielić przez zero")
        return a / b

    def calc_map(self, a: int, b: int, operation: str):
        """
        operation is expected in form "a+b", "a-b", etc.
        We extract the actual operator as operation[1:-1] and map it to functions.
        """
        op_symbol = operation[1:-1]                     # "+" or "-" or "*" or "**" or "/"
        operating_map = {
            "+": self.add,
            "-": self.subtract,
            "*": self.multiply,
            "**": self.power,
            "/": self.divide
        }
        if op_symbol not in operating_map:
            raise ValueError(f"Nieznany operator: {op_symbol}")
        func = operating_map[op_symbol]                  # select the function
        result = func(a, b)                              # compute result

        entry = f"{a} {op_symbol} {b} = {result}"        # human-friendly record
        self.history.append(entry)                       # keep in-session history

        # append to persistent history file (each entry on new line)
        with open(self.history_file, "a", encoding="utf-8") as f:
            f.write(entry + "\n")

        return result

# ---------------------------------------------------------------------
# Simple interactive menu to run demonstrations for each exercise
# ---------------------------------------------------------------------
def show_menu() -> None:
    print("\n=== Exercises menu ===")
    print("1 - save/read note (example)")
    print("2 - input sum & average (interactive)")
    print("3 - HistoryCalc demo (class)")
    print("4 - squares of even (list comprehension)")
    print("5 - slicing examples")
    print("6 - random numbers: write/read + average")
    print("7 - divide with exception")
    print("8 - dict comprehension (word counts)")
    print("9 - json write/read demo")
    print("10 - mini calculator (interactive)")
    print("q - quit")
    print("======================")

def run_exercise(choice: str) -> None:
    if choice == "1":
        # demo for save/read note
        path = "../pliki_przykladowe/note_demo.txt"
        text = "To jest przykładowy tekst dla funkcji save_note()"
        print("Saving note to", path)
        save_note(path, text)
        print("Reading note from", path)
        print(read_note(path))

    elif choice == "2":
        # interactive input demo for sum & average
        nums = get_two_ints_from_input()
        print("Suma:", add(nums[0], nums[1]))
        print("Średnia:", avg_list(nums))

    elif choice == "3":
        # HistoryCalc class demo
        calc = HistoryCalc()
        print("Dodajemy 2 + 3 i 10 + 5")
        print(calc.calc_sum(2, 3))
        print(calc.calc_sum(10, 5))
        calc.show_history()

    elif choice == "4":
        data = [2,3,6,5,8,9,62,31,23,33]
        print("Lista:", data)
        print("Kwadraty parzystych:", squares_of_even(data))

    elif choice == "5":
        slice_2_6, every_second, rev = slicing_examples()
        print("Indeksy 2..6:", slice_2_6)
        print("Co drugi (start 0):", every_second)
        print("Odwrócone:", rev)

    elif choice == "6":
        path = "../pliki_przykladowe/randoms.txt"
        n = 5
        print("Wygenerowane i zapisane:", write_random_nums(path, n))
        numbers = read_random_nums(path)
        print("Odczytane:", numbers)
        print("Średnia:", sum(numbers) / len(numbers))

    elif choice == "7":
        try:
            print("Divide 3/2 ->", divide(3, 2))
            print("Divide 10/0 -> expect exception")
            print(divide(10, 0))
        except ValueError as e:
            print("Caught ValueError:", e)

    elif choice == "8":
        words = ["kot", "pies", "kot", "mysz", "pies"]
        print("Words:", words)
        print("Counts (comprehension):", count_words_dict(words))
        print("Counts (Counter):", dict(Counter(words)))  # Counter to dict display

    elif choice == "9":
        path = "../pliki_przykladowe/config_demo.json"
        cfg = {"user": "Robert", "level": "junior"}
        print("Writing JSON to", path)
        json_write_data(path, cfg)
        print("Reading JSON from", path)
        print(json_read_data(path))

    elif choice == "10":
        # interactive calculator using Calculate class
        calc = Calculate(history_file="../pliki_przykladowe/history.txt")
        print("Calculator. Type operation like a+b, a-b, a*b, a**b, a/b. Type 'exit' to quit.")
        allowed = {"a+b","a-b","a*b","a**b","a/b"}
        while True:
            op_text = input("Operation (a+b etc) or exit: ").strip()
            if op_text == "exit":
                calc.show_history()
                break
            if op_text not in allowed:
                print("Nieznana operacja — użyj np. a+b")
                continue
            try:
                # get two numbers from user
                parts = input("Podaj liczby (a,b): ").split(",")
                nums = [int(x.strip()) for x in parts]
                if len(nums) != 2:
                    print("Podaj dokładnie dwie liczby")
                    continue
                res = calc.calc_map(nums[0], nums[1], op_text)
                print("Wynik:", res)
            except ValueError as e:
                print("Błąd:", e)
            except ZeroDivisionError as e:
                print("Błąd:", e)
            except KeyboardInterrupt:
                print("\nPrzerwano program klawiszem.")
                break

    else:
        print("Nieznane zadanie:", choice)


if __name__ == "__main__":
    # Upewnij się, że katalog ../pliki_przykladowe/ istnieje
    # This menu lets you run exercises one by one.
    while True:
        show_menu()
        choice = input("Wybierz numer zadania (q aby wyjść): ").strip()
        if choice.lower() == "q":
            print("Koniec. Miłego kodowania!")
            break
        run_exercise(choice)
