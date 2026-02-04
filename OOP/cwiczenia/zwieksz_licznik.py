class Licznik:
    def __init__(self,licznik):
        self.licznik = licznik
        
    def zwiększ(self):
        self.licznik = 1
        for i in range(3):
            self.licznik += i
        return self.licznik
        
obj = Licznik(0)
print(obj.zwiększ())

