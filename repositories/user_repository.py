from typing import List
from uuid import UUID
from bson import ObjectId
from pymongo import MongoClient

class UserRepository:
    def __init__(self, config):
        self.db_url = config["db_url"]
        self.db_name = config["db_name"]
        self.username = config["username"]
        self.password = config["password"]
        self.client = MongoClient(self.db_url)
        self.db = self.client[self.db_name]

    def connect_to_database(self):
        # Aquí realizas la conexión a la base de datos utilizando los detalles proporcionados en la configuración
        # Aquí hay un ejemplo de cómo podrías conectar a MongoDB
        from pymongo import MongoClient

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
        collection = self.db["users"]  
        user_data = collection.find_one({"username": username, "password": password})
        return user_data is not None