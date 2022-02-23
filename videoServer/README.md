## Descripcion
Este programa realiza videostream continúo y lo incorpora a tu dasbboard en Node Red
## Materiales
- ESP32CAM
- FTDI/Modulo programador
## Software necesario 
Visita el siguiente enlace: [software necesario](https://github.com/JorgeIsur/ESP32CAM-PROJECTS/tree/master/MAX30102/SintomasCovid/sintomasCOVID#software-necesario)
## Instalacion del soporte para ESP32CAM en Arduino IDE
Visita el siguiente enlace: [soporte esp32cam](https://github.com/JorgeIsur/ESP32CAM-PROJECTS/tree/master/MAX30102/SintomasCovid/sintomasCOVID#instalaci%C3%B3n-del-soporte-para-esp32cam-en-arduino-ide)
## Conexiones FTDI
Visitar el siguiente enlace: [FTDI](https://github.com/JorgeIsur/ESP32CAM-PROJECTS/tree/master/MAX30102/SintomasCovid/sintomasCOVID#ftdi)
## Programación

Para probar un código, escribimos lo siguiente en la terminal:

cd Documents

git clone https://github.com/ElierRosales/Capstone-project-Administrador-de-laboratorios.git

Nos vamos a la carpeta videoServer y copiamos el contenido del archivo videoserver en nuestra IDE de arduino

Antes de cargar el código, cambia estas variables por el nombre de tu wiFi y tu contraseña:

 `const char* ssid = "REPLACE_WITH_YOUR_SSID";
const char* password = "REPLACE_WITH_YOUR_PASSWORD"; `

Cargamos el código

Quitamos el puente que pusimos con anterioridad y presionamos el botón reset. 

Una vez que se haya conectado a internet, aparecerá una dirección ip la cual es la de tu dispositivo esp, deberas copiar esta dirección y pegarlo en algún navegador.

![image](https://user-images.githubusercontent.com/81974347/155417363-0d1a301d-b24a-4d9d-91ca-0d53c359e62e.png)

Para implementarlo como parte de tu dashboard en Node red, debaras insertar un nodo template del apartado dashboard e insertar el siguiente código:

`<div style="margin-bottom: 10px;">
<img src="Aqui pones la dirección ip que te arrojo arduino IDE" width="650px">
</div>`

damos clic en el botón deploy y revisamos el dashboard.
