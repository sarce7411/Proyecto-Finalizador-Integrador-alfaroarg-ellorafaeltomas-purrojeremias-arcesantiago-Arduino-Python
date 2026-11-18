from arce import nivel1
from alfaro import nivel2
from purro import nivel 3
import serial

PUERTO_SERIE = "COM3"
BAUDIOS = 9600

arduino = serial.Serial(PUERTO_SERIE, BAUDIOS, timeout=1)



nivel1()
nivel2()
nivel3()