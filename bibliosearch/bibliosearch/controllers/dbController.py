from bibliosearch.models.Ejemplar import Ejemplar
from bibliosearch.models.Com_con import COM_CON, Com_con, dict_2_com_con
from bibliosearch.models.Libro import LIBRO, Libro, dict_2_libro
from bibliosearch.models.Articulo import ARTICULO, Articulo, dict_2_articulo
from bibliosearch.models.Revista import Revista
from bibliosearch.models.Persona import Persona
import json
import sqlite3
from sqlite3.dbapi2 import Error

PATHS = ['static/ieeeXplore.json', 'static/dblp.json', 'static/google_scholar.json']

def insert_articulo(conn, articulo):
    """
    Inserts an article in "bbdd_articulo" table
    """
    sql_art = '''INSERT INTO bbdd_articulo(pagina_inicio, pagina_fin, publicacion_id, ejemplar_id)
                VALUES(?,?,?,?)'''

    cur = conn.cursor()
    
    try:
        id_publicacion = insert_publicacion(conn, articulo)
        if id_publicacion == 0:
            raise Exception("ID = 0 articulo")
        id_ejemplar = insert_ejemplar(conn, articulo.get_ejemplar())
        values = [articulo.get_pagina_inicio(), articulo.get_pagina_fin(), id_publicacion, id_ejemplar]
        cur.execute("BEGIN")
        cur.execute(sql_art, values)
        cur.execute("COMMIT")
        return cur.lastrowid
    except sqlite3.IntegrityError as err:
        cur.execute("ROLLBACK")
        print(err)
    except Exception as e:
        print(e)

def insert_ejemplar(conn, ejemplar):
    """
    Inserts an ejemplar in "bbdd_ejemplar" table
    """
    sql_ejemplar = '''INSERT INTO bbdd_ejemplar(id_ejemplar, volumen, numero, mes)
                    VALUES(?,?,?,?)'''
    cur = conn.cursor()
    try:
        values = [None, ejemplar.get_volumen(), ejemplar.get_numero(), ejemplar.get_mes()]

        cur.execute("BEGIN")
        cur.execute(sql_ejemplar, values)
        cur.execute("COMMIT")

        insert_revista(conn, ejemplar.get_revista(), cur.lastrowid)

        return cur.lastrowid
    except sqlite3.IntegrityError as err:
        cur.execute("ROLLBACK")
        print(err)

def insert_revista(conn, revista, ejemplar):
    """
    Inserts a revista in "bbdd_revista" table
    """
    sql_revista = '''INSERT INTO bbdd_revista(id_revista, nombre, ejemplar_id)
                    VALUES(?,?,?)'''
    cur = conn.cursor()

    try:

        values = [None, revista.get_nombre(), ejemplar]
        cur.execute("BEGIN")
        cur.execute(sql_revista, values)
        cur.execute("COMMIT")
        return cur.lastrowid
    except sqlite3.IntegrityError as err:
        cur.execute("ROLLBACK")
        print(err)

def insert_publicacion(conn, publicacion):
    """
    Inserts an article in "bbdd_publicacion" table
    """

    values = [None, publicacion.get_titulo(), publicacion.get_anyo(), publicacion.get_url()]

    sql = '''INSERT OR IGNORE INTO bbdd_publicacion(
            id_publicacion, titulo, anyo, URL) VALUES
            (?,?,?,?)
            '''
    cur = conn.cursor()
    try:
        cur.execute("BEGIN")
        cur.execute(sql, values)
        cur.execute("COMMIT")
    
        for persona in publicacion.get_autores():
            id_persona = insert_persona(conn, persona)
            if id_persona == 0:
                raise Exception("ID = 0 persona")
            insert_persona_publicacion(conn, id_persona,cur.lastrowid)
        return cur.lastrowid

    except sqlite3.IntegrityError as err:
        cur.execute("ROLLBACK")
        print(err)
    except Exception as e:
        print(e)
    
    

def insert_libro(conn, libro): 
    """
    Inserts a libro in "bbdd_libro" table
    """
    sql = '''INSERT INTO bbdd_libro(editorial, publicacion_id)
            VALUES(?,?)'''
    cur = conn.cursor()
    try:

        id_publicacion = insert_publicacion(conn, libro)
        if id_publicacion == 0:
            raise Exception("ID = 0 libro")
        values = [libro.get_editorial(), id_publicacion]
        cur.execute("BEGIN")
        cur.execute(sql, values)
        cur.execute("COMMIT")
        return cur.lastrowid
    except sqlite3.IntegrityError as err:
        cur.execute("ROLLBACK")
        print(err)
    except Exception as e:
        print(e)

def insert_comCon(conn, com_con): 
    """
    Inserts a com_con in "bbdd_com_con" table
    """
    sql = '''INSERT INTO bbdd_com_con(
            congreso, edicion, lugar, pagina_inicio, pagina_fin, publicacion_id) VALUES
            (?,?,?,?,?,?)'''
    cur = conn.cursor()
    try:

        id_publicacion = insert_publicacion(conn, com_con)
        if id_publicacion == 0:
            raise Exception("ID = 0 com_con")
        values = [com_con.get_congreso(), com_con.get_edicion(), com_con.get_lugar(), com_con.get_pagina_inicio(), com_con.get_pagina_fin(), id_publicacion]
        cur.execute("BEGIN")
        cur.execute(sql, values)
        cur.execute("COMMIT")
        return cur.lastrowid
    except sqlite3.IntegrityError as err:
        cur.execute("ROLLBACK")
        print(err)
    
    except Exception as e:
        print(e)


def insert_persona(conn, persona): 
    """
    Inserts a com_con in "bbdd_person" table
    """
    sql = '''INSERT OR IGNORE INTO bbdd_persona(
            id_persona,nombre,apellidos) VALUES
            (?,?,?)'''
    cur = conn.cursor()

    try:
        values = [None,persona.get_nombre(),persona.get_apellidos()]
        cur.execute("BEGIN")
        cur.execute(sql, values)
        cur.execute("COMMIT")
        return cur.lastrowid
    except sqlite3.IntegrityError as err:
        cur.execute("ROLLBACK")
        print(err)

def insert_persona_publicacion(conn, persona_id,publicacion_id): 
    """
    Inserts a com_con in "bbdd_personapublicacion" table
    """
    sql = '''INSERT INTO bbdd_personapublicacion(
            id_personapublicacion, persona_id,publicacion_id) VALUES
            (?,?,?)'''
    cur = conn.cursor()

    try:
        values = [None, persona_id,publicacion_id]
        cur.execute("BEGIN")
        cur.execute(sql, values)
        cur.execute("COMMIT")
        return cur.lastrowid
    except sqlite3.IntegrityError as err:
        cur.execute("ROLLBACK")
        print(err)

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

            if article['tipo'] == LIBRO:
                libro = Libro(article['editorial'], article_id, article['titulo'], article['anyo'], article['url'], personas)
                insert_libro(con, libro)
            if article['tipo'] == COM_CON:
                com_con = Com_con(article['congreso'], article['edicion'], article['lugar'], article['pagina_inicio'], article['pagina_fin'], article_id, article['titulo'], article['anyo'], article['url'], personas)
                insert_comCon(con, com_con)
            if article['tipo'] == ARTICULO:
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
            LEFT JOIN bbdd_personapublicacion AS pp
            ON p.id_publicacion = pp.publicacion_id
            LEFT JOIN bbdd_persona AS persona
            ON pp.persona_id = persona.id_persona
            JOIN bbdd_ejemplar AS e
            ON a.ejemplar_id = e.id_ejemplar
            JOIN bbdd_revista AS r
            ON a.ejemplar_id = r.ejemplar_id
            WHERE titulo LIKE '%''' + titulo + '''%' AND
            anyo >= ''' + fecha_desde + ''' AND anyo <= ''' + fecha_hasta +''' AND
            (IFNULL(persona.nombre || " " || persona.apellidos, '') LIKE '%''' + autor + '''%')
            GROUP BY a.publicacion_id
            '''

            #print(sql)

            cursor.execute(sql)

            columns = [column[0] for column in cursor.description]

            articulos = cursor.fetchall()

            for data_articulo in articulos:
                dictionary = dict(zip(columns, data_articulo))
                articulo = dict_2_articulo(dictionary)
                data.append(articulo)
            
            con.commit()
        
        if tipo == 'bbdd_com_con':

            sql = '''SELECT c.publicacion_id,
            group_concat(persona.nombre || " " || persona.apellidos, ', ') as autores,
            titulo, edicion, congreso, lugar, anyo, pagina_inicio, pagina_fin, url  from bbdd_com_con AS c 
            JOIN bbdd_publicacion AS p 
            ON c.publicacion_id = p.id_publicacion
            LEFT JOIN bbdd_personapublicacion AS pp
            ON p.id_publicacion = pp.publicacion_id
            LEFT JOIN bbdd_persona AS persona
            ON pp.persona_id = persona.id_persona
            WHERE titulo LIKE '%''' + titulo + '''%' AND
            anyo >= ''' + fecha_desde + ''' AND anyo <= ''' + fecha_hasta +''' AND
            (IFNULL(persona.nombre || " " || persona.apellidos, '') LIKE '%''' + autor + '''%')
            GROUP BY c.publicacion_id
            '''

            cursor.execute(sql)

            conferencias = cursor.fetchall()

            columns = [column[0] for column in cursor.description]


            for data_com_con in conferencias:
                dictionary = dict(zip(columns, data_com_con))
                com_con = dict_2_com_con(dictionary)
                data.append(com_con)
            
            con.commit()

        if tipo == 'bbdd_libro':

            sql = '''SELECT c.publicacion_id, 
            group_concat(persona.nombre || " " || persona.apellidos, ', ') as autores,
            titulo, editorial, anyo, url
            from bbdd_libro AS c 
            JOIN bbdd_publicacion AS p 
            ON c.publicacion_id = p.id_publicacion
            LEFT JOIN bbdd_personapublicacion AS pp
            ON p.id_publicacion = pp.publicacion_id
            LEFT JOIN bbdd_persona AS persona
            ON pp.persona_id = persona.id_persona
            WHERE titulo LIKE '%''' + titulo + '''%' AND
            anyo >= ''' + fecha_desde + ''' AND anyo <= ''' + fecha_hasta +''' AND
            (IFNULL(persona.nombre || " " || persona.apellidos, '') LIKE '%''' + autor + '''%')
            GROUP BY c.publicacion_id
            '''

            cursor.execute(sql)

            libros = cursor.fetchall()

            columns = [column[0] for column in cursor.description]

            for data_libro in libros:
                dictionary = dict(zip(columns, data_libro))
                libro = dict_2_libro(dictionary)
                data.append(libro)
            
            con.commit()
    
    data.sort(key=lambda x:x.get_titulo())
    return data

def delete_all_data():
    conn = sql_connection()
    cur = conn.cursor()

    sql_delete_publicaciones = 'DELETE FROM bbdd_publicacion'
    sql_delete_articulos = 'DELETE FROM bbdd_articulo'
    sql_delete_ejemplares = 'DELETE FROM bbdd_ejemplar'
    sql_delete_revistas = 'DELETE FROM bbdd_revista'
    sql_delete_libros = 'DELETE FROM bbdd_libro'
    sql_delete_com_con = 'DELETE FROM bbdd_com_con'
    sql_delete_personas = 'DELETE FROM bbdd_persona'
    sql_delete_personaspublicaciones = 'DELETE FROM bbdd_personapublicacion'

    sqls = [sql_delete_publicaciones, sql_delete_articulos, sql_delete_ejemplares, sql_delete_revistas, sql_delete_libros, sql_delete_com_con,
    sql_delete_personas, sql_delete_personaspublicaciones]

    for sql in sqls:
        cur.execute("BEGIN")
        cur.execute(sql)
        cur.execute("COMMIT")

        

def main():
    #-----------------------------CARGAR EN BASE DE DATOS--------------------------------------------#
    
    # con = sql_connection() 
    # insert_in_database(con, PATHS)

    #-----------------------------PRUEBAS CONSULTAS A LA BASE DE DATOS--------------------------------#
    # data = select_data('', '', '1000', '2020', ['bbdd_articulo','bbdd_libro', 'bbdd_com_con'])
    # for publi in data:
        # print(publi.get_titulo())
    delete_all_data()

if __name__ == '__main__':
    main()
