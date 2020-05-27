import subprocess

path = r"C:/Users/Hupra/Desktop/dbex/DB-Exam/"
subprocess.call(["mongoimport", "--db", "db_exam", "--collection", "orders", "--file", r"mongo-db/data/orders.json", "--jsonArray"])
subprocess.call(["mongoimport", "--db", "db_exam", "--collection", "promo_codes", "--file", f"mongo-db/data/promo_codes.json", "--jsonArray"])
