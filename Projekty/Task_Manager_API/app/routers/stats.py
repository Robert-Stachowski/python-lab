from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

# TODO: Zaimportuj modele i get_db

router = APIRouter()


# TODO: Zaimplementuj endpointy statystyk

# @router.get("/overview")
# def get_overview(db: Session = Depends(get_db)):
#     """Ogolne statystyki systemu."""
#     # Policz: laczna liczba zadan, projektow, uzytkownikow
#     # Policz: zadania wg statusu
#     # return {
#     #     "total_users": ...,
#     #     "total_projects": ...,
#     #     "total_tasks": ...,
#     #     "tasks_todo": ...,
#     #     "tasks_in_progress": ...,
#     #     "tasks_done": ...,
#     # }
#     pass

# @router.get("/tasks-by-status")
# def tasks_by_status(db: Session = Depends(get_db)):
#     """Zadania pogrupowane po statusie."""
#     # Uzyj group_by(Task.status) z func.count()
#     pass

# @router.get("/tasks-by-priority")
# def tasks_by_priority(db: Session = Depends(get_db)):
#     """Zadania pogrupowane po priorytecie."""
#     # Uzyj group_by(Task.priority) z func.count()
#     pass

# @router.get("/user/{user_id}/summary")
# def user_summary(user_id: int, db: Session = Depends(get_db)):
#     """Podsumowanie uzytkownika."""
#     # Policz: projekty usera, przypisane zadania, zadania wg statusu
#     pass
