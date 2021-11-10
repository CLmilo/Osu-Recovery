from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located
from selenium.webdriver.chrome.service import Service
import time




url = "https://osu.ppy.sh/users/21461538"

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

# Inicializando driver de chrome
ruta_driver = './chromedriver'
s=Service(ruta_driver)
webdriver = webdriver.Chrome(service=s)
#webdriver = webdriver.Chrome(executable_path=ruta_driver, options=options)

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

    for i in range(cantidad+1):
        button.click()
        time.sleep(2)
        if i == (cantidad):
            pass
        else:
            button = driver.find_element_by_xpath('//div[@class="page-extra"]/button')

    # Obteniendo el la data en bruto con el id del mapa
    f = open("data.txt", "w")

    mapas = driver.find_elements_by_xpath('//div[@class="beatmap-playcount"]/a')
    for mapa in mapas:
        link = mapa.get_attribute("style")
        print(link, file=f)
    f.close()
    # Quitando las repeticiones y filtrando el id del mapa
    lista_mapas=[]
    with open("data.txt") as fpin:
        for line in fpin:
            try:
                parts = line.rstrip("\n").split("/")
                lista_mapas.append(parts[4])
            except:
                pass
    arreglo_ordenado = set(lista_mapas)
    lista_ordenada = list(arreglo_ordenado)

    # Generando el link sin repeticiones
    f = open("mapas.txt", "w")

    for line in lista_ordenada:
        link = "https://osu.ppy.sh/beatmapsets/"+line+"/download"
        print(link, file=f)   
    f.close()
    driver.close()
 


