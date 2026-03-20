from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, selectinload


# TODO: Zaimportuj modele, schematy i get_db
from ..database import get_db
from ..import models
from ..schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate, ProjectWithTasksResponse
from ..schemas.pagination import PaginatedResponse


router = APIRouter()


# TODO: Zaimplementuj endpointy CRUD dla Project




@router.get("/", response_model=PaginatedResponse[ProjectResponse])
def get_projects(
    skip: int = Query(default=0, ge=0),             # ge=0: skip >= 0
    limit: int = Query(default=10, ge=1, le=100),   # limit: od 1 do 100
    db: Session = Depends(get_db)
    ):
    """Pobierz liste projektow."""
    # + paginacja

    total = db.query(models.Project).count()    # wracam liczbę wszytskich rekordów
    items = db.query(models.Project).offset(skip).limit(limit).all()    # zwracam rekordy od 0 - 10.

    return PaginatedResponse(
        total=total,
        skip=skip,
        limit=limit,
        items=items
    )




@router.post("/", response_model=ProjectResponse, status_code=201)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    """Utworz nowy projekt."""
    # Sprawdz czy owner istnieje
    existing = db.query(models.User).filter(models.User.id == project.owner_id).first()
    if existing is None:
        raise HTTPException(status_code=404, detail="Brak ownera")
    db_project = models.Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project






@router.get("/{project_id}", response_model=ProjectWithTasksResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """Pobierz projekt z zadaniami."""
    # Uzyj selectinload dla tasks
    db_project = db.query(models.Project).options(selectinload(models.Project.tasks)).filter(models.Project.id == project_id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Projekt nieodnaleziony... ")
    return db_project







@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project: ProjectUpdate, db: Session = Depends(get_db)):
    """Zaktualizuj projekt."""
    existing = db.query(models.Project).filter(models.Project.id == project_id).first()
    if existing is None:
        raise HTTPException(status_code=404, detail="ład, nie odnaleziono projektu!")
    update_data = project.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(existing, field, value)
    db.commit()
    db.refresh(existing)
    return existing







@router.delete("/{project_id}", status_code=204)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    """Usun projekt kaskadowo z zadaniami."""
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Nie znaleziono projektu")
    db.delete(db_project)
    db.commit()
