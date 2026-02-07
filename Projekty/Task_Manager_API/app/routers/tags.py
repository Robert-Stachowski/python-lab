from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# TODO: Zaimportuj modele, schematy i get_db

router = APIRouter()


# TODO: Zaimplementuj endpointy dla Tag

# @router.get("/")
# def get_tags(db: Session = Depends(get_db)):
#     """Pobierz liste tagow."""
#     pass

# @router.post("/", status_code=201)
# def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
#     """Utworz nowy tag."""
#     # Sprawdz czy tag o tej nazwie juz istnieje
#     pass

# @router.post("/tasks/{task_id}/tags")
# def add_tag_to_task(task_id: int, tag: TagCreate, db: Session = Depends(get_db)):
#     """Dodaj tag do zadania."""
#     # Znajdz task, znajdz lub utworz tag, dodaj do task.tags
#     pass

# @router.delete("/tasks/{task_id}/tags/{tag_id}", status_code=204)
# def remove_tag_from_task(task_id: int, tag_id: int, db: Session = Depends(get_db)):
#     """Usun tag z zadania."""
#     pass
