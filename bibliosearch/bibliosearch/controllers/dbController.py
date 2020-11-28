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
    sql_art = ''' INSERT INTO bbdd_articulo(pagina_inicio, pagina_fin, publicacion_id, ejemplar_id)
                VALUES(%s,%s,%s,%s) ''' % (articulo.get_pagina_inicio(), articulo.get_pagina_fin(),articulo.get_id(), articulo.get_ejemplar().get_id())
    insert_publicacion(conn, articulo)
    insert_ejemplar(conn, articulo.get_ejemplar())
    cur = conn.cursor()
    cur.execute(sql_art)
    conn.commit()
    return cur.lastrowid

def insert_ejemplar(conn, ejemplar):
    """
    Inserts an ejemplar in "bbdd_ejemplar" table
    """
    sql_ejemplar = ''' INSERT INTO bbdd_ejemplar(id_ejemplar, volumen, numero, mes, revista_id)
                    VALUES(%s,%s,%s,%s) ''' % (ejemplar.get_id(), ejemplar.get_volumen(), ejemplar.get_numero(), ejemplar.get_mes(), ejemplar.get_revista().get_id())
    insert_revista(ejemplar.get_revista())
    cur = conn.cursor()
    cur.execute(sql_ejemplar)
    conn.commit()
    return cur.lastrowid

def insert_revista(conn, revista):
    """
    Inserts a revista in "bbdd_revista" table
    """
    sql_revista = ''' INSERT INTO bbdd_revista(id_revista, nombre)
                    VALUES(%s,%s) ''' % (revista.get_id, revista.get_nombre)
    cur = conn.cursor()
    cur.execute(sql_revista)
    conn.commit()
    return cur.lastrowid

def insert_publicacion(conn, publicacion):
    """
    Inserts an article in "bbdd_publicacion" table
    """
    # sql = '''INSERT INTO bbdd_publicacion(id_publicacion, titulo, anyo, URL)
    #         VALUES(?,?,?,?)''' % (publicacion.get_id(), publicacion.get_titulo(), publicacion.get_anyo(), publicacion.get_url())
    cur = conn.cursor()
    values = [publicacion.get_id(), publicacion.get_titulo(), publicacion.get_anyo(), publicacion.get_url()]
    cur.execute('''INSERT INTO bbdd_publicacion(
            id_publicacion, titulo, anyo, URL) VALUES
            (?,?,?,?)''', values)
    conn.commit()
    return cur.lastrowid   

def insert_libro(conn, libro): 
    """
    Inserts a libro in "bbdd_libro" table
    """
    # sql = ''' INSERT INTO bbdd_libro(editorial, publicacion_id)
    #         VALUES(%s, %s) ''' % (libro.get_editorial(), libro.get_id())
    values = [libro.get_editorial(), libro.get_id()]
    insert_publicacion(conn, libro)
    cur = conn.cursor()
    cur.execute('''INSERT INTO bbdd_libro(
            editorial, publicacion_id) VALUES
            (?,?)''', values)
    conn.commit()
    return cur.lastrowid

def insert_comCon(conn, com_con): 
    """
    Inserts a com_con in "bbdd_com_con" table
    """
    # sql = ''' INSERT INTO bbdd_libro(editorial, publicacion_id)
    #         VALUES(%s, %s) ''' % (libro.get_editorial(), libro.get_id())
    values = [com_con.get_congreso(), com_con.get_edicion(), com_con.get_lugar(), com_con.get_pagina_inicio(), com_con.get_pagina_fin(), com_con.get_id()]
    insert_publicacion(conn, com_con)
    cur = conn.cursor()
    cur.execute('''INSERT INTO bbdd_com_con(
            congreso, edicion, lugar, pagina_inicio, pagina_fin, publicacion_id) VALUES
            (?,?,?,?,?,?)''', values)
    conn.commit()
    return cur.lastrowid