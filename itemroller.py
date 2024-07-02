import random
import json
from db.db import DB
from time import sleep, mktime, localtime, struct_time
from datetime import datetime, timedelta
from server import tier_to_currency, calculate_sale_price

# Database
db_host = '192.168.178.49'
db_user = 'neko'
db_password = 'Bigmischa98!'
db_database = 'minecraft'

time_file = 'timestamp.json'

db = DB(db_host, db_user, db_password, db_database)

def save_time(time_obj, filename):
    time_dict = {
        'tm_year': time_obj.tm_year,
        'tm_mon': time_obj.tm_mon,
        'tm_mday': time_obj.tm_mday,
        'tm_hour': time_obj.tm_hour,
        'tm_min': time_obj.tm_min,
        'tm_sec': time_obj.tm_sec,
        'tm_wday': time_obj.tm_wday,
        'tm_yday': time_obj.tm_yday,
        'tm_isdst': time_obj.tm_isdst
    }
    with open(filename, 'w') as file:
        json.dump(time_dict, file)

def load_time(filename):
    try:
        with open(filename, 'r') as file:
            time_dict = json.load(file)
    
        local_time = struct_time((
            time_dict['tm_year'],
            time_dict['tm_mon'],
            time_dict['tm_mday'],
            time_dict['tm_hour'],
            time_dict['tm_min'],
            time_dict['tm_sec'],
            time_dict['tm_wday'],
            time_dict['tm_yday'],
            time_dict['tm_isdst']
        ))
        return local_time
    except Exception:
        return None


def Chance(value):
    return random.randrange(100) <= value

def get_sale_pct():
    return random.randrange(99)

def has_days_passed(timestamp, days):
    current_time = localtime()
    seconds_in_a_day = 24 * 60 * 60
    
    current_time_seconds = mktime(current_time)
    timestamp_seconds = mktime(timestamp)
    time_difference = current_time_seconds - timestamp_seconds
    
    return time_difference >= (seconds_in_a_day * days)

def get_current_date():
    current_time = localtime()
    return struct_time((current_time.tm_year,
                             current_time.tm_mon,
                             current_time.tm_mday,
                             0, 0, 0,
                             current_time.tm_wday,
                             current_time.tm_yday,
                             current_time.tm_isdst))

def add_days_to_time(timestamp, days):
    current_datetime = datetime.fromtimestamp(timestamp)
    added_datetime = current_datetime + timedelta(days=days)
    return added_datetime.timestamp()

def get_tier_rating():
    tiers =   [1,   2,   3,   4,  5,  6,  7,  8,  9,  10]
    weights = [100, 100, 100, 60, 60, 60, 40, 20, 10, 5]
    return random.choices(tiers, weights)[0]

def get_item_amount_by_tier(tier):
    max_amount = [30000, 15000, 5000, 500, 300, 300, 30, 20, 10, 5]
    return random.randint(1, max_amount[tier-1])


def main(amount):
    items = []
    for i in range(0, amount):
        sale = None
        if Chance(1):
            sale = get_sale_pct()
        item = get_new_item()

        item_exists = False
        for e in items:
            for f in range(30):
                if e.get("name") == item.get("name"):
                    item_exists = True
                    item = get_new_item()
                else:
                    item_exists = False
        if item_exists:
            continue

        items.append({
            'tier': item.get('tier'),
            'displayname': item.get('displayname'),
            'name': item.get('name'),
            'amount': get_item_amount_by_tier(item.get('tier')),
            'sale': sale if sale != None and item['tier'] != 1 else 0
            })
    db.roller_table_delete()
    db.roller_table_create()
    for i in range(0, len(items)):
        db.roller_item_add(items[i]['name'], items[i]['amount'], items[i]['sale'])
        print(f"Tier: {items[i]['tier']} Price: {calculate_sale_price(tier_to_currency(items[i]['tier']), items[i]['sale'])} Id: {items[i]['name']}")

def get_new_item():
    db_items = None
    for i in range(10):
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






if __name__ == '__main__':
    first_run = False
    check_time = load_time(time_file)
    check_time = None
    if check_time == None:
        check_time = get_current_date()
        save_time(check_time, time_file)
        first_run = True

    #while True:
        if has_days_passed(check_time, 1) or first_run:
            first_run = False
            main(8)
        sleep(1)