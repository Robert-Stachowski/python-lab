import requests


class WeatherClient:
    
    def __init__(self, requester=None):
        self.base_url = "https://example_url.com/api"
        self.headers = {"Accept": "application/json"}
        self.requester = requester or requests
        self.session = self.requester.Session()
        self.session.headers.update(self.headers)
        

    def get_city_weather(self, city:str) -> dict:
        if city is None or not isinstance(city, str) or not city.strip():
            raise ValueError("Brak danych / Niepoprawne dane")
        
        url = f"{self.base_url}/weather" 
        response = self.session.get(url, params={"city": city}, timeout=5)
        response.raise_for_status()
        data = response.json()

        required = {"city","temp_c","condition"}

        if not required <= data.keys():
            raise ValueError("Brak wymaganych pól")
        return data