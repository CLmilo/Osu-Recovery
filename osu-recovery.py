from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
import time
import requests
import urllib3
import argparse

urllib3.disable_warnings()
ua = UserAgent(use_cache_server=False)
# Obteniendo parámetros
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--user", help="Name of user")
parser.add_argument("-p", "--password", help="Password of acount")
parser.add_argument("-n", "--novideo", help="This options download maps only without video", action="store_true")
args = parser.parse_args()

# Definiendo opciones básica al selenium
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

# Inicializando driver de chrome
ruta_driver = './chromedriver'
s=Service(ruta_driver)
webdriver = webdriver.Chrome(service=s, options=options)

url_home = "https://osu.ppy.sh/home"

with webdriver as driver:
    wait = WebDriverWait(driver, 10)
    driver.get(url_home)

    # Proceso para evitar la detección de scrapping
    button_login = driver.find_element(By.XPATH, '//a[@class="landing-nav__link js-nav-toggle js-click-menu js-user-login--menu"]')
    button_login.click()

    time.sleep(0.5)

    #Login a la cuenta
    username_field = driver.find_element(By.XPATH,'//input[@name="username"]')
    password_field = driver.find_element(By.XPATH,'//input[@name="password"]')

    username_field.clear()
    username_field.send_keys(args.user)
    password_field.clear()
    password_field.send_keys(args.password)

    button_login = driver.find_element(By.XPATH,'//button[@data-disable-with="Iniciando sesión..."]')
    button_login.click()

    time.sleep(2)
    
    print("Inicio de Sesión Completo [!1]")
    time.sleep(1.5)
    url_perfil = driver.find_element(By.XPATH,'//a[@data-click-menu-target="nav2-user-popup"]').get_attribute("href")
    print("Perfil : " + url_perfil)
    wait = WebDriverWait(driver, 10) 
    driver.get(url_perfil)

    wait.until(presence_of_all_elements_located,((By.CLASS_NAME, "page-extra")))
    time.sleep(2)
    # Obteniendo cantidad de veces de clickeos necesarios
    cantidad_xml = driver.find_element(By.XPATH,'//div[@class="page-extra"]/h3[2]/span')
    cantidad = int(cantidad_xml.text)
    cantidad = (cantidad - 5)/50
    cantidad = int(cantidad)

    
    # Obteniendo el total de mapas en la página
    button = driver.find_element(By.XPATH,'//div[@class="page-extra"]/button')

    for i in range(cantidad+1):
        button.click()
        time.sleep(2)
        if i == (cantidad):
            pass
        else:
            button = driver.find_element(By.XPATH,'//div[@class="page-extra"]/button')

    # Obteniendo el la data en bruto con el id del mapa
    f = open("data.txt", "w")

    mapas = driver.find_elements(By.XPATH,'//div[@class="beatmap-playcount"]/a')
    for mapa in mapas:
        link = mapa.get_attribute("style")
        print(link, file=f)
    f.close()
    # Quitando las repeticiones y filtrando el id del mapa
    lista_mapas=[]
    with open("data.txt") as data:
        for line in data:
            try:
                parts = line.rstrip("\n").split("/")
                lista_mapas.append(parts[4])
            except:
                pass
    arreglo_ordenado = set(lista_mapas)
    lista_ordenada = list(arreglo_ordenado)

    # Generando el link sin repeticiones
    f = open("mapas.txt", "w")
    contador = 0
    for line in lista_ordenada:
        link = "https://osu.ppy.sh/beatmapsets/"+line+"/download"
        contador = contador +1 
        print(link, file=f)   
    f.close()
    print("Cantidad de mapas a descargar : "+ str(contador) +" [!2]")

    # Obteniendo los headers necesarios para obtener el link de descarga real
    headers_pre = driver.get_cookies()
    parts = str(headers_pre[0]).rstrip("\n").split(",")
    cookie_pre = parts[6].rstrip("\n").split("'")
    cookie = cookie_pre[3]
    parts2 = str(headers_pre[1]).rstrip("\n").split(",")
    token_pre = parts2[6].rstrip("\n").split("'")
    token = token_pre[3]


    # Descargando los mapas
    contador2 = 0
    with open("mapas.txt") as lista_mapas:
        for line in lista_mapas:
            parts3 = line.rstrip("\n").split("/")
            codigo = parts3[4]
            link = line.rstrip("\n")
            cookies = {
            'XSRF-TOKEN': token,
            'osu_session': cookie,
            }
            headers = {
                'Host': 'osu.ppy.sh',
                'User-Agent': ua.opera,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate',
                'Referer': link,
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-User': '?1',
                'Te': 'trailers',
            }
            params = (
                ('noVideo', '1'),
            )
            if args.novideo: 
                response = requests.get(link, headers=headers, cookies=cookies, params=params, verify=False)
                time.sleep(5)
            else: 
                response = requests.get(link, headers=headers, cookies=cookies, verify=False)
                time.sleep(5)
            ruta = './canciones/' + codigo + '.osz'
            open(ruta, 'wb').write(response.content)
            contador2 = contador2 + 1
            porcentaje = (contador2/contador)*100
            if (porcentaje > 10 and porcentaje < 10.3):
                print("Porcentaje descargado : "+ str(int(porcentaje))+ "%")
            if (porcentaje > 20 and porcentaje < 20.3):
                print("Porcentaje descargado : "+ str(int(porcentaje))+ "%")
            if (porcentaje > 30 and porcentaje < 30.3):
                print("Porcentaje descargado : "+ str(int(porcentaje))+ "%")
            if (porcentaje > 40 and porcentaje < 40.3):
                print("Porcentaje descargado : "+ str(int(porcentaje))+ "%")
            if (porcentaje > 50 and porcentaje < 50.3):
                print("Porcentaje descargado : "+ str(int(porcentaje))+ "%")
            if (porcentaje > 60 and porcentaje < 60.3):
                print("Porcentaje descargado : "+ str(int(porcentaje))+ "%")
            if (porcentaje > 70 and porcentaje < 70.3):
                print("Porcentaje descargado : "+ str(int(porcentaje))+ "%")
            if (porcentaje > 80 and porcentaje < 80.3):
                print("Porcentaje descargado : "+ str(int(porcentaje))+ "%")
            if (porcentaje > 90 and porcentaje < 90.3):
                print("Porcentaje descargado : "+ str(int(porcentaje))+ "%")
            if (porcentaje == 100):
                print("Porcentaje descargado : "+ str(int(porcentaje))+ "%")
    driver.close()


    
    
 


