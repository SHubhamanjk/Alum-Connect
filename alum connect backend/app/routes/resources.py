from fastapi import APIRouter
from app.models.resources import ShareResource
from app.db import db
from datetime import datetime
import pytz

router = APIRouter()
resources = db["resources"]

@router.post("/share")
async def share_resource(data: ShareResource):
    data_dict = data.dict()
    ist = pytz.timezone('Asia/Kolkata')
    data_dict["shared_at"] = datetime.now(ist)
    result = await resources.insert_one(data_dict)
    return {"msg": "Resource shared", "resource_id": str(result.inserted_id)}

@router.get("/all")
async def get_all_resources():
    result = []
    async for r in resources.find().sort("shared_at", -1):
        r["_id"] = str(r["_id"])
        result.append(r)
    return result

@router.get("/search")
async def search_resources(tag: str):
    result = []
    async for r in resources.find({"tags": tag}):
        r["_id"] = str(r["_id"])
        result.append(r)
    return result
