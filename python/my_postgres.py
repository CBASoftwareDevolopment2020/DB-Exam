import psycopg2
import bcrypt

def login(conn, email, password):
    cur = conn.cursor()
    cur.callproc("get_password", [email])
    user = cur.fetchone()
    if user is None:
        return None
    else:
        user = {
            "id": user[0],
            "name": user[1],
            "email": user[2],
            "phone": user[3],
            "street": user[4],
            "password": user[5],
            "zip": user[6]
        }
    if bcrypt.checkpw(bytes(password, "utf-8"), bytes(user["password"], "utf-8")):
        return user
    else:
        return None

def delete_user(conn, email):
    cur = conn.cursor()
    cur.execute("CALL delete_user('{}')".format(email))

def create_user(conn, user):
    u = user
    u["password"] = bcrypt.hashpw(bytes(u["password"], "utf-8"), bcrypt.gensalt(4)).decode("utf-8")
    u = (u["name"], u["email"], u["phone"], u["street"], u["password"], int(u["zip"]))
    cur = conn.cursor()
    
    try:
        cur.callproc("create_user", u)
        res = cur.fetchone()
        return res
    except:
        cur.execute("ROLLBACK")

def get_user_info(conn, email):
    cur = conn.cursor()
    cur.callproc("get_user_info", [email])
    res = cur.fetchone()
    
    if res is None:
        return None
    user = {
        "id": res[0],
        "name": res[1],
        "email": res[2],
        "phone": res[3],
        "street": res[4],
        "password": res[5],
        "lat": float(res[6]),
        "lon": float(res[7]),
        "zip": int(res[8]),
        "region": res[9]
    }
    return user


def get_favorits(conn, user_id):
    cur = conn.cursor()
    cur.callproc("get_favorites", [user_id])
    res = cur.fetchall()
    return [x[0] for x in res]