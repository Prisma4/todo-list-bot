from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TaskCategoryCreateRequest(BaseModel):
    user_id: int
    name: str


class TaskCreateRequest(BaseModel):
    user_id: int
    content: str
    category: Optional[str] = None
    scheduled_at: Optional[str] = None


class TaskListRequest(BaseModel):
    user_id: int


class GetCategoryByNameRequest(BaseModel):
    user_id: int
    name: str


class GetCategoryByNameResponse(BaseModel):
    id: str
    name: str


class Category(BaseModel):
    name: str


class TaskListResponse(BaseModel):
    category: Optional[Category] = None
    content: str
    created_at: datetime
    scheduled_at: Optional[datetime] = None
