from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# TODO: Zaimportuj modele, schematy i get_db
from ..database import get_db
from ..import models 
from ..schemas.tag import TagCreate,TagResponse

router = APIRouter()


# TODO: Zaimplementuj endpointy dla Tag



@router.get("/", response_model=list[TagResponse])
def get_tags(db: Session = Depends(get_db)):
    """Pobierz liste tagow."""
    return db.query(models.Tag).all()






@router.post("/", status_code=201, response_model=TagResponse)
def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    """Utworz nowy tag."""
    # Sprawdz czy tag o tej nazwie juz istnieje

    existing = db.query(models.Tag).filter(models.Tag.name == tag.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Tag już istnieje!")
    
    db_tag = models.Tag(**tag.model_dump())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag






@router.post("/tasks/{task_id}/tags", response_model=TagResponse)
def add_tag_to_task(task_id: int, tag: TagCreate, db: Session = Depends(get_db)):
    """Dodaj tag do zadania."""
    # Znajdz task, znajdz lub utworz tag, dodaj do task.tags

    existing_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if existing_task is None:
        raise HTTPException(status_code=404,detail="Nie znaleziono odpowiedniego taska")
    
    existing_tag = db.query(models.Tag).filter(models.Tag.name == tag.name).first()
    if existing_tag is None:
        existing_tag = models.Tag(name = tag.name)
        db.add(existing_tag)
        db.flush()
    if existing_tag in existing_task.tags:
        raise HTTPException(status_code=400, detail="Tag już jest przypsany do taska")
    
    existing_task.tags.append(existing_tag)
    db.commit()
    return existing_tag






@router.delete("/tasks/{task_id}/tags/{tag_id}", status_code=204)
def remove_tag_from_task(task_id: int, tag_id: int, db: Session = Depends(get_db)):
    """Usun tag z zadania."""
    existing_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if existing_task is None:
        raise HTTPException(status_code=404, detail="Nie znaleziono taska")
    
    existing_tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if existing_tag is None:
        raise HTTPException(status_code=404, detail="Nie odnaleziono tagu")
    
    if existing_tag not in existing_task.tags:
        raise HTTPException(status_code=404, detail="Tag nie jest przypisany do taska")
    
    existing_task.tags.remove(existing_tag)
    db.commit()

