from fastapi import APIRouter, HTTPException
from app.models.user import UserRegister, UserLogin
from app.db import db
from app.utils.jwt_handler import create_token
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
users_collection = db["users"]

@router.post("/register")
async def register_user(user: UserRegister):
    user_exists = await users_collection.find_one({"email": user.email})
    if user_exists:
        raise HTTPException(status_code=409, detail="Email already registered")
    user_dict = user.dict()
    user_dict["password"] = pwd_context.hash(user.password)
    result = await users_collection.insert_one(user_dict)
    return {"msg": "User registered", "id": str(result.inserted_id)}

@router.post("/login")
async def login_user(user: UserLogin):
    found_user = await users_collection.find_one({"email": user.email})
    if not found_user or not pwd_context.verify(user.password, found_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token({"email": found_user["email"], "user_type": found_user["user_type"]})
    return {"access_token": token, "token_type": "bearer"}
