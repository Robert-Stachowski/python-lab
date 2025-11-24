import argparse
from pathlib import Path


parser = argparse.ArgumentParser(prog="Mini Explorer CLI")
parser.add_argument("path", help= "path → ścieżka do katalogu lub pliku")
parser.add_argument("--count","-c",action="store_true", help="→ wypisz liczbę plików w katalogu.")
parser.add_argument("--list", "-l", action="store_true",help=" → wypisz zawartość katalogu (nazwy).")
parser.add_argument("--ext","-e",help="→ filtruj tylko pliki o danym rozszerzeniu (np. .txt, .py).")
parser.add_argument("--info","-i", action="store_true",help="→ jeśli path wskazuje na plik → wypisz: * nazwę * rozszerzenie * rozmiar pliku w bajtach * czy jest plikiem, czy katalogiem")



def main():
    args = parser.parse_args()
    target_dir = Path(args.path)
    try:
        if not target_dir.exists():
            print("The target directory doesn't exist")
            raise SystemExit(1)
        if target_dir.is_dir():
            sample_path = target_dir / "example.txt"
# print(sample_path)  # zostawione jako przykład użycia operatora /
            if args.info:
                print("--info działa tylko dla plików.")
                return 2
            elif args.count:
                files = [f for f in target_dir.iterdir() if f.is_file()]
                print(len(files))
            elif args.list:
                for entry in target_dir.iterdir():
                    print(entry.name)
            elif args.ext:
                for entry in target_dir.iterdir():
                    if entry.is_file() and entry.suffix == args.ext:
                        print(entry.name)
            else:
                parser.print_help()
                return 2
        elif target_dir.is_file():
            if args.count or args.list or args.ext:
                print("Flagi --count, --list i --ext działają tylko na katalogach.")
                return 2
            if args.info:
                print("Nazwa:", target_dir.name)
                print("Rozszerzenie:", target_dir.suffix)
                print("Rozmiar (bajty):", target_dir.stat().st_size)
                print("Czy plik?", target_dir.is_file())
                print("Czy katalog?", target_dir.is_dir())
                return 0
            parser.print_help()
            return 2
    except Exception as e:
        print(f"Nieoczekiwany błąd: {e}")
        return 1
    

if __name__ == "__main__":
    raise SystemExit(main())