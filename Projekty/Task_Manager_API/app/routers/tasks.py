from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

# TODO: Zaimportuj modele, schematy i get_db

router = APIRouter()


# TODO: Zaimplementuj endpointy CRUD dla Task

# @router.get("/")
# def get_tasks(
#     status: Optional[str] = Query(None, description="Filtruj po statusie: todo/in_progress/done"),
#     priority: Optional[str] = Query(None, description="Filtruj po priorytecie: low/medium/high/critical"),
#     project_id: Optional[int] = Query(None, description="Filtruj po projekcie"),
#     assignee_id: Optional[int] = Query(None, description="Filtruj po przypisanym uzytkowniku"),
#     db: Session = Depends(get_db),
# ):
#     """Pobierz liste zadan z opcjonalnymi filtrami."""
#     # Buduj query dynamicznie na podstawie filtrow
#     pass

# @router.post("/", status_code=201)
# def create_task(task: TaskCreate, db: Session = Depends(get_db)):
#     """Utworz nowe zadanie."""
#     # Sprawdz czy project istnieje
#     # Sprawdz czy assignee istnieje (jesli podano)
#     pass

# @router.get("/{task_id}")
# def get_task(task_id: int, db: Session = Depends(get_db)):
#     """Pobierz zadanie po ID."""
#     pass

# @router.put("/{task_id}")
# def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
#     """Zaktualizuj zadanie."""
#     pass

# @router.patch("/{task_id}/status")
# def update_task_status(task_id: int, status_update: TaskStatusUpdate, db: Session = Depends(get_db)):
#     """Zmien status zadania."""
#     # Waliduj czy status jest prawidlowy
#     pass

# @router.delete("/{task_id}", status_code=204)
# def delete_task(task_id: int, db: Session = Depends(get_db)):
#     """Usun zadanie."""
#     pass
