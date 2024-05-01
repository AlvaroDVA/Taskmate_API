from abc import ABC, abstractmethod


class Page(ABC):
    def __init__(self) :
        self

class StandardPage(Page):
    def __init__(self,
                 pageId : int,
                 pageNumber : int,
                 title : str,
                 text : str
                 ) :
        self.pageId = pageId,
        self.pageNumber = pageNumber,
        self.title = title,
        self.text = text


class ImagePage1(Page):
    def __init__(self,
                 pageId : int,
                 pageNumber : int,
                 title : str,
                 text : str,
                 headerImage : str,
                 footerImage : str
                 ) :
        self.pageId = pageId,
        self.pageNumber = pageNumber,
        self.title = title,
        self.text = text,
        self.headerImage = headerImage,
        self.footerImage = footerImage

class ImagePage2(Page):
    def __init__(self,
                 pageId : int,
                 pageNumber : int,
                 title : str,
                 text : str,
                 headerImage : str
                 ) :
        self.pageId = pageId,
        self.pageNumber = pageNumber,
        self.title = title,
        self.text = text,
        self.headerImage = headerImage

