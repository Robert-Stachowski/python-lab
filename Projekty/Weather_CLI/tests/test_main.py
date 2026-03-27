import pytest
import sys
from main import main, build_parser
from unittest.mock import patch


def test_build_parser():
    parser = build_parser()
    args = parser.parse_args(["Warszawa"])
    assert args.city_name == "Warszawa"


def test_main_happy_path(capsys):
    # Patch WeatherClient tak, żeby nie wywoływać prawdziwego klienta
    with patch("main.WeatherClient") as FakeClient:
        fake_client_instance = FakeClient.return_value
        fake_client_instance.get_city_weather.return_value = {
            "city": "Poznań",
            "temp_c": 10.0,
            "condition": "clouds"
        }

        # Symulujemy wejście użytkownika
        with patch.object(sys, "argv", ["prog", "Poznań"]):
            exit_code = main()

    assert exit_code == 0
    out = capsys.readouterr().out
    assert "Pobieram dane pogodowe dla miasta: Poznań" in out
    assert "Miasto:" in out
    assert "Temperatura:" in out



def test_main_value_error(capsys):
    with patch("main.WeatherClient") as FakeClient:
        fake_client_instance = FakeClient.return_value
        fake_client_instance.get_city_weather.side_effect = ValueError("Brak danych")

        with patch.object(sys, "argv", ["prog", "X"]):
            exit_code = main()

    # Uwaga: w Twoim kodzie ValueError zwraca 1 
    assert exit_code == 1  
    out = capsys.readouterr().out
    assert "błąd: Brak danych" in out


def test_main_generic_exception(capsys):
    with patch("main.WeatherClient") as FakeClient:
        fake_client_instance = FakeClient.return_value
        fake_client_instance.get_city_weather.side_effect = Exception("boom :) ")

        with patch.object(sys, "argv", ["prog", "X"]):
            exit_code = main()

    assert exit_code == 2  # bo Exception powoduje zwrot 2
    out = capsys.readouterr().out
    assert "błąd krytyczny:" in out
