import subprocess
<<<<<<< HEAD

path = r"C:/Users/Hupra/Desktop/dbex/DB-Exam/"
subprocess.call(["mongoimport", "--db", "db_exam", "--collection", "orders", "--file", r"mongo-db/data/orders.json", "--jsonArray"])
subprocess.call(["mongoimport", "--db", "db_exam", "--collection", "promo_codes", "--file", "mongo-db/data/promo_codes.json", "--jsonArray"])
=======
subprocess.call(["mongoimport", "--db", "db_exam", "--collection", "orders", "--file", "mongo-db/data/orders.json", "--jsonArray"])
subprocess.call(["mongoimport", "--db", "db_exam", "--collection", "promo_codes", "--file", "mongo-db/data/promo_codes.json", "--jsonArray"])
>>>>>>> f4cbc2289db67a1ea42e96aeead9498f73a67052
