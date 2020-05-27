from psycopg2 import connect
import csv

postgres_access = {
    "host": "localhost",
    "database": "db_exam",
    "user": "postgres",
    "password": "12345678"
}

conn = connect(**postgres_access)


drop_tables_query = """
    DROP TABLE IF EXISTS favorite, region, "user";
    """

create_user_table_query = """
    CREATE TABLE "user" (
        "id" SERIAL PRIMARY KEY,
        "name" varchar NOT NULL,
        "email" varchar UNIQUE NOT NULL,
        "phone" varchar UNIQUE NOT NULL,
        "street" varchar NOT NULL,
        "password" varchar NOT NULL,
        "fk_zip" int NOT NULL
    );
    """

create_region_table_query = """
    CREATE TABLE "region" (
        "zip" int PRIMARY KEY,
        "name" varchar NOT NULL,
        "lat" decimal NOT NULL,
        "lon" decimal NOT NULL
    );
    """

create_favorite_table_query = """
    CREATE TABLE "favorite" (
        "fk_user_id" int NOT NULL,
        "fk_label_id" int NOT NULL,
        PRIMARY KEY (fk_user_id, fk_label_id)
    );
    """

create_reference_query = """
    ALTER TABLE "user" ADD FOREIGN KEY("fk_zip") REFERENCES "region" ("zip");
    ALTER TABLE "favorite" ADD FOREIGN KEY("fk_user_id") REFERENCES "user" ("id") ON DELETE CASCADE;
"""


def create_tables():
    with conn.cursor() as cursor:
        cursor.execute(drop_tables_query)
        cursor.execute(create_user_table_query)
        cursor.execute(create_region_table_query)
        cursor.execute(create_favorite_table_query)
        cursor.execute(create_reference_query)
        conn.commit()


def insert_regions():
    with conn.cursor() as cursor:
        with open('dbex/regions.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row.
            for row in reader:
                cursor.execute('INSERT INTO region VALUES (%s, %s, %s, %s)', row)
        conn.commit()


def insert_users():
    with conn.cursor() as cursor:
        with open('dbex/users.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row.
            for row in reader:
                cursor.execute('''
                INSERT INTO "user" (name, email, phone, street, password, fk_zip)
                VALUES (%s, %s, %s, %s, %s, %s)
                ''', row)
        conn.commit()


def insert_favorites():
    with conn.cursor() as cursor:
        with open('dbex/favorites.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row.
            for row in reader:
                cursor.execute('INSERT INTO "favorite" VALUES (%s, %s)', row)
        conn.commit()


def validate():
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM "user" LIMIT 1')
        user = cursor.fetchone()
        cursor.execute('SELECT count(*) FROM "user"')
        user_amount = cursor.fetchone()

        cursor.execute('SELECT * FROM "region" LIMIT 1')
        region = cursor.fetchone()
        cursor.execute('SELECT count(*) FROM "region"')
        region_amount = cursor.fetchone()

        cursor.execute('SELECT * FROM "favorite"  LIMIT 1')
        favorite = cursor.fetchone()
        cursor.execute('SELECT count(*) FROM "favorite"')
        favorite_amount = cursor.fetchone()

        conn.commit()

    # prints user validattion
    print('user amount', user_amount)
    print('user sample', user, '\n')

    # prints region validattion
    print('region amount', region_amount)
    print('region sample', region, '\n')

    # prints favorite validattion
    print('favorite amount', favorite_amount)
    print('favorite sample', favorite, '\n')


if __name__ == '__main__':
    create_tables()
    insert_regions()
    insert_users()
    insert_favorites()
    validate()
