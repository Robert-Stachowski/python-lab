import argparse
from weather_client import WeatherClient


def build_parser()-> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="Weather client",
        description="Pobiera aktualne dane pogodowe dla podanego miasta."
        )
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
    print(f"Miasto:  {data['city']}")
    print(f"Temperatura:  {data['temp_c']}°C")
    print(f"Pogoda:  {data['condition']}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
