# SQLAlchemy ORM - Sciagawka

Zasady zebrane z cwiczen 01-07. Wracaj tu za kazdym razem gdy nie jestes pewny.

---

## 1. query() = lista zakupow

Co zamowisz w `query()`, to dostaniesz w petli `for`. Nic wiecej.

```python
# OBIEKT - masz dostep do WSZYSTKIEGO (kolumny + relationship)
query(Grade)
for grade in result:
    grade.value          # kolumna
    grade.student.name   # relationship
    grade.course.name    # relationship

# KOLUMNY (tuple) - masz TYLKO to, o co pytasz
query(Student.name, func.avg(Grade.value))
for name, avg in result:
    name    # "Jan" (string)
    avg     # 4.5 (liczba)
    # email? NIE MASZ - nie pytales o email
```

**Zasada:** Przy agregacji (func.avg, func.count) musisz pytac o kolumny, nie o obiekt.

---

## 2. filter() vs filter_by()

```python
# filter_by() - proste kwargs, TA SAMA tabela co w query()
session.query(Student).filter_by(name="Jan")

# filter() - wyrazenia z ==, dowolna tabela, operatory
session.query(Grade).filter(Student.name == "Jan")  # inna tabela niz w query!
session.query(Grade).filter(Grade.value >= 4.0)       # operatory >, <, >=
session.query(Article).filter(Article.tags.any())      # relationship
session.query(Article).filter(~Article.tags.any())     # negacja z ~
```

**Zasada:** Jesli filtrujesz po INNEJ tabeli niz w query() - uzyj `filter()`, nie `filter_by()`.

---

## 3. .first() vs .all() vs .one() vs .scalar()

```python
.all()      # lista (moze byc pusta [])     - BEZPIECZNE
.first()    # jeden obiekt lub None          - SPRAWDZAJ if result:
.one()      # jeden obiekt lub WYJATEK       - gdy MUSISZ miec dokladnie 1
.scalar()   # pojedyncza wartosc (liczba)    - dla func.count(), func.sum()
```

**Zasada:** Po `.first()` ZAWSZE sprawdzaj `if result:` zanim uzyjesz wyniku.

---

## 4. Nawiasy () - wywolanie funkcji

```python
datetime.utcnow     # ZMIENNA wskazujaca na funkcje (NIE wywoluje!)
datetime.utcnow()   # WYWOLANIE funkcji - dostajesz date

result = ...all     # przypisujesz METODE (nie dziala!)
result = ...all()   # WYWOLUJESZ metode - dostajesz liste
```

**Zasada:** Bez `()` przypisujesz referencje do funkcji, nie jej wynik.

---

## 5. Relationship - kropka (.) dziala tak samo dla 1:N i N:M

```python
# 1:N (cwiczenie 03 - Author/Book)
for book in author.written_books:    # lista
    print(book.title)

# N:M (cwiczenie 05 - Article/Tag)
for tag in article.tags:             # lista (wyglada identycznie!)
    print(tag.name)

# Tabela posrednia (cwiczenie 07 - Student/Grade/Course)
for grade in student.grades:         # lista Grade
    print(grade.course.name)         # przez Grade do Course
```

---

## 6. Operacje na listach relationship

```python
article.tags.append(tag)        # dodaj jeden
article.tags.extend([t1, t2])   # dodaj wiele
article.tags.remove(tag)        # usun jeden
article.tags.clear()            # usun wszystkie
article.tags = [t1, t2, t3]    # zamien WSZYSTKIE (jak update)
```

---

## 7. Tabela asocjacyjna vs posrednia

```python
# ASOCJACYJNA - Table() - tylko klucze obce, bez własnych danych
# Uzyj gdy relacja N:M jest CZYSTA (artykuł <-> tag)
article_tag = Table(
    "article_tag",
    Base.metadata,
    Column("article_id", Integer, ForeignKey("articles.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)
# W relationship: secondary=article_tag
# Mozesz zagniezdzac: Article(tags=[Tag(), Tag()])

# POSREDNIA - class Model(Base) - ma własne kolumny (ocena, data, status)
# Uzyj gdy powiazanie NIESIE informacje (student <-> kurs + ocena)
class Grade(Base):
    value = Column(Float)     # dodatkowa dana!
    date = Column(Date)       # dodatkowa dana!
# NIE mozesz zagniezdzac Course w Student
# Zagniezdzasz Grade w Student, a Course podajesz w Grade:
# Student(grades=[Grade(value=5.0, course=math)])
```

---

## 8. JOIN - kolejnosc ma znaczenie

### Sposob 1: Reczny join (krok po kroku)
```python
# 1:N - jeden join wystarczy
query(Grade).join(Student).filter(Student.name == "Jan")

# N:M przez tabele asocjacyjna - join po kolei
query(Tag).join(article_tag).join(Article)

# Tabela posrednia - tez join po kolei
query(Student).join(Grade).join(Course).filter(Course.name == "Matematyka")
```

### Sposob 2: Join przez relationship (SQLAlchemy ogarnia za Ciebie)
```python
# 1:N - przez relacje
query(Grade).join(Grade.student).filter(Student.name == "Jan")

# N:M - SQLAlchemy SAM przechodzi przez tabele asocjacyjna!
query(Tag).join(Tag.posts)    # Tag → post_tag → Post (automatycznie)

# Tabela posrednia - po kolei przez relacje
query(Student).join(Student.grades).join(Grade.course)
```

**Zasada:** Nie mozna przeskoczyc tabeli posredniej/asocjacyjnej. Join idzie po kolei.
Sposob 2 (przez relationship) jest **zalecany** — krotszy, bezpieczniejszy, mniej szans na blad.

### Niejednoznaczny join — wiele FK w jednej tabeli

Gdy tabela ma **wiecej niz jeden ForeignKey** (np. Order ma customer_id i product_id),
SQLAlchemy nie wie po ktorym joinowac. Musisz wskazac **relacje**:

```python
# ❌ BŁĄD — Order ma 2 FK, SQLAlchemy nie wie ktorym joinowac
session.query(func.sum(Product.price * Order.quantity)).join(Product)

# ✅ DOBRZE — wskazujesz relacje: "joinuj przez Order.product"
session.query(func.sum(Product.price * Order.quantity)).join(Order.product)

# ✅ Wiele joinow — kazdy przez relacje
session.query(Customer.name, func.sum(Product.price * Order.quantity))
    .join(Customer.orders)     # Customer → Order (przez relacje "orders")
    .join(Order.product)       # Order → Product (przez relacje "product")
```

**Kiedy to potrzebne?**
- 1 FK w tabeli → `.join(Model)` wystarczy (cwiczenia 01-07)
- 2+ FK w tabeli → `.join(Model.relationship)` konieczne (cwiczenie 08+)

---

## 9. Agregacja - ZAWSZE z group_by

```python
func.count(Grade.id)      # ile
func.sum(Product.price)   # suma
func.avg(Grade.value)     # srednia
func.min(Product.price)   # minimum
func.max(Product.price)   # maksimum
```
```
func.sum(Product.price * Order.quantity)   # suma iloczynów
func.avg(Product.price * Order.quantity)   # średnia iloczynów
func.min(Product.price * Order.quantity)   # najmniejszy iloczyn
func.max(Product.price * Order.quantity)   # największy iloczyn
```

**Zasada:** Kazda kolumna w `query()` ktora NIE jest w func.xxx() MUSI byc w `group_by()`.

```python
query(Student.name, func.avg(Grade.value))  # Student.name nie jest w func
.group_by(Student.name)                      # wiec MUSI byc w group_by
```

---

## 10. HAVING - filtrowanie PO grupowaniu

```python
# WHERE (filter) - filtruje PRZED grupowaniem
# HAVING - filtruje PO grupowaniu (na wynikach agregacji)

query(Student.name, func.avg(Grade.value))
.join(Student)
.group_by(Student.name)
.having(func.avg(Grade.value) >= 4.0)    # powtorz cale wyrazenie func.avg!
```

**Zasada:** W `having()` musisz powtorzyc cale wyrazenie agregujace - nie mozesz uzyc .label().

---

## 11. Paginacja

```python
offset = (page - 1) * per_page    # ile rekordow pominac
total_pages = math.ceil(total / per_page)  # ile stron łącznie

query(Movie).offset(offset).limit(per_page).all()
```

**Zasada:** `total` musi liczyc PRZEFILTROWANE rekordy, nie wszystkie.

---

## 12. Wyszukiwanie tekstu

```python
# ilike = case-insensitive LIKE
Movie.title.ilike(f"%{fragment}%")    # f-string z %!

# between - zakres
Movie.year.between(year_from, year_to)

# in_ - lista wartosci
Tag.name.in_(["python", "orm", "sql"])
```

---

## 13. Operatory warunkow w filter()

### Porownania:
```python
.filter(Post.id == 5)             # rowne
.filter(Post.id != 5)             # rozne
.filter(Post.id > 5)              # wieksze
.filter(Post.id >= 5)             # wieksze lub rowne
.filter(Post.id < 5)              # mniejsze
.filter(Post.id <= 5)             # mniejsze lub rowne
```

### Tekst:
```python
.filter(Post.title.ilike("%python%"))  # zawiera (case-insensitive)
.filter(Post.title.like("%Python%"))   # zawiera (case-sensitive)
.filter(Post.title.startswith("Py"))   # zaczyna sie od
.filter(Post.title.endswith("on"))     # konczy sie na
```

### Listy i zakresy:
```python
.filter(Tag.name.in_(["python", "orm"]))      # IN — jedna z wartosci
.filter(~Tag.name.in_(["python", "orm"]))      # NOT IN — zadna z wartosci
.filter(Post.id.between(5, 10))                # BETWEEN 5 AND 10
```

### NULL:
```python
.filter(Post.category_id.is_(None))      # IS NULL
.filter(Post.category_id.is_not(None))   # IS NOT NULL
# lub:
.filter(Post.category_id == None)        # IS NULL (tez dziala)
.filter(Post.category_id != None)        # IS NOT NULL
```

### Łączenie warunkow:
```python
from sqlalchemy import and_, or_

# AND — trzy rownowazne sposoby:
.filter(Post.is_published == True, Post.id > 5)          # przecinek = AND
.filter(and_(Post.is_published == True, Post.id > 5))    # jawne and_()

# OR:
.filter(or_(Post.id == 1, Post.id == 2))                 # jawne or_()

# NOT:
.filter(~Post.tags.any())                                 # tylda = NOT
```

### Relacje (.any / ~.any):
```python
.filter(Post.tags.any(Tag.name == "python"))    # ma JAKIS tag "python"
.filter(~Post.tags.any())                        # NIE MA zadnych tagow
.filter(Post.comments.any())                     # MA jakies komentarze
```

**WAZNE:** Nigdy nie uzywaj Pythonowego `and` / `or` w filter()!
```python
# ❌ ZLE — Python ewaluuje to po swojemu!
.filter(Post.id > 5 and Post.is_published == True)

# ✅ DOBRZE — uzyj przecinka lub and_()
.filter(Post.id > 5, Post.is_published == True)
```

---

## 14. Dynamiczne sortowanie (mapowanie kolumn)

```python
columns = {
    "rating": Movie.rating,
    "year": Movie.year,
    "title": Movie.title,
}
sort_column = columns.get(sort_by, Movie.title)  # domyslnie po tytule
query(Movie).order_by(desc(sort_column))
```

**Zasada:** Nie przekazujesz stringa do order_by - mapujesz string na kolumne.

---

## 15. Cascade i usuwanie

```python
# BULK DELETE - pomija kaskade Pythona!
session.query(Author).delete()  # NIE usunie ksiazek automatycznie!

# OBJECT DELETE - uruchamia kaskade
author = session.query(Author).first()
session.delete(author)  # USUNIE tez ksiazki (jesli cascade="all, delete-orphan")
```

**Kolejnosc czyszczenia tabel (bez kaskady):** dzieci najpierw, rodzice na koncu.
```python
session.query(Grade).delete()    # najpierw tabela posrednia
session.query(Course).delete()   # potem rodzic
session.query(Student).delete()  # potem rodzic
```

---

## 16. Zagniezdzanie przy tworzeniu (seed)

```python
# ZAWSZE: dzieci wewnatrz rodzica, NIE rodzic wewnatrz dziecka

# 1:N - Book wewnatrz Author
author = Author(
    name="Tolkien",
    written_books=[Book(title="Hobbit"), Book(title="LOTR")]
)

# Tabela posrednia - Grade wewnatrz Student, Course jako zmienna
math = Course(name="Matematyka", instructor="Kowalski")
student = Student(
    name="Jan",
    grades=[Grade(value=5.0, date=date.today(), course=math)]
)
```

---

## 17. ForeignKey - ZAWSZE nazwa tabeli (z __tablename__)

```python
# DOBRZE - nazwa tabeli (z 's' jesli tablename ma 's')
student_id = Column(Integer, ForeignKey("students.id"))

# ZLE - nazwa klasy
student_id = Column(Integer, ForeignKey("Student.id"))
```

---

## 18. back_populates - krzyzowe odniesienia

```python
# Student
grades = relationship("Grade", back_populates="student")
#                                               ^^^^^^^^
#                                     nazwa atrybutu W GRADE

# Grade
student = relationship("Student", back_populates="grades")
#                                                 ^^^^^^
#                                       nazwa atrybutu W STUDENT
```

**Zasada:** Kazdy `back_populates` wskazuje na atrybut W DRUGIEJ klasie, nie w swojej.

---

## 19. Subquery - zapytanie wewnatrz zapytania

Gdy potrzebujesz wyniku jednego zapytania w drugim (np. "klienci powyzej sredniej").

```python
# KROK 1: Subquery — policz sume wydatkow KAZDEGO klienta
customer_totals = (
    session.query(func.sum(Product.price * Order.quantity).label("total"))
    .join(Product)
    .group_by(Order.customer_id)
    .subquery()                     # zamienia zapytanie w "tabele"
)

# KROK 2: scalar_subquery — policz srednia z tych sum (pojedyncza wartosc)
avg_spending = (
    session.query(func.avg(customer_totals.c.total))
    .scalar_subquery()              # zamienia zapytanie w JEDNA wartosc
)
#                         ^^
#            .c = "columns" — dostep do kolumn subquery
#            .total = nazwa z .label("total")

# KROK 3: Główne zapytanie — uzyj avg_spending jako wartosc do porownania
result = (
    session.query(Customer.name, func.sum(Product.price * Order.quantity))
    .join(Order).join(Product)
    .group_by(Customer.name)
    .having(func.sum(Product.price * Order.quantity) > avg_spending)
    .all()
)
```

**Kluczowe:**
- `.subquery()` → zamienia zapytanie w "tabele" (do uzycia w innym query)
- `.scalar_subquery()` → zamienia zapytanie w **pojedyncza wartosc** (do porownania w innym query)
- `.scalar()` → **wykonuje** zapytanie i zwraca **wynik** (liczbe, string, None)
- `.c.nazwa_kolumny` → wyciaga kolumne z subquery (`.c` = columns)
- `.label("nazwa")` → nadaje nazwe kolumnie, zeby potem uzyc przez `.c.nazwa`

**UWAGA: `.scalar()` vs `.scalar_subquery()` — NIE POMYL!**
```python
# .scalar() → WYKONUJE zapytanie, zwraca wartosc (do printa, do zmiennej)
result = session.query(func.avg(sub.c.cnt)).scalar()
print(result)  # np. 1.875

# .scalar_subquery() → tworzy WYRAZENIE SQL (do uzycia w having/filter)
avg_val = session.query(func.avg(sub.c.cnt)).scalar_subquery()
session.query(...).having(... > avg_val)  # uzycie w innym zapytaniu
```

---

## 20. NOT IN z subquery — "znajdz elementy ktorych NIE MA w innym zbiorze"

Dziala jak operacje na zbiorach:
- Zbior A = wszystkie produkty
- Zbior B = zamowione produkty (ID z tabeli Order)
- Wynik = A minus B (produkty ktorych NIE MA w zamowieniach)

```python
# Wzorzec: "Znajdz X, ktore NIE SA w Y"

# Krok 1: Zbior B — lista ID ktore SA w uzyciu
ordered_ids = session.query(Order.product_id).subquery()

# Krok 2: Zbior A minus B — elementy ktore NIE SA w zbiorze B
result = session.query(Product).filter(~Product.id.in_(ordered_ids)).all()
```

**Inne przyklady tego wzorca:**
```python
# Studenci bez ocen:
graded_ids = session.query(Grade.student_id).subquery()
result = session.query(Student).filter(~Student.id.in_(graded_ids)).all()

# Klienci bez zamowien:
customer_ids = session.query(Order.customer_id).subquery()
result = session.query(Customer).filter(~Customer.id.in_(customer_ids)).all()
```

**Zasada:** `~Model.id.in_(subquery)` = "daj mi te, ktorych ID NIE MA na liscie"

---

## 21. func.extract() - wyciaganie czesci z daty (PostgreSQL)

Gdy masz kolumne typu `Date` lub `DateTime` i chcesz pracowac z rokiem, miesiacem, dniem osobno.

```python
from sqlalchemy import func

# Wyciaganie czesci daty:
func.extract('year', Reservation.check_in)     # rok (np. 2026)
func.extract('month', Reservation.check_in)    # miesiac (np. 1 = styczen)
func.extract('day', Reservation.check_in)      # dzien (np. 15)
```

**Dwa zastosowania:**

```python
# 1. FILTROWANIE - "daj rezerwacje ze stycznia 2026"
.filter(
    func.extract('year', Reservation.check_in) == 2026,
    func.extract('month', Reservation.check_in) == 1
)

# 2. GRUPOWANIE - "podsumuj sprzedaz per miesiac"
.group_by(func.extract('month', Order.order_date))
```

**SQLite vs PostgreSQL:**
- SQLite: `func.strftime('%m', kolumna)` — zwraca string ("01", "02")
- PostgreSQL: `func.extract('month', kolumna)` — zwraca liczbe (1, 2)

**Zasada:** `func.extract` mozna uzyc wszedzie tam, gdzie normalnie uzyjesz kolumny:
w `filter()`, `group_by()`, `order_by()`, a nawet w `query()`.

---

## 22. .any() i ~.any() — sprawdzanie relacji N:M (i 1:N)

Gdy chcesz filtrowac po powiazanych obiektach BEZ pisania joinow.

```python
# Post ma JAKIS tag o nazwie "python"?
.filter(Post.tags.any(Tag.name == "python"))

# Post NIE MA zadnego tagu "python"?
.filter(~Post.tags.any(Tag.name == "python"))
```

**Kiedy uzywac:**
- `.any()` działa na relacjach (`relationship`) — nie potrzeba `.join()`!
- Idealne do relacji N:M (np. Post ↔ Tag przez tabele asocjacyjna)
- Działa tez na 1:N (np. "Posty ktore MAJA komentarze")

**Przykłady:**
```python
# Posty z tagiem "fastapi"
session.query(Post).filter(Post.tags.any(Tag.name == "fastapi")).all()

# Posty BEZ komentarzy (1:N)
session.query(Post).filter(~Post.comments.any()).all()

# Uzytkownicy ktorzy napisali JAKIS post
session.query(User).filter(User.posts.any()).all()

# Uzytkownicy ktorzy NIGDY nie komentowali
session.query(User).filter(~User.comments.any()).all()
```

**Zasada:**
- `.any()` = "czy istnieje CHOC JEDEN powiazany obiekt spelniajacy warunek"
- `~.any()` = "ZADEN powiazany obiekt nie spelnia warunku" (NOT)
- `.any()` bez argumentow = "czy istnieje JAKIKOLWIEK powiazany obiekt"

---

## 23. case() — warunkowe wartosci w zapytaniu (IF/ELSE w SQL)

Gdy chcesz policzyc rozne rzeczy w JEDNYM zapytaniu zamiast robic kilka osobnych.

```python
from sqlalchemy import case

# Skladnia:
case((WARUNEK, WARTOSC_GDY_TRUE), else_=WARTOSC_GDY_FALSE)
```

**Jak dziala — przyklad:**
```
Post A | is_published=True  → case daje 1
Post B | is_published=True  → case daje 1
Post C | is_published=False → case daje 0
func.sum(...) → 2 opublikowane, 1 draft
```

**Uzycie z func.sum — "warunkowe liczenie":**
```python
# Ile postow opublikowanych vs draftow na autora
session.query(
    User.username,
    func.sum(case((Post.is_published == True, 1), else_=0)).label("published"),
    func.sum(case((Post.is_published == False, 1), else_=0)).label("drafts")
)
.join(User.posts)
.group_by(User.username)
.all()
```

**Wynik:**
```
robert | published: 3 | drafts: 2
anna   | published: 5 | drafts: 0
```

**Kiedy uzywac:**
- Chcesz policzyc ROZNE KATEGORIE w jednym zapytaniu
- Zamiast 2-3 osobnych zapytań z roznymi filtrami
- Dziala z `func.sum`, `func.count`, `func.avg`

**Zasada:** `case()` zamienia warunek na wartosc (1 lub 0), a `func.sum()` sumuje te wartosci.

---

## 24. Piec pytan przed napisaniem zapytania

1. **CO** chce zobaczyc? → `query(???)`
2. **SKAD** dane? → `.join(???)`
3. **JAKI WARUNEK?** → `.filter(???)`
4. **JAK POGRUPOWAC?** → `.group_by(???)`
5. **JAK POSORTOWAC / ILE?** → `.order_by(???)` / `.limit(???)`

```
CO → SKAD → WARUNEK → GRUPUJ → SORTUJ → ILE
```
