from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located
from selenium.webdriver.chrome.service import Service
import time
import requests
import urllib3
import argparse
import os



urllib3.disable_warnings()
# Obteniendo parámetros
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--user", help="Name of user.")
parser.add_argument("-p", "--password", help="Password of acount.")
parser.add_argument("-wv", "--withvideo", help="This option downloads maps with video only in case the map has.", action="store_true")
parser.add_argument("-ou", "--otheruser", help="This option allows you to download maps from other users.")
parser.add_argument("-pt", "--part", help="This indicate the part of your list maps gonna be download, 0=[0-99], 1=[100-199], ...")
args = parser.parse_args()

# Definiendo opciones básica al selenium
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

# Inicializando driver de chrome
ruta_driver = './chromedriver.exe'
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

    button_login = driver.find_element(By.XPATH,'//button[@class="btn-osu-big btn-osu-big--nav-popup js-captcha--submit-button"]')
    button_login.click()

    time.sleep(2)
    
    print("Inicio de Sesión Completo [!1]")
    time.sleep(1.5)
    if args.otheruser :
        url_perfil = args.otheruser
    else:
        url_perfil = driver.find_element(By.XPATH,'//a[@data-click-menu-target="nav2-user-popup"]').get_attribute("href")
    
    print("Perfil : " + url_perfil)
    
    if not(os.path.exists('./mapas.txt')):
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
        print("Cantidad de mapas totales: "+ str(contador) +" [!2]")
    else:
        with open("mapas.txt") as lista_mapas:
            contador = 0
            for line in lista_mapas:
                contador = contador +1
        print("Cantidad de mapas totales: "+ str(contador) +" [!2]") 

    # Obteniendo los headers necesarios para obtener el link de descarga real
    headers_pre = driver.get_cookies()
    parts = str(headers_pre[0]).rstrip("\n").split(",")
    cookie_pre = parts[6].rstrip("\n").split("'")
    cookie = cookie_pre[3]
    parts2 = str(headers_pre[1]).rstrip("\n").split(",")
    token_pre = parts2[6].rstrip("\n").split("'")
    token = token_pre[3]


    # Descargando los mapas
    linea_actual_absoluta = 0
    linea_actual_relativa = 0
    inicio = int(args.part)*100
    final = (int(args.part)*100)+99
    print("Rango de Descarga: "+ str(inicio)+ " - "+ str(final)+" [!3]")

    with open("mapas.txt") as lista_mapas:
        for line in lista_mapas:
            linea_actual_absoluta = linea_actual_absoluta +1 
            if(linea_actual_absoluta >= inicio and linea_actual_absoluta<=final):
                parts3 = line.rstrip("\n").split("/")
                codigo = parts3[4]
                link = line.rstrip("\n")
                cookies = {
                'XSRF-TOKEN': token,
                'osu_session': cookie,
                }
                headers = {
                    'Host': 'osu.ppy.sh',
                    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0',
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
                if args.withvideo: 
                    response = requests.get(link, headers=headers, cookies=cookies, verify=False)
                    time.sleep(1)
                else: 
                    response = requests.get(link, headers=headers, cookies=cookies, params=params, verify=False)
                    time.sleep(1)
                ruta = './canciones/' + codigo + '.osz'
                open(ruta, 'wb').write(response.content)
                linea_actual_relativa = linea_actual_relativa + 1
                if (linea_actual_relativa % 10 == 0):
                    print( "Porcentaje: " + str(linea_actual_relativa)+ "%")
            else:
                pass
    driver.close()


    
    
 


