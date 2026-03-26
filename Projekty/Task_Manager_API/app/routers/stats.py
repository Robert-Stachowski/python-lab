from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db
from ..import models


router = APIRouter()


@router.get("/overview")
def get_overview(db: Session = Depends(get_db)):
    """Ogolne statystyki systemu."""
    return {
        "total_users": db.query(func.count(models.User.id)).scalar(),
        "total_projects": db.query(func.count(models.Project.id)).scalar(),
        "total_tasks": db.query(func.count(models.Task.id)).scalar(),
        "task_todo": db.query(func.count(models.Task.id)).filter(models.Task.status == "todo").scalar(),
        "task_in_progress": db.query(func.count(models.Task.id)).filter(models.Task.status == "in_progress").scalar(),
        "task_done": db.query(func.count(models.Task.id)).filter(models.Task.status == "done").scalar(),
    }


@router.get("/tasks-by-status")
def tasks_by_status(db: Session = Depends(get_db)):
    """Zadania pogrupowane po statusie."""
    result = db.query(models.Task.status, func.count(models.Task.id)).group_by(models.Task.status).all()
    return [{"status": status, "ilość": count} for status, count in result]


@router.get("/tasks-by-priority")
def tasks_by_priority(db: Session = Depends(get_db)):
    """Zadania pogrupowane po priorytecie."""
    result = db.query(models.Task.priority, func.count(models.Task.id)).group_by(models.Task.priority).all()
    return [{"priorytet": priority, "ilość": count} for priority, count in result]


@router.get("/user/{user_id}/summary")
def user_summary(user_id: int, db: Session = Depends(get_db)):
    """Podsumowanie uzytkownika."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User nie istnieje...")

    projects = db.query(func.count(models.Project.id)).filter(models.Project.owner_id == user_id).scalar()
    tasks = db.query(models.Task.status, func.count(models.Task.id)).group_by(models.Task.status).filter(models.Task.assignee_id == user_id).all()

    return {"user": user.username, "projects": projects, "tasks": [{"status": status, "ilość": count} for status, count in tasks]}
