import json
from collections import defaultdict
from pymongo import MongoClient, ASCENDING
from time import time
from pprint import pprint as pp

"""
client = MongoClient('localhost', 27017)
database = client['db_exam']
collections = {'promo_codes': database['promo_codes'], 'orders': database['orders']}
data_paths = {'promo_codes': 'mongo-db/data/promo_codes.json', 'orders': 'mongo-db/data/orders.json'}


def insert_json(col):
    with open(data_paths[col], encoding='utf-8') as file:
        data = file.read()
        data = json.loads(data)
        ids = collections[col].insert_many(data).inserted_ids
    return ids
"""


def get_orders(database, user_id=None):
    d = {'user_id': user_id} if user_id else dict()

    data = database['orders'].find(d).limit(100)

    res = []
    for x in data:
        total = 0
        for item in x['items']:
            total += item['amount']*item['price']
        x['price'] = total
        x['_id'] = str(x['_id'])
        res.append(x)
    return res


# pp(get_orders(7487)[0])


def use_promo_code(database, code):
    res = database['promo_codes'].find_one({'id': code})
    if res['expires'] < time():
        return 'Promo Code is expired'
    modified = database['promo_codes'].update_one({'id': code}, {"$set": {'used': 'true'}}).modified_count
    if modified == 0:
        return 'Promo Code can only be used one time'
    return 'Promo Code used'


# use_promo_code('gjsormci')
