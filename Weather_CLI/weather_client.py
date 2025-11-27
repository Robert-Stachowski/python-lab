import requests


class WeatherClient:
    def __init__(self):
        self.base_url = "https://example_url.com/api"
        self.headers = { "sample_headers" : "sample_headers"}
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        

    def get_city_weather(self, city:str):
        if city is None or not isinstance(city, str) or not city.strip():
            raise ValueError("Brak danych / Niepoprawne dane")
        url = f"{self.base_url}/weather?city={city}" # przykładowe URL do fikcyjnego API pogody — city to nazwa miasta użytkownika
        response = self.session.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if "temp_c" not in data or "condition" not in data:
            raise ValueError("Brak wymaganych pól")
        return data