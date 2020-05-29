# Database Setup Guides

## PostgreSQL

Create database called `db_exam`.

After create the Tables, Views, Functions & Procedures with this script.

_postgres shell_
```bash
\i SQL-scripts\setup.sql
```

Then Populate database with data.

_bash shell_
```bash
python setup/postgres.py
```

## Neo4j
Import `dbex/foodDone.csv` to your Neo4j database and run the script below.

_noe4j shell_
```sql
LOAD CSV WITH HEADERS FROM 'file:///foodDone.csv' AS r
MERGE (item: Item { name:r.name, price: toInteger(r.price), stock: toInteger(r.stock), img: r.link })
MERGE (brand: Brand { brand: r.brand })
FOREACH(label IN split(r.labels, ";")|MERGE (l:Label { name: label }))

WITH r
MATCH (item: Item { name: r.name })
UNWIND split(r.labels, ";") as l
MATCH (label: Label { name: l })
MERGE (item)-[:is]-(label)

WITH r
MATCH (item: Item { name: r.name })
MATCH (brand: Brand { brand:r.brand })
MERGE (item)-[:by]-(brand)
```

## mongoDB

Run the following script to populate the mongo db.

_bash shell_
```bash
python setup/mongo.py
```
