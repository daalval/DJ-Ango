from bibliosearch.models.Com_con import COM_CON, INPROCEEDING
from bibliosearch.models.Articulo import ARTICLE, ARTICULO
from bibliosearch.models.Libro import BOOK, LIBRO
import json
import requests

IEEE_ARTICULO = 'Journals'
IEEE_LIBRO = 'Books'
IEEE_COM_CON = 'Conferences'

def query(url, file, our_content_types, our_start_year, our_end_year):

    result = {}
    data = {}

    for type in our_content_types:
        params = dict(
            content_type = type,
            start_year = our_start_year,
            end_year = our_end_year,
            max_records = '20',
        )
        data = requests.get(url, verify=False, params=params).json()

        if ieee_type_to_type(type) == LIBRO:

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

                result.update({
                    book_id: {
                        'tipo': LIBRO,
                        'titulo': book['title'],
                        'anyo': book['publication_year'],
                        'url': book['pdf_url'],
                        'escrita_por': personas,
                        'editorial': book['publisher']
                    }
                })

        if ieee_type_to_type(type) == COM_CON:

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

                result.update({
                conference_id: {
                    'tipo': COM_CON,
                    'titulo': conference['title'],
                    'anyo': conference['publication_year'],
                    'url': conference['pdf_url'],
                    'escrita_por': personas,
                    'congreso': conference['publication_title'],
                    'edicion': conference['publication_year'],
                    'lugar': conference['conference_location'],
                    'pagina_inicio': conference['start_page'],
                    'pagina_fin': conference['end_page'],
                }
                
            })

        if ieee_type_to_type(type) == ARTICULO:

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

                result.update({
                journal_id: {
                    'tipo': ARTICULO,
                    'titulo': journal['title'],
                    'anyo': journal['publication_year'],
                    'url': journal['pdf_url'],
                    'escrita_por': personas,
                    'pagina_inicio': journal['start_page'],
                    'pagina_fin': journal['end_page'],
                    'publicado_en': {
                        'volumen': journal['volume'],
                        'numero': journal['is_number'],
                        'mes': None,
                        'revista': {
                            'nombre': journal['publisher']
                        }
                    }
                }
                
            })

    return result

def ieee_type_to_type(type):
    if type == IEEE_LIBRO:
        return LIBRO
    if type == IEEE_ARTICULO:
        return ARTICULO
    if type == IEEE_COM_CON:
        return COM_CON
    raise Exception("IeeeEngine error: ieee_type_to_type tipo inexistente")

def get_result():

    result = query("https://ieeexploreapi.ieee.org/api/v1/search/articles?parameter&apikey=efv84mzqq6ydx4dbd59jhdcn", 'static/ieeeXplore.json', [LIBRO,COM_CON,ARTICULO], '2010', '2015')

    with open('static/ieeeXplore.json', 'w') as json_file:
        json.dump(result, json_file)
    json_file.close()

def main():
    get_result()

if __name__ == '__main__':
    main()