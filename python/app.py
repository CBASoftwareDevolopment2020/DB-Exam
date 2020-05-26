from flask import Flask, render_template, request, g, session, redirect, url_for, jsonify
from flask_cors import CORS, cross_origin
import json
import db_access  # connection info for all dbs
import my_postgres as pg  # our postgres methods
import my_redis as rd  # our redis methods
import my_neo4j as neo  # our neo4j methods
import my_mongo as mongo  # our mongo methods
import psycopg2  # lib to connect to postgres
import redis  # lib to connect to redis

from neo4j import GraphDatabase
from pymongo import MongoClient

# database connections
# pgconn = psycopg2.connect(**db_access.postgres)
rdconn = redis.Redis(**db_access.redis)
#neoconn = GraphDatabase.driver(**db_access.neo4j)
monconn = MongoClient(db_access.mongo['host'], db_access.mongo['port'])[db_access.mongo['db_name']]

# general flask setup
app = Flask(__name__)

app.secret_key = "tsop secret key of awesomeness"
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['CORS_SUPPORTS_CREDENTIALS'] = True

cors = CORS(app)


# front page, returns user session
@app.route('/')
def main():
    if "user" in session:
        return json.dumps(session["user"], ensure_ascii=False)
    else:
        return "YOU ARE NOT A USER!!!!!"


############################
#     POSTGRES / USERS     #
############################

# login, can test with below endpoint
# http://127.0.0.1:5000/login/nancy1@claudia.io/1234
@app.route('/login/<email>/<password>')
def set_session(email, password):

    user = pg.login(pgconn, email, password)
    if user is None:
        return json.dumps({'success': False}), 400
    else:
        session["user"] = user
        session.permanent = True
        return jsonify(session["user"])

# logout
@app.route('/logout')
def logout():
    session.pop("user", None)
    return json.dumps({'success': True}), 200

# get user from email
@app.route('/user/<email>')
def get_user_info(email):
    return json.dumps(pg.get_user_info(pgconn, email), ensure_ascii=False)

# create user
# {
#     "name": "daniel",
#     "email": "da@ni.el",
#     "phone": "12345678",
#     "street": "vej24",
#     "password": "1234",
#     "zip": "2680"
# }
@app.route('/user/create', methods=["POST"])
def create_user():
    user = request.json
    return json.dumps(pg.create_user(pgconn, user), ensure_ascii=False)

# delete user from email
@app.route('/user/delete/<email>')
def delete_user(email):
    user = request.json
    pg.delete_user(pgconn, email)
    return json.dumps({'success': True}), 200


#############################
#       REDIS / CART        #
#############################
@app.route('/cart/get')
def get_cart():
    if "user" not in session:
        return json.dumps({'success': False}), 400

    return json.dumps(rd.get_cart(rdconn, session["user"]["email"]))


def get_compressed_cart():
    if "user" not in session:
        return json.dumps({'success': False}), 400

    return json.dumps(rd.get_compressed_cart(rdconn, session["user"]["email"]))


@app.route('/cart/add', methods=["POST"])
def add_to_cart():
    item = valid = request.json

    print(item, session)

    # check if item has the correct propperties
    item_keys = set(item.keys())
    for key in ['item_id', 'amount', 'price', 'name']:
        if key not in item_keys:
            valid = False

    if "user" not in session or item is not valid:
        return json.dumps({'success': False}), 400

    json.dumps(rd.add_to_cart(rdconn, session["user"]["email"], item))
    return json.dumps({'success': True}), 200


@app.route('/cart/remove', methods=["POST"])
def remove_from_cart():
    item_id = request.json
    if "user" in session and type(item_id) is int:
        rd.remove_from_cart(rdconn, session["user"]["email"], item_id)
        return json.dumps({'success': False}), 400

    return json.dumps({'success': True}), 200


@app.route('/cart/clear')
def clear_cart():
    if "user" in session:
        rd.clear_cart(rdconn, session["user"]["email"])
        return json.dumps({'success': False}), 400

    return json.dumps({'success': True}), 200

###########################
#########  NEO4J  #########
###########################


@app.route('/items/init')
def neo4j_init():
    neo.load_data_query(neoconn)
    return json.dumps({}), 200


# pass amount down as argument?
@app.route('/items/20')
def neo4j_get_all_items():
    items = neo.get_20_items_query(neoconn)
    res = [dict(item['item']) for item in items]
    return json.dumps(res), 200


@app.route('/items/<id>')
def neo4j_get_full_items(id):
    item = neo.get_full_item_query(neoconn, int(id))

    if item:
        res = dict(item)
        return json.dumps(res), 200
    else:
        return json.dumps({'error': 'not found'}), 404


# maybe check if name and brand exists instead of only item name
@app.route('/items/add', methods=["POST"])
def neo4j_add_item():
    body = request.json

    item = neo.add_item_query(
        neoconn, body['name'], int(body['price']),
        int(body['stock']), body['image'], body['brand'], body['labels']
    )

    if item:
        res = dict(item)
        return json.dumps(res), 200
    else:
        return json.dumps({'error': 'not acceptable'}), 406


@app.route('/items/update-labels', methods=["POST"])
def neo4j_update_labels():
    body = request.json

    item = neo.update_labels_query(neoconn, int(body['id']), body['labels'])

    if item:
        res = dict(item)
        return json.dumps(res), 200
    else:
        return json.dumps({'error': 'not found'}), 404


@app.route('/items/update-property', methods=["POST"])
def neo4j_update_property():
    body = request.json

    item = neo.update_item_query(neoconn, int(body['id']), body['property'], body['value'])

    if item:
        res = dict(item)
        return json.dumps(res), 200
    else:
        return json.dumps({'error': 'not found'}), 404


@app.route('/items/update-stock', methods=["POST"])
def neo4j_update_stock():
    body = request.json

    item = neo.update_item_amount_query(neoconn, int(body['id']), body['stock'])

    if item:
        res = dict(item)
        return json.dumps(res), 200
    else:
        return json.dumps({'error': 'not found'}), 404


@app.route('/items/remove-unused-labels')
def neo4j_remove_unused_labels():
    neo.remove_unused_labels_query(neoconn)
    return {}, 200


@app.route('/items/filter-by-label', methods=["POST"])
def neo4j_filter_by_label():
    body = request.json
    items = list(neo.filter_by_label_query(neoconn, body['label']))

    if items:
        res = [dict(item['item']) for item in items]
        return json.dumps(res), 200
    else:
        return json.dumps({'error': 'not found'}), 404


@app.route('/items/filter-by-favorits', methods=["POST"])
def neo4j_filter_by_favorits():
    body = request.json
    items = list(neo.filter_by_favorits_query(neoconn, body['favorits']))

    if items:
        res = [dict(item['item']) for item in items]
        return json.dumps(res), 200
    else:
        return json.dumps({'error': 'not found'}), 404


@app.route('/items/order-by-price')
def neo4j_order_by_price():
    items = list(neo.order_by_price_query(neoconn))

    if items:
        res = [dict(item['item']) for item in items]
        return json.dumps(res), 200
    else:
        return json.dumps({'error': 'not found'}), 404


@app.route('/items/filter-by-price', methods=["POST"])
def neo4j_filter_by_price():
    body = request.json
    items = list(neo.filter_price_query(neoconn, int(body['minimum']), int(body['maximum'])))

    res = [dict(item['item']) for item in items]
    return json.dumps(res), 200


@app.route('/items/get-nodes-by-ids', methods=["POST"])
def neo4j_get_nodes_by_ids():
    body = request.json
    records = list(neo.get_by_ids(neoconn, body))

    res = {
        "items": [],
        "labels": [],
        "brands": [],
    }

    for record in records:
        label = list(record['node'].labels)[0]
        res[label.lower() + 's'].append(dict(record['node']))

    return json.dumps(res), 200

###########################
#########  MONGO  #########
###########################


@app.route('/orders/by-user')
def mongo_get_all_orders():
    if "user" not in session:
        return json.dumps({'message': 'not logged in'}), 404

    id = session['user']['id']
    orders = mongo.get_orders(monconn, id)

    return json.dumps(orders), 200


@app.route('/orders/all')
def mongo_get_orders():
    orders = mongo.get_orders(monconn)
    return json.dumps(orders), 200


@app.route('/orders/use-promo/<code>')
def mongo_use_promo(code):
    message = mongo.use_promo_code(monconn, code)
    return json.dumps({'message': message}), 200


# start app
if __name__ == '__main__':
    app.run(debug=True)
