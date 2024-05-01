from typing import List
from uuid import UUID

from day import Day
from page import Page


class User() :
    def __init__(self, 
                 idUser : UUID,
                 username : str,
                 password : str,
                 email : str,
                 avatarUri : str,
                 dayList : List[Day],
                 notebookPages : List[Page]
                 ):
        self.idUser = idUser,
        self.username = username,
        self.password = password,
        self.email = email,
        self.avatarUri = avatarUri,
        self.dayList = dayList,
        self.notebookPages = notebookPages