"""

is_student = True
name = "Robert"
last_name = "Stachowski"
print(f"{name}, {last_name}, {is_student}")

a=10
b=4

print(not(a<b))
print(a//b)

str(a)
print(str(a))
"""

#age = input("ile masz lat?")
#age=int(age)
#years_to_100 = 100 - age
#print(f"do 100 zostało ci: {years_to_100}")

#password = "Admin"
#password_input = input("podaj hasło: ")

#if password_input == password:
#    print("poprawne hasło")
#else:
#    print("buuu")

#temp = int(input("ile jest dziś stopni?"))
#if temp < 0:
#   print("zimno jak sam skurwesyn")
#elif temp == 0:
#    print("zero jak nic")
#elif temp > 10:
#    print("ciepło")
#else:
#    print("łee na plusie")

"""
numbers = [1,2,3,5,9,5]
print(len(numbers))
add_num = int(input("podaj liczbę: "))
numbers.append(add_num)
print(numbers)
print(len(numbers))
numbers[0] = 25
print(numbers) 

"""

"""
task = ["one", "two", "three"]
task[1] = "test"
print(task)
task1 = task.pop()
print(task1)
word = input("podaj słowo: ")
if word in task:
    print("yeah it's in!")
if word not in task:
    print("nope...")
"""

"""
print("-----------")
numbers = [1,2,3,5,9,5,4,3,3,6,5,6,9]
a = numbers.count(3)
print(a)
b = numbers.index(3)
c = numbers.pop(b)
print(b)
print(c)
print(numbers)

"""
"""
colors = ["red","blue","green","yellow"]
for i in range(0, len(colors)):
    print(f"{i} {colors[i]}")


numbers = [1,2,3,5,9,5,4,3,3,6,5,6,9]
print(numbers)
print("--------------")

print(numbers[:3])
print(numbers[2:5])
print(numbers[::2])
print(numbers[::-1])
print(numbers[5::1])

x = int(input("podaj liczbę: "))
print(numbers[:x])
print(numbers[-x:])


#nums = list(range(1, 21))
nums = numbers[1::2]   
for a in nums:
    if a % 3 == 0:
        print(a)
    


numbers = [1,2,3,5,9,5,4,3,3,6,5,6,9]
print(numbers)
print("-----------------")
numbers[1:4] = [21,31,41,51]
print(numbers)
numbers[1:1] = [3,4]
print(numbers)
numbers[3:7] = []
print(numbers)
numbers[1:] = [11,12,13,14]
print(numbers)

"""

numbers = [1,2,3,5,9,5,4,3,3,6,5,6,9]
square = [x**2 for x in numbers]
print(square)

nums = list(range(10))
a = [x for x in nums if x % 3 == 0 ]
print(a)

text = "abrakadabra"
no_a = [char for char in text if char!="a"]
print(no_a)
stringi ="".join(no_a) 
print(stringi)