class Person:
    def __init__(self, ID, first_name, last_name):
        self.ID = ID
        self.first_name = first_name
        self.last_name = last_name

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def to_dict(self):
        return {
            "ID": self.ID,
            "first_name": self.first_name,
            "last_name": self.last_name
        }