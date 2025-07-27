from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from datetime import datetime

class MentorshipProfile(BaseModel):
    alumni_email: EmailStr
    expertise: list[str]
    availability: str
    bio: Optional[str] = ""

class MentorshipRequest(BaseModel):
    student_email: EmailStr
    alumni_email: EmailStr
    message: Optional[str] = ""

class MentorshipResponse(BaseModel):
    request_id: str
    action: Literal["accept", "reject"]