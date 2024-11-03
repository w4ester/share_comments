# app/schemas/comment.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CommentBase(BaseModel):
    content: str
    url: str
    parent_id: Optional[int] = None

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    ai_response: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    replies: List['Comment'] = []

    class Config:
        from_attributes = True

# This is needed to handle the recursive relationship
Comment.model_rebuild()