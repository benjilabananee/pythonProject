import json
import os
import pandas as pd
from src.Personn.employee import Employee
from src.Mongodb_handler.mongo import MongoDBManager


class DataProcessor:
    def __init__(self, input_file_directory: str, output_file_name_after_trans: str,
                 output_file_dir_for_mutual_friends: str, mongo: MongoDBManager):
        self.input_file_directory = input_file_directory
        self.output_file_name_after_trans = output_file_name_after_trans
        self.output_file_dir_for_mutual_friends = output_file_dir_for_mutual_friends
        self.mongo = mongo

    def _extract_json_data(self):
        try:
            with open(self.input_file_directory, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Input file '{self.input_file_directory}' not found.")
            return None
        except json.JSONDecodeError:
            print(f"Error decoding JSON file '{self.input_file_directory}'.")
            return None

    def _save_json_to_disk(self, file_name: str, json_data: dict):
        try:
            with open(file_name, 'w') as outfile:
                json.dump(json_data, outfile, indent=2)
        except Exception as e:
            print(f"Error saving JSON data to file '{file_name}': {e}")


    def _delete_json_file_from_disk(self, file_name: str):
        try:
            os.remove(file_name)
        except FileNotFoundError:
            print(f"File '{file_name}' not found.")
        except Exception as e:
            print(f"Error deleting file '{file_name}': {e}")

    def save_each_file_with_enrichment(self):
        json_data = self._extract_json_data()
        if not json_data:
            return

        for person_data in json_data:
            try:
                employee = Employee(person_data)
                file_path = os.path.join(self.output_file_name_after_trans, f'{employee.guid}.json')
                self._save_json_to_disk(file_path, vars(employee))

                existing_doc = self.mongo.find_document_by_key('guid', employee.guid, 'employee_enrichments')
                if existing_doc:
                    self.mongo.update_document('guid', employee.guid, vars(employee), 'employee_enrichments')
                    print(f'Document with guid {employee.guid} updated.')
                else:
                    self.mongo.insert_document('employee_enrichments', vars(employee))
                    print(f'New document with guid {employee.guid} inserted.')

                # self._delete_json_file_from_disk(self.input_file)
            except Exception as e:
                print(f"Error processing employee data: {e}")

    def find_mutual_friends(self):
        json_data = self._extract_json_data()
        if not json_data:
            return

        df = pd.DataFrame(json_data)

        for i in range(len(df)):
            for j in range(i + 1, len(df)):
                try:
                    friends1 = set([item['name'] for item in df['friends'][i]])
                    friends2 = set([item['name'] for item in df['friends'][j]])
                    mutual_friends = friends1.intersection(friends2)
                    if mutual_friends:
                        key = '{}_{}'.format(df.iloc[i]['_id'], df.iloc[j]['_id'])
                        dict_to_insert = {key: list(mutual_friends)}
                        file_path = os.path.join(self.output_file_dir_for_mutual_friends, f'{key}.json')
                        self._save_json_to_disk(file_path, dict_to_insert)

                        existing_doc = self.mongo.find_document_by_dynamic_key(key, 'mutual_friends')
                        if existing_doc:
                            self.mongo.update_document(key, existing_doc[key], {key: list(mutual_friends)},
                                                       'mutual_friends')
                            print(f'Document {key} updated.')
                        else:
                            self.mongo.insert_document('mutual_friends', dict_to_insert)
                            print(f'New document {key} inserted.')
                except Exception as e:
                    print(f"Error finding mutual friends: {e}")


if __name__ == "__main__":
    try:
        mongo = MongoDBManager('localhost', 27017, 'my_database')
        input_directory = 'C:\\Users\\benji\\PycharmProjects\\pythonProject\\file_to_be_transformed\\'
        output_directory_enriched = 'C:\\Users\\benji\\PycharmProjects\\pythonProject\\file_to_be_loaded_into_mongo\\'
        output_directory_mutual_friends = 'C:\\Users\\benji\\PycharmProjects\\pythonProject\\mutual_friend_save\\'


        for filename in os.listdir(input_directory):
            if filename.endswith('.json'):
                input_file_path = input_directory + filename

                process_data = DataProcessor(
                    input_file_path,
                    output_directory_enriched,
                    output_directory_mutual_friends,
                    mongo)

                process_data.find_mutual_friends()
                process_data.save_each_file_with_enrichment()
                os.remove(input_file_path)
    except Exception as e:
        print(f"An error occurred: {e}")
