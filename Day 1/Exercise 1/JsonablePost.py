from ExtendedClass import ExtendedClass
import json

class JsonablePost(ExtendedClass):
    def __init__(self, created_at, user_id, id, title, body):
        super().__init__(created_at, user_id, id, title, body)

    def create_json(self):
        my_extended_class = ExtendedClass(self.created_at, self.user_id, self.id, self.title, self.body)
        json_data = json.dumps(my_extended_class)
        return json_data