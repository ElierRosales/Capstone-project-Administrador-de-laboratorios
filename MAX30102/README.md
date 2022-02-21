# **LECTOR DE SINTOMAS COVID EN ESP32CAM-AITHINKER**
## **Descripción**
Este programa realiza una medición de signos vitales (Pulso cardiaco/Oxigenación), para posteriormente enviar los valores mediante MQTT a un tema monitoreado en Node-Red.
## **Materiales**
- ESP32-CAM
- MAX3010x (en este caso Max30102)
- FTDI/Modulo programador
- Conexión WiFi a internet o a una Red Local.
- Broker MQTT (Público o Privado)
## **Instrucciones** ##
## **CONEXIONES EN HARDWARE** ##
### Primero tenemos que asegurarnos de realizar las conexiones del circuito correctamente, como se muestra a continuación:
  - 5V = 5V (3.3V también funciona)
  - GND = GND
  - SDA = GPIO15
  - SCL = GPIO14
  - INT = No se conecta.
  - LED ROJO = GPIO12
  - LED AZUL = GPIO13
  - LED VERDE = GPIO2
### RECORDEMOS QUE LOS COLORES SON INDIFERENTES.
Siguiendo el siguiente de mapeo de pines:
- ESP32CAM/AI-THINKER![ESP32CAM](../../SintomasCovid/sintomasCOVID/imagenes/esp32cam_pinout.png)
- MAX30102

![max3012](../../SintomasCovid/sintomasCOVID/imagenes/max30102_pinout.jpg)
## FTDI 
Para poder programar nuestro ESP32CAM se necesita un modulo programador, en este caso se utilizó un FTDI con las siguientes conexiones para subir el código:

- Modulo programador FTDI

![FTDI](../../SintomasCovid/sintomasCOVID/imagenes/programar.png)
## SOFTWARE NECESARIO ##
Se utilizó arduino IDE para el manejo de bibliotecas y la edición del código fuente.

Arduino IDE está disponible para Windows/Linux y MacOS en el siguiente enlace:
- https://www.arduino.cc/en/software

## Instalación del soporte para ESP32CAM en Arduino IDE. ##
- Abrir el Arduino IDE, hacer click en File > Preferences ![preferencias](../../SintomasCovid/sintomasCOVID/imagenes/arduino-ide-open-preferences.png)
- Ingresa la siguiente URL `https://dl.espressif.com/dl/package_esp32_index.json` en el campo llamado "Aditional Board Manager URLs mostrado abajo. Despúes presiona OK.![CAMPO_TEXTO](../../SintomasCovid/sintomasCOVID/imagenes/board.png)
- Abrir el administrador de tarjetas o Board Manager. ![BOARD_MANAGER](../../SintomasCovid/sintomasCOVID/imagenes/a2boardmanager.png)
- Dentro del board manager buscar 'ESP32' y presionar "Install" en la opción "ESP32 by Espresif Systems".![INSTALAR](../../SintomasCovid/sintomasCOVID/imagenes/install.png)
## Comprobar la instalación ##
- Selecciona tu tarjeta en Tools > Board, en mi caso AI-THINKER ESP32-CAM. ![ESP32CAM](../../SintomasCovid/sintomasCOVID/imagenes/Screenshot_20220203_161506.png)
- Si no aparece este modelo, es probable que no hayas instalado el soporte de manera correcta, debes reintentarlo.
## Instalar biblioteca necesaria para el manejo del MAX3015
- Abrir el administrador de bibliotecas del Arduino IDE, Tools > Manage Libraries. ![admin_lib](../../SintomasCovid/sintomasCOVID/imagenes/librerias.png)
- En el buscador de librerias, buscar "MAX30105" e instalar la siguiente: ![sparkfun](../../SintomasCovid/sintomasCOVID/imagenes/sparkfun.png)
## Instalar biblioteca para el manejo de funciones MQTT.
- En el mismo administrador de bibliotecas, buscar e instalar la siguiente librería: ![pubsub](../../SintomasCovid/sintomasCOVID/imagenes/pubsubclient.png)
### Ahora solo queda programar el ESP32-CAM con el código de este repositorio.
