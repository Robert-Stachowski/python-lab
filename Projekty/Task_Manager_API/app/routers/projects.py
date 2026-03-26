from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, selectinload

from ..database import get_db
from ..import models
from ..schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate, ProjectWithTasksResponse
from ..schemas.pagination import PaginatedResponse

from app.auth.dependencies import get_current_user


router = APIRouter()


@router.get("/mine", response_model=list[ProjectResponse])
def get_my_projects(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(models.Project).filter(models.Project.owner_id == current_user.id).all()


@router.get("/", response_model=PaginatedResponse[ProjectResponse])
def get_projects(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
    ):
    """Pobierz liste projektow."""
    total = db.query(models.Project).count()
    items = db.query(models.Project).offset(skip).limit(limit).all()

    return PaginatedResponse(
        total=total,
        skip=skip,
        limit=limit,
        items=items
    )


@router.post("/", response_model=ProjectResponse, status_code=201)
def create_project(project: ProjectCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Utworz nowy projekt."""
    db_project = models.Project(**project.model_dump(), owner_id=current_user.id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


@router.get("/{project_id}", response_model=ProjectWithTasksResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """Pobierz projekt z zadaniami."""
    db_project = db.query(models.Project).options(selectinload(models.Project.tasks)).filter(models.Project.id == project_id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Projekt nieodnaleziony... ")
    return db_project


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project: ProjectUpdate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Zaktualizuj projekt."""
    existing = db.query(models.Project).filter(models.Project.id == project_id).first()
    if existing is None:
        raise HTTPException(status_code=404, detail="Błąd, nie odnaleziono projektu!")
    if existing.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Tylko właściciel projektu może go zaktualizować")

    update_data = project.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(existing, field, value)
    db.commit()
    db.refresh(existing)
    return existing


@router.delete("/{project_id}", status_code=204)
def delete_project(project_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Usun projekt kaskadowo z zadaniami."""
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Nie znaleziono projektu")
    if db_project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Tylko właściciel projektu może go usunąć")
    db.delete(db_project)
    db.commit()
