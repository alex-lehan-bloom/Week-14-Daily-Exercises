from BaseClass import BaseClass
from datetime import datetime


class ExtendedClass(BaseClass):
    def __init__(self, post):
        date = datetime.now()
        self.created_at = date.strftime("%m/%d/%Y %H:%M:%S")
        super().__init__(post)