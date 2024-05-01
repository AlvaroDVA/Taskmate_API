from typing import List
from element_task import ElementTask

class Task:
    def __init__(self,
                  idTask: int,
                  title: str,
                  elementList : List[ElementTask],
                  colorHex : str,
                  isCheked : bool
                    ):
        self.idTask = idTask,
        self.title = title,
        self.elementList = elementList,
        self.colorHex = colorHex,
        self.isCheked = isCheked

    