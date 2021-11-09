from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located
import time


url = "https://osu.ppy.sh/users/21461538"

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

ruta_driver = './chromedriver'
webdriver = webdriver.Chrome(executable_path=ruta_driver, options=options)

with webdriver as driver:
    wait = WebDriverWait(driver, 10) 
    driver.get(url)

    wait.until(presence_of_all_elements_located,((By.CLASS_NAME, "page-extra")))

    # Obteniendo cantidad de veces de clickeos necesarios
    cantidad_xml = driver.find_element_by_xpath('//div[@class="page-extra"]/h3[2]/span')
    cantidad = int(cantidad_xml.text)
    cantidad = (cantidad - 5)/50
    cantidad = int(cantidad)

    # Obteniendo el total de mapas en la página
    button = driver.find_element_by_xpath('//div[@class="page-extra"]/button')

    for i in range(cantidad):
        button.click()
        time.sleep(2)
        button = driver.find_element_by_xpath('//div[@class="page-extra"]/button')

    # Obteniendo los links del arreglo de mapas
    mapas = driver.find_elements_by_xpath('//div[@class="beatmap-playcount"]/a')
    for mapa in mapas:
        link = mapa.get_attribute("href")
        print(link)
    driver.close()
 


