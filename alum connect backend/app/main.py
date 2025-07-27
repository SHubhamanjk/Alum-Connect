from fastapi import FastAPI
from app.routes import auth, feed, mentorship, events, resources, chat

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(feed.router, prefix="/feed", tags=["Feed"])
app.include_router(mentorship.router, prefix="/mentorship", tags=["Mentorship"])
app.include_router(events.router, prefix="/events", tags=["Events & Workshops"])
app.include_router(resources.router, prefix="/resources", tags=["Resources"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])

@app.get("/")
def home():
    return {"msg": "AlumConnect API is running!"}
