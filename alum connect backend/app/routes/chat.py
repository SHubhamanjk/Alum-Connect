from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.db import db
from datetime import datetime
from app.models.chat import ChatMessage
from jose import JWTError, jwt
import os

router = APIRouter()
chat_collection = db["chat_messages"]

SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = "HS256"

active_connections = {} 


def get_user_email_from_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("email")
    except JWTError:
        return None


@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    token = websocket.headers.get("authorization")
    if not token:
        await websocket.close()
        return

    user_email = get_user_email_from_token(token)
    if not user_email:
        await websocket.close()
        return

    await websocket.accept()
    active_connections[user_email] = websocket

    try:
        while True:
            data = await websocket.receive_json()
            message = ChatMessage(
                sender_email=user_email,
                receiver_email=data["receiver_email"],
                message=data["message"],
                timestamp=datetime.utcnow()
            )

            await chat_collection.insert_one(message.dict())

            receiver_ws = active_connections.get(data["receiver_email"])
            if receiver_ws:
                await receiver_ws.send_json({
                    "from": user_email,
                    "message": message.message,
                    "timestamp": message.timestamp.isoformat()
                })

    except WebSocketDisconnect:
        del active_connections[user_email]


@router.get("/history")
async def chat_history(sender_email: str, receiver_email: str):
    messages_cursor = chat_collection.find({
        "$or": [
            {"sender_email": sender_email, "receiver_email": receiver_email},
            {"sender_email": receiver_email, "receiver_email": sender_email}
        ]
    }).sort("timestamp", 1)

    result = []
    async for msg in messages_cursor:
        msg["_id"] = str(msg["_id"])
        result.append(msg)

    return result
