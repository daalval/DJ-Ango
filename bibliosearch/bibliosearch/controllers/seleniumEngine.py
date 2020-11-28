
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pybtex.database import parse_string

ARTICLE = 'article'
BOOK = 'book'
INPROCEEDINGS = 'inproceedings'


class Selenium(object):
    def search(self, fecha_inicial, fecha_final, autor, tipos):
        result = {}
        try:
            driver = webdriver.Chrome(
                'bibliosearch/controllers/chromedriver.exe')
            driver.get('https://scholar.google.es/#d=gs_asd')
            author_element = WebDriverWait(driver, 10).until(
                lambda driver: driver.find_element_by_id('gs_asd_sau'))
            author_element.send_keys(autor)
            fecha_inicial_element = WebDriverWait(driver, 10).until(
                lambda driver: driver.find_element_by_id('gs_asd_ylo'))
            fecha_inicial_element.send_keys(fecha_inicial)
            fecha_final_element = driver.find_element_by_id('gs_asd_yhi')
            fecha_final_element.send_keys(fecha_final)
            fecha_final_element.send_keys(Keys.RETURN)

            listElements = driver.find_elements_by_class_name(
                'gs_or_cit.gs_nph')

            if len(listElements) == 0:
                return result

            index = 0

            while(index < len(listElements)):
                result.update(self.extract_element(
                    listElements[index], driver, tipos))
                index = index + 1
                listElements = WebDriverWait(driver, 10).until(
                    lambda driver: driver.find_elements_by_class_name('gs_or_cit.gs_nph'))

            mas_paginas = driver.find_element_by_xpath(
                '/html/body/div/div[9]/div[3]/div').get_attribute('innerText')

            if mas_paginas[0] == 'P':
                next_page = driver.find_element_by_xpath(
                    '//*[@id="gs_nm"]/button[2]')

                while next_page.is_enabled():
                    next_page.click()
                    listElements = WebDriverWait(driver, 10).until(
                        lambda driver: driver.find_elements_by_class_name('gs_or_cit.gs_nph'))
                    index = 0
                    while(index < len(listElements)):
                        result.update(self.extract_element(
                            listElements[index], driver, tipos))
                        index = index + 1
                        listElements = WebDriverWait(driver, 10).until(
                            lambda driver: driver.find_elements_by_class_name('gs_or_cit.gs_nph'))
                    next_page = driver.find_element_by_xpath(
                        '//*[@id="gs_nm"]/button[2]')

        except Exception as e:
            print(e)
            return result

        return result

    def search_only_first_element(self, fecha_inicial, fecha_final, tipos):
        result = {}
        try:
            driver = webdriver.Chrome(
                'bibliosearch/controllers/chromedriver.exe')
            driver.get('https://scholar.google.es/#d=gs_asd')
            fecha_inicial_element = WebDriverWait(driver, 10).until(
                lambda driver: driver.find_element_by_id('gs_asd_ylo'))
            fecha_inicial_element.send_keys(fecha_inicial)
            fecha_final_element = driver.find_element_by_id('gs_asd_yhi')
            fecha_final_element.send_keys(fecha_final)
            fecha_final_element.send_keys(Keys.RETURN)

            listElements = driver.find_elements_by_class_name(
                'gs_or_cit.gs_nph')

            if len(listElements) == 0:
                return result

            result.update(self.extract_element(
                listElements[0], driver, tipos))

            mas_paginas = driver.find_element_by_xpath(
                '/html/body/div/div[9]/div[3]/div').get_attribute('innerText')

            print(mas_paginas)

            if mas_paginas[0] == 'P' or mas_paginas[0] == 'A':
                next_page = driver.find_element_by_xpath(
                    '//*[@id="gs_nm"]/button[2]')

                while next_page.is_enabled():
                    next_page.click()
                    listElements = WebDriverWait(driver, 10).until(
                        lambda driver: driver.find_elements_by_class_name('gs_or_cit.gs_nph'))
                    result.update(self.extract_element(
                        listElements[0], driver, tipos))
                    next_page = driver.find_element_by_xpath(
                        '//*[@id="gs_nm"]/button[2]')

        except Exception as e:
            print(e)
            return result

        return result

    def extract_element(self, element, driver, tipos):
        element.click()
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'gs_citi'))).click()
        text = driver.find_element_by_tag_name(
            'pre').get_attribute('innerText')

        data = parse_string(text, 'bibtex')

        entry = list(data.entries.values())[0]

        type = entry.type

        key = entry.key

        if type not in tipos:
            driver.back()
            driver.back()
            return {}

        fields = entry.fields
        title = self.fix_string_without_accent(fields.get('title'))

        authors = entry.persons.get('author')
        year = fields.get('year')
        publisher = self.fix_string_without_accent(fields.get(
            'publisher')) or self.fix_string_without_accent(fields.get('journal'))

        personas = []

        for author in authors:
            persona = {'nombre': author.first_names,
                       'apellidos': author.middle_names + author.last_names,
                       }
            personas.append(persona)

        result = {

            'ano': year,
            'escrita_por': personas,
            'titulo': title,
        }

        # --------------------------------------------ARTICULOS------------------------------------------
        if type == 'article':

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
                'tipo': 'articulo',
                'pagina_inicio': initial_page,
                'pagina_final': final_page,
                'publicado_en': publicado_en
            })
        # --------------------------------------------LIBROS------------------------------------------
        if type == 'book':
            pages = fields.get('pages')
            result.update({
                'tipo': 'libro',
                'paginas': pages,
                'editorial': publisher
            })

        # --------------------------------------------COMUNICACION-CONGRESO------------------------------------------
        if type == INPROCEEDINGS:
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
                'tipo': 'con_con',
                'pagina_inicio': initial_page,
                'pagina_final': final_page,
                'editorial': publisher,
                'congreso': organization,
                'lugar': place
            })

        driver.back()
        driver.back()

        url = None

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


def main():
    selenium = Selenium()
    result = selenium.search(
        '1000', '1500', '', [ARTICLE, BOOK, INPROCEEDINGS])

    with open('results/google_schoolar.json', 'w') as json_file:
        json.dump(result, json_file)
    json_file.close()


if __name__ == '__main__':
    main()
