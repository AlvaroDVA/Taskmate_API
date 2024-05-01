from typing import List

from day import Day
from page import Page


class User() :
    def __init__(self, 
                 username : str,
                 password : str,
                 email : str,
                 avatarUri : str,
                 dayList : List[Day],
                 notebookPages : List[Page]
                 ):
        self.username = username,
        self.password = password,
        self.email = email,
        self.avatarUri = avatarUri,
        self.dayList = dayList,
        self.notebookPages = notebookPages