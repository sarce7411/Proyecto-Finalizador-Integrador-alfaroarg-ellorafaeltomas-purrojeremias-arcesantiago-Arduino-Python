import tkinter as tk

ventana = tk.Tk()
ventana.title("Escape Room")
ventana.geometry("400x300")

titulo = tk.Label(
    ventana,
    text="Escape Room",
)
titulo.pack(pady=20)

mensaje = tk.Label(ventana, text="Presioná Iniciar para jugar")
mensaje.pack(pady=10)


def iniciar():
    mensaje.config(text="¡El juego comenzó!")


boton = tk.Button(ventana, text="Iniciar", command=iniciar)
boton.pack(pady=20)

ventana.mainloop()