from fastapi import APIRouter
from models.user import User
from config.db import mongoClient
from schemas.user import userEntity, usersEntity
from bson import ObjectId

user = APIRouter()
user_db = mongoClient.local # using local database
user_collection = user_db.user # user collection


@user.get("/")
async def get_all_user():
    return usersEntity(user_collection.find())


@user.post("/")
async def create_user(user: User):
    user_collection.insert_one(dict(user))
    return usersEntity(user_collection.find())


@user.put("/")
async def update_user(id, user: User):
    user_collection.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": dict(user)})
    return userEntity(user_collection.find_one({"_id": ObjectId(id)}))


@user.delete("/")
async def delete_user(id):
    user_collection.find_one_and_delete({"_id": ObjectId(id)})


@user.get("/{id}")
async def get_user_by_id(id):
    return userEntity(user_collection.find_one({"_id": ObjectId(id)}))
