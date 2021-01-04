from bibliosearch.models.Ejemplar import Ejemplar
from bibliosearch.models.Com_con import Com_con, dict_2_com_con
from bibliosearch.models.Libro import Libro, dict_2_libro
from bibliosearch.models.Articulo import Articulo, dict_2_articulo
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
    sql = '''INSERT OR IGNORE INTO bbdd_personapublicacion(
            id_personapublicacion, persona_id,publicacion_id) VALUES
            (?,?,?)'''
    values = [None, persona_id,publicacion_id]
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
    data = []

    for tipo in tipos:
        if tipo == 'bbdd_articulo':

            sql = '''SELECT a.publicacion_id,
            group_concat(persona.nombre || " " || persona.apellidos, ', ') as autores,
            titulo, r.nombre, volumen, numero, mes, anyo, pagina_inicio, pagina_fin, url from bbdd_articulo AS a 
            JOIN bbdd_publicacion AS p 
            ON a.publicacion_id = p.id_publicacion
            JOIN bbdd_personapublicacion AS pp
            ON p.id_publicacion = pp.publicacion_id
            JOIN bbdd_persona AS persona
            ON pp.persona_id = persona.id_persona
            JOIN bbdd_ejemplar AS e
            ON a.ejemplar_id = e.id_ejemplar
            JOIN bbdd_revista AS r
            ON e.revista_id = r.id_revista
            WHERE titulo LIKE '%''' + titulo + '''%' AND
            anyo >= ''' + fecha_desde + ''' AND anyo <= ''' + fecha_hasta +''' AND
            (persona.nombre LIKE '%''' + autor + '''%' OR
            persona.apellidos LIKE '%''' + autor + '''%')
            GROUP BY a.publicacion_id
            '''

            #print(sql)

            cursor.execute(sql)

            columns = [column[0] for column in cursor.description]

            print(columns)

            articulos = cursor.fetchall()

            for data_articulo in articulos:
                print(data_articulo)
                dictionary = dict(zip(columns, data_articulo))
                articulo = dict_2_articulo(dictionary)
                data.append(articulo)
            
            con.commit()
        
        if tipo == 'bbdd_com_con':

            sql = '''SELECT c.publicacion_id,
            group_concat(persona.nombre || " " || persona.apellidos, ', ') as autores,
            titulo, edicion, congreso, lugar, anyo, pagina_inicio, pagina_fin, url  from bbdd_com_con AS c 
            INNER JOIN bbdd_publicacion AS p 
            ON c.publicacion_id = p.id_publicacion
            INNER JOIN bbdd_personapublicacion AS pp
            ON p.id_publicacion = pp.publicacion_id
            INNER JOIN bbdd_persona AS persona
            ON pp.persona_id = persona.id_persona
            WHERE titulo LIKE '%''' + titulo + '''%' AND
            anyo >= ''' + fecha_desde + ''' AND anyo <= ''' + fecha_hasta +''' AND
            (persona.nombre LIKE '%''' + autor + '''%' OR
            persona.apellidos LIKE '%''' + autor + '''%')
            GROUP BY c.publicacion_id
            '''

            cursor.execute(sql)

            conferencias = cursor.fetchall()

            columns = [column[0] for column in cursor.description]

            print(columns)

            for data_com_con in conferencias:
                print(data_com_con)
                dictionary = dict(zip(columns, data_com_con))
                com_con = dict_2_com_con(dictionary)
                data.append(com_con)
            
            con.commit()

        if tipo == 'bbdd_libro':

            sql = '''SELECT c.publicacion_id, 
            group_concat(persona.nombre || " " || persona.apellidos, ', ') as autores,
            titulo, editorial, anyo, url
            from bbdd_libro AS c 
            INNER JOIN bbdd_publicacion AS p 
            ON c.publicacion_id = p.id_publicacion
            INNER JOIN bbdd_personapublicacion AS pp
            ON p.id_publicacion = pp.publicacion_id
            INNER JOIN bbdd_persona AS persona
            ON pp.persona_id = persona.id_persona
            WHERE titulo LIKE '%''' + titulo + '''%' AND
            anyo >= ''' + fecha_desde + ''' AND anyo <= ''' + fecha_hasta +''' AND
            (persona.nombre LIKE '%''' + autor + '''%' OR
            persona.apellidos LIKE '%''' + autor + '''%')
            GROUP BY c.publicacion_id
            '''

            cursor.execute(sql)

            libros = cursor.fetchall()

            columns = [column[0] for column in cursor.description]

            print(columns)

            for data_libro in libros:
                print(data_libro)
                dictionary = dict(zip(columns, data_libro))
                libro = dict_2_libro(dictionary)
                data.append(libro)
            
            con.commit()
    
    return data

            
        

def main():
    #-----------------------------CARGAR EN BASE DE DATOS--------------------------------------------#
    paths = ['static/ieeeXplore.json', 'static/google_schoolar.json', 'static/dblp.json']
    con = sql_connection() 
    insert_in_database(con, paths)

    #-----------------------------PRUEBAS CONSULTAS A LA BASE DE DATOS--------------------------------#
    select_data('', '', '2010', '2020', ['bbdd_articulo'])
    #print(data)

if __name__ == '__main__':
    main()
