import json
from db.db import DB



def create_items(db):
    data = None
    with open('vanilla_conversion.json', 'r') as file:
        data = json.load(file)

    for name, tier in data.items():
        display_name = name.replace("_", " ").split(':')[1].title()
        print(f"{str(tier).ljust(2)} | {str(display_name).ljust(40)} | {str(name).ljust(50)}")
        db.shop_item_create(tier, display_name, name, "", "", 0)

def create_enchants(db):
    data = None
    with open('enchants.json', 'r') as file:
        data = json.load(file)

    for item in data:
        tier = 10
        id_name = "minecraft:enchanted_book"
        display_name = item['name']
        description = item['description']
        enchantments = item['enchantments']
        print(f"{str(tier).ljust(2)} | {str(display_name).ljust(60)} | {str(enchantments).ljust(100)}")
        db.shop_item_create(tier, display_name, id_name, description, enchantments, 1)

with open('db_data.json', 'r') as file:
    data = json.load(file)
db = DB(data['address'], data['username'], data['password'], data['database'])
create_items(db)
create_enchants(db)