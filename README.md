The goal in this Project is to get all json employee data from a folder and for each of this json file and to seperate the big json into smalls json that will be pushed into mongo db
1) get the data from json and make manipulation of this data
2) separate the big json into smaller json when:
   - first type: json for one employee with the modification
   - second type: json for mutual friends between each of the friends that was in the original big json
3) insert the json into MongoDB
4) receive other json and make a query on mongo by index to see if the data exist on db and if it's exist update the json on mongo
   and if it's not insert the new data.
