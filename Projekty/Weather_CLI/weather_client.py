import requests


class WeatherClient:
    
    def __init__(self, requester = None):
        self.base_url = "https://example_url.com/api"
        self.headers = { "sample_headers" : "sample_headers"}
        self.requester = requester or requests
        self.session = self.requester.Session()
        self.session.headers.update(self.headers)
        

    def get_city_weather(self, city:str):
        if city is None or not isinstance(city, str) or not city.strip():
            raise ValueError("Brak danych / Niepoprawne dane")
        
        url = f"{self.base_url}/weather?city={city}" # przykładowe URL do fikcyjnego API pogody — city to nazwa miasta użytkownika
        response = self.session.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        required = {"temp_c","condition"}
        # Sprawdzamy, czy wszystkie wymagane pola istnieją w słowniku `data`.
        # `required` to zbiór kluczy obowiązkowych, np. {"temp_c", "condition"}.
        # `data.keys()` zwraca zbiór kluczy zwróconych przez API.
        # Operator `<=` działa na zbiorach i oznacza "czy jest podzbiorem".
        # Czyli: `required <= data.keys()` zwróci True, jeśli KAŻDY klucz z `required`
        # znajduje się w data – dokładnie to samo, co seria warunków:
        #    "temp_c" in data and "condition" in data
        # Refaktoryzacja: zamiast wielu OR/AND używamy logiki zbiorów – krócej, czytelniej i łatwo rozszerzalnie.
        if not required <= data.keys():
            raise ValueError("Brak wymaganych pól")
        return data