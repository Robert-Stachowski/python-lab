import argparse
from pathlib import Path


def create_parser():
    parser = argparse.ArgumentParser(prog="Mini Explorer CLI")
    parser.add_argument("path", help="ścieżka do katalogu lub pliku")
    parser.add_argument("--count", "-c", action="store_true", help="wypisz liczbę plików w katalogu")
    parser.add_argument("--list", "-l", action="store_true", help="wypisz zawartość katalogu (nazwy)")
    parser.add_argument("--ext", "-e", help="filtruj pliki po rozszerzeniu (np. .txt, .py)")
    parser.add_argument("--info", "-i", action="store_true", help="wypisz informacje o pliku")
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    path = Path(args.path)
    try:
        if not path.exists():
            print("Podana ścieżka nie istnieje...")
            raise SystemExit(1)
        if path.is_dir():            
            if args.info:
                print("--info działa tylko dla plików.")
                return 2
            elif args.count:
                files = [f for f in path.iterdir() if f.is_file()]
                print(len(files))
                return 0
            elif args.list:
                for entry in path.iterdir():
                    print(entry.name)
                return 0
            elif args.ext:
                for entry in path.iterdir():
                    if entry.is_file() and entry.suffix == args.ext:
                        print(entry.name)
                return 0
            else:
                parser.print_help()
                return 2
        elif path.is_file():
            if args.count or args.list or args.ext:
                print("Flagi --count, --list i --ext działają tylko na katalogach.")
                return 2
            if args.info:
                print("Nazwa:", path.name)
                print("Rozszerzenie:", path.suffix)
                print("Rozmiar (bajty):", path.stat().st_size)
                print("Czy plik?", path.is_file())
                print("Czy katalog?", path.is_dir())
                return 0
            parser.print_help()
            return 2
    except Exception as e:
        print(f"Nieoczekiwany błąd: {e}")
        return 1
    

if __name__ == "__main__":
    raise SystemExit(main())


