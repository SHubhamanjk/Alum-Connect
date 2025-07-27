from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ShareResource(BaseModel):
    title: str
    type: str
    link: str
    description: Optional[str] = ""
    tags: Optional[List[str]] = []
    shared_by: str