from configparser import ConfigParser
from datetime import date
from typing import List
from uuid import UUID
from fastapi import Body, FastAPI
from pydantic import BaseModel

from models.day import Day, UserCreate
from models.element_task import create_element_task_from_json
from repositories.user_repository import UserRepository

app = FastAPI()

db_url, db_name = ConfigParser("database.properties")
user_repo = UserRepository(db_url, db_name)


@app.get("/hello")
def read_root():
    return {"message": "¡Hola mundo!"}


@app.post("/users", response_model=UserCreate)
async def create_user(user_data: UserCreate):
    user_dict = user_data.model_dump()
    saved_user = user_repo.save_user(user_dict)
    return saved_user

@app.post('/tasks')
async def create_tasks(task_data: List[dict] = Body(...)):
    tasks = []
    for task_dict in task_data:
        task = create_element_task_from_json(task_dict)
        tasks.append(task)

        
    return {"message": "Tareas creadas con éxito"}
