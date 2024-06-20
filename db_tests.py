from db.db import DB
import uuid

db = DB('192.168.178.49', 'neko', 'Bigmischa98!', 'minecraft')

id = "test"
user = "katse2"
password = "test123"
balance = 5000

#print(f"{id}:{user}:{password}:{balance}")
result = db.roller_get_all_items()
for i in result:
    print(i)