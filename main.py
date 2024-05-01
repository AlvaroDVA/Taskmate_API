from typing import List
from fastapi import Body, FastAPI

from models.element_task import create_element_task_from_json

app = FastAPI()

@app.get("/hello")
def read_root():
    return {"message": "¡Hola mundo!"}

@app.post('/tasks')
async def create_tasks(task_data: List[dict] = Body(...)):
    tasks = []
    for task_dict in task_data:
        task = create_element_task_from_json(task_dict)
        tasks.append(task)

        
    return {"message": "Tareas creadas con éxito"}
