import requests
import json
import uuid

class Transfer:
    def __init__(self, username, password):
        self.from_name = username
        self.pin = password

def post():
    link = 'banking/card'
    url = f'http://127.0.0.1:5000/{link}'
    data = json.dumps(Transfer('ganning', 'adolf123').__dict__)
    return requests.post(url, data).content

def get():
    link = 'banking/account'
    arguments = f'?uuid=test&username=katse2'
    url = f'http://127.0.0.1:5000/{link}{arguments}'
    return requests.get(url).json()


print(get())