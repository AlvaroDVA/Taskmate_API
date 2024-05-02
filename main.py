from configparser import ConfigParser
from typing import List
from fastapi import Body, FastAPI

from models.element_task import create_element_task_from_json
from repositories.user_repository import UserRepository

app = FastAPI()

# db_url = "mongodb://taskmate:AnUb1s7302@taskmate.ddns.net:15555/"
db_url = "mongodb://localhost:27017/"
db_name = "taskmate"
user_repo = UserRepository(db_url, db_name)


@app.get("/hello")
def read_root():
    return {"message": "¡Hola mundo!"}


@app.post("/users")
async def create_user(user_data: dict):
    saved_user = user_repo.create_user(user_data)
    return saved_user

@app.post('/tasks')
async def create_tasks(task_data: List[dict] = Body(...)):
    tasks = []
    for task_dict in task_data:
        task = create_element_task_from_json(task_dict)
        tasks.append(task)

        
    return {"message": "Tareas creadas con éxito"}


