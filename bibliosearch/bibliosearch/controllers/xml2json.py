import collections
import json
from typing import OrderedDict
import xmltodict


def xml_parser(xml_file, json_file):
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
        # key
        key = article_dict[KEY]
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
        # ano
        new_dict['ano'] = article_dict[ANO]
        # url
        if URL in list(article_dict.keys()):
            new_dict['URL'] = article_dict[URL]

        if (PAGINA_FIN) in list(article_dict.keys()):
            p = article_dict[PAGINA_INICIO].split('-')
            # pagina_inicio
            new_dict['pagina_inicio'] = p[0]
            # pagina_fin
            if(len(p)>1):
                new_dict['pagina_fin'] = article_dict[PAGINA_FIN].split('-')[1]

        publicado_en = {}
        if (VOLUMEN) in list(article_dict.keys()):
            # publicado_en.volumen
            publicado_en['volumen'] = article_dict[VOLUMEN]
        if (NUMBER) in list(article_dict.keys()):
            # publicado_en.numero
            publicado_en['numero'] = article_dict[NUMBER]
        # publicado_en.mes
        publicado_en['mes'] = None
        new_dict['publicado_en'] = publicado_en
        # Ejemplar.tiene.nombre
        ejemplar = {
            'nombre': article_dict[NOMBRE]
        }
        new_dict['ejemplar'] = ejemplar
        # Revista.nombre
        revista = {
            'nombre': article_dict[NOMBRE]
        }
        new_dict['revista'] = revista
        articles[key] = new_dict

    json_data = json.dumps(articles, indent=4)
    

    with open(json_file, "w") as json_file_opened:
        json_file_opened.write(json_data)
        json_file_opened.close()


def main():
    """
    Main IEI parser
    """
    xml_parser("../../static/DBLP-SOLO_ARTICLE.XML", "../../static/dblp.json")


if __name__ == "__main__":
    main()
