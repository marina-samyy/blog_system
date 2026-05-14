from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class CommentBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)

class CommentCreate(CommentBase):
    post_id: int
    parent_id: Optional[int] = None

class CommentUpdate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    author_id: int
    post_id: int
    parent_id: Optional[int]
    created_at: datetime
    model_config = {
        "from_attributes": True
    }

class CommentTreeResponse(CommentResponse):
    replies: List['CommentTreeResponse'] = []

CommentTreeResponse.model_rebuild()