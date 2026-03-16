from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List
from enum import Enum
from .tag import TagResponse


# TODO: Zdefiniuj schematy Pydantic dla Task

class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.todo          # todo / in_progress / done
    priority: TaskPriority = TaskPriority.medium      # low / medium / high / critical
    due_date: Optional[date] = None
    project_id: int
    assignee_id: Optional[int] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[date] = None
    assignee_id: Optional[int] = None

class TaskStatusUpdate(BaseModel):
    status: TaskStatus   # todo / in_progress / done

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    due_date: Optional[date]
    created_at: datetime
    updated_at: Optional[datetime]
    project_id: int
    assignee_id: Optional[int]
    tags: List[TagResponse] = []

    class Config:
        from_attributes = True
