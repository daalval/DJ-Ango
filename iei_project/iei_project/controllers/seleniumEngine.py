from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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

        # bibTeX = driver.find_element_by_id("gs_citi")

        # print(bibTeX)
            
        autorElement.close()

def main():
    selenium = Selenium()
    selenium.search('García Márquez')
    

if __name__ == "__main__":
    main()