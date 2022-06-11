import psycopg2

def get_connection():
    return psycopg2.connect(host='127.0.0.1', dbname='substake', user='substake', password='substake!', port='5432')
