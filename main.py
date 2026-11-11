import tkinter as tk
import serial
from secrandom import generar

ventana = tk.Tk()
ventana.title("Escape Room")
ventana.geometry("800x300")
ventana.anchor("n")

mensaje = tk.Label(ventana, text=f"Presioná {"Siguiente"} para jugar")
mensaje.grid(row=0, column=0, pady=20)

def iniciar():
    secuencia = generar()

    s_p = tk.Label(ventana, text=f"Secuencia generada ({secuencia}).")
    s_p.grid(row=3, column=0)

    mj = tk.Label(ventana, text="Repeti la secuencia.")
    mj.grid(row=4)


def verificar():
    if len(ingresada) == len(secuencia):
        if ingresada == secuencia:
            mensaje.config(text="¡Secuencia correcta!")
        else:
            mensaje.config(text="Secuencia incorrecta")

        ingresada.clear()

boton = tk.Button(ventana, text="Siguiente", command=iniciar)
boton.grid(row=1, column=0)

ventana.mainloop()



arduino = serial.Serial("/dev/ttyACM0", 9600)

while True:
    mensaje = arduino.readline().decode().strip()
    print(mensaje)