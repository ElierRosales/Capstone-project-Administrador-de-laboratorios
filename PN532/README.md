# PN532-Raspberry pi model B+
### Lector de sensor NFC (PN532) con raspberry
## INSTRUCCIONES 
### CONFIGURACIÓN SENSOR
Colocar el sensor en el modo I2C, para esto debemos de mover el dipswitch. En este caso como es modo I2C, colocamos el 1 en ON y el 2 en OFF. (También nos podemos guiar viendo la tabla del sensor, esta se encuentra a un lado del dipswitch como se puee ver en la siguiente imagen) 

<img src = "https://github.com/ElierRosales/Capstone-project-Administrador-de-laboratorios/blob/1591fc57af5bbe840283c8702dcfac98775471e2/PN532/Imagenes%20PN532/DIP-SWITCH-I_PN532.jpg" width="500">

### CONEXIÓN DEL SENSOR A RASPBERRY

| Pin en el modulo NFC | Pin Raspberry |
| -- | -- |
| GND | 6 |
| VCC | 4 |
| SDA | 3 |
| SCL | 5 |

Nota: Esto podría cambiar dependiendo de tu modelo de Raspberry.

#### Diagrama esquematico de conexiones 

<img src = "https://github.com/ElierRosales/Capstone-project-Administrador-de-laboratorios/blob/1591fc57af5bbe840283c8702dcfac98775471e2/PN532/Imagenes%20PN532/DIP-SWITCH-I_PN532.jpg" width="500">
