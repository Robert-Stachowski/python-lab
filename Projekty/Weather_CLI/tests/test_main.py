import pytest
import sys
from main import main
from unittest.mock import patch


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
    assert "Wynik:" in out


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


# ===================================================================
# KOMENTARZ – Testy modułu main.py (CLI)
#
# Te testy sprawdzają zachowanie warstwy CLI, czyli:
#   - parsowanie argumentów (sys.argv),
#   - integrację z klasą WeatherClient,
#   - obsługę wyjątków,
#   - poprawne kody wyjścia (exit code),
#   - poprawne komunikaty wypisywane na stdout.
#
# Jest to testowanie „zewnętrznej” warstwy programu, która zwykle
# decyduje o doświadczeniu użytkownika oraz o integracji z innymi
# narzędziami, pipeline’ami i CI/CD.
#
# Aby testować CLI BEZ wywoływania prawdziwego klienta HTTP:
#   - patchujemy klasę WeatherClient w module main:
#         patch("main.WeatherClient")
#   - patchujemy sys.argv, aby symulować wejście użytkownika,
#   - używamy capsys (pytest) do przechwycenia stdout.
#
# Dzięki temu testy są całkowicie izolowane od świata zewnętrznego.
# ===================================================================
#
# 1) HAPPY PATH – poprawne dane, brak błędów
# ---------------------------------------------------------------
# - get_city_weather() zwraca poprawny słownik,
# - main() powinien wypisać dane,
# - exit code powinien być 0 (sukces),
# - stdout powinien zawierać komunikat startowy i wynik.
#
# patch("main.WeatherClient"):
#   Patchujemy *klasę* WeatherClient w module `main`, a nie w weather_client.
#   To ważne, bo main importuje klasę lokalnie i tam trzeba podmienić referencję.
#
# FakeClient.return_value:
#   To instancja klasy, którą main() naprawdę będzie wywoływać.
#
# patch.object(sys, "argv", ["prog", "Poznań"]):
#   Udajemy, że użytkownik uruchomił:
#       python main.py Poznań
#
# capsys.readouterr().out:
#   Pobiera tekst wypisany na stdout — pozwala sprawdzić, co CLI pokazało.
#
# ---------------------------------------------------------------

# 2) VALUE ERROR – błąd użytkownika (np. złe dane)
# ---------------------------------------------------------------
# get_city_weather() rzuca ValueError → CLI powinno:
#   - wypisać komunikat błędu,
#   - zwrócić exit code 1 (błąd użytkownika).
#
# Ten test potwierdza, że CLI rozróżnia błędy użytkownika
# od błędów systemowych i API.
#
# Dzięki patchowaniu WeatherClient test nie wykonuje żadnej logiki HTTP,
# a jedynie sprawdza przepływ błędów i komunikatów w main().
# ---------------------------------------------------------------

# 3) GENERIC EXCEPTION – błąd systemowy / API
# ---------------------------------------------------------------
# get_city_weather() rzuca Exception (np. ConnectionError).
#
# Oczekujemy:
#   - wypisania komunikatu "błąd krytyczny: <tekst>",
#   - exit code == 2 (poważny błąd),
#   - brak dalszego wypisywania wyników.
#
# Ten test sprawdza odporność CLI na awarie warstwy API.
# ---------------------------------------------------------------
#
# PODSUMOWANIE
# ---------------------------------------------------------------
# Te trzy testy pokrywają cały kontrakt CLI:
#   ✔ poprawna ścieżka działania
#   ✔ błąd użytkownika
#   ✔ błąd programu/systemu/API
#
# Testy są szybkie, izolowane i nie wymagają sieci.
# To wzorcowy sposób testowania warstwy CLI w Pythonie.
# ===================================================================
