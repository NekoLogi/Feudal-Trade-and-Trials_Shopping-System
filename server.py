from db.db import DB
from flask import Flask, request, render_template, jsonify
import json
import uuid


app = Flask(__name__)

currency_name = "Taler"

# Database
db_host = '192.168.178.49'
db_user = 'neko'
db_password = 'Bigmischa98!'
db_database = 'minecraft'



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
        print(e)
        return error('Invalid JSON!')
    
    if is_none_or_empty(json['uuid']):
        return error('UUID from sender is required!')
    if is_none_or_empty(json['from_name']):
        return error('Username for sender is required!')
    if is_none_or_empty(json['to_name']):
        return error('Username for receiver is required!')
    if is_none_or_empty(json['amount']):
        return error('Amount is required!')
    if (json['amount'] < 1):
        return error('Amount must be more than 0!')

    
    sender = [json['uuid'], json['from_name']]
    receiver = json['to_name']
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
        print(e)
        return error('Invalid JSON!')
    
    if is_none_or_empty(json['uuid']):
        return error('UUID from sender is required!')
    if is_none_or_empty(json['from_name']):
        return error('Username for sender is required!')
    if is_none_or_empty(json['amount']):
        return error('Amount is required!')
    if (json['amount'] < 1):
        return error('Amount must be more than 0!')

    
    user = [json['uuid'], json['from_name']]
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
        print(e)
        return error('Invalid JSON!')
    
    if is_none_or_empty(json['uuid']):
        return error('UUID from sender is required!')
    if is_none_or_empty(json['from_name']):
        return error('Username for sender is required!')
    if is_none_or_empty(json['amount']):
        return error('Amount is required!')
    if (json['amount'] < 1):
        return error('Amount must be more than 0!')

    user = [json['uuid'], json['from_name']]
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
        if is_none_or_empty(request.args.get('username')):
            return error('Username is required!')
        id = request.args.get('uuid')
        username = request.args.get('username')
        db = DB(db_host, db_user, db_password, db_database)
        result = db.user_get_by_uuid(id, username)
        if result == None:
            return error('User not found!')
        return jsonify(uuid=result.get("uuid"),
                       username=result.get("username"),
                       id=result.get("id"),
                       balance=result.get("balance"),
                       currency_name=currency_name)

    
    try:
        data = request.data.decode('utf-8')
        json = to_json(data)
    except Exception as e:
        print(e)
        return error('Invalid JSON!')
    
# POST
    if request.method == 'POST':
        if is_none_or_empty(json['username']):
            return error('Username is required!')
        if is_none_or_empty(json['password']):
            return error('Password is required!')
        id = uuid.uuid4()
        username = json['username']
        password = json['password']
        db = DB(db_host, db_user, db_password, db_database)
        if db.user_create(id, username, password, 0):
            result = db.user_get_by_uuid(id, username)
        if result == None:
            return error('User not found!')
        return jsonify(uuid=result.get("uuid"),
                       username=result.get("username"),
                       id=result.get("id"),
                       balance=result.get("balance"),
                       currency_name=currency_name)
            
# DELETE
    elif request.method == 'DELETE':
        if is_none_or_empty(json['uuid']):
            return error('UUID is required!')
        if is_none_or_empty(json['username']):
            return error('Username is required!')
        if is_none_or_empty(json['password']):
            return error('Password is required!')
        id = json['uuid']
        username = json['username']
        password = json['password']
        db = DB(db_host, db_user, db_password, db_database)
        result = db.user_get_by_uuid(id, username)
        if result != None:
            if login(password, result.get('password')):
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
        print(json)
    except Exception as e:
        print(e)
        return error('Invalid JSON!')
    
    if request.method == 'POST':
        if is_none_or_empty(json['username']):
            return error('Username is required!')
        if is_none_or_empty(json['password']):
            return error('Pin is required!')
        username = json['username']
        pin = json['password']
        db = DB(db_host, db_user, db_password, db_database)
        result = db.user_get_by_pin(pin, username)
        if result == None:
            return error('User not found!')
        return to_json(result)
    return error('Processing failed, contact admin, if error persists!')



# Shop functions
@app.route('/shop/items/count', methods=['GET'])
def shop_get_item_count():
    db = DB(db_host, db_user, db_password, db_database)
    count = db.shop_get_item_count()
    if count != None:
        return jsonify(count=count)
    print(count)
    return error('Failed to get item count!')

@app.route('/shop/items', methods=['GET'])
def shop_get_items():
    db = DB(db_host, db_user, db_password, db_database)
    roller_items = db.roller_get_all_items()
    if roller_items == None:
        return error("No items recycled yet to display.")
    
    shop_items = []
    for i in roller_items:
        print(i)
        item = db.shop_get_item_by_name(i.get("name"))
        if item == None:
            return error("Can't find item: " + to_json(item))
        shop_items.append(item)
    items = []
    for i in range(0, len(roller_items)):
        currency = tier_to_currency(shop_items[i].get("tier"))
        end_price = calculate_sale_price(currency, roller_items[i].get("sale"))
        items.append({
            "id":roller_items[i].get("id"),
            "name":shop_items[i].get("name"),
            "displayname":shop_items[i].get("displayname"),
            "tier":shop_items[i].get("tier"),
            "currency":end_price,
            "currencyname":currency_name
        })
    return to_json(items)

@app.route('/shop/item', methods=['GET'])
def shop_get_item():
    if not is_none_or_empty(request.args.get('name_id')):
        name_id = request.args.get('name_id')
        db = DB(db_host, db_user, db_password, db_database)
        result = db.shop_get_item_by_name(name_id)
        if result != None:
            return to_json(result)
        return error('Item not found!')
    
    db = DB(db_host, db_user, db_password, db_database)
    result = db.shop_get_all_items()
    if result != None:
        return to_json(result)
    return error('Processing failed, contact admin, if error persists!')

@app.route('/shop/item/purchase', methods=['PUT'])
def shop_buy_item():
    data = request.data.decode('utf-8')
    json = to_json(data)
    if is_none_or_empty(json['uuid']):
        return error('UUID from sender is required!')
    if is_none_or_empty(json['from_name']):
        return error('Username for sender is required!')
    if is_none_or_empty(json['amount']):
        return error('Item amount is required!')
    
    user = [json['uuid'], json['from_name']]
    item_id = json['item_id']
    amount = json['amount']

    db = DB(db_host, db_user, db_password, db_database)
    db_account = db.user_get_by_uuid(user[0], user[1])
    if db_account != None:
        db_item = db.shop_get_item_by_name(item_id)
        if db_item != None:
            if db.user_withdraw(db_account.get("uuid"),
                                db_account.get("username"),
                                (amount * tier_to_currency(db_item.get("tier")))):
                return to_json(db_item)
            return error('Purchase failed, contact admin, if error persists!')
        return error('Item not found')
    return error('User not found!')

@app.route('/shop/converter', methods=['GET'])
def shop_convert_to_currency():
    id_name = request.args.get('id_name')
    amount = request.args.get('amount')
    if is_none_or_empty(id_name):
        return error('id_name is required!')
    db = DB(db_host, db_user, db_password, db_database)
    item = db.shop_get_item_by_name(id_name)
    if item is None:
        return error('Item not found!')
    currency = tier_to_currency(item['tier'])
    if not is_none_or_empty(id_name):
        currency = int(amount) * currency
    json = jsonify(currency=currency,
                   display_name=str(item['displayname']),
                   id_name=str(item['name'])
                   )
    print(json)
    return json

@app.route('/shop/recycle', methods=['PUT'])
def shop_recycle():
    data = request.data.decode('utf-8')
    json = to_json(data)
    
    if is_none_or_empty(json['uuid']):
        return error('UUID from sender is required!')
    if is_none_or_empty(json['from_name']):
        return error('Username is required!')
    
    if is_none_or_empty(json['id_name']):
        return error('Item-id is required!')
    if is_none_or_empty(json['amount']):
        return error('Amount is required!')
    if (json['amount'] < 1):
        return error('Amount must be more than 0!')

    db = DB(db_host, db_user, db_password, db_database)
    item = db.shop_get_item_by_name(json['id_name'])
    if item is None:
        return error('Item not found!')
    
    if item['recycled'] == False:
        db.shop_item_recycled(json['id_name'])

    currency = tier_to_currency(item['tier'])
    currency = int(json['amount']) * currency

    if not db.user_deposit(json['uuid'], json['from_name'], currency):
        return error(f"Failed to recycle Item: {json['id_name']}")
    
    item = db.shop_get_item_by_name(json['id_name'])
    json = jsonify(currency=currency,
                   id_name=item['name'],
                   display_name=item['displayname'],
                   amount=json['amount'],
                   recycled=item['recycled'],
                   currency_name=currency_name)
    print(json)
    return json



# utils
def to_json(data):
    try:
        return json.loads(data)
    except Exception:
        return json.dumps(data)

def error(message):
    return jsonify(error=str(message))

def tier_to_currency(tier):
    try:
        with open('tier.json', 'r') as file:
            tiers = json.load(file)
            return tiers[str(tier)]
    except Exception as e:
        print(e)
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




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True, threaded=True)