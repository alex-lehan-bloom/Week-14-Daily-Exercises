from BaseClass import BaseClass


class ExtendedClass(BaseClass):
    def __init__(self, created_at, user_id, id, title, body):
        self.created_at = created_at
        super().__init__(user_id, id, title, body)