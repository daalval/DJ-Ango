
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
    def search(self, fecha_inicial, fecha_final, types):
        driver = webdriver.Chrome('bibliosearch/controllers/chromedriver.exe')
        driver.get("https://scholar.google.es/#d=gs_asd")
        fecha_inicial_element = WebDriverWait(driver, 10).until(
            lambda driver: driver.find_element_by_id("gs_asd_ylo"))
        fecha_inicial_element.send_keys(fecha_inicial)
        fecha_final_element = driver.find_element_by_id("gs_asd_yhi")
        fecha_final_element.send_keys(fecha_final)
        fecha_final_element.send_keys(Keys.RETURN)

        listElements = driver.find_elements_by_class_name("gs_or_cit.gs_nph")

        if len(listElements) == 0:
            return {}

        result = {}

        index = 0

        while(index < len(listElements)):
            result.update(self.extract_element(
                listElements[index], driver, types))
            index = index + 1
            listElements = WebDriverWait(driver, 10).until(
                lambda driver: driver.find_elements_by_class_name("gs_or_cit.gs_nph"))

        try:
            next_page = driver.find_element_by_xpath(
                '//*[@id="gs_nm"]/button[2]')
            next_page.click()

            while next_page.is_enabled():
                listElements = WebDriverWait(driver, 10).until(
                    lambda driver: driver.find_elements_by_class_name("gs_or_cit.gs_nph"))
                index = 0
                while(index < len(listElements)):
                    result.update(self.extract_element(
                        listElements[index], driver, types))
                    index = index + 1
                    listElements = WebDriverWait(driver, 10).until(
                        lambda driver: driver.find_elements_by_class_name("gs_or_cit.gs_nph"))
                next_page = driver.find_element_by_xpath(
                '//*[@id="gs_nm"]/button[2]')
                next_page.click()
        except:
            pass

            

        return result

    def extract_element(self, element, driver, types):
        element.click()
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "gs_citi"))).click()
        text = driver.find_element_by_tag_name(
            'pre').get_attribute('innerText')

        data = parse_string(text, 'bibtex')

        entry = list(data.entries.values())[0]

        type = entry.type

        key = entry.key

        if type not in types:
            driver.back()
            driver.back()
            return {}

        fields = entry.fields
        title = fields.get('title')
        authors = entry.persons.get('author')
        year = fields.get('year')
        publisher = fields.get('publisher') or fields.get('journal')

        personas = []

        for author in authors:
            persona = {'nombre': author.first_names,
                       'apellidos': author.middle_names + author.last_names}
            personas.append(persona)

        result = {

            'ano': year,
            'url': None,
            'escrita_por': personas,
            'titulo': title
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
                final_page = pages[1]
            result.update({
                'tipo': 'articulo',
                'titulo': title,
                'pagina_inicio': initial_page,
                'pagina_final': final_page,
                'publicado_en': publicado_en
            })
        # --------------------------------------------LIBROS------------------------------------------
        if type == 'book':
            pages = fields.get('pages')

            result.update({
                'tipo': 'libro',
                'titulo': title,
                'paginas': pages,
                'editorial': publisher
            })

        # --------------------------------------------COMUNICACION-CONGRESO------------------------------------------
        if type == INPROCEEDINGS:
            initial_page = fields.get('pages')
            final_page = None
            pages = fields.get('pages')
            organization = fields.get('organization')
            volume = fields.get('volume')
            pages = fields.get('pages')
            initial_page = None
            final_page = None
            if pages != None:
                pages = pages.split('--')
                initial_page = pages[0]
                final_page = pages[1]
            place = None

            result.update({
                'tipo': 'con_con',
                'titulo': title,
                'pagina_inicio': initial_page,
                'pagina_final': final_page,
                'editorial': publisher,
                'congreso': organization,
                'edicion': volume,
                'lugar': place
            })

        driver.back()
        driver.back()
        
        url = driver.find_element_by_xpath(f"//*[text()='{title}']").get_attribute('href')
        result.update({'url': url})
        return {
            key: result
        }


def main():
    selenium = Selenium()
    result = selenium.search('1000', '1560', [ARTICLE])

    with open('results/google_schoolar.json', 'w') as json_file:
        json.dump(result, json_file)
    json_file.close()


if __name__ == "__main__":
    main()
