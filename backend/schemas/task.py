from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class TaskCreate(BaseModel):
    title: str
    description: str | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    is_completed: bool | None = None


class TaskResponse(BaseModel):
    id: UUID
    title: str
    description: str | None
    is_completed: bool
    owner_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
