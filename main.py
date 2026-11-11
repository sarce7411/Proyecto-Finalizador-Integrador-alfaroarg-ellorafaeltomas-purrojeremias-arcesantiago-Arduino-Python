import tkinter as tk

from secrandom import generar
from secrandom import potenciometro

ventana = tk.Tk()
ventana.title("Escape Room")
ventana.geometry("400x300")
ventana.anchor("n")

mensaje = tk.Label(ventana, text=f"Presioná {"Siguiente"} para jugar")
mensaje.grid(row=0, column=0, pady=20)


def iniciar():
    secuencia = generar()
    p = potenciometro()
    m_p = tk.Label(ventana, text="Nro potenciometro generada")
    m_p.grid(row=2, column=0)
    s_p = tk.Label(ventana, text="Secuencia generada")
    s_p.grid(row=3, column=0)

boton = tk.Button(ventana, text="Siguiente", command=iniciar)
boton.grid(row=1, column=0)

ventana.mainloop()