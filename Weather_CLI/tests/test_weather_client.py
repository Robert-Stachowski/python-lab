import pytest
from requests.exceptions import HTTPError, ConnectionError
from unittest.mock import Mock
from weather_client import WeatherClient



@pytest.fixture
def client_and_session():
    fake_requester = Mock()
    fake_session = Mock()

    fake_requester.Session.return_value = fake_session
    client = WeatherClient(requester= fake_requester)

    return client,fake_session



def test_get_city_weather_happy_path(client_and_session):
    client , fake_session = client_and_session

    fake_response = Mock()
    fake_response.raise_for_status.return_value = None
    fake_response.json.return_value = {
        "city": "Poznań",
        "temp_c": 10.0,
        "condition": "clouds"
        }
    fake_session.get.return_value = fake_response

    result = client.get_city_weather("Poznań")
    assert result == {
        "city": "Poznań",
        "temp_c": 10.0,
        "condition": "clouds"
    }

    expected_url = "https://example_url.com/api/weather?city=Poznań"
    fake_session.get.assert_called_once_with(expected_url, timeout = 5 )

# Ten test sprawdza poprawne działanie metody w sytuacji idealnej:
# - wejście jest poprawne,
# - serwer zwraca prawidłowy status (200 OK),
# - JSON zawiera wszystkie wymagane pola.
#
# KLUCZOWE ZAŁOŻENIA TESTU:
# -------------------------------------------------------------
# 1. W teście mockujemy cały moduł "requester" (czyli requests.Session),
#    aby NIE wykonywać żadnych prawdziwych requestów HTTP.
#
# 2. Metoda get_city_weather() wymaga w JSONie TRZECH kluczy:
#       "city", "temp_c", "condition"
#    Dlatego fake_response.json.return_value MUSI zwracać dict 
#    zawierający wszystkie te pola. W przeciwnym razie kod klienta
#    wykryje brak wymaganych pól i rzuci ValueError.
#
# 3. Używamy timeout=5 w asercji, ponieważ dokładnie tak wywołuje 
#    sesję kod produkcyjny:
#       self.session.get(url, timeout=5)
#    Test musi odzwierciedlać realne wywołanie, inaczej nie 
#    sprawdzamy prawdziwego zachowania.
#
# 4. Po zmockowaniu response.raise_for_status() ustawiamy:
#       return_value = None
#    co symuluje sytuację, w której serwer zwrócił 200 OK 
#    (brak wyjątku HTTPError).
#
# 5. Asercje:
#    - wynik zwracany przez metodę klienta musi być EXACT tego samego dictu,
#    - session.get() musi zostać wywołane RAZ z poprawnym URL i timeoutem.
#
# -------------------------------------------------------------
# LINIJKA PO LINIJCE CO SIĘ DZIEJE:
#
# fake_response = Mock()
#   Tworzymy fejkowy obiekt odpowiedzi HTTP. Będzie udawał wynik
#   self.session.get(). Dzięki temu test nie dotyka sieci.
#
# fake_response.raise_for_status.return_value = None
#   Mówimy: "wywołanie .raise_for_status() NIC nie rzuca", czyli
#   symulujemy status 200 OK.
#
# fake_response.json.return_value = {
#     "city": "Poznań",
#     "temp_c": 10.0,
#     "condition": "clouds"
# }
#   To JEST PEŁNY, POPRAWNY JSON wymagany przez WeatherClient.
#   Muszą być wszystkie klucze, bo klient sprawdza:
#       required = {"temp_c", "condition"}
#       if not required <= data.keys(): raise ValueError
#
# fake_session.get.return_value = fake_response
#   Mówimy sesji: "każde wywołanie get() zwróci fake_response".
#
# result = client.get_city_weather("Poznań")
#   Wywołujemy metodę – powinna przejść przez cały pipeline:
#     - walidacja inputu
#     - budowa URL
#     - session.get(...)
#     - raise_for_status()
#     - json()
#     - sprawdzenie required fields
#
# assert result == {
#     "city": "Poznań",
#     "temp_c": 10.0,
#     "condition": "clouds"
# }
#   Sprawdzamy, czy metoda zwróciła dokładnie to, co JSON z fake_response.
#
# expected_url = "https://example_url.com/api/weather?city=Poznań"
#
# fake_session.get.assert_called_once_with(expected_url, timeout=5)
#   Kluczowa asercja:
#     - wywołano dokładnie RAZ
#     - wywołano z tym samym URL
#     - timeout=5 MUSI się zgadzać z kodem produkcyjnym
#
# -------------------------------------------------------------
# Dzięki temu test dokładnie potwierdza poprawną integrację:
#   konstruktor → session → wywołanie HTTP → walidacje → JSON.
# -------------------------------------------------------------

def test_get_city_weather_http_error(client_and_session):
    client, fake_session = client_and_session
    
    fake_response = Mock()
    fake_response.raise_for_status.side_effect = HTTPError("404")
    fake_session.get.return_value = fake_response
    fake_response.json.return_value = {}

    with pytest.raises(HTTPError):
        client.get_city_weather("fake_city")

# -------------------------------------------------------------
# KOMENTARZ – Test "HTTP error" dla WeatherClient.get_city_weather()
#
# Ten test sprawdza zachowanie metody w sytuacji, gdy serwer API
# zwraca błąd HTTP (np. 404, 500). W takiej sytuacji:
# - response.raise_for_status() powinno rzucić HTTPError,
# - metoda get_city_weather() NIE powinna nic przetwarzać dalej,
# - test oczekuje przechwycenia wyjątku HTTPError.
#
# KLUCZOWE ZAŁOŻENIA TESTU:
# -------------------------------------------------------------
# 1. Klient pracuje na requester.Session(), więc w teście mockujemy
#    cały requester, aby żadne prawdziwe wywołania HTTP nie miały miejsca.
#
# 2. session.get() musi zwracać fake_response – to jest OBOWIĄZKOWE,
#    ponieważ metoda produkcyjna:
#         response = self.session.get(...)
#    spodziewa się prawdziwego obiektu odpowiedzi.
#
# 3. raise_for_status.side_effect = HTTPError("404")
#    To kluczowe — symulujemy, że serwer zwrócił status błędu.
#    Dzięki użyciu side_effect zamiast return_value test wymusza,
#    że metoda rzuci wyjątek, dokładnie tak jak robi requests.
#
# 4. fake_response.json.return_value = {}
#    Ta linijka jest konieczna mimo że JSON nie będzie używany.
#    Dlaczego? Ponieważ Python tworzy ramkę wywołania i spodziewa się,
#    że wszystkie wywoływane metody (json(), keys()) istnieją.
#    Gdyby json() nie było ustawione, mógłby polecieć AttributeError
#    zamiast właściwego HTTPError.
#
# 5. with pytest.raises(HTTPError):
#    Oczekujemy, że metoda rzuci HTTPError. Jeżeli tak się stanie —
#    test przechodzi. Jeżeli NIE — test upada.
#
# -------------------------------------------------------------
# LINIJKA PO LINIJCE CO SIĘ DZIEJE:
#
# fake_response = Mock()
#   Tworzymy fałszywy obiekt odpowiedzi HTTP. To ON będzie udawał
#   wynik session.get().
#
# fake_response.raise_for_status.side_effect = HTTPError("404")
#   Kiedy zostanie wywołane raise_for_status(), rzuci HTTPError.
#   To symuluje zachowanie biblioteki requests przy kodach 4xx/5xx.
#
# fake_session.get.return_value = fake_response
#   Mówimy: "każde wywołanie session.get(...) ma zwrócić fake_response".
#   To podłącza nasz fejkowy response pod kod klienta.
#
# fake_response.json.return_value = {}
#   Zapewniamy istnienie json(), nawet jeśli metoda nie zdąży do niego dojść.
#   Dzięki temu test nigdy nie rzuci przypadkowego AttributeError.
#
# with pytest.raises(HTTPError):
#   Oczekujemy, że próba pobrania danych zakończy się wyjątkiem HTTPError.
#
#     client.get_city_weather("fake_city")
#       Wywołujemy metodę produkcyjną. Jej flow:
#         - walidacja parametru,
#         - session.get(...) → zwraca fake_response,
#         - raise_for_status() → rzuca HTTPError (side_effect),
#         - metoda kończy się wyjątkiem.
#
# -------------------------------------------------------------
# REZULTAT
# -------------------------------------------------------------
# Test potwierdza, że klient:
# - poprawnie obsługuje błędy HTTP,
# - nie ukrywa ich i nie zwraca błędnych danych,
# - zachowuje się identycznie jak prawdziwa biblioteka requests.
# -------------------------------------------------------------


def test_get_city_weather_connection_error(client_and_session):
    client, fake_session = client_and_session

    fake_session.get.side_effect = ConnectionError("network down")

    with pytest.raises(ConnectionError):
        client.get_city_weather("fake_city")




INVALID_VALUES = [""," ", None , 123]

@pytest.mark.parametrize("city", INVALID_VALUES)
def test_invalid_values_get_city_weather(client_and_session, city):
    client, _ = client_and_session

    with pytest.raises(ValueError):
        client.get_city_weather(city)


def test_get_city_weather_missing_fields(client_and_session):
    client, fake_session = client_and_session

    fake_response = Mock()
    fake_response.raise_for_status.return_value = None
    fake_response.json.return_value = {"city":"Poznań"}

    fake_session.get.return_value = fake_response
    with pytest.raises(ValueError):
        client.get_city_weather("Poznań")

# -------------------------------------------------------------
# KOMENTARZ – Test "missing fields in JSON" dla WeatherClient
#
# Ten test sprawdza zachowanie klienta w sytuacji, gdy API zwraca
# poprawny status HTTP oraz poprawny format JSON, ale zawartość
# JSON jest NIEKOMPLETNA. To bardzo częsty realny przypadek,
# gdy serwer działa, ale zwraca ucięte lub niepełne dane.
#
# ZACHOWANIE KLIENTA:
#   Jeśli JSON nie zawiera dwóch kluczy wymaganych:
#       "temp_c" oraz "condition"
#   to metoda get_city_weather() powinna rzucić:
#       ValueError("Brak wymaganych pól")
#
# -------------------------------------------------------------
# LINIJKA PO LINIJCE:
#
# fake_response = Mock()
#   Tworzymy fejkowy obiekt odpowiedzi HTTP.
#
# fake_response.raise_for_status.return_value = None
#   Symulujemy status HTTP 200 OK (brak wyjątków HTTPError).
#
# fake_response.json.return_value = {"city": "Poznań"}
#   Najważniejsza część tego testu:
#   JSON jest poprawny składniowo, ale NIE posiada kluczy:
#       "temp_c"
#       "condition"
#   To powinno uruchomić blok walidacji pól w kliencie.
#
# fake_session.get.return_value = fake_response
#   Podłączamy fake_response pod session.get(), tak aby metoda
#   produkcyjna dostała dokładnie ten JSON.
#
# with pytest.raises(ValueError):
#     client.get_city_weather("Poznań")
#   Oczekujemy ValueError, ponieważ walidacja pól:
#       required = {"temp_c", "condition"}
#       required <= data.keys()
#   zwróci False → klient rzuci wyjątek.
#
# -------------------------------------------------------------
# Dzięki temu testowi upewniamy się, że klient:
#   - poprawnie wykrywa niepełne dane z API,
#   - nie przepuszcza błędnych struktur JSON dalej,
#   - zgłasza ValueError zgodnie z kontraktem metody.
# -------------------------------------------------------------


def test_get_weather_city_invalid_json(client_and_session):
    client, fake_session = client_and_session

    fake_response = Mock()
    fake_response.raise_for_status.return_value = None
    fake_response.json.side_effect = ValueError("invalid JSON")

    fake_session.get.return_value = fake_response

    with pytest.raises(ValueError):
        client.get_city_weather("poznań")

# -------------------------------------------------------------
# KOMENTARZ – Test "invalid JSON" dla WeatherClient.get_city_weather()
#
# Ten test sprawdza sytuację, w której serwer API zwraca poprawny
# status HTTP (np. 200 OK), ale treść odpowiedzi NIE JEST prawidłowym
# JSON-em. Wtedy response.json() rzuci wyjątek ValueError.
#
# Kod klienta NIE przechwytuje tego wyjątku — i słusznie.
# W takim wypadku metoda powinna przerwać działanie i przekazać
# błąd dalej. Ten test upewnia się, że zachowanie jest zgodne 
# z kontraktem i metodą biblioteki requests.
#
# -------------------------------------------------------------
# LINIJKA PO LINIJCE:
#
# fake_response = Mock()
#   Tworzymy fałszywy obiekt odpowiedzi HTTP.
#
# fake_response.raise_for_status.return_value = None
#   Symulujemy brak błędu HTTP — serwer zwrócił np. 200 OK.
#
# fake_response.json.side_effect = ValueError("invalid JSON")
#   Najważniejsza część testu:
#   - kiedy klient wykona response.json(),
#   - zostanie rzucony ValueError,
#   - dokładnie tak zachowuje się biblioteka requests, 
#     gdy API zwróci uszkodzone dane.
#
# fake_session.get.return_value = fake_response
#   Podłączamy naszą fejką odpowiedź pod session.get().
#
# with pytest.raises(ValueError):
#     client.get_city_weather("Poznań")
#   Oczekujemy ValueError, ponieważ json() nie da się sparsować
#   i klient nie łapie tego wyjątku.
#
# -------------------------------------------------------------
# Test gwarantuje, że klient poprawnie propaguje wyjątki 
# związane z niepoprawną treścią JSON — to kluczowe w API clientach.
# -------------------------------------------------------------
