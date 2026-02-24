import sys
sys.stdout.reconfigure(encoding='utf-8')
from models import Base, User, Category, Post, Tag, Comment, post_tag
from db import engine, SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, text, desc, and_, case
from datetime import datetime, timedelta


def create_tables():
    """Tworzy tabele w bazie danych."""
    Base.metadata.create_all(engine)

def clear_all_tables(session):
    session.execute(post_tag.delete())
    session.query(Tag).delete()
    session.query(Comment).delete()
    session.query(Post).delete()
    session.query(Category).delete()
    session.query(User).delete()
    session.execute(text("ALTER SEQUENCE users_id_seq RESTART WITH 1"))
    session.execute(text("ALTER SEQUENCE categories_id_seq RESTART WITH 1"))
    session.execute(text("ALTER SEQUENCE posts_id_seq RESTART WITH 1"))
    session.execute(text("ALTER SEQUENCE tags_id_seq RESTART WITH 1"))
    session.execute(text("ALTER SEQUENCE comments_id_seq RESTART WITH 1"))
    session.commit()




def seed_data(session):
    """Zadanie 1: Dodaj userów, kategorie, tagi, posty i komentarze."""
    # TODO: Kompletne seedowanie


    now = datetime.utcnow()

    # --- USERS (3: 1 admin, 2 authors) ---
    admin = User(
        username="admin",
        email="admin@example.com",
        role="admin",
        created_at=now - timedelta(days=120),
    )
    author_1 = User(
        username="robert",
        email="robert@example.com",
        role="author",
        created_at=now - timedelta(days=90),
    )
    author_2 = User(
        username="anna",
        email="anna@example.com",
        role="author",
        created_at=now - timedelta(days=60),
    )

    session.add_all([admin, author_1, author_2])

    # --- CATEGORIES (4) ---
    cat_python = Category(
        name="Python",
        description="Python od podstaw po backend i narzędzia."
    )
    cat_databases = Category(
        name="Bazy danych",
        description="SQL, ORM, modelowanie, migracje, indeksy."
    )
    cat_web = Category(
        name="Web Backend",
        description="API, architektura, frameworki, bezpieczeństwo."
    )
    cat_testing = Category(
        name="Testowanie",
        description="pytest, unittest, mocki, CI i dobre praktyki."
    )

    session.add_all([cat_python, cat_databases, cat_web, cat_testing])

    # --- TAGS (8) ---
    tag_python = Tag(name="python")
    tag_sqlalchemy = Tag(name="sqlalchemy")
    tag_orm = Tag(name="orm")
    tag_django = Tag(name="django")
    tag_fastapi = Tag(name="fastapi")
    tag_api = Tag(name="api")
    tag_pytest = Tag(name="pytest")
    tag_best_practices = Tag(name="best-practices")

    session.add_all([
        tag_python, tag_sqlalchemy, tag_orm, tag_django,
        tag_fastapi, tag_api, tag_pytest, tag_best_practices
    ])

    # --- POSTS (10) ---
    # Post: user, category, tags=[...]
    post_1 = Post(
        title="Python: zmienne, typy danych i pułapki",
        content="Krótki przegląd typów danych, konwersji i typowych błędów początkujących.",
        is_published=True,
        created_at=now - timedelta(days=30),
        updated_at=now - timedelta(days=28),
        user=author_1,
        category=cat_python,
        tags=[tag_python, tag_best_practices],
    )
    post_2 = Post(
        title="SQLAlchemy ORM: modele i sesja w praktyce",
        content="Jak zdefiniować modele, stworzyć sesję i wykonać podstawowe operacje CRUD.",
        is_published=True,
        created_at=now - timedelta(days=26),
        updated_at=now - timedelta(days=25),
        user=author_1,
        category=cat_databases,
        tags=[tag_python, tag_sqlalchemy, tag_orm],
    )
    post_3 = Post(
        title="Relacje 1:N i N:M w ORM — jak tego nie zepsuć",
        content="Relacje, cascade, back_populates oraz typowe problemy z duplikacją i N+1.",
        is_published=True,
        created_at=now - timedelta(days=22),
        updated_at=now - timedelta(days=21),
        user=author_2,
        category=cat_databases,
        tags=[tag_sqlalchemy, tag_orm, tag_best_practices],
    )
    post_4 = Post(
        title="Django vs FastAPI: co wybrać do projektu backendowego",
        content="Porównanie podejścia, szybkości developmentu, ekosystemu i typowych zastosowań.",
        is_published=True,
        created_at=now - timedelta(days=20),
        updated_at=now - timedelta(days=19),
        user=author_2,
        category=cat_web,
        tags=[tag_django, tag_fastapi, tag_api],
    )
    post_5 = Post(
        title="REST API: sensowne endpointy i walidacja danych",
        content="Jak projektować API, jak walidować wejście i jak nie robić chaosu w zasobach.",
        is_published=True,
        created_at=now - timedelta(days=17),
        updated_at=now - timedelta(days=16),
        user=author_1,
        category=cat_web,
        tags=[tag_api, tag_best_practices],
    )
    post_6 = Post(
        title="pytest: najważniejsze wzorce do testów w Pythonie",
        content="Fixture, parametrize, mockowanie i jak pisać testy, które mają sens.",
        is_published=True,
        created_at=now - timedelta(days=14),
        updated_at=now - timedelta(days=13),
        user=author_2,
        category=cat_testing,
        tags=[tag_pytest, tag_python, tag_best_practices],
    )
    post_7 = Post(
        title="Draft: jak ogarnąć strukturę projektu backendowego",
        content="Szkic: foldery, warstwy, serwisy, repozytoria, spójne nazewnictwo.",
        is_published=False,
        created_at=now - timedelta(days=12),
        updated_at=now - timedelta(days=12),
        user=author_1,
        category=cat_web,
        tags=[tag_best_practices],
    )
    post_8 = Post(
        title="Draft: migracje i wersjonowanie bazy — plan minimum",
        content="Szkic: po co migracje, jak dbać o spójność środowisk i jak nie psuć produkcji.",
        is_published=False,
        created_at=now - timedelta(days=10),
        updated_at=now - timedelta(days=10),
        user=author_2,
        category=cat_databases,
        tags=[tag_sqlalchemy, tag_best_practices],
    )
    post_9 = Post(
        title="SQLAlchemy: wydajność i problem N+1",
        content="selectinload/joinedload, kiedy join, a kiedy lazy loading i dlaczego boli.",
        is_published=True,
        created_at=now - timedelta(days=8),
        updated_at=now - timedelta(days=7),
        user=author_1,
        category=cat_databases,
        tags=[tag_sqlalchemy, tag_orm, tag_best_practices],
    )
    post_10 = Post(
        title="FastAPI: sensowne schematy i dokumentacja",
        content="Pydantic, walidacja, OpenAPI/Swagger i minimalny zestaw dobrych praktyk.",
        is_published=True,
        created_at=now - timedelta(days=5),
        updated_at=now - timedelta(days=4),
        user=author_2,
        category=cat_web,
        tags=[tag_fastapi, tag_api, tag_best_practices],
    )

    posts = [post_1, post_2, post_3, post_4, post_5, post_6, post_7, post_8, post_9, post_10]
    session.add_all(posts)

    # --- COMMENTS (15+) ---
    # Zagnieżdżamy w Post.comments 
    post_1.comments = [
        Comment(content="Fajnie w punkt, szczególnie o konwersji typów.", created_at=now - timedelta(days=29), user=admin),
        Comment(content="Dodałbym jeszcze coś o bool('0') i bool('False').", created_at=now - timedelta(days=29), user=author_2),
    ]
    post_2.comments = [
        Comment(content="Super, wreszcie ktoś jasno tłumaczy sesję.", created_at=now - timedelta(days=25), user=author_2),
        Comment(content="Możesz dopisać przykład flush vs commit.", created_at=now - timedelta(days=24), user=admin),
    ]
    post_3.comments = [
        Comment(content="Relacje N:M zawsze mnie bolały — dzięki.", created_at=now - timedelta(days=21), user=author_1),
        Comment(content="Dobre przypomnienie o cascade i orphan.", created_at=now - timedelta(days=21), user=admin),
    ]
    post_4.comments = [
        Comment(content="Django wygrywa adminem, ale FastAPI jest szybsze do MVP.", created_at=now - timedelta(days=19), user=author_1),
        Comment(content="Przydałby się case: projekt z auth + panel admina.", created_at=now - timedelta(days=18), user=admin),
    ]
    post_5.comments = [
        Comment(content="Walidacja wejścia to podstawa, ludzie to ignorują.", created_at=now - timedelta(days=16), user=admin),
    ]
    post_6.comments = [
        Comment(content="Parametrize i fixture uratowały mi życie.", created_at=now - timedelta(days=13), user=author_1),
        Comment(content="Daj proszę przykład patchowania funkcji w module.", created_at=now - timedelta(days=13), user=admin),
        Comment(content="Mock vs MagicMock — temat rzeka.", created_at=now - timedelta(days=12), user=author_2),
    ]
    post_7.comments = [
        Comment(content="Ten szkic ma sens, czekam na wersję finalną.", created_at=now - timedelta(days=11), user=admin),
    ]
    post_8.comments = [
        Comment(content="Migracje to temat, który zawsze jest odkładany…", created_at=now - timedelta(days=9), user=author_1),
    ]
    post_9.comments = [
        Comment(content="N+1 to najczęstszy killer wydajności u juniorów.", created_at=now - timedelta(days=7), user=admin),
        Comment(content="selectinload w praktyce robi robotę.", created_at=now - timedelta(days=7), user=author_2),
    ]
    post_10.comments = [
        Comment(content="Swagger w FastAPI to złoto, fajnie że o tym piszesz.", created_at=now - timedelta(days=4), user=author_1),
        Comment(content="Dobrze byłoby dodać przykład błędów 422 i walidacji.", created_at=now - timedelta(days=4), user=admin),
    ]

    session.commit()
    print("Dodano posty, tagi i komentarze")







def create_post(session, author_id, category_id, title, content, tag_names):
    """Zadanie 2a: Utworz nowy post z tagami."""
    # TODO: Utworz post i przypisz tagi

    try:
        tags = session.query(Tag).filter(Tag.name.in_(tag_names)).all()

        found_names = {tag.name for tag in tags}
        missing = set(tag_names)-found_names #różnica zbiorów( przekazany parametr tag_names - found_names)
        if missing:
            print(f"Nie znaleziono tagów: {missing}")
            return

        new_post = Post(
            title=title,
            content=content,
            author_id=author_id,
            category_id=category_id,
            tags=tags
        )
        session.add(new_post)
        session.commit()
        print(f"utworzono posta {title}")

    except SQLAlchemyError as e:
        session.rollback()
        print(f"Bład: {e}")





def edit_post(session, post_id, new_content):
    """Zadanie 2b: Edytuj tresc posta."""
    # TODO: Zaktualizuj content (updated_at powinno sie zmienic)
    post_result = session.query(Post).filter_by(id=post_id).first()
    if post_result:
        post_result.content = new_content
        post_result.updated_at = datetime.utcnow()
        session.commit()
        print(f"Zaktualizowano post  '{post_result.title}' ")
    else:
        print("Nie znaleziono postu")


def publish_post(session, post_id):
    """Zadanie 2c: Opublikuj draft."""
    # TODO: Zmien is_published na True
    result = session.query(Post).filter(Post.id == post_id).first()
    if result:
        result.is_published = True
        session.commit()
        print(f"Zmieniono status {result.title}")
    else:
        print("Nie znaleziono postu do zmiany")




def delete_post(session, post_id):
    """Zadanie 2d: Usun post kaskadowo."""
    # TODO: Usun post (komentarze powinny zniknac automatycznie)
    try:

        post = session.query(Post).filter(Post.id == post_id).first()
        if post:
            title = post.title
            session.delete(post)
            session.commit()
            print(f"Usunięto post: '{title}' (komentarze usunięte kaskadowo)")
           
        else:
            print("Nie znaleziono postu...")

    except SQLAlchemyError as e:
        session.rollback()
        print(f"Błąd: {e}")





def posts_by_author(session, username):
    """Zadanie 3a: Posty autora."""
    # TODO: Join z User
    result = (
        session.query(Post)
        .join(Post.user)
        .filter(User.username == username)
        .all()        
        )
    for post in result:
        print(f"Posty autora: {username}: {post.title}")





def comments_on_post(session, post_id):
    """Zadanie 3b: Komentarze pod postem."""
    # TODO: Join z User (autor komentarza)

    result = (
        session.query(Comment.content, User.username)
        .join(Comment.user)
        .filter(Comment.post_id == post_id)
        .order_by(desc(Comment.created_at))
        .all()
        )
    for content, username in result:
        print(f"{username}: {content}")





def posts_in_category(session, category_name):
    """Zadanie 3c: Posty w kategorii."""
    result = (
        session.query(Post)
        .join(Post.category)
        .filter(Category.name == category_name)
        .all()
        )
    for post in result:
        print(f"Kategoria {category_name} | Posty: {post.title}")




def posts_with_tag(session, tag_name):
    """Zadanie 3d: Posty z tagiem."""
    # TODO: Uzyj Post.tags.any()
    
    result = (
        session.query(Post)        
        .filter(Post.tags.any(Tag.name == tag_name))
        .all()
        )
    for post in result:
        print(f"Tag: {tag_name} | Posty: {post.title}")





def published_posts_with_tag(session, tag_name):
    """Zadanie 3e: Opublikowane posty z tagiem."""
    # TODO: Połącz filtr published + tag
    result = (
        session.query(Post)
        .filter(and_(Post.tags.any(Tag.name == tag_name), (Post.is_published == True)))
        .all()
        )    
    for post in result:
        print(f"Opublikowane posty: {tag_name} | posty: {post.title}")






def posts_per_author(session):
    """Zadanie 4a: Liczba postow na autora."""
    result = (
        session.query(User.username, func.count(Post.id))
        .join(User.posts)
        .group_by(User.username)
        .order_by(desc(func.count(Post.id)))
        .all()
        )
    for name, total in result:
        print(f"Autor {name}, liczba postów: {total}")





def comments_per_post(session):
    """Zadanie 4b: Liczba komentarzy na post."""
    result = (
        session.query(Post.title, func.count(Comment.id))
        .join(Post.comments)
        .group_by(Post.title)
        .order_by(desc(func.count(Comment.id)))
        .all()
        )
    for title, total in result:
        print(f"Post: {title}, liczba komentarzy: {total}")





def avg_comments_per_post(session):
    """Zadanie 4c: Srednia komentarzy na post."""
    # TODO: Uzyj subquery
    
    count_posts = (
        session.query(Post.title, func.count(Comment.id).label("cnt"))
        .join(Post.comments)
        .group_by(Post.title)
        .subquery()
        )

    result = session.query(func.avg(count_posts.c.cnt)).scalar()

    print(f"Średnia komentarzy na post: {result:.2f}")



def most_popular_tag(session):
    """Zadanie 4d: Najpopularniejszy tag."""
    result = (
        session.query(Tag.name, func.count(Post.id))        
        .join(Tag.posts)
        .group_by(Tag.name)
        .order_by(desc(func.count(Post.id)))
        .first()
        )
    if result:
        name, total = result
        print(f"najpopularniejszy tag: {name}, ilość użyć: {total}")





def top_category(session):
    """Zadanie 4e: Kategoria z najwieksza liczba opublikowanych postow."""
    
    result = (
        session.query(Category.name, func.count(Post.id))
        .join(Category.posts)
        .filter(Post.is_published == True)
        .group_by(Category.name)
        .order_by(desc(func.count(Post.id)))
        .first()
    )
    if result:
        name,total = result
        print(f"Kategoria: {name}, ilość opublikowanych postów: {total} " )





def most_active_commenter(session):
    """Zadanie 4f: Najaktywniejszy komentujacy."""
    result = (
        session.query(User.username, func.count(Comment.id))
        .join(User.comments)
        .group_by(User.username)
        .order_by(desc(func.count(Comment.id)))
        .first()
        )
    if result:
        name, total = result
        print(f"Najaktywniejszy komentujacy: {name}, ilość komentarzy: {total}")





def author_ranking(session):
    """Zadanie 5a: Ranking autorow."""
    result = (
        session.query(User.username, func.count(Post.id))
        .join(User.posts)
        .group_by(User.username)
        .order_by(desc(func.count(Post.id)))
        .all()
        )
    print("--- Ranking autorów: ---")
    for name, total in result:
        print(f"Imię: {name}, ilość postów: {total}")
        



def posts_without_comments(session):
    """Zadanie 5b: Posty bez komentarzy."""
    # TODO: Uzyj ~Post.comments.any()

    result = (
        session.query(Post.title)
        .filter(~Post.comments.any())
        .all()
        )    
    #Unpack tuple (title,)
    for (title,) in result:
        print(f"Posty bez komentarzy: {title}")





def posts_with_many_comments(session, min_count=3):
    """Zadanie 5c: Posty z > min_count komentarzy."""
    # TODO: Uzyj HAVING
    
    result = (
        session.query(Post.title, func.count(Comment.id))
        .join(Post.comments)
        .group_by(Post.title)
        .having(func.count(Comment.id) > min_count)
        .all()
        )    
    for title, total in result:
        print(f"Posty z min {min_count} komentarzy : {title} | {total}")





def latest_comments(session, limit=5):
    """Zadanie 5d: Ostatnie komentarze."""
    
    result = (
        session.query(Comment)        
        .order_by(desc(Comment.created_at))
        .limit(limit)
        .all()
        )
    for comments in result:
        print(f" {comments.user.username} , {comments.post.title}, {comments.content}")








def draft_vs_published_per_author(session):
    """Zadanie 5e: Draft vs opublikowane na autora."""
    
    result = (
        session.query(
            User.username, 
            func.sum(case((Post.is_published == True, 1), else_ = 0)).label("published"),
            func.sum(case((Post.is_published == False, 1), else_ = 0)).label("drafts")
            )
        .join(User.posts)
        .group_by(User.username)
        .all()
        )
    for name, published, drafts in result:
        print(f" {name} | published: {published} | drafts: {drafts}")








if __name__ == "__main__":
    create_tables()

    with SessionLocal() as session:
        try:
            print("\n")
            clear_all_tables(session)
            seed_data(session)
            print("\n")
            posts_with_tag(session, "python")
            print("\n")
            create_post(session, 1, 3, "Najnowszy tytuł dodany", "Balbla bla bla bla", ["python", "api"])
            print("\n")
            edit_post(session, 1, "nowy tekst dla postu id 1")
            print("\n")
            publish_post(session, 1)
            print("\n")
            delete_post(session, 7)
            print("\n")
            posts_by_author(session, "robert")
            print("\n")
            comments_on_post(session, 2)
            print("\n")
            posts_in_category(session, "Web Backend")
            print("\n")
            published_posts_with_tag(session, "django")
            print("\n")
            posts_per_author(session)
            print("\n")
            comments_per_post(session)
            print("\n")
            avg_comments_per_post(session)
            print("\n")
            most_popular_tag(session)
            print("\n")
            top_category(session)
            print("\n")
            most_active_commenter(session)
            print("\n")
            author_ranking(session)
            print("\n")
            posts_without_comments(session)
            print("\n")
            posts_with_many_comments(session, min_count=3)
            print("\n")
            latest_comments(session, limit=5)
            print("\n")
            draft_vs_published_per_author(session)

        except SQLAlchemyError as e:
            session.rollback()
            print(f"Błąd bazy danych: {e}")
