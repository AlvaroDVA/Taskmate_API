# -*- coding: utf-8 -*-

import json
from typing import List
from fastapi import Body, FastAPI, HTTPException, Request, Response
from fastapi.params import Header

from models.models import DeleteUser, User
from repositories.user_repository import UserRepository

from repositories.task_repository import TaskRepository

app = FastAPI(encoding="utf-8", debug=True)

def load_config(filename):
    with open(filename, "r") as file:
        config = json.load(file)
    return config

config = load_config("config.json")
database_config = config["database"]

user_repo = UserRepository(database_config)
task_repo = TaskRepository(database_config)

# Endpoint para crear usuarios
@app.post("/users")
async def create_user(user_data: dict):
    required_fields = ["idUser", "username", "password", "email", "avatar"]
    for field in required_fields:
        if field not in user_data:
            return {"error" : "1030"}
    
    saved_user = user_repo.create_user(user_data)
    return saved_user

@app.get("/users")
async def get_user_by_id(
    request: Request,
    user_id: str,
    username: str = Header(None, description="Username of the user"),
    password: str = Header(None, description="Password of the user")
):
    if username is None or password is None:
        raise HTTPException(status_code=400, detail="Username and password are required")

    if not user_repo.verify_user_credentials(username, password):
        raise HTTPException(status_code=401, detail="Unauthorized")

    return user_repo.get_user_by_id(user_id, username)

# Endpoint para actualizar usuarios
@app.put("/users")
async def update_user(user_data: dict, 
                      username: str = Header(None, description="Username of the user"), 
                      password: str = Header(None, description="Password of the user")):

    if username is None or password is None:
        return {"error": "1030"}

    if not user_repo.verify_user_credentials(username, password):
        return {"error" : "1020"}
    
    user_id = user_data.pop("idUser", None)

    allowed_fields = {"username", "password", "email", "avatar"}
    for key in user_data.keys():
        if key not in allowed_fields:
            return {"error" : "1030"}
        
    if user_id is None:
        return {"error": "1023"}

    return user_repo.update_user(user_id, user_data, username)

# Endpoint para eliminar usuarios
@app.delete("/users")
async def delete_user(
    user_data: DeleteUser = Body(..., example = {
        "id": "c1356b19-0dd9-49ee-81b5-7f7a78c4655e",
    }
    ),
    username: str = Header(..., description="Username of the user"),
    password: str = Header(..., description="Password of the user")):

    if username is None or password is None:
        return {"error": "1030"}

    if not user_repo.verify_user_credentials(username, password):
        return {"error" : "1020"}
    else:
        return user_repo.delete_user(user_data.idUser, username)

@app.get("/login")
async def login_user(
    username: str = Header(None, description="Username of the user"),
    password: str = Header(None, description="Password of the user"),
):
    if username is None:
        return {"error": "1021"}
    if password is None:
        return {"error": "1022"}

    return user_repo.login_user(username=username, password=password)

# Endpoint para crear tareas
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

# Endpoint para obtener tareas por fecha
@app.get("/tasks")
async def get_tasks_by_date(request: Request):
    user = request.headers.get("username")
    password = request.headers.get("password")
    
    if not user_repo.verify_user_credentials(user, password):
        return {"error" : "1020"}
    
    user_id = request.headers.get("idUser")
    date = request.headers.get("date")

    if user_id is None or date is None:
        return {"error" : "1061"}

    if not user_repo.verify_user_connected(user, user_id):
        return {"error" : "1020"}
    
    tasks = task_repo.get_tasks_by_date(user_id, date)
    if tasks:
        return {"tasks": tasks}
    else:
        return {"tasks" : [] }

# Endpoint para obtener páginas del cuaderno
@app.get("/notebook")
async def get_pages(
    username: str = Header(..., example="user1"),
    password: str = Header(..., example="password123")):
    
    if not user_repo.verify_user_credentials(username, password):
        return {"error" : "1020"}

    notebook = user_repo.get_notebook(username)
    if notebook:
        response_body = json.dumps({"pages": notebook}, ensure_ascii=False)
        response = Response(content=response_body, media_type="application/json; charset=UTF-8")
        return response
    else:
        response_body = json.dumps({"pages": []}, ensure_ascii=False)
        response = Response(content=response_body, media_type="application/json; charset=UTF-8")
        return response
    
@app.post("/notebook")
async def save_pages(
    pages = Body(..., example={"pages": [{
        "pageNumber" : 1, "text" : "Esto es una pagina"
    }, {
        "pageNumber" : 2, "text" : "Esto es una pagina 2"
    }]}),
    username: str = Header(..., example="user1"),
    password: str = Header(..., example="password123")):
    
    """Guarda páginas del cuaderno."""
    if not user_repo.verify_user_credentials(username, password):
        return {"error": "1020"}

    notebook = user_repo.save_notebook(username, pages)
    return {"pages": notebook}