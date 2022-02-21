
# Micro Servo 9g-Raspberry pi 3 model B+

### Simulación de apertura de puerta

Con el servo se simula la cerradura de una puerta que al recibir una señal por medio de MQTT,  cambia su posición dependiendo la instrucción que este recibe:

abierto == true ---> abierto 

abierto == false --> cerrado

## INSTRUCCIONES 
### DIAGRAMA ESQUEMATICO DE CONEXIONES

<img src = "https://github.com/ElierRosales/Capstone-project-Administrador-de-laboratorios/blob/480a784622240541d6610b1a2f70da48cefa3222/Servo%20Motor/imagenes/diagrama%20servo%20.png" width="500">

### CONEXIÓN DEL MOTOR A RASPBERRY

| Pin del servo| Color del cable en el servo | Pin físico Raspberry |
| -- | -- | -- |
| GND | cafe o negro | 9 |
| VCC | rojo | 1 |
| PWM | naranja | 11 |

Nota: Esto podría cambiar dependiendo de tu modelo de Raspberry.

#### Diagrama esquematico de conexiones 

<img src =  width="500">

### INSTALACIÓN DE BIBLIOTECAS Y MODULOS QUE SE UTILIZAN
* Abrimos la terminal y revisamos si tenemos y que versión de Python tenemos instalado con :

  `python --version`

   en caso de no tenerlo instalado, podemos instalarlo con:
 
  `sudo apt-get install python3`

* Revisamos si tenemos las ultimas actualizaciones disponibles, para esto colocamos lo siguiente:

  `sudo apt update && sudo apt upgrade`

* Instalamos el modulo paho de Python que es el que nos permitirá realizar la conexión MQTT:

  `pip3 install paho-mqtt` 
      
  en caso de que no lo permita, usamos `sudo` antes de la instrucción.
  
* El servo recibe una instrucción por medio de MQTT la cual decidira la posición del mismo 
  
* Ahora vamos a probar un código, escribimos lo siguiente en la terminal:

   `cd Documents` 

 `git clone https://github.com/ElierRosales/Capstone-project-Administrador-de-laboratorios.git`
 
  entramos en la carpeta PN532 la cual encontraremos dentro de nuestra carpeta Documents, abrimos el archivo UIDporMQTT.py
  con Thony Python IDE y damos en el botón Run.
  Ahora pasamos un tag NFC y en consola se imprimirá el UID de tu tag.
