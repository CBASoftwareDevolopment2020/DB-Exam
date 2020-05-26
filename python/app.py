from flask import Flask, render_template, request, g, session, redirect, url_for
from flask_cors import CORS, cross_origin
import json
import db_access # connection info for all dbs
import my_postgres as pg # our postgres methods
import my_redis as rd # our redis methods
import psycopg2 # lib to connect to postgres
import redis # lib to connect to redis

#database connections
pgconn = psycopg2.connect(**db_access.postgres)
rdconn = redis.Redis(**db_access.redis)

# general flask setup
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

app.secret_key = "top secret key of awesomeness"

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
    
#login, can test with below endpoint
#http://127.0.0.1:5000/login/nancy1@claudia.io/1234
@app.route('/login/<email>/<password>')
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def set_session(email, password):
    
    user = pg.login(pgconn, email, password)
    if user is None:
        return json.dumps({'success':False}), 400
    else:
        session["user"] = user
        session.permanent = True
        return json.dumps(user, ensure_ascii=False)

#logout
@app.route('/logout')
def logout():
    session.pop("user", None)
    return json.dumps({'success':True}), 200

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
    return json.dumps({'success':True}), 200


#############################
#       REDIS / CART        #
#############################
@app.route('/cart/get')
def get_cart():
    if "user" not in session:
        return json.dumps({'success':False}), 400
    
    return json.dumps(rd.get_cart(rdconn, session["user"]["email"]))

def get_compressed_cart():
    if "user" not in session:
        return json.dumps({'success':False}), 400

    return json.dumps(rd.get_compressed_cart(rdconn, session["user"]["email"]))

@app.route('/cart/add', methods=["POST"])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def add_to_cart():
    print(123)
    item = valid = request.json
    
    print(item, session)
    
    # check if item has the correct propperties
    item_keys = set(item.keys())
    for key in ['item_id','amount','price','name']:
        if key not in item_keys:
            valid = False
            
    if "user" not in session or item is not valid:
        return json.dumps({'success':False}), 400
    
    json.dumps(rd.add_to_cart(rdconn, session["user"]["email"], item))
    return json.dumps({'success':True}), 200


@app.route('/cart/remove', methods=["POST"])
def remove_from_cart():
    item_id = request.json
    if "user" in session and type(item_id) is int:
        rd.remove_from_cart(rdconn, session["user"]["email"], item_id)
        return json.dumps({'success':False}), 400
        
    return json.dumps({'success':True}), 200


@app.route('/cart/clear')
def clear_cart():
    if "user" in session:
        rd.clear_cart(rdconn, session["user"]["email"])
        return json.dumps({'success':False}), 400
        
    return json.dumps({'success':True}), 200

# start app
if __name__ == '__main__':
    app.run(debug=True)