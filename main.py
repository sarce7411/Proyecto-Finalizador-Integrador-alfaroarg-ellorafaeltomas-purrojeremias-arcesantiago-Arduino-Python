import tkinter as tk
import serial
from secrandom import generar

secuencia = []
ingresada = []

ventana = tk.Tk()
ventana.title("Escape Room")
ventana.geometry("800x300")
ventana.columnconfigure(0, weight=1)

mensaje = tk.Label(ventana, text=f"Presioná {"Siguiente"} para jugar")
mensaje.grid(row=0, column=0, pady=20)

def iniciar():
    global secuencia
    secuencia = generar()
    ingresada.clear()
    mensaje.config(text="Ingresá la secuencia")

def verificar():
    if len(ingresada) == len(secuencia):
        if ingresada == secuencia:
            mensaje.config(text="¡Secuencia correcta!")
        else:
            mensaje.config(text="Secuencia incorrecta")

        ingresada.clear()

def presionar(numero):
    if not secuencia:
        return

    ingresada.append(numero)
    mensaje.config(text=f"Ingresaste: {ingresada}")

    if len(ingresada) == 4:
        if ingresada == secuencia:
            mensaje.config(text="¡Correcto! Ganaste")
        else:
            mensaje.config(text="Secuencia incorrecta")

        ingresada.clear()

boton = tk.Button(ventana, text="Siguiente", command=iniciar)
boton.grid(row=1, column=0, pady=10)

botones = tk.Frame(ventana)
botones.grid(row=2, column=0, pady=10)

a = tk.Button(botones, text="A", command=lambda: presionar(1))
a.grid(row=0, column=0, padx=5)

b = tk.Button(botones, text="B", command=lambda: presionar(2))
b.grid(row=0, column=1, padx=5)

c = tk.Button(botones, text="C", command=lambda: presionar(3))
c.grid(row=0, column=2, padx=5)

d = tk.Button(botones, text="D", command=lambda: presionar(4))
d.grid(row=0, column=3, padx=5)

ventana.mainloop()