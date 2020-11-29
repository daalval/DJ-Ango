from bibliosearch.models.Ejemplar import Ejemplar
from bibliosearch.models.Com_con import Com_con
from bibliosearch.models.Libro import Libro
from bibliosearch.models.Articulo import Articulo
from bibliosearch.models.Revista import Revista
import json
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

def insert_articulo(conn, articulo):
    """
    Inserts an article in "bbdd_articulo" table
    """
    sql_art = '''INSERT INTO bbdd_articulo(pagina_inicio, pagina_fin, publicacion_id, ejemplar_id)
                VALUES(?,?,?,?)'''
    id_publicacion = insert_publicacion(conn, articulo)
    id_ejemplar = insert_ejemplar(conn, articulo.get_ejemplar())
    cur = conn.cursor()
    values = [articulo.get_pagina_inicio(), articulo.get_pagina_fin(), id_publicacion, id_ejemplar]
    cur.execute(sql_art, values)
    conn.commit()
    return cur.lastrowid

def insert_ejemplar(conn, ejemplar):
    """
    Inserts an ejemplar in "bbdd_ejemplar" table
    """
    sql_ejemplar = '''INSERT INTO bbdd_ejemplar(id_ejemplar, volumen, numero, mes, revista_id)
                    VALUES(?,?,?,?,?)'''
    id_revista = insert_revista(conn, ejemplar.get_revista())
    cur = conn.cursor()
    values = [None, ejemplar.get_volumen(), ejemplar.get_numero(), ejemplar.get_mes(), id_revista]
    cur.execute(sql_ejemplar, values)
    conn.commit()
    return cur.lastrowid

def insert_revista(conn, revista):
    """
    Inserts a revista in "bbdd_revista" table
    """
    sql_revista = '''INSERT INTO bbdd_revista(id_revista, nombre)
                    VALUES(?,?)'''
    cur = conn.cursor()
    values = [None, revista.get_nombre()]
    cur.execute(sql_revista, values)
    conn.commit()
    return cur.lastrowid

def insert_publicacion(conn, publicacion):
    """
    Inserts an article in "bbdd_publicacion" table
    """
    sql = '''INSERT INTO bbdd_publicacion(
            id_publicacion, titulo, anyo, URL) VALUES
            (?,?,?,?)'''
    cur = conn.cursor()
    print(publicacion.get_anyo())
    print(type(publicacion.get_anyo()))
    values = [None, publicacion.get_titulo(), publicacion.get_anyo(), publicacion.get_url()]
    cur.execute(sql, values)
    conn.commit()
    return cur.lastrowid   

def insert_libro(conn, libro): 
    """
    Inserts a libro in "bbdd_libro" table
    """
    sql = '''INSERT INTO bbdd_libro(editorial, publicacion_id)
            VALUES(?,?)'''
    id_publicacion = insert_publicacion(conn, libro)
    values = [libro.get_editorial(), id_publicacion]
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    return cur.lastrowid

def insert_comCon(conn, com_con): 
    """
    Inserts a com_con in "bbdd_com_con" table
    """
    sql = '''INSERT INTO bbdd_com_con(
            congreso, edicion, lugar, pagina_inicio, pagina_fin, publicacion_id) VALUES
            (?,?,?,?,?,?)'''
    id_publicacion = insert_publicacion(conn, com_con)
    values = [com_con.get_congreso(), com_con.get_edicion(), com_con.get_lugar(), com_con.get_pagina_inicio(), com_con.get_pagina_fin(), id_publicacion]
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    return cur.lastrowid

def sql_connection():

    try:

        con = sqlite3.connect('db.sqlite3')

        return con

    except Error:

        print(Error)

def insert_in_database(con, path):

    with open (path,'r') as f:
        jsondata = json.loads(f.read())

    for article_id in jsondata:
        article = jsondata[article_id]
        if article['tipo'] == 'libro':
            libro = Libro(article['editorial'], article_id, article['titulo'], article['anyo'], article['url'], article['escrita_por'])
            insert_libro(con, libro)
        if article['tipo'] == 'com_con':
            com_con = Com_con(article['congreso'], article['edicion'], article['lugar'], article['pagina_inicio'], article['pagina_fin'], article_id, article['titulo'], article['anyo'], article['url'], article['escrita_por'])
            insert_comCon(con, com_con)
        if article['tipo'] == 'articulo':
            publicado_en = article['publicado_en'] 
            articulo = Articulo(article['pagina_inicio'], article['pagina_fin'], article_id, article['titulo'], article['anyo'], article['url'], article['escrita_por'], Ejemplar(None, publicado_en['volumen'], publicado_en['numero'], publicado_en['mes'], Revista(None, publicado_en['revista']['nombre'])))
            insert_articulo(con, articulo)

    con.commit()  

def main():
    path = 'static/dblp.json'
    con = sql_connection() 
    insert_in_database(con, path)

if __name__ == '__main__':
    main()