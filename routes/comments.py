from fastapi import APIRouter, Depends, HTTPException
from database import comments_collection
from auth import verify_token
from pydantic import BaseModel
router = APIRouter()

class comments(BaseModel):
   comment : str


@router.post("/posts/{post_id}/comments")
async def add_comment(post_id: str, comment:comments, username: str = Depends(verify_token)):
   comments_collection.insert_one({"post_id": post_id, "comment": comment.comment, "author": username})
   return {"message": "Comment added successfully"}


@router.get("/posts/{post_id}/comments")
async def get_comments(post_id: str):
   comments = list(comments_collection.find({"post_id": post_id}, {"_id": 0}))
   return {"comments": comments}