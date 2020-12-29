from bibliosearch.models.Ejemplar import Ejemplar
from bibliosearch.models.Com_con import Com_con
from bibliosearch.models.Libro import Libro
from bibliosearch.models.Articulo import Articulo
from bibliosearch.models.Revista import Revista
from bibliosearch.models.Persona import Persona
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
    values = [None, publicacion.get_titulo(), publicacion.get_anyo(), publicacion.get_url()]
    cur.execute(sql, values)
    conn.commit()
    for persona in publicacion.get_autores():
        id_persona = insert_persona(conn, persona)
        insert_persona_publicacion(conn, id_persona,cur.lastrowid)
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

def insert_persona(conn, persona): 
    """
    Inserts a com_con in "bbdd_person" table
    """
    sql = '''INSERT OR IGNORE INTO bbdd_persona(
            id_persona,nombre,apellidos) VALUES
            (?,?,?)'''
    values = [None,persona.get_nombre(),persona.get_apellidos()]
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    return cur.lastrowid

def insert_persona_publicacion(conn, persona_id,publicacion_id): 
    """
    Inserts a com_con in "bbdd_personapublicacion" table
    """
    sql = '''INSERT INTO bbdd_personapublicacion(
            id,publicacion_id,persona_id) VALUES
            (?,?,?)'''
    values = [None,persona_id,publicacion_id]
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

def insert_in_database(con, paths):

    for path in paths:
        with open (path,'r') as f:
            jsondata = json.loads(f.read())

        for article_id in jsondata:
            article = jsondata[article_id]
            personas = []
            for escrita_por in article['escrita_por']:
                personas.append(Persona(None,escrita_por['nombre'],escrita_por['apellidos']))

            if article['tipo'] == 'libro':
                libro = Libro(article['editorial'], article_id, article['titulo'], article['anyo'], article['url'], personas)
                insert_libro(con, libro)
            if article['tipo'] == 'com_con':
                com_con = Com_con(article['congreso'], article['edicion'], article['lugar'], article['pagina_inicio'], article['pagina_fin'], article_id, article['titulo'], article['anyo'], article['url'], personas)
                insert_comCon(con, com_con)
            if article['tipo'] == 'articulo':
                publicado_en = article['publicado_en'] 
                articulo = Articulo(article['pagina_inicio'], article['pagina_fin'], article_id, article['titulo'], article['anyo'], article['url'], personas, Ejemplar(None, publicado_en['volumen'], publicado_en['numero'], publicado_en['mes'], Revista(None, publicado_en['revista']['nombre'])))
                insert_articulo(con, articulo)

        con.commit()

def select_data(titulo, autor, fecha_desde, fecha_hasta, tipos):
    con = sql_connection()
    cursor = con.cursor()

    articulos = []
    conferencias = []
    libros = []

    if titulo == "" and autor == "":
        for tipo in tipos:
            if tipo == 'bbdd_articulo':

                #sql = '''SELECT * from bbdd_articulo AS a WHERE publicacion_id = (SELECT id_publicacion from bbdd_publicacion WHERE anyo >= ''' + fecha_desde + ''' AND
                 #anyo <= ''' + fecha_hasta + ''')'''

                sql = '''SELECT * from bbdd_articulo AS a 
                INNER JOIN bbdd_publicacion AS p ON a.publicacion_id = p.id_publicacion
                INNER JOIN bbdd_
                '''

                cursor.execute(sql)

                rows = cursor.fetchall()

                for row in rows:
                    print(row)

                con.commit()
        
        

def main():
    #paths = ['static/ieeeXplore.json', 'static/google_schoolar.json', 'static/dblp.json']
    #con = sql_connection() 
    #insert_in_database(con, paths)
    select_data("", "", '2000', '2020', ['bbdd_articulo', 'bbdd_com_con', 'bbdd_libro'])

if __name__ == '__main__':
    main()