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

```python
# 1:N - jeden join wystarczy
query(Grade).join(Student).filter(Student.name == "Jan")

# N:M przez tabele asocjacyjna - join po kolei
query(Tag).join(article_tag).join(Article)

# Tabela posrednia - tez join po kolei
query(Student).join(Grade).join(Course).filter(Course.name == "Matematyka")
```

**Zasada:** Nie mozna przeskoczyc tabeli posredniej/asocjacyjnej. Join idzie po kolei.

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

## 13. Dynamiczne sortowanie (mapowanie kolumn)

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

## 14. Cascade i usuwanie

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

## 15. Zagniezdzanie przy tworzeniu (seed)

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

## 16. ForeignKey - ZAWSZE nazwa tabeli (z __tablename__)

```python
# DOBRZE - nazwa tabeli (z 's' jesli tablename ma 's')
student_id = Column(Integer, ForeignKey("students.id"))

# ZLE - nazwa klasy
student_id = Column(Integer, ForeignKey("Student.id"))
```

---

## 17. back_populates - krzyzowe odniesienia

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

## 18. Subquery - zapytanie wewnatrz zapytania

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
- `.scalar_subquery()` → zamienia zapytanie w **pojedyncza wartosc** (do porownania)
- `.c.nazwa_kolumny` → wyciaga kolumne z subquery (`.c` = columns)
- `.label("nazwa")` → nadaje nazwe kolumnie, zeby potem uzyc przez `.c.nazwa`

---

## 19. NOT IN z subquery — "znajdz elementy ktorych NIE MA w innym zbiorze"

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

## 20. Piec pytan przed napisaniem zapytania

1. **CO** chce zobaczyc? → `query(???)`
2. **SKAD** dane? → `.join(???)`
3. **JAKI WARUNEK?** → `.filter(???)`
4. **JAK POGRUPOWAC?** → `.group_by(???)`
5. **JAK POSORTOWAC / ILE?** → `.order_by(???)` / `.limit(???)`

```
CO → SKAD → WARUNEK → GRUPUJ → SORTUJ → ILE
```
