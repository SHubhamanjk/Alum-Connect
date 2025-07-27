from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class ChatMessage(BaseModel):
    sender_email: EmailStr
    receiver_email: EmailStr
    message: str
    timestamp: Optional[datetime] = None
