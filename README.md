# Osu-Recovery
Programa para la descarga o recuperación de todas la canciones jugadas de OSU de un perfil determinado.

Este programa usa Python3 con el paquete Selenium.

## Requerimientos
Este programa puede ser ejecutado tanto en Linux como en Windows.
Se requiere tener:
- Python 3
- Paquete Selenium

Para tener la instalación de estos requerimientos se puede realizar de la siguiente forma.
### **Linux**
1. #### **Python 3**
Actualmente linux viene instalado con Python 3, puede verificar la versión que está usando con el siguiente comando.
~~~
$ python3 --version
~~~
Si no cuenta con Python 3 puede revisar la documentación para la instalación en : <https://docs.python-guide.org/starting/install3/linux/>

2. #### **Selenium**
Para obtener el paquete Selenium en Linux se usará la herramienta PIP que viene instalada con Python en las ultimas versiones.

En caso no cuente con PIP puede revisar el siguiente enlace para la instalación con Python 3 : <https://tecnonucleous.com/2018/01/28/como-instalar-pip-para-python-en-windows-mac-y-linux/>

La instalación de Selenium se puede realizar con el siguiente comando.
~~~
$ pip install selenium
~~~

### **Windows**
#### **Python 3**
Para la instalación de Python 3 en Windows, se puede realizar descargandolo desde su web oficial : <https://www.python.org/downloads/>

Al iniciar la instalación deberá marcar la casilla "Add Python3 to PATH"

## Instrucciones de uso
Para el uso del programa de debe abrir una terminal y dirigirse a la carpeta "Osu-Recovery".

El programa requiere que el inicio de sesión para la descarga adecuada de mapas.

~~~
usage: extraccion_mapas.py [-h] [-u USER] [-p PASSWORD]
options arguments:
-h, --help                              show this help message and exit.
-u USER, --user USER                    Name of user.
-p PASSWORD, --password PASSWORD        Password of account.
-n, --novideo                           This options downloads maps only without video.
-ou, OTHERUSER, --otheruser OTHERUSER   This option allows you to download maps from other users.
~~~

### Ejemplo de uso:
---
#### Linux:

~~~
python3 osu-recovery.py -u "Fulanito" -p "Fulanito123"
python3 osur-recovery.py -u "Fulanito" -p "Fulanito123" -n -ou "https://osu.ppy.sh/users/7562902" 
~~~