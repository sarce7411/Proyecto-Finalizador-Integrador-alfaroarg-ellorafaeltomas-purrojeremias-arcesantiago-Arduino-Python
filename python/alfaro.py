
import tkinter as tk
from tkinter import messagebox
import serial
import time

from secrandom import generar1


def nivel_2():

    intentos = 5

    PUERTO_SERIE = "COM3"
    BAUDIOS = 9600

    arduino = serial.Serial(PUERTO_SERIE, BAUDIOS, timeout=0.1)

    time.sleep(2)

    arduino.reset_input_buffer()
    arduino.write(b"NIVEL2\n")

    ventana = tk.Tk()
    ventana.geometry("600x400")
    ventana.title("Escape Room")

    num = generar1()

    tiempo = 90
    ultimo_valor = None
    pendiente = b""

    # Titulo
    tk.Label(
        ventana,
        text="NIVEL 2",
        font=("Arial", 20, "bold")
    ).grid(row=0, column=0, sticky="w", padx=20, pady=15)

    # Numero secreto
    tk.Label(
        ventana,
        text=f"Numero a adivinar (0 a 1023):\n{num}",
        font=("Arial", 14)
    ).grid(row=1, column=0, padx=20, pady=20)

    # Numero del potenciometro
    pot_label = tk.Label(
        ventana,
        text="Pusiste el numero:\n---",
        font=("Arial", 14)
    )
    pot_label.grid(row=1, column=1, padx=20, pady=20)

    # Intentos
    intentos_label = tk.Label(
        ventana,
        text=f"Intentos: {intentos}",
        font=("Arial", 14)
    )
    intentos_label.grid(row=2, column=0, padx=20, pady=15)

    # Mensaje
    mensaje = tk.Label(
        ventana,
        text="",
        font=("Arial", 12)
    )
    mensaje.grid(row=3, column=0, columnspan=2)

    # Reloj
    reloj = tk.Label(
        ventana,
        text=f"Tiempo: {tiempo}s"
    )
    reloj.grid(row=4, column=0, columnspan=2)

    def recibir_valor():
        nonlocal ultimo_valor, pendiente

        if arduino.in_waiting:
            pendiente += arduino.read(arduino.in_waiting)
            lineas = pendiente.split(b"\n")
            pendiente = lineas.pop()
            for linea in lineas:
                dato = linea.strip().removeprefix(b"POT:")
                if dato.isdigit() and len(dato) <= 4 and int(dato) <= 1023:
                    ultimo_valor = int(dato)

    def leer_arduino():
        recibir_valor()
        ventana.after(100, leer_arduino)

    def verificar():
        nonlocal intentos
        recibir_valor()

        if ultimo_valor is None:
            mensaje.config(text="Mueve el potenciometro primero.")
            return

        pot_label.config(text=f"Pusiste el numero:\n{ultimo_valor}")

        if abs(ultimo_valor - num) <= 5:

            mensaje.config(text="¡Encontraste el numero!")
            arduino.write(b"BUZZER:OK\n")

            messagebox.showinfo(
                "¡Ganaste!",
                "¡Completaste el nivel 2!"
            )

            arduino.close()
            ventana.destroy()

        else:

            intentos -= 1

            intentos_label.config(
                text=f"Intentos: {intentos}"
            )

            arduino.write(b"BUZZER:ERROR\n")

            if intentos > 0:

                mensaje.config(
                    text="Numero incorrecto. Intenta nuevamente."
                )

            else:

                arduino.close()
                ventana.destroy()

                messagebox.showinfo(
                    "Fin",
                    "Te quedaste sin intentos."
                )

    # Boton confirmar
    b_confirmar = tk.Button(
        ventana,
        text="Confirmar",
        command=verificar,
        height=2,
        width=12,
        font=("Arial", 12),
        bg="green",
        fg="white"
    )

    b_confirmar.grid(row=2, column=1, padx=20, pady=15)

    def actualizar_tiempo():

        nonlocal tiempo

        reloj.config(text=f"Tiempo: {tiempo}s")

        if tiempo > 0:

            tiempo -= 1

            ventana.after(1000, actualizar_tiempo)

        else:

            arduino.write(b"BUZZER:ERROR\n")
            arduino.close()
            ventana.destroy()

            messagebox.showinfo(
                "Fin",
                "¡Se acabó el tiempo!"
            )

    leer_arduino()
    actualizar_tiempo()

    ventana.mainloop()

