# 10 - Blog CMS (Kompletny system)

## Trudnosc: ⭐⭐⭐⭐⭐ (Ekspert)

## Cel
Zbuduj kompletny system zarzadzania trescia (CMS) laczacy wszystkie poznane koncepcje.

## Baza danych
- **PostgreSQL** (wymaga serwera PostgreSQL)

## Model danych

### User (Uzytkownik)
| Kolumna | Typ | Ograniczenia |
|---------|-----|-------------|
| id | Integer | Primary Key |
| username | String(50) | NOT NULL, UNIQUE |
| email | String(100) | NOT NULL, UNIQUE |
| role | String(20) | default="author" (admin/author/reader) |
| created_at | DateTime | default=utcnow |

### Category (Kategoria)
| Kolumna | Typ | Ograniczenia |
|---------|-----|-------------|
| id | Integer | Primary Key |
| name | String(100) | NOT NULL, UNIQUE |
| description | Text | opcjonalny |

### Post (Wpis)
| Kolumna | Typ | Ograniczenia |
|---------|-----|-------------|
| id | Integer | Primary Key |
| title | String(200) | NOT NULL |
| content | Text | NOT NULL |
| is_published | Boolean | default=False |
| created_at | DateTime | default=utcnow |
| updated_at | DateTime | onupdate=utcnow |
| author_id | Integer | FK -> User.id |
| category_id | Integer | FK -> Category.id |

### Tag
| Kolumna | Typ | Ograniczenia |
|---------|-----|-------------|
| id | Integer | Primary Key |
| name | String(50) | NOT NULL, UNIQUE |

### Comment (Komentarz)
| Kolumna | Typ | Ograniczenia |
|---------|-----|-------------|
| id | Integer | Primary Key |
| content | Text | NOT NULL |
| created_at | DateTime | default=utcnow |
| author_id | Integer | FK -> User.id |
| post_id | Integer | FK -> Post.id |

### post_tag (Tabela asocjacyjna)
| Kolumna | Typ |
|---------|-----|
| post_id | FK -> Post.id, PK |
| tag_id | FK -> Tag.id, PK |

### Relacje
- User -> Post: 1:N (autor postow)
- User -> Comment: 1:N (autor komentarzy)
- Category -> Post: 1:N
- Post <-> Tag: N:M (przez post_tag)
- Post -> Comment: 1:N (cascade delete)

## Zadania

### Zadanie 1: Modele i seedowanie
- Zdefiniuj wszystkie 5 modeli + tabele asocjacyjna
- Dodaj 3 userow (1 admin, 2 authorow)
- Dodaj 4 kategorie, 8 tagow
- Dodaj 10 postow (niektore opublikowane, inne jako draft)
- Dodaj 15+ komentarzy

### Zadanie 2: CRUD na postach
- Utworz nowy post z tagami i kategoria
- Edytuj tresc posta (updated_at powinno sie zaktualizowac)
- Opublikuj draft (is_published = True)
- Usun post (kaskadowo z komentarzami)

### Zadanie 3: Zapytania relacyjne
- Wszystkie posty danego autora
- Wszystkie komentarze pod postem (z autorami)
- Posty w danej kategorii
- Posty z danym tagiem
- Posty ktore maja tag "python" ORAZ sa opublikowane

### Zadanie 4: Agregacje i statystyki
- Liczba postow na autora
- Liczba komentarzy na post
- Srednia liczba komentarzy na post (subquery)
- Najpopularniejszy tag (najwiecej postow)
- Kategoria z najwieksza liczba opublikowanych postow
- Najaktywniejszy komentujacy

### Zadanie 5: Zaawansowane zapytania
- Ranking autorow po liczbie opublikowanych postow
- Posty bez komentarzy
- Posty z wiecej niz 3 komentarzami (HAVING)
- Ostatnie 5 komentarzy w calym systemie (z nazwami postow i autorow)
- Statystyki: ile postow jest draft vs opublikowanych na autora

## Podpowiedzi
- `onupdate=datetime.utcnow` w kolumnie updated_at
- `cascade="all, delete-orphan"` na relacji Post -> Comment
- Subquery: `session.query(func.count(Comment.id)).filter(Comment.post_id == Post.id).correlate(Post).scalar_subquery()`
- `selectinload()` dla eager loading relacji
- `~Post.comments.any()` - posty bez komentarzy

## Przykladowy output
```
--- Posty autora: Jan Kowalski ---
1. [OPUBLIKOWANY] Wprowadzenie do Pythona | Technologia | python, tutorial
2. [DRAFT] Zaawansowany SQL | Technologia | sql, bazy-danych
3. [OPUBLIKOWANY] Flask REST API | Technologia | python, api

--- Statystyki ---
Laczna liczba postow: 10
Opublikowane: 7 | Drafty: 3
Srednia komentarzy na post: 2.1

--- Ranking autorow ---
1. Jan Kowalski - 5 postow (4 opublikowane)
2. Anna Nowak - 3 posty (2 opublikowane)
3. Admin - 2 posty (1 opublikowany)

--- Najpopularniejszy tag ---
python (5 postow)
```
