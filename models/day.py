from datetime import datetime
from typing import List

from task import Task

class Day () :
    def __init__(self, date : str, todayTask : List[Task]) :
        self.date = datetime.strptime(date, "%Y-%m-%d").date(),
        self.todayTask = todayTask