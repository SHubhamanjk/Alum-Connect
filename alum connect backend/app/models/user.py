from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    user_type: str
    bio: Optional[str] = ""
    profile_pic: Optional[str] = ""
    skills: Optional[list[str]] = []

class UserLogin(BaseModel):
    email: EmailStr
    password: str
