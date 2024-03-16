import json
import pandas as pd
from src.Personn.employee import Employee


class DataProcessor:
    def __init__(self, input_file_directory: str, output_file_name_after_trans: str,
                 output_file_dir_for_mutual_friends: str):
        self.input_file_directory = input_file_directory
        self.output_file_name_after_trans = output_file_name_after_trans
        self.json_data = self.extract_json_data()
        self.output_file_dir_for_mutual_friends = output_file_dir_for_mutual_friends

    def extract_json_data(self):
        with open(self.input_file_directory, 'r') as file:
            return json.load(file)

    @staticmethod
    def save_json_to_disk(file_name: str, json_data: dict):
        with open(file_name, 'w') as outfile:
            json.dump(json_data, outfile, indent=2)

    def save_each_file_with_enrichment(self):
        employee_list_json = []
        for person_data in self.json_data:
            employee = Employee(person_data)
            file_name = self.output_file_name_after_trans + f'{employee.guid}.json'
            self.save_json_to_disk(file_name, vars(employee)) #convert the employee object into a dictionary
            employee_list_json.append(employee)
            print(f'{file_name} saved successfully as single employee file.')
        return employee_list_json

    def find_mutual_friends(self):
        df = pd.DataFrame(self.json_data)

        for i in range(len(df)):
            for j in range(i + 1, len(df)):
                friends1 = set([item['name'] for item in df['friends'][i]])
                friends2 = set([item['name'] for item in df['friends'][j]])
                mutual_friends = friends1.intersection(friends2)
                if mutual_friends:
                    key = '{}_{}'.format(df.iloc[i]['_id'], df.iloc[j]['_id'])
                    self.save_json_to_disk(self.output_file_dir_for_mutual_friends + key + '.json',
                                           {key: list(mutual_friends)})
                    print(f'{key} mutual friends was saved sucessfully!')


if __name__ == "__main__":
    process_data = DataProcessor(
        'C:\\Users\\benji\\PycharmProjects\\pythonProject\\file_to_be_transformed\\jsonEx.json',
        'C:\\Users\\benji\\PycharmProjects\\pythonProject\\file_to_be_loaded_into_mongo\\',
        'C:\\Users\\benji\\PycharmProjects\\pythonProject\\mutual_friend_save\\')

    process_data.save_each_file_with_enrichment()
    print('******************************')
    process_data.find_mutual_friends()
