import subprocess
subprocess.call(["mongoimport", "--db", "db_exam", "--collection", "orders", "--file", "mongo-db/data/orders.json", "--jsonArray"])
subprocess.call(["mongoimport", "--db", "db_exam", "--collection", "promo_codes", "--file", "mongo-db/data/promo_codes.json", "--jsonArray"])
