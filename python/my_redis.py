import redis

def add_to_cart(conn, ses, item, count):
    d = {item: count}
    conn.hmset(ses, d)
    conn.expire(ses, 1800)
    
def remove_from_cart(conn, ses, item):
    conn.hdel(ses, item)
    conn.expire(ses, 1800)

def clear_cart(conn, ses):
    conn.delete(ses)

def get_cart(conn, ses):
    conn.expire(ses, 1800)
    x = conn.hgetall(ses)
    return {int(k): int(v) for k,v in x.items()}