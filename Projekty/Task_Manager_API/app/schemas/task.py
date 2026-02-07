from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List


# TODO: Zdefiniuj schematy Pydantic dla Task

# class TaskCreate(BaseModel):
#     title: str
#     description: Optional[str] = None
#     status: str = "todo"          # todo / in_progress / done
#     priority: str = "medium"      # low / medium / high / critical
#     due_date: Optional[date] = None
#     project_id: int
#     assignee_id: Optional[int] = None

# class TaskUpdate(BaseModel):
#     title: Optional[str] = None
#     description: Optional[str] = None
#     status: Optional[str] = None
#     priority: Optional[str] = None
#     due_date: Optional[date] = None
#     assignee_id: Optional[int] = None

# class TaskStatusUpdate(BaseModel):
#     status: str   # todo / in_progress / done

# class TaskResponse(BaseModel):
#     id: int
#     title: str
#     description: Optional[str]
#     status: str
#     priority: str
#     due_date: Optional[date]
#     created_at: datetime
#     updated_at: Optional[datetime]
#     project_id: int
#     assignee_id: Optional[int]
#
#     class Config:
#         from_attributes = True
