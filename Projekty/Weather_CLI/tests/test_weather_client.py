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

    expected_url = "https://example_url.com/api/weather"
    fake_session.get.assert_called_once_with(expected_url, params={"city": "Poznań"}, timeout = 5 )


def test_get_city_weather_http_error(client_and_session):
    client, fake_session = client_and_session
    
    fake_response = Mock()
    fake_response.raise_for_status.side_effect = HTTPError("404")
    fake_session.get.return_value = fake_response

    with pytest.raises(HTTPError):
        client.get_city_weather("fake_city")



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


def test_get_weather_city_invalid_json(client_and_session):
    client, fake_session = client_and_session

    fake_response = Mock()
    fake_response.raise_for_status.return_value = None
    fake_response.json.side_effect = ValueError("invalid JSON")

    fake_session.get.return_value = fake_response

    with pytest.raises(ValueError):
        client.get_city_weather("poznań")
