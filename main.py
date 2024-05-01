from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def read_root():
    return {"message": "¡Hola mundo!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
