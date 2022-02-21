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

## Descripcion de los programas en este repositorio.
Los programas principales utilizados en el proyecto capstone son:
- buscarUID.py
  
  Este script lee el mensaje recibido mediante mqtt en el tema "isur/uid" para buscarlo en la base de datos, imprimir y enviar los datos del usuario al que pertenece tal UID y ademas registrar la hora de salida/entrada.
- RegistroBaseDatos.py
  
  Este script requiere de intervencion manual, ya que al igual que el script mencionado anteriormente, lee el uid recibido en el tema ya antes mencionado, una vez leido nos pedira los datos del usuario para registrarlos en la base de datos.


