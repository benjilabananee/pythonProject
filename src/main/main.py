import json
from src.Personn.employee import Employee

with open('C:\\Users\\benji\\PycharmProjects\\pythonProject\\file_to_be_transformed\\jsonEx.json', 'r') as file:
    json_data = json.load(file)

for person_data in json_data:
    person = Employee(person_data)
    filename = 'C:\\Users\\benji\\PycharmProjects\\pythonProject\\file_to_be_loaded_into_mongo\\' + f'{person.guid}.json'
    person.save_to_json(filename)
    print(f'{filename} saved successfully.')

