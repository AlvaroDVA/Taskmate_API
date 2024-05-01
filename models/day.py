from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel

from models.page import Page
from task import Task

class Day () :
    def __init__(self, date : str, todayTask : List[Task]) :
        self.date = datetime.strptime(date, "%Y-%m-%d").date(),
        self.todayTask = todayTask

class UserCreate(BaseModel):
    id: UUID
    username: str
    password: str
    email: str
    avatar_uri: str
    day_list: List[Day] = []
    notebook_pages: List[Page] = []