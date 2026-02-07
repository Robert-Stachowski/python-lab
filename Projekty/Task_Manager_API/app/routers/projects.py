from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# TODO: Zaimportuj modele, schematy i get_db

router = APIRouter()


# TODO: Zaimplementuj endpointy CRUD dla Project

# @router.get("/")
# def get_projects(db: Session = Depends(get_db)):
#     """Pobierz liste projektow."""
#     pass

# @router.post("/", status_code=201)
# def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
#     """Utworz nowy projekt."""
#     # Sprawdz czy owner istnieje
#     pass

# @router.get("/{project_id}")
# def get_project(project_id: int, db: Session = Depends(get_db)):
#     """Pobierz projekt z zadaniami."""
#     # Uzyj selectinload dla tasks
#     pass

# @router.put("/{project_id}")
# def update_project(project_id: int, project: ProjectUpdate, db: Session = Depends(get_db)):
#     """Zaktualizuj projekt."""
#     pass

# @router.delete("/{project_id}", status_code=204)
# def delete_project(project_id: int, db: Session = Depends(get_db)):
#     """Usun projekt kaskadowo z zadaniami."""
#     pass
