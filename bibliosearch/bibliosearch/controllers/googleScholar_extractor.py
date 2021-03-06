

import os
from bibliosearch.models.Libro import LIBRO
from bibliosearch.models.Articulo import ARTICULO
from bibliosearch.models.Com_con import COM_CON
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pybtex.database import parse_string

GOOGLE_SCHOLAR_ARTICULO = 'article'
GOOGLE_SCHOLAR_COM_CON = 'inproceedings'
GOOGLE_SCHOLAR_LIBRO = 'book'

class Selenium(object):


    # Metodo que dandole una fecha_inicial, una fecha_final, unos tipos y
    # opcionalmente un autor, selenium hace una busqueda en google scholar
    def search(self, fecha_inicial, fecha_final, autor, tipos):
        result = {}
        listElements = []
        driver = None
        
        # Accede a las opciones avanzadas de google scholar para realizar la busqueda
        try:
            driver = webdriver.Chrome(
                'bibliosearch/controllers/chromedriver.exe')
            driver.get('https://scholar.google.es/#d=gs_asd')
            print(driver.page_source)
            author_element = WebDriverWait(driver, 4).until(
                lambda driver: driver.find_element_by_id('gs_asd_sau'))
            author_element.send_keys(autor)
            fecha_inicial_element = WebDriverWait(driver, 4).until(
                lambda driver: driver.find_element_by_id('gs_asd_ylo'))
            fecha_inicial_element.send_keys(str(fecha_inicial))
            fecha_final_element = driver.find_element_by_id('gs_asd_yhi')
            fecha_final_element.send_keys(str(fecha_final))
            fecha_final_element.send_keys(Keys.RETURN)
            
            # Los elementos obtenidos en la busqueda
            listElements = WebDriverWait(driver, 4).until(
                lambda driver: driver.find_elements_by_class_name('gs_or_cit.gs_nph'))
        except:
            driver.close()
            # Salida si detecta que somos un robot sin ningun resultado, lanza excepcion
            raise Exception("SeleniumEngine error: El navegador ha detectado que eres un robot, sin resultados")
        try:
            # Salida si no ha encontrado elementos
            if len(listElements) == 0:
                driver.close()
                return result

            index = 0
            # Extraer cada elemento
            while(index < len(listElements)):
                result.update(self.extract_element(
                    listElements[index], driver, tipos))
                index = index + 1
                listElements = WebDriverWait(driver, 4).until(
                    lambda driver: driver.find_elements_by_class_name('gs_or_cit.gs_nph'))

            mas_paginas = driver.find_element_by_xpath(
                '/html/body/div/div[9]/div[3]/div').get_attribute('innerText')
            # Si hay más páginas, pasa de página
            if mas_paginas[0] == 'P':
                next_page = driver.find_element_by_xpath(
                    '//*[@id="gs_nm"]/button[2]')

                while next_page.is_enabled():
                    next_page.click()
                    listElements = WebDriverWait(driver, 4).until(
                        lambda driver: driver.find_elements_by_class_name('gs_or_cit.gs_nph'))
                    index = 0
                    # Extraer cada elemento
                    while(index < len(listElements)):
                        result.update(self.extract_element(
                            listElements[index], driver, tipos))
                        index = index + 1
                        listElements = WebDriverWait(driver, 4).until(
                            lambda driver: driver.find_elements_by_class_name('gs_or_cit.gs_nph'))
                    next_page = driver.find_element_by_xpath(
                        '//*[@id="gs_nm"]/button[2]')

        except:
            driver.close()
            # Salida si detecta que somosun robot con algún resultado
            return result

        driver.close()
        # Salida si no detecta que somos robots
        return result

    # Metodo que apartir de un elemento html crea una publicacion segun su tipo
    def extract_element(self, element, driver, tipos):
        # Entramos en el bibtex
        element.click()
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'gs_citi'))).click()
        text = driver.find_element_by_tag_name(
            'pre').get_attribute('innerText')

        # Usamos la libreria bibtex para parsear el texto
        data = parse_string(text, 'bibtex')

        entry = list(data.entries.values())[0]

        type = self.google_scholar_type_to_type(entry.type)

        key = entry.key

        # Salida si esta publicacion no es de un tipo buscado
        if type not in tipos:
            driver.back()
            driver.back()
            return {}

        # Obtenemos los campos del elemento
        fields = entry.fields
        title = self.fix_string_without_accent(fields.get('title'))

        authors = entry.persons.get('author')
        year = fields.get('year')
        publisher = self.fix_string_without_accent(fields.get(
            'publisher')) or self.fix_string_without_accent(fields.get('journal'))

        personas = []

        for author in authors:
            persona = {'nombre': ' '.join(author.first_names),
                       'apellidos':  ' '.join(author.last_names),
                       }
            personas.append(persona)

        # Campos en comun
        result = {

            'anyo': year,
            'escrita_por': personas,
            'titulo': title,
        }

        # Si la publicacion es un articulo
        if type == ARTICULO:

            volume = fields.get('volume')
            number = fields.get('number')
            revista = {
                'nombre': publisher
            }
            publicado_en = {
                'volumen': volume,
                'numero': number,
                'mes': None,
                'revista': revista
            }
            pages = fields.get('pages')
            initial_page = None
            final_page = None
            if pages != None:
                pages = pages.split('--')
                initial_page = pages[0]
                if len(pages) > 1:
                    final_page = pages[1]
            result.update({
                'tipo': ARTICULO,
                'pagina_inicio': initial_page,
                'pagina_fin': final_page,
                'publicado_en': publicado_en
            })
        # Si la publicacion es un libro
        if type == LIBRO:
            pages = fields.get('pages')
            result.update({
                'tipo': LIBRO,
                'paginas': pages,
                'editorial': publisher
            })

        # Si la publicacion es un com_con
        if type == COM_CON:
            organization = self.fix_string_without_accent(
                fields.get('organization'))
            pages = fields.get('pages')
            initial_page = None
            final_page = None
            if pages != None:
                pages = pages.split('--')
                initial_page = pages[0]
                if len(pages) > 1:
                    final_page = pages[1]
            place = None

            result.update({
                'tipo': COM_CON,
                'pagina_inicio': initial_page,
                'pagina_fin': final_page,
                'editorial': publisher,
                'congreso': organization,
                'lugar': place
            })

        driver.back()
        driver.back()

        url = None

        # Obtener la url
        try:
            url = driver.find_element_by_xpath(
            '/html/body/div/div[10]/div[2]/div[2]/div[2]/div[4]/div/h3/a')
            
            result.update({'url': url.get_attribute('href')})
        except:
            pass
        if url == None :
            try:
                url = driver.find_element_by_xpath(
                '/html/body/div/div[10]/div[2]/div[2]/div[2]/div[4]/div[2]/h3/a')

                result.update({'url': url.get_attribute('href')})
            except:
                pass
        return {
            key: result
        }

    # Metodo para transformar el tipo de google scholar en nuestro propio tipo
    def google_scholar_type_to_type(self,type):
        if type == GOOGLE_SCHOLAR_LIBRO:
            return LIBRO
        if type == GOOGLE_SCHOLAR_ARTICULO:
            return ARTICULO
        if type == GOOGLE_SCHOLAR_COM_CON:
            return COM_CON
        raise Exception("GoogleScholar error: google_scholar_type_to_type tipo inexistente")

    # Metodo para arreglar los acentos
    def fix_string_without_accent(self, string):
        if string == None:
            return None
        index = string.find('{\\')
        while index != -1:
            charIndex = 0

            if string[index + 3] == '\\':
                charIndex = 4
            else:
                charIndex = 3

            char = string[index + charIndex]
            pre = string[0:index]
            post = string[index + charIndex + 2: len(string)]
            string = pre + char + post
            index = string.find('{\\\'')
        return string

# Metodo main para realizar pruebas
def main():
    selenium = Selenium()
    
    result = selenium.search(
        2000, 2020, '', [ARTICULO, LIBRO, COM_CON])

    with open('static/google_scholar.json', 'w') as json_file:
        json.dump(result, json_file)
    json_file.close()


if __name__ == '__main__':
    main()
