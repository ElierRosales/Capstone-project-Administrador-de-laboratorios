# Mongo DB-Samsung Innovation Campus
Para la realizacion de nuestro proyecto capstone, utilizaremos MongoDB como principal gestor de bases de datos.

![mongo](imagenes/mongo.png)

Ademas de utilizar python como lenguaje de programacion para manipular MongoDB mediante Pymongo.

![pymongo](imagenes/pymongo.png)
## Instalar Pymongo
PyMongo es un modulo de Python que nos ayudara a crear, administrar y manipular una base de datos hospedada en MongoDB.

La forma mas sencilla de instalar Pymongo es mediante pip, recordemos que la forma de utilizar pip cambia de distribucion a distribucion, en ubuntu/debian tenemos dos maneras.

Para pip en Python 3:

`pip3 install pymongo`

Para pip en Python 2(deprecated):

`pip install pymongo`

Para mas informacion sobre el uso de este modulo y mas opciones de instalacion visitar el siguiente enlace:  [pymongo](https://pymongo.readthedocs.io/en/stable/installation.html)
## Instalar PahoMQTT
Paho es un modulo de Python que nos ayudara a el manejo de conexiones MQTT, tanto el envio de mensajes por este medio asi como de la recepcion de los mismos.

De la misma manera podemos instalar PahoMQTT mediante pip, y aplican las mismas instrucciones mencionadas para la instalacion de Pymongo.

Para pip en Python 3:

`pip3 install paho-mqtt`

para pip en Python2(deprecated):

`pip install paho-mqtt`

Para mas informacion sobre el uso de este modulo y mas opciones de instalacion visitar el siguiente enlace: [paho-mqtt](https://github.com/eclipse/paho.mqtt.python)

## Conflictos entre MongoDB(RASPBERRY) y PyMongo.
Desgraciadamente la version de MongoDB que se encuentra en los repositorios de la raspberry es demasiado vieja, lo cual la hace incompatible con Pymongo, por lo tanto es necesario que instales una version de MongoDB actualizada o corras MongoDB en una maquina externa.

## Instalar MongoDB en Ubuntu 20.04
Los repositorios oficiales de Ubuntu incluyen una versión estable de MongoDB. Sin embargo, la versión de MongoDB disponible en los repositorios predeterminados de Ubuntu es la 3.6, mientras que la última versión estable y compatible con PyMongo es la 4.4.

Para obtener la versión más reciente de este software, debe incluir el repositorio dedicado de MongoDB en nuestros repositorios.

Para comenzar, importamos la clave GPG pública para la última versión estable de MongoDB ejecutando el siguiente comando. Si tienes la intención de usar una versión de MongoDB que no sea la 4.4, asegúrate de cambiar 4.4 en la parte de la URL de este comando para alinearla con la versión que desea instalar:

`curl -fsSL https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -`

Posteriormente ingresamos el siguiente comando para agregar el repositorio a nuestra lista de repositorios de nuestro administrador de paquetes.

`echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list`

Despues actualizamos nustra lista de repositorios con el siguiente comando:

`sudo apt-get update` ó `sudo apt update`

Ahora solo queda instalar el paquete con el siguiente comando:

`sudo apt-get install mongodb-org`
## Iniciando el servicio mongod.service

Asumiendo que usas Ubuntu 20.04 sin ninguna modificación en el sistema init, tenemos dos alternativas.
- `sudo systemctl start mongod.service`
  
  Este comando iniciará el servicio en ese momento, pero tendrás que iniciarlo nuevamente después de cada reinicio de manera manual. 
- `sudo systemctl enable --now mongod.service` 
  
  Este comando iniciará el servicio en este momento, además de habilitar el inicio automático en cada inicio de sesión, por lo tanto no tendrás que iniciarlo manualmente después de cada reinicio.
  
  En mi opinión es la manera ideal, pero tener muchos servicios iniciandose cada inicio de sesión puede alentar el tiempo de inicio.
## Descripcion de los programas en este repositorio.
Los programas principales utilizados en el proyecto capstone son:
- buscarUID.py
  
  Este script lee el mensaje recibido mediante mqtt en el tema "isur/uid" para buscarlo en la base de datos, imprimir y enviar los datos del usuario al que pertenece tal UID y ademas registrar la hora de salida/entrada.
- RegistroBaseDatos.py
  
  Este script requiere de intervencion manual, ya que al igual que el script mencionado anteriormente, lee el uid recibido en el tema ya antes mencionado, una vez leido nos pedira los datos del usuario para registrarlos en la base de datos.


