import json
import requests

def query(path, file, our_content_types, our_start_year, our_end_year):

    result = {}
    with open(path, "r", encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)

    for type in our_content_types:

        for article in data['articles']:

            if type == 'Books' and article['content_type'] == "Books" and article['publication_year'] >= our_start_year and article['publication_year'] <= our_end_year:

                book_id = article['article_number']

                personas = []

                for author in article['authors']['authors']:

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
                        'tipo': 'libro',
                        'titulo': article['title'],
                        'anyo': article['publication_year'],
                        'url': article['pdf_url'],
                        'escrito_por': personas,
                        'editorial': article['publisher']
                    }
                
                })

            if type == 'Conferences' and article['content_type'] == "Conferences" and article['publication_year'] >= our_start_year and article['publication_year'] <= our_end_year:

                conference_id = article['article_number']

                personas = []

                for author in article['authors']['authors']:

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
                    'tipo': 'conferencia',
                    'titulo': article['title'],
                    'anyo': article['publication_year'],
                    'url': article['pdf_url'],
                    'escrito_por': personas,
                    'congreso': article['publication_title'],
                    'edicion': article['publication_year'],
                    'lugar': article['conference_location'],
                    'pagina_inicio': article['start_page'],
                    'pagina_fin': article['end_page'],
                }
            
            })

            if type == 'Journals' and article['content_type'] == "Journals" and article['publication_year'] >= our_start_year and article['publication_year'] <= our_end_year:

                
                journal_id = article['article_number']

                personas = []

                for author in article['authors']['authors']:

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
                    'tipo': 'articulo',
                    'titulo': article['title'],
                    'anyo': article['publication_year'],
                    'url': article['pdf_url'],
                    'escrito_por': personas,
                    'pagina_inicio': article['start_page'],
                    'pagina_fin': article['end_page'],
                    'ejemplar': {
                        'volumen': article['volume'],
                        'numero': article['is_number'],
                        'mes': None,
                        'revista': article['publisher']
                    }
                }
            
            })

    return result
    
    

def main():
    result = query("bibliosearch\controllers\pobre.json", 'static/ieeeXplore.json', ['Journals'], 2018, 2020)
    with open('static/ieeeXplore.json', 'w') as json_file:
        json.dump(result, json_file)
    json_file.close()

if __name__ == "__main__":
    main()