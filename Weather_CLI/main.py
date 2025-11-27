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
    except Exception as e:
        print(f"bład: {e}")
        return 1
    print(f"Wynik: {data}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())