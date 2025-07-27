from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CreatePost(BaseModel):
    author_email: str
    text: str
    image_url: Optional[str] = None
    tags: Optional[List[str]] = []

class CreateComment(BaseModel):
    post_id: str
    author_email: str
    comment_text: str

class LikePost(BaseModel):
    post_id: str
    liker_email: str