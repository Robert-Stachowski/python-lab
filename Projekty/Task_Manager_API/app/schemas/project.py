from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from .task import TaskResponse

# TODO: Zdefiniuj schematy Pydantic dla Project

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ProjectWithTasksResponse(ProjectResponse):
    tasks: List[TaskResponse] = []
