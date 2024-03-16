from src.Personn.personn import Person
import json
class Employee(Person):
    def __init__(self, data: dict):
        super().__init__(data)
        self.department = data.get("department", "")
        self.salary = data.get("salary", 0)
        self.experience_year = data.get("experience",0)
