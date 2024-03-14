import pandas as pd
import json


def find_mutual_friends(json_list):
    # Convert JSON list to DataFrame
    df = pd.DataFrame(json_list)

    # Initialize an empty list to store mutual friends
    mutual_friends_list = []

    # Iterate through combinations of JSON objects
    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            friends1 = set(df.iloc[i]['friends'])
            friends2 = set(df.iloc[j]['friends'])
            mutual_friends = friends1.intersection(friends2)
            mutual_friends_list.append({'{}_{}'.format(df.iloc[i]['_id'], df.iloc[j]['_id']): list(mutual_friends)})
    return mutual_friends_list


# Convert the list of dictionaries to JSON format


# Example list of JSON objects
json_list = [
    {
        "_id": "65eee2e6143c9f64752ff4ed",
        "friends": ["Serena Whitaker", "Alexandria Gill", "Simon Hanson"]
    },
    {
        "_id": "some_other_id",
        "friends": ["Serena Whitaker", "John Doe", "Simon Hanson"]
    },
    {
        "_id": "another_id",
        "friends": ["John Doe", "Mamie Cline", "Alexandria Gill"]
    },
    {
        "_id": "yet_another_id",
        "friends": ["Simon Hanson", "Serena Whitaker", "John Doe"]
    }
]

# Finding mutual friends using pandas DataFrame
mutual_friends_list = find_mutual_friends(json_list)
mutual_friends_json = json.dumps(mutual_friends_list)

print("Mutual Friends JSON:")
print(mutual_friends_json)
# print(mutual_friends_list)
