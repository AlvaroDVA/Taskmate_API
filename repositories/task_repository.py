from pymongo import MongoClient


class TaskRepository () :
    def __init__(self, config):
        self.db_url = config["db_url"]
        self.db_name = config["db_name"]
        self.username = config["username"]
        self.password = config["password"]
        self.client = MongoClient(self.db_url)
        self.db = self.client[self.db_name]
        self.collection = self.db["Users"]

    def create_task(self, user_id: str, date: str, task_data: dict) -> dict:
        collection = self.db[user_id]
        
        # Busca el documento existente con la fecha proporcionada
        existing_document = collection.find_one({"date": date})
        
        if existing_document:
            # Si el documento existe, actualiza la lista de tareas con la proporcionada en el JSON
            collection.update_one({"date": date}, {"$set": {"tasks": task_data}})
        else:
            # Si el documento no existe, crea uno nuevo con la fecha y la lista de tareas proporcionadas
            document = {"date": date, "tasks": task_data}
            collection.insert_one(document)
        
        return {"worked": True}









    def get_tasks_by_date(self, user_id: str, date: str) -> list:
        collection = self.db[user_id]
        
        document = collection.find_one({"date": date})
        if document:
            return document["tasks"]
        else:
            return []

    def update_task(self, user_id: str, date: str, task_id: str, task_data: dict) -> dict:
        collection = self.db[user_id]
        
        result = collection.update_one({"date": date, "tasks.taskId": task_id}, {"$set": {"tasks.$": task_data}})
        if result.modified_count > 0:
            return {"worked": True}
        else:
            return {"error": "1062"}

    def delete_task(self, user_id: str, date: str, task_id: str) -> dict:
        collection = self.db[user_id]
        
        result = collection.update_one({"date": date}, {"$pull": {"tasks": {"taskId": task_id}}})
        if result.modified_count > 0:
            return {"worked": True}
        else:
            return {"error": "1063"}
    
    