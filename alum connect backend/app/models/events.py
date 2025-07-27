from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class CreateEvent(BaseModel):
    title: str
    description: Optional[str] = ""
    host_email: EmailStr
    date: datetime
    location: Optional[str] = ""

class RegisterEvent(BaseModel):
    event_id: str
    user_email: EmailStr