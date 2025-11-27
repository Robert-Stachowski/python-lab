import requests


class Weather_client:
    def __init__(self):
        self.base_url = "https://example_url.com/api"
        self.headers = { "sample_headers" : "sample_headers"}
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        

    def get_city_weather(self, city:str):
        if city is None or isinstance(city, str) or not city.strip():
            raise ValueError("Brak danych")
        url = "f{self.base_url}/weather?city = {city}" # przykładowo zbudowane url do fejkowego api pogody, wywołującego podane maisto(city)
        response = self.session.get(url, timeout=5)
        response.raise_for_status()
        return response.json()