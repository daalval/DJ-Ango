from bibliosearch.models.Com_con import COM_CON
from bibliosearch.models.Articulo import  ARTICULO
from bibliosearch.models.Libro import  LIBRO
import json
import requests

IEEE_ARTICULO = 'Journals'
IEEE_LIBRO = 'Books'
IEEE_COM_CON = 'Conferences'

# Método que se encarga de realizar la consulta en la web de ieeXplore
# Parámetros: 
#   url: link de consulta a ieeeXplore con su respectiva Api key
#   file: archivo json en el que se guarda la info extraída
#   our_content_types: tipos (articulos, libros, conferencias) sobre los que se quiere hacer la consulta
#   our_start_year: año de comienzo
#   our_end_year: año final
def query(url, file, our_content_types, our_start_year, our_end_year):

    result = {}
    data = {}

    # Para cada tipo se realizará una extracción distinta explicada dentro del for

    for type in our_content_types:
        # Parámetros necesarios para la consulta a ieee
        params = dict(
            content_type = type_to_ieee_type(type),
            start_year = our_start_year,
            end_year = our_end_year,
            max_records = '20',
        )
        # se guarda en data el json que devuelve la consulta en ieee
        try:
            data = requests.get(url, verify=False, params=params).json()
        except Exception as e:
            raise Exception("ieee_extractor error: Máximo de consultas sobrepasado")

        # para cada tipo de publicacion se haran los mappings correspondientes
        if type == LIBRO:

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

        if type == COM_CON:

            for conference in data['articles']:
                
                conference_id = conference['article_number']

                if('end_page' in conference):
                    end_page = conference['end_page']
                else:
                    end_page = None
                
                if('start_page' in conference):
                    start_page = conference['start_page']
                else:
                    start_page = None
                
                if('conference_location' in conference):
                    conference_location = conference['conference_location']
                else:
                    conference_location = None

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
                        'lugar': conference_location,
                        'pagina_inicio': start_page,
                        'pagina_fin': end_page,
                    }
                
                })
        
        if type == ARTICULO:

            for journal in data['articles']:
                
                journal_id = journal['article_number']

                if('volume' in journal):
                    volume = journal['volume']
                else:
                    volume = None
                
                if('is_number' in journal):
                    is_number = journal['is_number']
                else:
                    is_number = None
                
                if('start_page' in journal):
                    start_page = journal['start_page']
                else:
                    start_page = None
                
                if('end_page' in journal):
                    end_page = journal['end_page']
                else:
                    end_page = None

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
                        'pagina_inicio': start_page,
                        'pagina_fin': end_page,
                        'publicado_en': {
                            'volumen': volume,
                            'numero': is_number,
                            'mes': None,
                            'revista': {
                                'nombre': journal['publisher']
                            }
                        }
                    }
                
                })

    return result

# método para cambiar el tipo normal al que necesita ieee
def type_to_ieee_type(type):
    if type == LIBRO:
        return IEEE_LIBRO
    if type == ARTICULO:
        return IEEE_ARTICULO
    if type == COM_CON:
        return IEEE_COM_CON
    raise Exception("IeeeEngine error: ieee_type_to_type tipo inexistente")

# método que llama al método query comentado anteriormente
def get_result():

    result = query("https://ieeexploreapi.ieee.org/api/v1/search/articles?parameter&apikey=efv84mzqq6ydx4dbd59jhdcn", 'static/ieeeXplore.json', [ARTICULO, LIBRO, COM_CON], '2000', '2020')

    # esto escribe el resultado en el archivo pasado como primer argumento en el método open
    with open('static/ieeeXplore.json', 'w') as json_file:
        json.dump(result, json_file)
    json_file.close()

def main():
    get_result()

if __name__ == '__main__':
    main()