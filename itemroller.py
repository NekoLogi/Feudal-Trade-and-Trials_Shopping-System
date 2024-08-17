import random
import json
import os
from db.db import DB
from time import sleep
from datetime import datetime, timedelta
from server import tier_to_currency, calculate_sale_price

# Database
with open('db_data.json', 'r') as file:
    data = json.load(file)

db_host = data['address']
db_user = data['username']
db_password = data['password']
db_database = data['database']

time_file = 'timestamp.json'

db = DB(db_host, db_user, db_password, db_database)


def Chance(value):
    return random.randrange(100) <= value

def get_sale_pct():
    return random.randrange(99)

def get_tier_rating():
    tiers =   [1,   2,   3,   4,  5,  6,  7,  8,  9,  10]
    weights = [100, 100, 100, 60, 60, 60, 40, 20, 10, 5]
    return random.choices(tiers, weights)[0]

def get_item_amount_by_tier(tier):
    max_amount = [30000, 15000, 5000, 500, 300, 300, 30, 20, 10, 5]
    return random.randint(1, max_amount[tier-1])


def main(amount):
    items = []
    for i in range(amount):
        sale = None
        if Chance(1):
            sale = get_sale_pct()
        item = get_new_item()

        item_exists = True
        while item_exists:
            if len(items) <= 1:
                item_exists = False
            for e in items:
                if e.get("id") == item.get("id"):
                    print(e.get("id"))
                    print(item.get("id"))
                    item = get_new_item()
                    item_exists = True
                    break
                else:
                    item_exists = False
            sleep(0.5)
        items.append({
            'id': item.get('id'),
            'tier': item.get('tier'),
            'name': item.get('name'),
            'displayname': item.get('displayname'),
            'description': item.get('description'),
            'enchantments': item.get('enchantments'),
            'amount': get_item_amount_by_tier(item.get('tier')),
            'sale': sale if sale != None and item['tier'] != 1 else 0
            })
        
    db.roller_table_delete()
    db.roller_table_create()
    for i in range(0, len(items)):
        db.roller_item_add(items[i]['id'], items[i]['tier'], items[i]['name'], items[i]['displayname'], items[i]['description'], items[i]['enchantments'], items[i]['amount'], items[i]['sale'])
        print(f"{str(items[i]['id']).ljust(4)} | {str(items[i]['tier']).ljust(2)} | {str(items[i]['name']).ljust(40)} | {str(items[i]['displayname']).ljust(40)} | {items[i]['description']} | {items[i]['enchantments']} | {str(items[i]['amount']).ljust(20)} | {str(calculate_sale_price(tier_to_currency(items[i]['tier']), items[i]['sale'])).ljust(20)}")

def get_new_item():
    db_items = []
    while True:
        if db_items == None or len(db_items) == 0:
            tier = get_tier_rating()
            db_items = db.shop_get_item_by_tier(tier)
            sleep(0.5)
        else:
            break
    item = None
    if len(db_items) == 1:
        item = db_items[0]
    else:
        item = db_items[random.randrange(len(db_items) - 1)]
    return item


def save_time_to_json(file_path, minutes):
    current_time = datetime.now()
    target_time = current_time + timedelta(minutes=minutes)
    data = {'target_time': target_time.isoformat()}
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)

def load_time_from_json(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        target_time = datetime.fromisoformat(data['target_time'])
    return target_time

def has_minutes_passed(file_path):
    target_time = load_time_from_json(file_path)
    current_time = datetime.now()
    return current_time >= target_time




if __name__ == '__main__':
    minutes_to_pass = 60
    if not os.path.exists(time_file):
        save_time_to_json(time_file, minutes_to_pass)
    while True:
        test_mode = False
        if has_minutes_passed(time_file) or test_mode:
            main(8)
            save_time_to_json(time_file, minutes_to_pass)
        sleep(1)