"""
cli_template.py

Uniwersalny szablon aplikacji CLI w Pythonie z użyciem argparse.

Co tu masz:
- gotowy schemat budowy parsera,
- przykład globalnych opcji (np. --verbose, --token),
- przykład podkomend (subparsers): np. 'repos', 'repo', 'invite',
- oddzielne funkcje-handler'y dla każdej komendy,
- główną funkcję main() z obsługą błędów,
- standardowy blok if __name__ == "__main__".

Możesz:
- skopiować ten plik do dowolnego projektu,
- zmienić nazwy komend, argumentów i logikę w handlerach,
- zachować konstrukcję argparse tak, jak jest.
"""

import argparse  # standardowy moduł do parsowania argumentów z linii poleceń
import sys       # używany m.in. do zwrócenia kodu wyjścia programu (sys.exit)


# ======================================================================
# 1. Funkcja budująca parser (ArgumentParser) i wszystkie komendy
# ======================================================================

def build_parser() -> argparse.ArgumentParser:
    """
    Tworzy i konfiguruje główny parser argparse.

    Zawiera:
    - opis programu (description),
    - globalne argumenty (np. --verbose, --token),
    - podkomendy (subparsers), np.: repos, repo, invite.

    Zwraca:
        Obiekt argparse.ArgumentParser gotowy do użycia w main().
    """

    # Tworzymy główny parser.
    # To on odpowiada za:
    # - wyświetlanie pomocy (main.py --help),
    # - parsowanie argumentów z sys.argv.
    parser = argparse.ArgumentParser(
        prog="mycli",  # nazwa programu pokazywana w helpie; możesz zmienić
        description=(
            "Przykładowe CLI oparte na argparse.\n"
            "Dostosuj komendy i argumenty do swojego projektu."
        ),
    )

    # -----------------------------
    # Globalne argumenty (opcjonalne)
    # -----------------------------

    # Przykładowa globalna flaga logiczna: --verbose
    # - action="store_true" oznacza, że:
    #   - jeśli flaga jest podana → args.verbose = True
    #   - jeśli nie → args.verbose = False
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Włącz tryb gadatliwy (dodatkowe logi w konsoli).",
    )

    # Przykładowy globalny argument opcjonalny: --token
    # Możesz go użyć np. do podania tokena do API.
    parser.add_argument(
        "--token",
        help="Opcjonalny token / klucz (np. do API). Jeśli nie podany, "
             "użyj wartości z konfiguracji / .env.",
        default=None,
    )

    # -----------------------------
    # Podkomendy (subparsers)
    # -----------------------------
    #
    # subparsers = grupa komend, np.:
    # - mycli repos ...
    # - mycli repo ...
    # - mycli invite ...
    #
    # dest="command" → nazwa pola w args (args.command),
    # required=True → użytkownik MUSI podać jakąś komendę.
    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
        help="Dostępne komendy",
    )

    # ------------------------------------------------------------------
    # Komenda: repos
    # Przykład sensownego użycia:
    #   mycli repos some_user
    # ------------------------------------------------------------------
    cmd_repos = subparsers.add_parser(
        "repos",                        # nazwa komendy, np. mycli repos ...
        help="Przykład: wypisz listę repozytoriów użytkownika.",
        description=(
            "Komenda 'repos' może np. pobierać listę repozytoriów z API "
            "i wyświetlać ich nazwy."
        ),
    )

    # Pozycjonalny argument: username
    # - użytkownik MUSI go podać,
    # - wartość trafi do args.username.
    cmd_repos.add_argument(
        "username",
        help="Nazwa użytkownika (np. na GitHubie).",
    )

    # ------------------------------------------------------------------
    # Komenda: repo
    # Przykład:
    #   mycli repo owner_name repo_name
    # ------------------------------------------------------------------
    cmd_repo = subparsers.add_parser(
        "repo",
        help="Przykład: pokaż szczegóły jednego elementu (np. repo).",
        description=(
            "Komenda 'repo' może pobierać szczegółowe informacje o jednym "
            "konkretnym zasobie (np. pojedyncze repozytorium)."
        ),
    )

    cmd_repo.add_argument(
        "owner",
        help="Właściciel (np. nazwa użytkownika lub organizacji).",
    )

    cmd_repo.add_argument(
        "name",
        help="Nazwa zasobu (np. repozytorium).",
    )

    # ------------------------------------------------------------------
    # Komenda: invite
    # Przykład:
    #   mycli invite owner_name repo_name username_to_invite
    # ------------------------------------------------------------------
    cmd_invite = subparsers.add_parser(
        "invite",
        help="Przykład: wyślij zaproszenie (np. do współpracy).",
        description=(
            "Komenda 'invite' może np. wysyłać zaproszenia do współpracy "
            "na podstawie podanych argumentów."
        ),
    )

    cmd_invite.add_argument(
        "owner",
        help="Właściciel zasobu (np. repozytorium).",
    )

    cmd_invite.add_argument(
        "name",
        help="Nazwa zasobu (np. repozytorium).",
    )

    cmd_invite.add_argument(
        "invitee",
        help="Adresat zaproszenia (np. nazwa użytkownika).",
    )

    # Zwracamy w pełni skonfigurowany parser.
    return parser


# ======================================================================
# 2. Funkcje handlerów dla poszczególnych komend
#    (tu w realnym projekcie wołasz swoją logikę / API / biznes)
# ======================================================================

def handle_repos(args: argparse.Namespace) -> int:
    """
    Handler dla komendy 'repos'.

    Parametry:
        args: Namespace z polami odpowiadającymi argumentom,
              np. args.username, args.verbose, args.token.

    Zwraca:
        Kod wyjścia (0 = OK, !=0 = błąd).
    """
    # Tu podłączasz swoją logikę, np. klienta API.
    # Poniżej prosty przykład "na sucho".

    if args.verbose:
        print("[DEBUG] Wywołano handle_repos()")

    username = args.username
    print(f"Symuluję pobieranie repozytoriów dla użytkownika: {username}")

    # TODO: w realnym projekcie:
    # - stwórz klienta API,
    # - pobierz dane,
    # - wyświetl wyniki w sensownym formacie.

    return 0  # 0 oznacza, że wszystko OK


def handle_repo(args: argparse.Namespace) -> int:
    """
    Handler dla komendy 'repo'.

    Parametry:
        args: Namespace z polami args.owner, args.name, args.verbose itd.

    Zwraca:
        Kod wyjścia programu (0 = sukces).
    """
    if args.verbose:
        print("[DEBUG] Wywołano handle_repo()")

    owner = args.owner
    name = args.name

    print(f"Symuluję pobieranie szczegółów dla: {owner}/{name}")

    # TODO: w realnym projekcie:
    # - API: pobierz szczegóły zasobu,
    # - wypisz kluczowe pola (opis, status, daty, itp.).

    return 0


def handle_invite(args: argparse.Namespace) -> int:
    """
    Handler dla komendy 'invite'.

    Parametry:
        args: Namespace z polami args.owner, args.name, args.invitee.

    Zwraca:
        Kod wyjścia (0 = OK, !=0 = błąd).
    """
    if args.verbose:
        print("[DEBUG] Wywołano handle_invite()")

    owner = args.owner
    name = args.name
    invitee = args.invitee

    print(
        f"Symuluję wysłanie zaproszenia do '{invitee}' "
        f"do zasobu {owner}/{name}"
    )

    # TODO: w realnym projekcie:
    # - wywołaj API wysyłające zaproszenie,
    # - obsłuż odpowiedź, statusy błędów, itp.

    return 0


# ======================================================================
# 3. Główna funkcja main() – spina wszystko w całość
# ======================================================================

def main() -> int:
    """
    Główna funkcja uruchamiana po wpisaniu:
        python cli_template.py <komenda> [opcje] [argumenty]

    Odpowiada za:
    - zbudowanie parsera,
    - sparsowanie argumentów z linii poleceń,
    - wybranie odpowiedniego handlera,
    - obsługę ewentualnych wyjątków,
    - zwrócenie kodu wyjścia (dla sys.exit()).
    """

    # 1. Tworzymy parser (konfiguracja komend i argumentów).
    parser = build_parser()

    # 2. Parsujemy argumenty z linii poleceń → powstaje obiekt Namespace.
    #    np. args.command, args.username, args.token, args.verbose, itd.
    args = parser.parse_args()

    # 3. Na podstawie args.command wybieramy, który handler wywołać.
    #    To jest prosty "router" komend.
    try:
        if args.command == "repos":
            return handle_repos(args)

        elif args.command == "repo":
            return handle_repo(args)

        elif args.command == "invite":
            return handle_invite(args)

        # Teoretycznie nie powinniśmy tu trafić przy required=True,
        # ale zostawiamy na wszelki wypadek.
        else:
            parser.print_help()
            return 2  # kod 2 często oznacza błędne użycie programu

    except KeyboardInterrupt:
        # Obsługa Ctrl+C – ładne zakończenie programu.
        print("\nPrzerwano przez użytkownika (Ctrl+C).", file=sys.stderr)
        return 130  # standardowy kod dla SIGINT

    except Exception as exc:
        # Uniwersalny "bezpiecznik" – nie wyrzucamy pełnego trace'a
        # do użytkownika końcowego, tylko prosty komunikat.
        print(f"Nieoczekiwany błąd: {exc}", file=sys.stderr)
        return 1


# ======================================================================
# 4. Standardowy blok uruchomienia skryptu
# ======================================================================

if __name__ == "__main__":
    # Uruchamiamy main() i przekazujemy jego wynik do sys.exit().
    # Dzięki temu CLI zwraca poprawny kod wyjścia do systemu operacyjnego.
    raise SystemExit(main())
