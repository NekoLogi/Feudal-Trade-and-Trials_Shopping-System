from db.db import DB
from flask import Flask, request, render_template, jsonify
from waitress import serve
import json
import uuid


app = Flask(__name__)

currency = "Taler"

# Database
with open('db_data.json', 'r') as file:
    data = json.load(file)

db_host = data['address']
db_user = data['username']
db_password = data['password']
db_database = data['database']



# Redirects
@app.route('/', defaults={'path': ''})
def hello_world():
    if request.method == 'GET':
        return render_template('login.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        return f'Hello {name}!'
    elif request.method == 'GET':
        return request.args.get('name')



# Banking functions
@app.route('/banking/transaction/transfer', methods=['PUT'])
def banking_transfer():
    try:
        data = request.data.decode('utf-8')
        json = to_json(data)
    except Exception as e:
        return error('Invalid JSON!')
    
    if is_none_or_empty(json['uuid']):
        return error('UUID from sender is required!')
    if is_none_or_empty(json['from']):
        return error('Username for sender is required!')
    if is_none_or_empty(json['to']):
        return error('Username for receiver is required!')
    if is_none_or_empty(json['amount']):
        return error('Amount is required!')
    if (json['amount'] < 1):
        return error('Amount must be more than 0!')

    
    sender = [json['uuid'], json['from']]
    receiver = json['to']
    amount = json['amount']

    db = DB(db_host, db_user, db_password, db_database)
    if db.user_transfer(sender[0], sender[1], receiver, amount):
        return jsonify(status=True)
    return error('Processing failed, contact admin, if error persists!')

@app.route('/banking/transaction/withdraw', methods=['PUT'])
def banking_withdraw():
    try:
        data = request.data.decode('utf-8')
        json = to_json(data)
    except Exception as e:
        return error('Invalid JSON!')
    
    if is_none_or_empty(json['uuid']):
        return error('UUID from sender is required!')
    if is_none_or_empty(json['from']):
        return error('Username for sender is required!')
    if is_none_or_empty(json['amount']):
        return error('Amount is required!')
    if (json['amount'] < 1):
        return error('Amount must be more than 0!')

    
    user = [json['uuid'], json['from']]
    amount = json['amount']

    db = DB(db_host, db_user, db_password, db_database)
    if db.user_withdraw(user[0], user[1], amount):
        return jsonify(status=True)
    return error('Processing failed, contact admin, if error persists!')

@app.route('/banking/transaction/deposit', methods=['PUT'])
def banking_deposit():
    try:
        data = request.data.decode('utf-8')
        json = to_json(data)
    except Exception as e:
        return error('Invalid JSON!')
    
    if is_none_or_empty(json['uuid']):
        return error('UUID from sender is required!')
    if is_none_or_empty(json['from']):
        return error('Username for sender is required!')
    if is_none_or_empty(json['amount']):
        return error('Amount is required!')
    if (json['amount'] < 1):
        return error('Amount must be more than 0!')

    user = [json['uuid'], json['from']]
    amount = json['amount']
    db = DB(db_host, db_user, db_password, db_database)
    if db.user_deposit(user[0], user[1], amount):
        return jsonify(status=True)
    return error('Processing failed, contact admin, if error persists!')

@app.route('/banking/account', methods=['POST', 'DELETE', 'GET'])
def banking_account():
# GET
    if request.method == 'GET':
        if is_none_or_empty(request.args.get('uuid')):
            return error('UUID is required!')
        if is_none_or_empty(request.args.get('from')):
            return error('Username is required!')
        id = request.args.get('uuid')
        username = request.args.get('from')
        db = DB(db_host, db_user, db_password, db_database)
        result = db.user_get_by_uuid(id, username)
        if result == None:
            return error('User not found!')
        items = {
            "id":result.get("id"),
            "uuid":result.get("uuid"),
            "from":result.get("username"),
            "balance":result.get("balance"),
            "currency":currency
        }
        return to_json(items)
    
    try:
        data = request.data.decode('utf-8')
        json = to_json(data)
    except Exception as e:
        return error('Invalid JSON!')
    
# POST
    if request.method == 'POST':
        if is_none_or_empty(json['from']):
            return error('Username is required!')
        if is_none_or_empty(json['pin']):
            return error('Pin is required!')
        id = uuid.uuid4()
        username = json['from']
        pin = json['pin']
        db = DB(db_host, db_user, db_password, db_database)
        if db.user_create(id, username, pin, 0):
            result = db.user_get_by_uuid(id, username)
        if result == None:
            return error('User not found!')
        items = []
        items = {
            "id":result.get("id"),
            "uuid":result.get("uuid"),
            "from":result.get("username"),
            "balance":result.get("balance"),
            "pin":result.get("password"),
            "currency":currency
        }
        return to_json(items)
            
# DELETE
    elif request.method == 'DELETE':
        if is_none_or_empty(request.args.get('uuid')):
            return error('UUID is required!')
        if is_none_or_empty(request.args.get('from')):
            return error('Username is required!')
        if is_none_or_empty(request.args.get('pin')):
            return error('Pin is required!')
        id = request.args.get('uuid')
        username = request.args.get('from')
        pin = request.args.get('pin')
        db = DB(db_host, db_user, db_password, db_database)
        result = db.user_get_by_uuid(id, username)
        if result != None:
            if login(pin, result.get('password')):
                db.user_remove(id, username)
                return jsonify(status=True)
            return error('Failed to login, check your input!')
        return error('User not found!')
    return error('Processing failed, contact admin, if error persists!')

@app.route('/banking/card', methods=['POST'])
def banking_card():
    try:
        data = request.data.decode('utf-8')
        json = to_json(data)
    except Exception as e:
        return error('Invalid JSON!')
    
    if request.method == 'POST':
        if is_none_or_empty(json['from']):
            return error('Username is required!')
        if is_none_or_empty(json['pin']):
            return error('Pin is required!')
        username = json['from']
        pin = json['pin']
        db = DB(db_host, db_user, db_password, db_database)
        result = db.user_get_by_pin(pin, username)
        if result == None:
            return error('User not found!')
        items = []
        items = {
            "id":result.get("id"),
            "uuid":result.get("uuid"),
            "from":result.get("username"),
            "balance":result.get("balance"),
            "pin":result.get("password"),
            "currency":currency
        }
        return to_json(items)
    return error('Processing failed, contact admin, if error persists!')



# Shop functions
@app.route('/shop/items/count', methods=['GET'])
def shop_get_item_count():
    db = DB(db_host, db_user, db_password, db_database)
    count = db.shop_get_item_count()
    if count != None:
        return jsonify(count=count)
    return error('Failed to get item count!')

@app.route('/shop/item', methods=['GET'])
def shop_get_item():
    if not is_none_or_empty(request.args.get('name')):
        name = request.args.get('name')
        db = DB(db_host, db_user, db_password, db_database)
        result = db.shop_get_item_by_name(name)
        if result != None:
            return to_json(result)
        return error('Item not found!')
    
    db = DB(db_host, db_user, db_password, db_database)
    result = db.shop_get_all_items()
    if result != None:
        return to_json(result)
    return error('Processing failed, contact admin, if error persists!')

@app.route('/shop/converter', methods=['GET'])
def shop_convert_to_currency():
    name = request.args.get('name')
    amount = request.args.get('amount')
    if is_none_or_empty(name):
        return error('Item name is required!')
    db = DB(db_host, db_user, db_password, db_database)
    item = db.shop_get_item_by_name(name)
    if item is None:
        return error('Item not found!')
    price = tier_to_currency(item['tier'])
    if not is_none_or_empty(name):
        price = int(amount) * price
    json = jsonify(price=price,
                   display_name=str(item['displayname']),
                   name=str(item['name'])
                   )
    return json

@app.route('/shop/recycle', methods=['PUT'])
def shop_recycle():
    data = request.data.decode('utf-8')
    json = to_json(data)
    
    if is_none_or_empty(json['uuid']):
        return error('UUID from sender is required!')
    if is_none_or_empty(json['from']):
        return error('Username is required!')
    if is_none_or_empty(json['name']):
        return error('Item-id is required!')
    if is_none_or_empty(json['amount']):
        return error('Amount is required!')
    if (json['amount'] < 1):
        return error('Amount must be more than 0!')

    db = DB(db_host, db_user, db_password, db_database)
    item = db.shop_get_item_by_name(json['name'])
    if item is None:
        return error('Item not found!')
    
    if item['recycled'] == False:
        db.shop_item_recycled(json['name'])

    price = tier_to_currency(item['tier'])
    price = int(json['amount']) * price

    if not db.user_deposit(json['uuid'], json['from'], price):
        return error(f"Failed to recycle Item!")
    
    item = db.shop_get_item_by_name(json['name'])
    json = jsonify(price=price,
                   name=item['name'],
                   display_name=item['displayname'],
                   amount=json['amount'],
                   recycled=item['recycled'],
                   currency=currency)
    return json

# Item-Roller functions
@app.route('/roller/items', methods=['GET'])
def shop_get_items():
    db = DB(db_host, db_user, db_password, db_database)
    roller_items = db.roller_get_all_items()
    if roller_items == None:
        return error("No items recycled yet to display.")
    
    items = []
    for i in range(0, len(roller_items)):
        price = tier_to_currency(roller_items[i].get("tier"))
        end_price = calculate_sale_price(price, roller_items[i].get("sale"))
        items.append({
            "id":roller_items[i].get("id"),
            "tier":roller_items[i].get("tier"),
            "name":roller_items[i].get("name"),
            "display_name":roller_items[i].get("displayname"),
            "description":roller_items[i].get("description"),
            "amount":roller_items[i].get("amount"),
            "price":end_price,
            "currency":currency
        })
    return to_json(items)

@app.route('/roller/item/purchase', methods=['PUT'])
def shop_buy_item():
    data = request.data.decode('utf-8')
    json = to_json(data)
    if is_none_or_empty(json['uuid']):
        return error('UUID from sender is required!')
    if is_none_or_empty(json['from']):
        return error('Username for sender is required!')
    if is_none_or_empty(json['amount']):
        return error('Item amount is required!')
    if is_none_or_empty(json['id']):
        return error('Shop item id is required!')

    
    user = [json['uuid'], json['from']]
    id = json['id']
    amount = json['amount']

    db = DB(db_host, db_user, db_password, db_database)
    db_account = db.user_get_by_uuid(user[0], user[1])
    if db_account == None:
        return error('User not found!')
    roller_item = db.roller_get_item_by_id(id)
    if roller_item == None:
        return error('Item is old, reload shop for new item')
    
    price = tier_to_currency(roller_item.get("tier"))
    end_price = amount * calculate_sale_price(price, roller_item.get("sale"))
    if db_account.get("balance") < end_price:
        return error(f'Not enough {currency}, required: {end_price} {currency}!')
    if not db.roller_item_purchase_by_id(id, amount):
        return error('Not enough Items or Item doesnt exist!')
    if not db.user_withdraw(db_account.get("uuid"),
                            db_account.get("username"),
                            end_price):
        return error('Purchase failed, contact admin, if error persists!')
    
    items = {
        "id":roller_item.get("id"),
        "name":roller_item.get("name"),
        "display_name":roller_item.get("displayname"),
        "description":roller_item.get("description"),
        "tier":roller_item.get("tier"),
        "price":end_price,
        "currency":currency,
        "command":generate_command(roller_item, amount)
    }
    return to_json(items)



# utils
def to_json(data):
    try:
        return json.loads(data)
    except Exception:
        return json.dumps(data)

def error(message):
    print(message)
    return jsonify(error=str(message))

def tier_to_currency(tier):
    try:
        with open('tier.json', 'r') as file:
            tiers = json.load(file)
            return tiers[str(tier)]
    except Exception as e:
        return None

def calculate_sale_price(price, sale_percentage):
    return int(price * (100 - sale_percentage) / 100)

def is_none_or_empty(s):
    if s == None or s == "":
        return True
    return False

def login(input_password, db_password):
    if input_password == db_password:
        return True
    return False

def generate_command(item, amount):
    command = f"/give @p {item.get("name")}"
    if not is_none_or_empty(item.get("enchantments")):
        command += '{display:{Name:"\\"' + item.get("displayname") + '\\"",Lore:["\\"' + item.get("description") + '\\""]},'
        command += f'StoredEnchantments:[{item.get("enchantments")}],'
        command += ' HideFlags:63'
        command += '}'
    command += ' ' + str(amount)
    return command


if __name__ == '__main__':
    serve(app, host='127.0.0.1', port=5000)
    #app.run(host='127.0.0.1', port=5000, debug=True, threaded=True)