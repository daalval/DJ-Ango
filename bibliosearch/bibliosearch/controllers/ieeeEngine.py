import json
import requests

def query(url, file, our_content_types, our_start_year, our_end_year):

    result = {
        'articles': {

        }
    }
    data = {}

    for type in our_content_types:
        params = dict(
            content_type = type,
            start_year = our_start_year,
            end_year = our_end_year,
            max_records = '200',
        )
        data = requests.get(url, verify=False, params=params).json()

        if type == 'Books':

            for book in data['articles']:
                book_id = book['article_number']

                personas = []

                for author in book['authors']['authors']:

                    full_name = author['full_name'].split()

                    name = full_name[0]
                    last_name = ''
                
                    if len(full_name) > 1:
                        full_name = full_name[1:len(full_name)]
                        for ln in full_name:
                            last_name = last_name + ln + ' '

                    persona = {
                        'nombre': name,
                        'apellidos': last_name.strip()
                    }
                    personas.append(persona)

                result['articles'].update({
                    book_id: {
                        'id': book_id,
                        'tipo': 'libro',
                        'titulo': book['title'],
                        'anyo': book['publication_year'],
                        'url': book['pdf_url'],
                        'escrito_por': personas,
                        'editorial': book['publisher']
                    }
                })

        if type == 'Conferences':

            for conference in data['articles']:
                conference_id = conference['article_number']

                personas = []

                for author in conference['authors']['authors']:

                    full_name = author['full_name'].split()

                    name = full_name[0]
                    last_name = ''
                
                    if len(full_name) > 1:
                        full_name = full_name[1:len(full_name)]
                        for ln in full_name:
                            last_name = last_name + ln + ' '

                    persona = {
                        'nombre': name,
                        'apellidos': last_name.strip()
                    }
                    personas.append(persona)

                result['articles'].update({
                conference_id: {
                    'id': conference_id,
                    'tipo': 'com_con',
                    'titulo': conference['title'],
                    'anyo': conference['publication_year'],
                    'url': conference['pdf_url'],
                    'escrito_por': personas,
                    'congreso': conference['publication_title'],
                    'edicion': conference['publication_year'],
                    'lugar': conference['conference_location'],
                    'pagina_inicio': conference['start_page'],
                    'pagina_fin': conference['end_page'],
                }
                
            })

        if type == 'Journals':

            for journal in data['articles']:
                journal_id = journal['article_number']

                personas = []

                for author in journal['authors']['authors']:

                    full_name = author['full_name'].split()

                    name = full_name[0]
                    last_name = ''
                
                    if len(full_name) > 1:
                        full_name = full_name[1:len(full_name)]
                        for ln in full_name:
                            last_name = last_name + ln + ' '

                    persona = {
                        'nombre': name,
                        'apellidos': last_name.strip()
                    }
                    personas.append(persona)

                result['articles'].update({
                journal_id: {
                    'id': journal_id,
                    'tipo': 'articulo',
                    'titulo': journal['title'],
                    'anyo': journal['publication_year'],
                    'url': journal['pdf_url'],
                    'escrito_por': personas,
                    'pagina_inicio': journal['start_page'],
                    'pagina_fin': journal['end_page'],
                    'ejemplar': {
                        'volumen': journal['volume'],
                        'numero': journal['is_number'],
                        'mes': None,
                        'revista': journal['publisher']
                    }
                }
                
            })

        

    return result
    
    

# def main():
#     result = query("https://ieeexploreapi.ieee.org/api/v1/search/articles?parameter&apikey=efv84mzqq6ydx4dbd59jhdcn", 'static/ieeeXplore.json', ['Conferences', 'Journals', 'Books'], '2010', '2015')
#     with open('static/ieeeXplore.json', 'w') as json_file:
#         json.dump(result, json_file)
#     json_file.close()

# if __name__ == "__main__":
#     main()

import sqlite3
from sqlite3 import Error

def sql_connection():

    try:

        con = sqlite3.connect('mydatabase.db')

        return con

    except Error:

        print(Error)

def sql_table(con):

    cursorObj = con.cursor()

    result = query("https://ieeexploreapi.ieee.org/api/v1/search/articles?parameter&apikey=efv84mzqq6ydx4dbd59jhdcn", 'static/ieeeXplore.json', ['Books', 'Conferences', 'Journals'], '2010', '2015')

    with open('static/ieeeXplore.json', 'w') as json_file:
        json.dump(result, json_file)
    json_file.close()

    with open ('static/ieeeXplore.json','r') as f:
        jsondata = json.loads(f.read())
        # print(jsondata)

    cursorObj.execute("CREATE TABLE IF NOT EXISTS publicacion(id_publicacion integer PRIMARY KEY, titulo text, anyo integer, url text)")
    cursorObj.execute("CREATE TABLE IF NOT EXISTS persona(id_persona integer PRIMARY KEY, nombre text, apellidos text)")
    cursorObj.execute("CREATE TABLE IF NOT EXISTS personaPublicacion(persona NOT NULL, publicacion NOT NULL, FOREIGN KEY(persona) REFERENCES persona(id_persona))")
    cursorObj.execute("CREATE TABLE IF NOT EXISTS com_con(congreso text, edicion text, lugar text, pagina_inicio integer, pagina_fin integer, publicacion integer PRIMARY KEY, FOREIGN KEY(publicacion) REFERENCES publicacion(id_publicacion))")
    cursorObj.execute("CREATE TABLE IF NOT EXISTS libro(editorial text, publicacion integer PRIMARY KEY, FOREIGN KEY(publicacion) REFERENCES publicacion(id_publicacion))")
    cursorObj.execute("CREATE TABLE IF NOT EXISTS revista(id_revista integer PRIMARY KEY, nombre text)")
    cursorObj.execute("CREATE TABLE IF NOT EXISTS ejemplar(id_ejemplar integer PRIMARY KEY, volumen integer, numero integer, mes integer, revista integer, FOREIGN KEY(revista) REFERENCES revista(id_revista))")
    cursorObj.execute("CREATE TABLE IF NOT EXISTS articulo(pagina_inicio integer, pagina_fin integer, ejemplar integer, publicacion integer PRIMARY KEY, FOREIGN KEY(ejemplar) REFERENCES ejemplar(id_ejemplar), FOREIGN KEY(publicacion) REFERENCES publicacion(id_publicacion))")

    cont = 0

    for article in jsondata['articles']:
        id = jsondata['articles'][article]['id']
        titulo = jsondata['articles'][article]['titulo']
        anyo = jsondata['articles'][article]['anyo']
        url = jsondata['articles'][article]['url']
        cursorObj.execute("""INSERT INTO publicacion VALUES (
            str(cont) + ", " + 'hola' + ", " + str(192) + ", " + 'wqrwr' + ")")"""
        cont = cont + 1

    con.commit()

con = sql_connection()

sql_table(con)