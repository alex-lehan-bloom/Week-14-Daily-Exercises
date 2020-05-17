from ExtendedClass import ExtendedClass
import json

class JsonablePost(ExtendedClass):
    def __init__(self, post):
        super().__init__(post)

    def create_json(self):
        return json.dumps(self.__dict__)
