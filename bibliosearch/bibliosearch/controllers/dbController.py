import sqlite3
from sqlite3.dbapi2 import Error

def create_connection(db_file):
    """
    creates a connection with the sqlite database
    :param db_file: database file
    :return Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def insert_articulo(conn,dict):
    """
    Inserts an article in "bbdd_articulo" table
    """
    sql = ''' INSERT INTO bbdd_articulo() '''