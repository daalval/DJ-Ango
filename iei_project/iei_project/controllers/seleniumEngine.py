from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class Selenium(object):
    def search(self,autor):
        driver = webdriver.Chrome("iei_project/controllers/chromedriver.exe")
        driver.get("https://scholar.google.es/#d=gs_asd")
        autorElement = driver.find_element_by_id("gs_asd_sau")
        autorElement.send_keys(autor)
        autorElement.send_keys(Keys.RETURN)
        listElements = driver.find_elements_by_class_name("gs_or_cit.gs_nph")

        print(len(listElements))


        listElements[0].click()
        bib = WebDriverWait(driver,10).until(lambda driver: driver.find_elements_by_class_name("gs_citi"))
        bib[0].click()
        text = driver.find_element_by_tag_name('pre').get_attribute('innerText')
        print(text)
        driver.back()
        driver.back()

        listElements = driver.find_elements_by_class_name("gs_or_cit.gs_nph")


        listElements[1].click()
        bib = WebDriverWait(driver,10).until(lambda driver: driver.find_elements_by_class_name("gs_citi"))
        bib[0].click()
        text = driver.find_element_by_tag_name('pre').get_attribute('innerText')
        print(text)
        driver.back()
        driver.back()

        listElements = driver.find_elements_by_class_name("gs_or_cit.gs_nph")


        listElements[2].click()
        bib = WebDriverWait(driver,10).until(lambda driver: driver.find_elements_by_class_name("gs_citi"))
        bib[0].click()
        text = driver.find_element_by_tag_name('pre').get_attribute('innerText')
        print(text)
        driver.back()
        driver.back()

        listElements = driver.find_elements_by_class_name("gs_or_cit.gs_nph")


        listElements[3].click()
        bib = WebDriverWait(driver,10).until(lambda driver: driver.find_elements_by_class_name("gs_citi"))
        bib[0].click()
        text = driver.find_element_by_tag_name('pre').get_attribute('innerText')
        print(text)
        driver.back()
        driver.back()

        listElements = driver.find_elements_by_class_name("gs_or_cit.gs_nph")


        listElements[4].click()
        bib = WebDriverWait(driver,10).until(lambda driver: driver.find_elements_by_class_name("gs_citi"))
        bib[0].click()
        text = driver.find_element_by_tag_name('pre').get_attribute('innerText')
        print(text)
        driver.back()
        driver.back()

        listElements = driver.find_elements_by_class_name("gs_or_cit.gs_nph")


        listElements[5].click()
        bib = WebDriverWait(driver,10).until(lambda driver: driver.find_elements_by_class_name("gs_citi"))
        bib[0].click()
        text = driver.find_element_by_tag_name('pre').get_attribute('innerText')
        print(text)
        driver.back()
        driver.back()

        listElements = driver.find_elements_by_class_name("gs_or_cit.gs_nph")


        listElements[6].click()
        bib = WebDriverWait(driver,10).until(lambda driver: driver.find_elements_by_class_name("gs_citi"))
        bib[0].click()
        text = driver.find_element_by_tag_name('pre').get_attribute('innerText')
        print(text)
        driver.back()
        driver.back()

        listElements = driver.find_elements_by_class_name("gs_or_cit.gs_nph")


        listElements[7].click()
        bib = WebDriverWait(driver,10).until(lambda driver: driver.find_elements_by_class_name("gs_citi"))
        bib[0].click()
        text = driver.find_element_by_tag_name('pre').get_attribute('innerText')
        print(text)
        driver.back()
        driver.back()

        listElements = driver.find_elements_by_class_name("gs_or_cit.gs_nph")


        listElements[8].click()
        bib = WebDriverWait(driver,10).until(lambda driver: driver.find_elements_by_class_name("gs_citi"))
        bib[0].click()
        text = driver.find_element_by_tag_name('pre').get_attribute('innerText')
        print(text)
        driver.back()
        driver.back()

        listElements = driver.find_elements_by_class_name("gs_or_cit.gs_nph")


        listElements[9].click()
        bib = WebDriverWait(driver,10).until(lambda driver: driver.find_elements_by_class_name("gs_citi"))
        bib[0].click()
        text = driver.find_element_by_tag_name('pre').get_attribute('innerText')
        print(text)
        driver.back()
        driver.back()

def main():
    selenium = Selenium()
    selenium.search('García Márquez')
    

if __name__ == "__main__":
    main()