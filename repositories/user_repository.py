from typing import List
from uuid import UUID
from pymongo import MongoClient

class UserRepository:
    def __init__(self, config):
        self.db_url = config["db_url"]
        self.db_name = config["db_name"]
        self.username = config["username"]
        self.password = config["password"]
        self.client = MongoClient(self.db_url)
        self.db = self.client[self.db_name]
        self.collection = self.db["Users"]

    def create_user(self, user_data: dict) -> str:
        if self.db["Users"].find_one({"email": user_data['email']}):
            return {"error" : "1002"}
        
        if self.db["Users"].find_one({"username": user_data['username']}):
            return {"error" : "1003"}
        
        if self.db["Users"].find_one({"_id": user_data['idUser']}):
            return {"error" : "1001"}
        
        user_data["_id"] = user_data.pop("idUser")
        
        user_id = self.collection.insert_one(user_data).inserted_id
        
        return str(user_id)

    def get_user_by_id(self, user_id: str) -> dict:
        user_data = self.collection.find_one({'_id': user_id})
        if user_data:
            # Convertir el resultado en un diccionario
            user_data_dict = dict(user_data)
            return user_data_dict
        else:
            return {"error": "1050"}


    def update_user(self, user_id: str, update_data: dict) -> dict:

        user_data = self.get_user_by_id(user_id)
        if not user_data:
            return {"error": "1050"} 
        
        if "username" in update_data or "email" in update_data:
            return {"error": "1053"} 
        
        update_fields = {key: value for key, value in update_data.items() if key not in {"username", "email"}}
        result = self.collection.update_one({'_id': user_id}, {'$set': update_fields})
        
        if result.modified_count > 0:
            return {"worked": "true"} 
        else:
            return {"error": "1051"} 


    def delete_user(self, user_id: UUID) -> dict:
        result = self.collection.delete_one({'_id': user_id})
        if result.deleted_count > 0:
            return {"worked" : "true"}
        else:
            return {"error" : "1052"}
    
    def verify_user_credentials(self, username: str, password: str) -> bool:
        user_data = self.collection.find_one({"username": username, "password": password})
        return user_data is not None
    
    def login_user(self, username: str = None, password: str = None, email: str = None) -> bool:
        if username is not None and password is not None:
            user_data = self.collection.find_one({"username": username, "password": password})
            if user_data:
                return user_data
            else:
                return {"error": 1020} 
            
        elif email is not None and password is not None:
            user_data = self.collection.find_one({"email": email, "password": password})
            if user_data:
                return user_data
            else:
                return {"error": 1020}
            
        else:
            return {"error": 1020}
