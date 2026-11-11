import tkinter as tk

from secrandom import generar
from secrandom import potenciometro

ventana = tk.Tk()
ventana.title("Escape Room")
ventana.geometry("800x300")
ventana.anchor("n")

mensaje = tk.Label(ventana, text=f"Presioná {"Siguiente"} para jugar")
mensaje.grid(row=0, column=0, pady=20)


def iniciar():
    secuencia = generar()
    p = potenciometro()
    m_p = tk.Label(ventana, text=f"Nro potenciometro generada ({p}).")
    m_p.grid(row=2, column=0)
    s_p = tk.Label(ventana, text=f"Secuencia generada ({secuencia}).")
    s_p.grid(row=3, column=0)

    mj = tk.Label(ventana, text="El jugador debera acertar el patron " \
    "y el numero del potenciometro generado.")
    mj.grid(row=4)

boton = tk.Button(ventana, text="Siguiente", command=iniciar)
boton.grid(row=1, column=0)

ventana.mainloop()