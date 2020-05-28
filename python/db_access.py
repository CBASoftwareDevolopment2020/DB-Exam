postgres = {
    "host": "localhost",
    #    "database": "dbex3",
    "database": "db_exam",
    "user": "postgres",
    "password": "password123"
}

redis = {
    "host": 'localhost',
    "port": 6379,
    "db": 0
}

neo4j = {
    'uri': 'bolt://localhost:7687',
    'auth': ('db_exam', '1234')
}

mongo = {
    'host': 'localhost',
    'port': 27017,
    'db_name': 'db_exam'
}
