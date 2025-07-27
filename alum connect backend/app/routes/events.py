from fastapi import APIRouter, HTTPException
from app.models.events import CreateEvent, RegisterEvent
from app.db import db
from bson.objectid import ObjectId
from datetime import datetime
import pytz

router = APIRouter()
events = db["events"]
registrations = db["event_registrations"]

@router.post("/create")
async def create_event(data: CreateEvent):
    data_dict = data.dict()
    ist = pytz.timezone('Asia/Kolkata')
    data_dict["created_at"] = datetime.now(ist)
    result = await events.insert_one(data_dict)
    return {"msg": "Event created", "event_id": str(result.inserted_id)}

@router.get("/upcoming")
async def get_upcoming_events():
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    cursor = events.find({"date": {"$gte": now}}).sort("date", 1)
    result = []
    async for ev in cursor:
        ev["_id"] = str(ev["_id"])
        result.append(ev)
    return result

@router.get("/past")
async def get_past_events():
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    cursor = events.find({"date": {"$lt": now}}).sort("date", -1)
    result = []
    async for ev in cursor:
        ev["_id"] = str(ev["_id"])
        result.append(ev)
    return result

@router.post("/register")
async def register_for_event(data: RegisterEvent):
    eid = ObjectId(data.event_id)
    already = await registrations.find_one({
        "event_id": eid,
        "user_email": data.user_email
    })
    if already:
        raise HTTPException(status_code=400, detail="Already registered")

    ist = pytz.timezone('Asia/Kolkata')
    await registrations.insert_one({
        "event_id": eid,
        "user_email": data.user_email,
        "registered_at": datetime.now(ist)
    })
    return {"msg": "Registered successfully"}

@router.get("/registrations/{event_id}")
async def get_registered_users(event_id: str):
    eid = ObjectId(event_id)
    users = []
    async for reg in registrations.find({"event_id": eid}):
        reg["_id"] = str(reg["_id"])
        reg["event_id"] = str(reg["event_id"])
        users.append(reg)
    return users
