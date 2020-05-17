from BaseClass import BaseClass
from RandomDateTime import create_random_date


class ExtendedClass(BaseClass):
    def __init__(self, post):
        self.created_at = create_random_date()
        super().__init__(post)