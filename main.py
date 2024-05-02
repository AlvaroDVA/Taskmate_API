from configparser import ConfigParser
import json
from typing import List
from fastapi import Body, FastAPI

from models.element_task import create_element_task_from_json
from repositories.user_repository import UserRepository

app = FastAPI()

def load_config(filename):
    with open(filename, "r") as file:
        config = json.load(file)
    return config

config = load_config("config.json")
database_config = config["database"]

user_repo = UserRepository(database_config)


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


