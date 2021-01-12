import collections
import json
from typing import OrderedDict
import xmltodict

# Este método recorre el archivo dado en el parámetro "xml_file",
# seleccionando los artículos que van desde el año "year_st" hasta el "year_end"
def xml_parser(xml_file, year_st, year_end):
    """Parser from XML to JSON / IEI"""
    with open(xml_file) as xml_f:
        data_dict = xmltodict.parse(xml_f.read())
        xml_f.close()


    #Constantes de los atributos xml
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

        # Comprobación del año
        if int(article_dict[ANO])>=year_st and int(article_dict[ANO])<=year_end:
            new_dict['anyo'] = str(article_dict[ANO])

            # Key
            key = article_dict[KEY]

            # Tipo de publicación
            new_dict['tipo'] = "articulo"

            # Titulo
            new_dict['titulo'] = article_dict[TITULO]

            # Escritores
            escrita_por = []
            if AUTOR in list(article_dict.keys()):
                aut = article_dict[AUTOR]

                # Si el atributo es un OrderedDict
                if type(aut) == type(collections.OrderedDict()):
                    nom_ap = aut['#text'].split()
                    nombre = nom_ap[0]
                    apellidos = ''
                    for ap in nom_ap[1:len(nom_ap)]:
                        apellidos += f'{ap} '
                    escrita_por.append({'nombre': nombre, 'apellidos': apellidos})

                # Si el atributo es una lista
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

                # Si el atributo es un String
                if type(aut) == type(""):
                    nom_ap = aut.split()
                    nombre = nom_ap[0]
                    apellidos = ''
                    for ap in nom_ap[1:len(nom_ap)]:
                        apellidos += f'{ap} '
                    escrita_por.append({'nombre': nombre, 'apellidos': apellidos})
            
            new_dict['escrita_por'] = escrita_por

            # Url
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

            # Páginas
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

            # Publicado_en
            publicado_en = {}

            # publicado_en.volumen
            if (VOLUMEN) in list(article_dict.keys()):
                publicado_en['volumen'] = article_dict[VOLUMEN]
            else:
                publicado_en['volumen'] = None
            
            # publicado_en.numero
            if (NUMBER) in list(article_dict.keys()):
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

            articles[key] = new_dict

    return articles


def main():
    """
    Main IEI parser
    """
    result = xml_parser("static/DPLB-ENTREGA-FINAL.xml", 2005, 2020)

    with open('static/dblp.json', 'w') as json_file:
        json.dump(result, json_file)
    json_file.close()
    


if __name__ == "__main__":
    main()