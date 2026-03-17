from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, selectinload
from typing import Optional

# TODO: Zaimportuj modele, schematy i get_db

from ..database import get_db
from ..import models
from ..schemas.task import TaskCreate,TaskResponse,TaskStatus,TaskPriority,TaskStatusUpdate,TaskUpdate


router = APIRouter()


# TODO: Zaimplementuj endpointy CRUD dla Task




@router.get("/", response_model=list[TaskResponse])
def get_tasks(
    status: Optional[str] = Query(None, description="Filtruj po statusie: todo/in_progress/done"),
    priority: Optional[str] = Query(None, description="Filtruj po priorytecie: low/medium/high/critical"),
    project_id: Optional[int] = Query(None, description="Filtruj po projekcie"),
    assignee_id: Optional[int] = Query(None, description="Filtruj po przypisanym uzytkowniku"),
    db: Session = Depends(get_db),
    ):

    """Pobierz liste zadan z opcjonalnymi filtrami."""
    # Buduj query dynamicznie na podstawie filtrow
    query = db.query(models.Task)
    if status is not None:
        query = query.filter(models.Task.status == status)
    if priority is not None:
        query = query.filter(models.Task.priority == priority)
    if project_id is not None:
        query = query.filter(models.Task.project_id == project_id)
    if assignee_id is not None:
        query = query.filter(models.Task.assignee_id == assignee_id)

    return query.all()







@router.post("/", status_code=201, response_model=TaskResponse)
def create_task(task: TaskCreate,db: Session = Depends(get_db)):

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
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    """Zaktualizuj zadanie."""
    existing = db.query(models.Task).filter(models.Task.id == task_id).first()
    if existing is None:
        raise HTTPException(status_code=404, detail="Nie odnaleziono zadania :( ")
    
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
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Usun zadanie."""
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Nie odnaleziono zadania do usunięcia...")
    db.delete(db_task)
    db.commit()
