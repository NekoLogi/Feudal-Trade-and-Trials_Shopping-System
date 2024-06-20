import json
from db.db import DB


db = DB('192.168.178.49', 'neko', 'Bigmischa98!', 'minecraft')

data = None
with open('vanilla_conversion.json', 'r') as file:
    data = json.load(file)

for name, tier in data.items():
    id_name = name
    display_name = name.replace("_", " ").replace("minecraft:", "").title()
    print(f"{str(tier).ljust(2)} | {str(display_name).ljust(40)} | {str(name).ljust(50)}")
    db.shop_item_create(tier, display_name, name)