from fastapi import APIRouter, Depends, HTTPException, status

from auth import create_access_token, get_password_hash, verify_password, verify_token

from database import users_collection

from datetime import timedelta
from pydantic import BaseModel

router = APIRouter()

class Signup(BaseModel):
    username : str
    password : str

@router.post("/signup")
async def signup(user:Signup):

    if users_collection.find_one({"username": user.username}):

        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = get_password_hash(user.password)

    users_collection.insert_one({"username": user.username, "password": hashed_password})

    return {"message": "User created successfully"}

@router.post("/login")

async def login(user:Signup):

    user_ = users_collection.find_one({"username": user.username})

    if not user or not verify_password(user.password, user_["password"]):

        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=60))

    return {"access_token": token, "token_type": "bearer"}

@router.get("/users/me")

async def get_current_user(username: str = Depends(verify_token)):

    user = users_collection.find_one({"username": username}, {"_id": 0, "password": 0})

    if not user:

        raise HTTPException(status_code=404, detail="User not found")

    return user 