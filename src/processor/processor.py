import json
import pandas as pd
from src.Personn.employee import Employee
from src.Mongodb_handler.mongo import MongoDBManager



class DataProcessor:
    def __init__(self, input_file_directory: str, output_file_name_after_trans: str,
                 output_file_dir_for_mutual_friends: str):
        self.input_file = input_file_directory
        self.output_file_name_after_trans = output_file_name_after_trans
        self.json_data = self._extract_json_data()
        self.output_file_dir_for_mutual_friends = output_file_dir_for_mutual_friends

    def _extract_json_data(self):
        with open(self.input_file, 'r') as file:
            return json.load(file)

    @staticmethod
    def _save_json_to_disk(file_name: str, json_data: dict):
        with open(file_name, 'w') as outfile:
            json.dump(json_data, outfile, indent=2)

    def _delete_json_file_from_disk(self, file_name: str):
        pass

    def save_each_file_with_enrichment(self):
        for person_data in self.json_data:
            employee = Employee(person_data)
            self._save_json_to_disk(self.output_file_name_after_trans + f'{employee.guid}.json', vars(employee))
            if mongo.find_document_by_key('guid', employee.guid, 'employee_enrichments') is None:
                mongo.insert_document('employee_enrichments', vars(employee))
                print(f'new Document with guid {employee.guid} was inserted!!')
            else:
                mongo.update_document('guid', employee.guid, vars(employee), 'employee_enrichments')
                print(f'new Document with guid {employee.guid} was updated!!')

            self._delete_json_file_from_disk(self.input_file)

    def find_mutual_friends(self):
        df = pd.DataFrame(self.json_data)

        for i in range(len(df)):
            for j in range(i + 1, len(df)):
                friends1 = set([item['name'] for item in df['friends'][i]])
                friends2 = set([item['name'] for item in df['friends'][j]])
                mutual_friends = friends1.intersection(friends2)
                if mutual_friends:
                    key = '{}_{}'.format(df.iloc[i]['_id'], df.iloc[j]['_id'])
                    dict_to_insert = {key: list(mutual_friends)}
                    self._save_json_to_disk(self.output_file_dir_for_mutual_friends + key + '.json', dict_to_insert)
                    document_in_db = mongo.find_document_by_dynamic_key(key, 'mutual_friends')
                    if document_in_db is not None:
                        mongo.update_document(key, document_in_db[key], {key: list(mutual_friends)}, 'mutual_friends')
                        print(f'document {key} exist on db schema mutual friends and was updated')
                    else:
                        mongo.insert_document('mutual_friends', dict_to_insert)
                        print(f'new document {key} was inserted on db schema mutual_friends!')

        self._delete_json_file_from_disk(self.input_file)


if __name__ == "__main__":
    mongo = MongoDBManager('localhost', 27017, 'my_database')
    process_data = DataProcessor(
        'C:\\Users\\benji\\PycharmProjects\\pythonProject\\file_to_be_transformed\\jsonEx.json',
        'C:\\Users\\benji\\PycharmProjects\\pythonProject\\file_to_be_loaded_into_mongo\\',
        'C:\\Users\\benji\\PycharmProjects\\pythonProject\\mutual_friend_save\\')

    while (True):
        process_data.find_mutual_friends()
        process_data.save_each_file_with_enrichment()
