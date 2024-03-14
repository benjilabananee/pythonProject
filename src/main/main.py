import json
from src.Personn.employee import Employee
import pandas as pd


def create_json_data(file_name: str):
    with open(file_name, 'r') as file:
        json_data = json.load(file)
    return json_data


def save_json_to_disk(file_name: str, json_data: dict):
    with open(file_name, 'w') as outfile:
        json.dump(json_data, outfile, indent=2)


def save_each_file_with_enrichment(json_data: dict, file_name: str):
    employee_list_json = []
    for person_data in json_data:
        employee = Employee(person_data)
        filename = file_name + f'{employee.guid}.json'
        employee.save_single_json(filename)
        employee_list_json.append(employee)
        print(f'{filename} saved successfully as single employee file.')
    return employee_list_json


def find_mutual_friends(json_data: dict, directory_to_put_json: str):
    df = pd.DataFrame(json_data)
    mutual_friends_list = []

    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            friends1 = set([item['name'] for item in df['friends'][i]])
            friends2 = set([item['name'] for item in df['friends'][j]])
            mutual_friends = friends1.intersection(friends2)
            if mutual_friends:
                key = '{}_{}'.format(df.iloc[i]['_id'], df.iloc[j]['_id'])
                save_json_to_disk(directory_to_put_json + key + '.json',{key: list(mutual_friends)})


original_json_data = create_json_data(
    'C:\\Users\\benji\\PycharmProjects\\pythonProject\\file_to_be_transformed\\jsonEx.json')

json_data_with_enrichment = save_each_file_with_enrichment(original_json_data,'C:\\Users\\benji\\PycharmProjects\\pythonProject\\file_to_be_loaded_into_mongo\\')

find_mutual_friends(original_json_data,'C:\\Users\\benji\\PycharmProjects\\pythonProject\\mutual_friend_save\\')


