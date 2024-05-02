from typing import Dict, List, Union
from uuid import UUID
from abc import ABC, abstractmethod
from fastapi import File

from models.sublist import SubList


class ElementTask (ABC):
    def __init__(self,
                 elementId : UUID,
                 taskOrder : int
                 ):
        self.elementId = elementId,
        self.taskOrder = taskOrder

class ImageTask(ElementTask):
    def __init__(self,
                 elementId : UUID,
                 taskOrder : int,
                 image : File
                 ):
        super().__init__(elementId, taskOrder)
        self.image = image

class TextTask(ElementTask):
    def __init__(self,
                 elementId : UUID,
                 taskOrder : int,
                 text : str
                 ):
        super().__init__(elementId, taskOrder)
        self.text = text

class VideoElement(ElementTask):
    def __init__(self,
                 elementId : UUID,
                 taskOrder : int,
                 video : File
                 ):
        super().__init__(elementId, taskOrder)
        self.video = video

class ListElement(ElementTask):
    def __init__(self,
                 elementId : UUID,
                 taskOrder : int,
                 video : str,
                 subList : List[SubList]
                 ):
        super().__init__(elementId, taskOrder)
        self.video = video

def create_element_task_from_json(json_data: Dict[str, Union[UUID, int, str, File, List]]) -> ElementTask:
    if 'image' in json_data:
        return ImageTask(
            elementId=json_data['elementId'],
            taskOrder=json_data['taskOrder'],
            image=json_data['image']
        )
    elif 'text' in json_data:
        return TextTask(
            elementId=json_data['elementId'],
            taskOrder=json_data['taskOrder'],
            text=json_data['text']
        )
    elif 'video' in json_data:
        return VideoElement(
            elementId=json_data['elementId'],
            taskOrder=json_data['taskOrder'],
            video=json_data['video']
        )
    elif 'subList' in json_data:
        return ListElement(
            elementId=json_data['elementId'],
            taskOrder=json_data['taskOrder'],
            video=json_data['video'],
            subList=json_data['subList']
        )
    else:
        raise ValueError('JSON no contiene información suficiente para crear una instancia de ElementTask')