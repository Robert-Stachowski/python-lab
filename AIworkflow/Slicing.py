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
squares = [i**2 for i in x]         # potęga i pętla w jednym wyrażeniu
print(squares)
print("-----------------------")
even_num = [i for i in x if i % 2==0]   #
