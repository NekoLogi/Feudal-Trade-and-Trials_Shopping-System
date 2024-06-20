import uuid

class Card:
    username = ""
    uuid = ""

    def generate(self, new_username):
        self.username = new_username
        self.uuid = str(uuid.uuid4())

    def info(self):
        return f"Username: {self.username}, UUID: {self.uuid}"