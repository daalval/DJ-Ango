from logging import setLogRecordFactory
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


class Selenium(object):
    def search(self, fecha_inicial, fecha_final):
        profile = webdriver.FirefoxProfile(
            'C:/Users/Dani/AppData/Roaming/Mozilla/Firefox/Profiles/s6ttqby6.default-release')

        PROXY_HOST = "12.12.12.123"
        PROXY_PORT = "1234"
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", PROXY_HOST)
        profile.set_preference("network.proxy.http_port", int(PROXY_PORT))
        profile.set_preference("dom.webdriver.enabled", False)
        profile.set_preference('useAutomationExtension', False)
        profile.update_preferences()
        desired = webdriver.DesiredCapabilities.FIREFOX
        driver = webdriver.Firefox(executable_path=r"iei_project/controllers/geckodriver.exe",
                                   firefox_profile=profile, desired_capabilities=desired)
        # driver = webdriver.Chrome('iei_project/controllers/chromedriver.exe')
        driver.get("https://scholar.google.es/#d=gs_asd")
        fecha_inicial_element = driver.find_element_by_id("gs_asd_ylo")
        fecha_inicial_element.send_keys(fecha_inicial)
        fecha_final_element = driver.find_element_by_id("gs_asd_yhi")
        fecha_final_element.send_keys(fecha_final)
        fecha_final_element.send_keys(Keys.RETURN)

        listElements = driver.find_elements_by_class_name("gs_or_cit.gs_nph")

        if len(listElements) == 0:
            return []

        index = 0
        while(index < len(listElements)):
            self.extract_element(listElements[index], driver)
            index = index + 1
            listElements = WebDriverWait(driver, 10).until(
                lambda driver: driver.find_elements_by_class_name("gs_or_cit.gs_nph"))

        if len(listElements) == 10:
            next_page = driver.find_element_by_xpath(
                '//*[@id="gs_nm"]/button[2]')
            while next_page.is_enabled():
                next_page.click()

                listElements = WebDriverWait(driver, 10).until(
                    lambda driver: driver.find_elements_by_class_name("gs_or_cit.gs_nph"))

                index = 0
                while(index < len(listElements)):
                    self.extract_element(listElements[index], driver)
                    index = index + 1
                    listElements = WebDriverWait(driver, 10).until(
                        lambda driver: driver.find_elements_by_class_name("gs_or_cit.gs_nph"))

    def extract_element(self, element, driver):
        element.click()
        # bib = WebDriverWait(driver, 10).until(
        #     lambda driver: driver.find_elements_by_class_name("gs_citi"))
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "gs_citi"))).click()
        text = driver.find_element_by_tag_name(
            'pre').get_attribute('innerText')
        print(text)
        driver.back()
        driver.back()


def main():
    selenium = Selenium()
    selenium.search('1000', '1600')


if __name__ == "__main__":
    main()
