from fastapi import APIRouter, Depends, HTTPException
from database import posts_collection
from pydantic import BaseModel
import uuid
from auth import verify_token
router = APIRouter()


class PostCreate(BaseModel):
    title: str
    content : str

@router.post("/posts")
async def create_post(post:PostCreate,username: str = Depends(verify_token)):
    post = {"title": post.title, "content": post.content, "author": username,"post_id":str(uuid.uuid4().int)[:4]}
    posts_collection.insert_one(post)
    return {"message": "Post created successfully",'post_id':post['post_id']}

@router.get("/posts")
async def get_all_posts():
    posts = list(posts_collection.find({}, {"_id": 0}))
    return {"posts": posts}

@router.get("/posts/mine")
async def get_my_posts(username: str = Depends(verify_token)):
    posts = list(posts_collection.find({"author": username}, {"_id": 0}))
    return {"posts": posts} 