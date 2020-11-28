from bibliosearch.controllers.dbController import insert_libro
from bibliosearch.models.Libro import Libro
import json
import requests
import sqlite3
from sqlite3 import Error


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

def sql_connection():

    try:

        con = sqlite3.connect('db.sqlite3')

        return con

    except Error:

        print(Error)

def insert_in_database(con):

    result = query("https://ieeexploreapi.ieee.org/api/v1/search/articles?parameter&apikey=efv84mzqq6ydx4dbd59jhdcn", 'static/ieeeXplore.json', ['Books'], '2010', '2015')

    with open('static/ieeeXplore.json', 'w') as json_file:
        json.dump(result, json_file)
    json_file.close()

    with open ('static/ieeeXplore.json','r') as f:
        jsondata = json.loads(f.read())

    for article in jsondata['articles']:
        if jsondata['articles'][article]['tipo'] == 'libro':
            libro = Libro(jsondata['articles'][article]['editorial'], jsondata['articles'][article]['id'], jsondata['articles'][article]['titulo'], jsondata['articles'][article]['anyo'], jsondata['articles'][article]['url'], jsondata['articles'][article]['escrito_por'])
            print(libro.get_anyo())
            insert_libro(con, libro)

    con.commit()

con = sql_connection()

insert_in_database(con)   