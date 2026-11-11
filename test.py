import serial

arduino = serial.Serial("/dev/ttyACM0", 9600)

while True:
    mensaje = arduino.readline().decode().strip()
    print(mensaje)