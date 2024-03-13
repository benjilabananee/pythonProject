from src.Personn.personn import Person
import json


class Employee(Person):
    def __init__(self, data: dict):
        super().__init__(data)
        self.department = data.get("department", "")
        self.salary = data.get("salary", 0)

    def save_to_json(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.__dict__, file, indent=4)
