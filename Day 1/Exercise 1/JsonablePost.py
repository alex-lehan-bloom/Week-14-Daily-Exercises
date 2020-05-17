from ExtendedClass import ExtendedClass
import json

class JsonablePost:
    def __init__(self, post):
        self.post = post

    def create_json(self):
        my_extended_class = ExtendedClass(self.post)
        json_data = json.dumps(my_extended_class.__dict__)
        return json_data
