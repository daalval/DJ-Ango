import collections
import json
from typing import OrderedDict
import xmltodict


def xml_parser(xml_file, json_file, year_st, year_end):
    """Parser from XML to JSON / IEI"""
    with open(xml_file) as xml_f:
        data_dict = xmltodict.parse(xml_f.read())
        xml_f.close()

    KEY = '@key'
    AUTOR = 'author'
    TITULO = 'title'
    ANO = 'year'
    URL = 'ee'
    PAGINA_INICIO = 'pages'
    PAGINA_FIN = 'pages'
    VOLUMEN = 'volume'
    NUMBER = 'number'
    NOMBRE = 'journal'

    articles = {}
    for article_dict in data_dict['dblp']['article']:
        new_dict = {}
        # ano
        if int(article_dict[ANO])>=year_st and int(article_dict[ANO])<=year_end:
            new_dict['anyo'] = str(article_dict[ANO])
            # key
            key = article_dict[KEY]
            new_dict['tipo'] = "articulo"
            # titulo
            new_dict['titulo'] = article_dict[TITULO]

            # list escritores
            escrita_por = []
            if AUTOR in list(article_dict.keys()):
                aut = article_dict[AUTOR]
                if type(aut) == type(collections.OrderedDict()):
                    nom_ap = aut['#text'].split()
                    nombre = nom_ap[0]
                    apellidos = ''
                    for ap in nom_ap[1:len(nom_ap)]:
                        apellidos += f'{ap} '
                    escrita_por.append({'nombre': nombre, 'apellidos': apellidos})
                if type(aut) == type([]):
                    for esc in aut:
                        if type(esc) == type(collections.OrderedDict()):
                            nom_ap = esc['#text'].split()
                            nombre = nom_ap[0]
                            apellidos = ''
                            for ap in nom_ap[1:len(nom_ap)]:
                                apellidos += f'{ap} '
                            escrita_por.append({'nombre': nombre, 'apellidos': apellidos})
                        if type(esc) == type(''):
                            nom_ap = esc.split()
                            nombre = nom_ap[0]
                            apellidos = ''
                            for ap in nom_ap[1:len(nom_ap)]:
                                apellidos += f'{ap} '
                            escrita_por.append({'nombre': nombre, 'apellidos': apellidos})
                if type(aut) == type(""):
                    nom_ap = aut.split()
                    nombre = nom_ap[0]
                    apellidos = ''
                    for ap in nom_ap[1:len(nom_ap)]:
                        apellidos += f'{ap} '
                    escrita_por.append({'nombre': nombre, 'apellidos': apellidos})
            
            new_dict['escrita_por'] = escrita_por


            # url
            añadir_url = ""
            if URL in list(article_dict.keys()):
                url = article_dict[URL]
                if type(url) == type(collections.OrderedDict()):
                    añadir_url = url['#text']
                if type(url) == type([]):
                    añadir_url = url[0]
                if type(url) == type(""):
                    añadir_url = url
            
            new_dict['url'] = añadir_url

            if (PAGINA_FIN) in list(article_dict.keys()):
                p = article_dict[PAGINA_INICIO].split('-')
                # pagina_inicio
                new_dict['pagina_inicio'] = p[0]
                # pagina_fin
                if(len(p)>1):
                    new_dict['pagina_fin'] = article_dict[PAGINA_FIN].split('-')[1]
                else:
                    new_dict['pagina_fin'] = None
            else:
                new_dict['pagina_inicio'] = None
                new_dict['pagina_fin'] = None

            publicado_en = {}
            if (VOLUMEN) in list(article_dict.keys()):
                # publicado_en.volumen
                publicado_en['volumen'] = article_dict[VOLUMEN]
            else:
                publicado_en['volumen'] = None
            if (NUMBER) in list(article_dict.keys()):
                # publicado_en.numero
                publicado_en['numero'] = article_dict[NUMBER]
            else:
                publicado_en['numero'] = None
            # publicado_en.mes
            publicado_en['mes'] = None
            # Revista.nombre
            revista = {
                'nombre': article_dict[NOMBRE]
            }
            publicado_en['revista'] = revista
            new_dict['publicado_en'] = publicado_en
            # Ejemplar.tiene.nombre
            #ejemplar = {
            #    'nombre': article_dict[NOMBRE]
            #}
            #new_dict['ejemplar'] = ejemplar
            # Revista.nombre
            articles[key] = new_dict

    return articles

    # json_data = json.dumps(articles, indent=4)
    

    # with open(json_file, "w") as json_file_opened:
    #     json_file_opened.write(json_data)
    #     json_file_opened.close()


def main():
    """
    Main IEI parser
    """
    result = xml_parser("static/dblp-pruebas.xml", "static/dblp.json", 2005, 2020)

    with open('static/dblp.json', 'w') as json_file:
        json.dump(result, json_file)
    json_file.close()
    


if __name__ == "__main__":
    main()