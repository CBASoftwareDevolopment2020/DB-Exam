import redis

# item = {"item_id": 421,
#         "amount": 3,
#         "price": 6900,
#         "name": "Badeand"}

def item_to_redis_d(item):
    return {item["item_id"]:"{}|{}|{}".format(item["amount"],item["price"],item["name"])}

def redis_d_to_item(d):
    items = []
    for k,v in d.items():
        amount, price, name = v.decode("utf-8").split("|")
        item = {"item_id": int(k),
                "amount": int(amount),
                "price":int(price),
                "name": name}
        items.append(item)
    return items

def add_to_cart(conn, ses, item):
    d = item_to_redis_d(item)
    conn.hmset(ses, d)
    conn.expire(ses, 1800)
    
def remove_from_cart(conn, ses, item_id):
    conn.hdel(ses, item_id)
    conn.expire(ses, 1800)

def clear_cart(conn, ses):
    conn.delete(ses)

def get_cart(conn, ses):
    conn.expire(ses, 1800)
    d = conn.hgetall(ses)
    return redis_d_to_item(d)#{int(k): int(v) for k,v in x.items()}

def get_compressed_cart(conn, ses):
    items = get_cart(conn, ses)
    return {item['item_id'] : item["amount"] for item in items}