The goal in this Project is to get all json employee data from a folder (the process will run in a while loop everytime) and for each of this json files seperate the big json into small one that will be pushed into mongo db after being modified
1) get the data from json and make manipulation of this data
2) separate the big json into smaller json when:
   - first type: each json will represent one employee (the data will be transformed)
   - second type: json for mutual friends between each of the employee that was in the original big json
3) insert the json into MongoDB (you'll need to run a container for mongodb)
4) receive other json and make a query on mongo by index to see if the data exist on db and if it's exist update the json on mongo
   and if it's not insert the new data.
