# Mini Explorer CLI

Narzedzie do eksploracji systemu plikow z poziomu terminala.

## Funkcje

- Listowanie plikow w katalogu
- Liczenie plikow i folderow
- Filtrowanie po rozszerzeniu
- Wyswietlanie informacji o pliku (nazwa, rozmiar, typ)

## Technologie

- `argparse` - parsowanie argumentow CLI
- `pathlib` - operacje na sciezkach (nowoczesne podejscie zamiast os.path)
- Flagi: `--count`, `--list`, `--ext`, `--info`

## Jak uruchomic

```bash
python mini_explorer_cli.py .
python mini_explorer_cli.py /sciezka --count
python mini_explorer_cli.py /sciezka --ext .py
python mini_explorer_cli.py /sciezka --info plik.txt
```

## Czego uczy

- Profesjonalne wzorce CLI
- pathlib jako zamiennik os.path
- Obsluga bledow i edge cases
- Czytelna dokumentacja w kodzie
