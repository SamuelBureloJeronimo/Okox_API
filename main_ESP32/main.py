from time import sleep

# Configura la comunicación serial a 9600 baudios
import sys
sys.stdout.write("Prueba de ESP32 iniciada...\n")

# Bucle principal
while True:
    sys.stdout.write("LED ENCENDIDO\n")
    sleep(1)  # Espera 1 segundo
    sys.stdout.write("LED APAGADO\n")
    sleep(1)  # Espera 1 segundo
