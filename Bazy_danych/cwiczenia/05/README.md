# 05 - System tagow (Relacja wiele-do-wielu)

## Trudnosc: ⭐⭐⭐ (Sredniozaawansowany+)

## Cel
Przecwicz relacje wiele-do-wielu (N:M) z tabela asocjacyjna.

## Baza danych
- **SQLite** (plik `articles.db`)

## Model danych

### Article (Artykul)
| Kolumna | Typ | Ograniczenia |
|---------|-----|-------------|
| id | Integer | Primary Key |
| title | String(200) | NOT NULL |
| content | Text | NOT NULL |
| created_at | DateTime | default=datetime.utcnow |

### Tag
| Kolumna | Typ | Ograniczenia |
|---------|-----|-------------|
| id | Integer | Primary Key |
| name | String(50) | NOT NULL, UNIQUE |

### article_tag (Tabela asocjacyjna)
| Kolumna | Typ | Ograniczenia |
|---------|-----|-------------|
| article_id | Integer | FK -> Article.id, PK |
| tag_id | Integer | FK -> Tag.id, PK |

### Relacje
- Article <-> Tag: wiele-do-wielu przez tabele article_tag
- Uzyj `Table()` do tabeli asocjacyjnej
- Uzyj `relationship()` z parametrem `secondary`

## Zadania

### Zadanie 1: Modele i seedowanie
- Zdefiniuj tabele asocjacyjna `article_tag` za pomoca `Table()`
- Zdefiniuj modele Article i Tag z relacja N:M
- Dodaj 5 artykulow i 6 tagow
- Przypisz po 2-3 tagi do kazdego artykulu

### Zadanie 2: Zapytania relacyjne
- Wyswietl wszystkie tagi danego artykulu
- Wyswietl wszystkie artykuly z danym tagiem
- Znajdz artykuly ktore maja tag "python" I tag "tutorial"

### Zadanie 3: Modyfikacja relacji
- Dodaj nowy tag do istniejacego artykulu
- Usun tag z artykulu (bez usuwania samego taga)
- Zamien wszystkie tagi artykulu na nowe

### Zadanie 4: Statystyki
- Policz ile artykulow ma kazdy tag
- Znajdz najpopularniejszy tag (najwiecej artykulow)
- Znajdz artykuly bez tagow (jesli sa)

## Podpowiedzi
- Tabela asocjacyjna: `Table("article_tags", Base.metadata, Column(...), Column(...))`
- Relacja: `tags = relationship("Tag", secondary=article_tag, back_populates="articles")`
- Dodawanie taga: `article.tags.append(tag)`
- Usuwanie taga: `article.tags.remove(tag)`
- Zapytanie przez tag: `session.query(Article).filter(Article.tags.any(Tag.name == "python"))`

## Przykladowy output
```
--- Tagi artykulu "Wprowadzenie do SQLAlchemy" ---
python, sql, tutorial

--- Artykuly z tagiem "python" ---
1. Wprowadzenie do SQLAlchemy
2. Flask dla poczatkujacych
3. Automatyzacja z Python

--- Najpopularniejszy tag ---
python (3 artykuly)

--- Dodawanie taga ---
Dodano tag "orm" do artykulu "Wprowadzenie do SQLAlchemy"
Nowe tagi: python, sql, tutorial, orm
```
