from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, selectinload
from typing import Optional

# TODO: Zaimportuj modele, schematy i get_db

from ..database import get_db
from ..import models
from ..schemas.task import TaskCreate,TaskResponse,TaskStatus,TaskPriority,TaskStatusUpdate,TaskUpdate
from ..schemas.pagination import PaginatedResponse

from app.auth.dependencies import get_current_user
from app.models import User, Task


router = APIRouter()


# TODO: Zaimplementuj endpointy CRUD dla Task




@router.get("/", response_model=PaginatedResponse[TaskResponse])
def get_tasks(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    status: Optional[str] = Query(None, description="Filtruj po statusie: todo/in_progress/done"),
    priority: Optional[str] = Query(None, description="Filtruj po priorytecie: low/medium/high/critical"),
    project_id: Optional[int] = Query(None, description="Filtruj po projekcie"),
    assignee_id: Optional[int] = Query(None, description="Filtruj po przypisanym uzytkowniku"),
    db: Session = Depends(get_db),
    ):

    """Pobierz liste zadan z opcjonalnymi filtrami."""
    # Buduj query dynamicznie na podstawie filtrów
    # + paginacja

    query = db.query(models.Task)
    
    if status is not None:
        query = query.filter(models.Task.status == status)
    if priority is not None:
        query = query.filter(models.Task.priority == priority)
    if project_id is not None:
        query = query.filter(models.Task.project_id == project_id)
    if assignee_id is not None:
        query = query.filter(models.Task.assignee_id == assignee_id)

    total = query.count()
    items = query.offset(skip).limit(limit).all()

    return PaginatedResponse(
        total=total,
        skip=skip,
        limit=limit,
        items=items
    )







@router.post("/", status_code=201, response_model=TaskResponse)
def create_task(task: TaskCreate, current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):

    """Utworz nowe zadanie."""
    # Sprawdz czy project istnieje
    # Sprawdz czy assignee istnieje (jesli podano)
    existing_project = db.query(models.Project).filter(models.Project.id == task.project_id).first()
    if existing_project is None:
        raise HTTPException(status_code=404, detail="Nie odnaleziono projektu, nie można utworzyć zadania")
    if task.assignee_id is not None:
        user = db.query(models.User).filter(models.User.id == task.assignee_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="Nie odnaleziono przypisanego usera")
        
    # assignee_id nie jest nadpisywane przez current_user.id — task może być stworzony
    # przez zalogowanego usera, ale przypisany do wykonania komuś innemu (lub nikomu).
    # current_user zapewnia tylko autoryzację, nie determinuje assignee.
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task









@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Pobierz zadanie po ID."""
    db_task = (
        db.query(models.Task)
        .options(selectinload(models.Task.tags))
        .filter(models.Task.id == task_id)
        .first()
        )
    if db_task is None:
        raise HTTPException(status_code=404, detail="Nie znaleziono zadania...")
    return db_task








@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate, current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    """Zaktualizuj zadanie."""
    existing = db.query(models.Task).filter(models.Task.id == task_id).first()
    if existing is None:
        raise HTTPException(status_code=404, detail="Nie odnaleziono zadania :( ")
    db_project = db.query(models.Project).filter(models.Project.id == existing.project_id).first()
    if db_project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Tylko właściciel projektu, moze aktualizować taska")
    
    update_data = task.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(existing, field, value)
    db.commit()
    db.refresh(existing)
    return existing









@router.patch("/{task_id}/status", response_model=TaskResponse)
def update_task_status(task_id: int, status_update: TaskStatusUpdate, db: Session = Depends(get_db)):
    """Zmien status zadania."""
    # Waliduj czy status jest prawidlowy

    # Walidacja statusu — wykonywana automatycznie przez Pydantic (TaskStatus Enum)

    existing = db.query(models.Task).filter(models.Task.id == task_id).first()
    if existing is None:
        raise HTTPException(status_code=404, detail="Nie odnaleziono zadania...")
    
    existing.status = status_update.status

    db.commit()
    db.refresh(existing)
    return existing









@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    """Usun zadanie."""
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Nie odnaleziono zadania do usunięcia...")
    db_project = db.query(models.Project).filter(models.Project.id == db_task.project_id).first()
    if db_project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Tylko własciciel projektu może usunąć taska")
    db.delete(db_task)
    db.commit()
