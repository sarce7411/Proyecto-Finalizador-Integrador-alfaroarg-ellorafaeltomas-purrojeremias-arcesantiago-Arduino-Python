
import tkinter as tk
from tkinter import messagebox
import serial
import random
import time


def nivel3():

    arduino = serial.Serial("COM3", 9600, timeout=0.1)
    time.sleep(2)
    arduino.reset_input_buffer()
    arduino.write(b"NIVEL3\n")

    ventana = tk.Tk()
    ventana.geometry("600x400")
    ventana.title("Escape Room - Nivel 3")

    tiempo = 90
    objetivo = random.randint(100, 920)
    pendiente = b""
    tiempo_inicio = None
    terminado = False
    leds_anteriores = -1

    print("Numero secreto:", objetivo)

    # Interfaz
    tk.Label(
        ventana,
        text="Gira el potenciometro hasta encender los 4 LEDs",
        font=("Arial", 12)
    ).grid(row=0, column=0, columnspan=4, pady=20)

    leds_ui = []

    for i in range(4):
        led = tk.Label(
            ventana, text=f"LED {i+1}",
            width=8, height=2,
            bg="gray", fg="white",
            font=("Arial", 12, "bold"),
            relief="solid"
        )
        led.grid(row=1, column=i, padx=10)
        leds_ui.append(led)

    mensaje = tk.Label(ventana, text="Buscando señal...", font=("Arial", 13))
    mensaje.grid(row=2, column=0, columnspan=4, pady=20)

    progreso = tk.Label(
        ventana, text="Estabilizacion: 0.0 / 3.0 segundos"
    )
    progreso.grid(row=3, column=0, columnspan=4)

    reloj = tk.Label(ventana, text="Tiempo: 90 segundos")
    reloj.grid(row=4, column=0, columnspan=4, pady=20)

    # Procesar potenciometro
    def procesar_potenciometro(valor):

        nonlocal tiempo_inicio, leds_anteriores

        distancia = abs(valor - objetivo)

        if distancia <= 20:
            cantidad = 4
        elif distancia <= 80:
            cantidad = 3
        elif distancia <= 180:
            cantidad = 2
        elif distancia <= 320:
            cantidad = 1
        else:
            cantidad = 0

        if cantidad != leds_anteriores:

            arduino.write(f"LEDS:{cantidad}\n".encode())
            leds_anteriores = cantidad

            for i in range(4):
                if i < cantidad:
                    leds_ui[i].config(
                        bg="green" if cantidad == 4 else "orange"
                    )
                else:
                    leds_ui[i].config(bg="gray")

        if cantidad == 4:
            if tiempo_inicio is None:
                tiempo_inicio = time.time()

            mensaje.config(text="¡Encontraste la señal!", fg="green")

        else:
            tiempo_inicio = None
            mensaje.config(text="Buscando señal...", fg="black")
            progreso.config(text="Estabilizacion: 0.0 / 3.0 segundos")

    # Recibir valor (igual que nivel 2)
    def recibir_valor():

        nonlocal pendiente

        if arduino.in_waiting:

            pendiente += arduino.read(arduino.in_waiting)
            lineas = pendiente.split(b"\n")
            pendiente = lineas.pop()

            for linea in lineas:

                dato = linea.strip().removeprefix(b"POT:")

                if dato.isdigit() and len(dato) <= 4 and int(dato) <= 1023:
                    procesar_potenciometro(int(dato))

    # Leer Arduino y controlar victoria
    def leer_arduino():

        nonlocal terminado

        if terminado:
            return

        recibir_valor()

        if tiempo_inicio is not None:

            transcurrido = time.time() - tiempo_inicio

            progreso.config(
                text=f"Estabilizacion: {transcurrido:.1f} / 3.0 segundos"
            )

            if transcurrido >= 3:

                terminado = True
                arduino.write(b"BUZZER:OK\n")
                arduino.write(b"LEDS:0\n")
                arduino.close()
                ventana.destroy()

                messagebox.showinfo(
                    "¡Ganaste!",
                    "¡Completaste el nivel tres!"
                )
                return

        ventana.after(50, leer_arduino)

    # Cronometro
    def actualizar_tiempo():

        nonlocal tiempo, terminado

        if terminado:
            return

        reloj.config(text=f"Tiempo: {tiempo} segundos")

        if tiempo > 0:
            tiempo -= 1
            ventana.after(1000, actualizar_tiempo)

        else:
            terminado = True
            arduino.write(b"BUZZER:ERROR\n")
            arduino.write(b"LEDS:0\n")
            arduino.close()
            ventana.destroy()

            messagebox.showinfo("Fin", "¡Se acabo el tiempo!")

    leer_arduino()
    actualizar_tiempo()

    ventana.mainloop()


if __name__ == "__main__":
    nivel3()
