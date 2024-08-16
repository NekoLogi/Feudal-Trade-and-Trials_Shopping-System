from db.db import DB
import json
import uuid

with open('db_data.json', 'r') as file:
    data = json.load(file)
db = DB(data['address'], data['username'], data['password'], data['database'])

id = "test"
user = "katse2"
password = "test123"
balance = 5000

#print(f"{id}:{user}:{password}:{balance}")
result = db.roller_get_all_items()
for i in result:
    print(i)