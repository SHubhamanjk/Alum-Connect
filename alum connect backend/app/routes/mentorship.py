from fastapi import APIRouter, HTTPException
from app.models.mentorship import MentorshipProfile, MentorshipRequest, MentorshipResponse
from app.db import db
from bson.objectid import ObjectId
from datetime import datetime

router = APIRouter()
profiles = db["mentorship_profiles"]
requests = db["mentorship_requests"]

@router.post("/create-profile")
async def create_profile(profile: MentorshipProfile):
    existing = await profiles.find_one({"alumni_email": profile.alumni_email})
    if existing:
        raise HTTPException(status_code=409, detail="Profile already exists")
    await profiles.insert_one(profile.dict())
    return {"msg": "Mentorship profile created"}

@router.get("/alumni")
async def list_mentors():
    result = []
    async for p in profiles.find():
        p["_id"] = str(p["_id"])
        result.append(p)
    return result

@router.post("/request")
async def request_mentorship(data: MentorshipRequest):
    duplicate = await requests.find_one({
        "student_email": data.student_email,
        "alumni_email": data.alumni_email,
        "status": "pending"
    })
    if duplicate:
        raise HTTPException(status_code=400, detail="You already requested mentorship from this alumni")
    data_dict = data.dict()
    data_dict["status"] = "pending"
    data_dict["requested_at"] = datetime.utcnow()
    result = await requests.insert_one(data_dict)
    return {"msg": "Mentorship requested", "request_id": str(result.inserted_id)}

@router.post("/respond")
async def respond_to_request(response: MentorshipResponse):
    req = await requests.find_one({"_id": ObjectId(response.request_id)})
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    if req["status"] != "pending":
        raise HTTPException(status_code=400, detail="Request already handled")
    await requests.update_one(
        {"_id": ObjectId(response.request_id)},
        {"$set": {"status": response.action, "responded_at": datetime.utcnow()}}
    )
    return {"msg": f"Mentorship request {response.action}ed"}

@router.get("/requests/{email}")
async def get_requests(email: str):
    result = []
    async for r in requests.find({"alumni_email": email}):
        r["_id"] = str(r["_id"])
        result.append(r)
    return result
