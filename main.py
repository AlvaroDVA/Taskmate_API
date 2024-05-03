import json
from typing import List
from fastapi import Body, FastAPI, Request
from fastapi.params import Header

from models.element_task import create_element_task_from_json
from repositories.user_repository import UserRepository
from repositories.task_repository import TaskRepository

app = FastAPI()

def load_config(filename):
    with open(filename, "r") as file:
        config = json.load(file)
    return config

config = load_config("config.json")
database_config = config["database"]

user_repo = UserRepository(database_config)
task_repo = TaskRepository(database_config)


@app.get("/hello")
def read_root():
    return {"message": "¡Hola mundo!"}


@app.post("/users")
async def create_user(user_data: dict):
    required_fields = ["idUser", "username", "password", "email", "avatar_uri"]
    for field in required_fields:
        if field not in user_data:
            return {"error" : "1030"}
    
    saved_user = user_repo.create_user(user_data)
    return saved_user

@app.get("/users")
async def get_user_by_id(request: Request):
    user_data = await request.json()
    if user_data is None or "idUser" not in user_data:
        return {"error": "1023"}

    user_id = user_data["idUser"]
    
    user = request.headers.get("username")
    password = request.headers.get("password")

    if user is None or password is None:
        return {"error": "1030"}
    
    if not user_repo.verify_user_credentials(user, password):
        return {"error": "1020"}
    else:
        return user_repo.get_user_by_id(user_id, user)

@app.put("/users")
async def update_user(request: Request):
    user_data = await request.json()
    
    user = request.headers.get("username")
    password = request.headers.get("password")

    if user is None or password is None:
        return {"error": "1030"}

    if not user_repo.verify_user_credentials(user, password):
        return {"error" : "1020"}
    
    user_id = user_data.pop("idUser", None)

    allowed_fields = {"username", "password", "email", "avatar_uri"}
    for key in user_data.keys():
        if key not in allowed_fields:
            return {"error" : "1030"}
        
    if user_id is None:
        return {"error": "1023"}

    return user_repo.update_user(user_id, user_data,user)

@app.delete("/users")
async def delete_user(request: Request):
    user_data = await request.json()
    if user_data is None or "idUser" not in user_data:
        return {"error": "1061"}

    user_id = user_data["idUser"]
    user = request.headers.get("username")
    password = request.headers.get("password")
    if not user_repo.verify_user_credentials(user, password):
        return {"error" : "1020"}
    else:
        return user_repo.delete_user(user_id, user)

@app.post("/login")
async def login_user(request: Request):
    username = request.headers.get("username")
    password = request.headers.get("password")
    email = request.headers.get("email")
    if username is None and email is None:
        return {"error" : "1021"}
    if password is None:
        return {"error" : "1022"}
    
    return user_repo.login_user(username=username, password=password, email=email)

@app.post("/tasks")
async def create_task(request: Request):
    task_data = await request.json()
    if task_data is None or "idUser" not in task_data or "date" not in task_data or "tasks" not in task_data:
        return {"error" : "1061"}
    
    user = request.headers.get("username")
    password = request.headers.get("password")
    if not user_repo.verify_user_credentials(user, password):
        return {"error" : "1020"}
    
    user_id = task_data["idUser"]
    date = task_data["date"]
    tasks = task_data["tasks"]

    if not user_repo.verify_user_connected(user, user_id):
        return {"error" : "1020"}
    
    return task_repo.create_task(user_id, date, tasks)
        
@app.get("/tasks")
async def get_tasks_by_date(request: Request):
    task_data = await request.json()
    if task_data is None or "idUser" not in task_data or "date" not in task_data:
        return {"error" : "1061"}
    
    user = request.headers.get("username")
    password = request.headers.get("password")
    
    if not user_repo.verify_user_credentials(user, password):
        return {"error" : "1020"}
    
    user_id = task_data["idUser"]
    date = task_data["date"]

    if not user_repo.verify_user_connected(user, user_id):
        return {"error" : "1020"}
    
    tasks = task_repo.get_tasks_by_date(user_id, date)
    if tasks:
        return {"tasks": tasks}
    else:
        return {"tasks" : [] }
