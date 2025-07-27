from fastapi import APIRouter, HTTPException, Query
from app.models.feed import CreatePost, CreateComment, LikePost
from app.db import db
from bson.objectid import ObjectId
from datetime import datetime

router = APIRouter()
posts_collection = db["posts"]
comments_collection = db["comments"]
likes_collection = db["likes"]

@router.post("/create")
async def create_post(post: CreatePost):
    post_data = post.dict()
    post_data["created_at"] = datetime.utcnow()
    post_data["likes"] = 0
    result = await posts_collection.insert_one(post_data)
    return {"msg": "Post created", "post_id": str(result.inserted_id)}

@router.get("/all")
async def get_all_posts(user_email: str = Query(None), all: bool = Query(None)):
    if not user_email and not all:
        raise HTTPException(status_code=400, detail="Either user_email or all must be provided.")
    if user_email:
        posts_cursor = posts_collection.find({"author_email": user_email}).sort("created_at", -1)
        posts = []
        async for post in posts_cursor:
            post["_id"] = str(post["_id"])
            posts.append(post)
        return posts
    if all:
        posts_cursor = posts_collection.find().sort("created_at", -1)
        user_posts = {}
        async for post in posts_cursor:
            post["_id"] = str(post["_id"])
            author = post.get("author_email", "unknown")
            if author not in user_posts:
                user_posts[author] = []
            user_posts[author].append(post)
        return user_posts

@router.post("/comment")
async def comment_post(comment: CreateComment):
    comment_data = comment.dict()
    comment_data["created_at"] = datetime.utcnow()
    comment_data["post_id"] = ObjectId(comment_data["post_id"])
    result = await comments_collection.insert_one(comment_data)
    return {"msg": "Comment added", "comment_id": str(result.inserted_id)}

@router.get("/comments/{post_id}")
async def get_comments(post_id: str):
    comments_cursor = comments_collection.find({"post_id": ObjectId(post_id)})
    comments = []
    async for comment in comments_cursor:
        comment["_id"] = str(comment["_id"])
        comment["post_id"] = str(comment["post_id"])
        comments.append(comment)
    return comments

@router.post("/like")
async def like_post(data: LikePost):
    post_id = ObjectId(data.post_id)
    already_liked = await likes_collection.find_one({"post_id": post_id, "liker_email": data.liker_email})
    if already_liked:
        raise HTTPException(status_code=400, detail="Post already liked")
    await likes_collection.insert_one({
        "post_id": post_id,
        "liker_email": data.liker_email,
        "liked_at": datetime.utcnow()
    })
    await posts_collection.update_one({"_id": post_id}, {"$inc": {"likes": 1}})
    return {"msg": "Post liked!"}

