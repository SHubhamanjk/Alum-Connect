from pymongo import AsyncMongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

client = AsyncMongoClient(MONGO_URI)
db = client["alumconnect"]  # Database name
