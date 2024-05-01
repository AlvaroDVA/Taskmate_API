from typing import List
from uuid import UUID
from bson import ObjectId
from pymongo import MongoClient

class UserRepository:
    def __init__(self, db_url: str, db_name: str):
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]

    def create_user(self, user_data: dict) -> str:
        collection = self.db[str(user_data['idUser'])]  
        user_id = collection.insert_one(user_data).inserted_id
        return str(user_id)

    def get_user_by_id(self, user_id: UUID) -> dict:
        collection = self.db[str(user_id)]
        user_data = collection.find_one({'_id': ObjectId(str(user_id))})
        return user_data

    def update_user(self, user_id: UUID, update_data: dict) -> bool:
        collection = self.db[str(user_id)]
        result = collection.update_one({'_id': ObjectId(str(user_id))}, {'$set': update_data})
        return result.modified_count > 0

    def delete_user(self, user_id: UUID) -> bool:
        collection = self.db[str(user_id)]
        result = collection.delete_one({'_id': ObjectId(str(user_id))})
        return result.deleted_count > 0
    
    def verify_user_credentials(self, username: str, password: str) -> bool:
        collection = self.db["users"]  # Suponiendo que la colección de usuarios se llama "users"
        user_data = collection.find_one({"username": username, "password": password})
        return user_data is not None