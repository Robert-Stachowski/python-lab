import argparse
from weather_client import WeatherClient


def build_parser()-> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="Weather client")
    parser.add_argument("city_name", help="Pogoda dla konkretnego miasta")
    return parser

def main()->int:
    parser = build_parser()
    args = parser.parse_args()
    client = WeatherClient()
    print(f"Pobieram dane pogodowe dla miasta: {args.city_name}")

    try:
        data = client.get_city_weather(args.city_name)
    except ValueError as e:
        print(f"błąd: {e}")
        return 1
    except Exception as e:
        print(f"błąd krytyczny: {e}")
        return 2
    print(f"Wynik: {data}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

# ===================================================================
# KOMENTARZ – Plik main.py (Warstwa CLI aplikacji WeatherClient)
#
# Ten moduł stanowi wejściowy punkt programu i odpowiada za:
#   - parsowanie argumentów przekazanych z linii poleceń,
#   - wywołanie logiki biznesowej (WeatherClient),
#   - obsługę błędów,
#   - zwracanie prawidłowego kodu wyjścia (exit code),
#   - wypisywanie komunikatów dla użytkownika.
#
# main.py NIE wykonuje logiki HTTP samodzielnie – jedynie deleguje
# zadania do klasy WeatherClient. Dzięki temu:
#   - kod jest oddzielony warstwami,
#   - łatwo testuje się zarówno WeatherClient, jak i CLI,
#   - całość jest zgodna z dobrymi praktykami projektowania CLI.
#
# ===================================================================
# 1. build_parser() – konfiguracja argparse
# ===================================================================
# Funkcja buduje parser argumentów linii poleceń. W tej wersji CLI
# przyjmuje tylko jeden argument:
#
#     city_name – nazwa miasta, dla którego chcemy pobrać pogodę.
#
# argparse konwertuje wpisaną wartość na atrybut args.city_name.
#
# Ta funkcja została wydzielona osobno, aby dało się ją testować
# niezależnie w testach jednostkowych oraz aby main() było czyste.
# ===================================================================
#
# 2. main() – główna funkcja programu
# ===================================================================
# Struktura funkcji:
#
#   parser = build_parser()
#   args = parser.parse_args()
#   client = WeatherClient()
#
#   print(f"Pobieram dane ...")
#
#   try:
#       data = client.get_city_weather(args.city_name)
#   except ValueError:
#       ...
#   except Exception:
#       ...
#
#   print("Wynik: ...")
#   return 0
#
# Jest to układ zgodny ze standardami CLI:
#   - komunikaty dla użytkownika,
#   - przechwytywanie błędów,
#   - semantyka kodów wyjścia.
#
# ===================================================================
# 3. Obsługa wywołania WeatherClient.get_city_weather()
# ===================================================================
# Ten fragment wywołuje metodę odpowiedzialną za pobranie danych
# pogodowych z API. WeatherClient może zwrócić dane lub rzucić wyjątek.
#
# W zależności od rodzaju wyjątku main() określa, jaki kod wyjścia
# zwrócić do systemu operacyjnego.
#
# ===================================================================
# 4. Obsługa wyjątków i semantyka exit code
# ===================================================================
#
#  a) except ValueError:
#       print("błąd: ...")
#       return 1
#
#      ValueError oznacza błąd użytkownika:
#        - błędna nazwa miasta,
#        - pusty string,
#        - nieprawidłowe dane wejściowe,
#        - brak wymaganych pól w JSON.
#
#      Kod wyjścia 1 → "błąd użytkownika".  
#      To jest standard UNIX-owy.
#
#  b) except Exception:
#       print("błąd krytyczny: ...")
#       return 2
#
#      Exception oznacza poważny problem:
#        - awaria API,
#        - błąd sieci,
#        - nieobsłużony wyjątek,
#        - błąd biblioteki requests.
#
#      Kod wyjścia 2 → "błąd systemowy / krytyczny".
#
#  c) jeśli nie wystąpił żaden wyjątek → wypisujemy wynik i zwracamy 0:
#
#         print("Wynik: ...")
#         return 0
#
#      Kod wyjścia 0 → sukces.
#
# Taki podział kodów wyjścia jest profesjonalny i ułatwia:
#      - pisanie testów integracyjnych,
#      - pracę w CI/CD,
#      - używanie skryptu w automatyzacji.
# ===================================================================
#
# 5. Blok if __name__ == "__main__":
# ===================================================================
# Standardowy wzorzec uruchamiania programu w Pythonie.
#
#   raise SystemExit(main())
#
# Dzięki temu:
#   - exit code zwrócony przez main() jest przekazywany do systemu OS,
#   - moduł może być importowany w testach (main() nie odpala się wtedy),
#   - zachowanie programu jest w pełni kontrolowane i przewidywalne.
#
# ===================================================================
# PODSUMOWANIE
# ===================================================================
# main.py jest czystą, dobrze zaprojektowaną warstwą CLI:
#
#   ✔ oddziela logikę biznesową od interfejsu użytkownika,
#   ✔ używa argparse zgodnie z dobrymi praktykami,
#   ✔ poprawnie obsługuje wyjątki,
#   ✔ stosuje semantykę kodów wyjścia (0 / 1 / 2),
#   ✔ współpracuje idealnie z testami jednostkowymi.
#
# Ten plik może być bez problemu częścią portfolio, ponieważ pokazuje:
#   - świadomość architektury,
#   - poprawne podejście do błędów,
#   - umiejętność pisania testowalnego CLI.
# ===================================================================
