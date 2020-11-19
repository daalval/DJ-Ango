import json
import xmltodict

def xml_parser(xml_file, json_file):
    """Parser from XML to JSON / IEI"""
    with open(xml_file) as xml_f: 
        data_dict = xmltodict.parse(xml_f.read()) 
        xml_f.close() 

    KEY='@key'
    TITULO='title'
    ANO='year'
    URL='ee'
    PAGINA_INICIO='pages'
    PAGINA_FIN='pages'
    VOLUMEN='volume'
    NUMBER='number'
    NOMBRE='journal'
      
    json_data = json.dumps(data_dict) 
    articles=[]
    for article_dict in data_dict['dblp']['article']:
        new_dict = {}
        #key
        new_dict['key'] = article_dict[KEY]
        #titulo
        new_dict['titulo'] = article_dict[TITULO]
        #list escritores
        escrita_por = []
        for esc in article_dict['author']:
            nom_ap = esc.split()
            nombre = nom_ap[0]
            apellidos = ''
            for ap in nom_ap[1:len(nom_ap)]:
                apellidos += f'{ap} '
            escrita_por.append({nombre, apellidos})

        new_dict['escrita_por'] = escrita_por
        #ano
        new_dict['ano'] = article_dict[ANO]
        #url
        new_dict['URL'] = article_dict[URL]
        #pagina_inicio
        new_dict['pagina_inicio'] = article_dict[PAGINA_INICIO].split('-')[0]
        #pagina_fin
        new_dict['pagina_fin'] = article_dict[PAGINA_FIN].split('-')[1]
        #publicado_en.volumen
        publicado_en = {}
        publicado_en['volumen'] = article_dict[VOLUMEN]
        #publicado_en.numero
        publicado_en['numero'] = article_dict[NUMBER]
        #publicado_en.mes
        publicado_en['mes'] = None
        new_dict['publicado_en'] = publicado_en
        #Ejemplar.tiene.nombre
        Ejemplar = {
            'nombre': article_dict[NOMBRE]
        }
        new_dict['Ejemplar'] = Ejemplar
        #Revista.nombre
        Revista = {
            'nombre': article_dict[NOMBRE]
        }
        new_dict['Revista'] = Revista
    
      
    with open(json_file, "w") as json_file_opened: 
        json_file_opened.write(json_data) 
        json_file_opened.close()

def main():
    """
    Main IEI parser
    """
    xml_parser("../../static/dblp-pruebas.xml", "../../static/dblp.json")


if __name__ == "__main__":
    main()

