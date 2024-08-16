import requests
import json
import uuid

values = {
    "uuid":"9d314e73-8497-4c95-a713-7e51fe171ccd",
    "from":"ganning",
    #"pin":"gandalf123",
    #"to":3,
    "amount":50,
    #"id":11,
    "name":"minecraft:book",
}

def post(values, link):
    url = f'http://127.0.0.1:5000/{link}'
    data = json.dumps(values)
    return requests.post(url, data).content

def put(values, link):
    url = f'http://127.0.0.1:5000/{link}'
    data = json.dumps(values)
    return requests.put(url, data).content

def get():
    link = 'shop/converter'
    arguments = f'?name=minecraft:book&amount=5'
    url = f'http://127.0.0.1:5000/{link}{arguments}'
    return requests.get(url).json()

def delete():
    link = 'banking/account'
    arguments = f'?name=minecraft:book&amount=5'
    url = f'http://127.0.0.1:5000/{link}{arguments}'
    return requests.delete(url).json()


#print(get())
print(put(values, "shop/recycle"))