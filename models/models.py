# models.py
from pydantic import BaseModel, Field
from typing import List

class Page(BaseModel):
    pageNumber: int = Field(..., example=1)
    text: str = Field(..., example="Page content")

class NotebookPage(BaseModel):
    pages: List[Page] = Field(..., example=[{"pageNumber": 1, "text": "Page content"}])

class User(BaseModel):
    idUser: str
    username: str
    password: str
    email: str
    avatar: str


class DeleteUser(BaseModel):
    idUser: str

class TaskData(BaseModel):
    idUser: str
    date: str
    tasks: List[dict]