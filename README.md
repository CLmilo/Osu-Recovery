# Osu-Recovery
Programa en python para recuperar todas la canciones jugadas de OSU de un perfil determinado.

Este programa usa Python3 con el paquete Selenium.



## Instrucciones de uso

El programa requiere que el inicio de sesión para la descarga adecuada de mapas.

~~~
usage: extraccion_mapas.py [-h] [-u USER] [-p PASSWORD]
options arguments:
-h, --help                          show this help message and exit
-u USER, --user USER                Name of user
-p PASSWORD, --password PASSWORD    Password of account
~~~

### Ejemplo de uso:
---
#### Linux:

~~~
python3 extraccion_mapas.py -u "Fulanito" -p "Fulanito123"
~~~