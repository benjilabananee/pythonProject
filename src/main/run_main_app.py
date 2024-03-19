from src.processor.processor import DataProcessor
from src.Mongodb_handler.mongo import MongoDBManager
import os

mongo = MongoDBManager('localhost', 27017, 'my_database')
input_directory = 'C:\\Users\\benji\\PycharmProjects\\pythonProject\\file_to_be_transformed\\'
output_directory_enriched = 'C:\\Users\\benji\\PycharmProjects\\pythonProject\\file_to_be_loaded_into_mongo\\'
output_directory_mutual_friends = 'C:\\Users\\benji\\PycharmProjects\\pythonProject\\mutual_friend_save\\'
count = 0

while True:
    try:
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
