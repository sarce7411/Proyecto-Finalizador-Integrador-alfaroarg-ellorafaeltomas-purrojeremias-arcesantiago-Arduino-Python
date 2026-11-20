# Nivel 3
import tkinter as tk
from tkinter import messagebox
import serial
import random
import time

def nivel3():
    PUERTO_SERIE = "COM3"  
    BAUDIOS = 9600

    arduino = serial.Serial(PUERTO_SERIE, BAUDIOS, timeout=1)
    time.sleep(2)  # Esperamos a que reinicie el Arduino al abrir el puerto
    arduino.write(b"NIVEL3\n")  

    ventana = tk.Tk()
    ventana.geometry("600x400")
    ventana.title("Escape Room - Nivel 3")
    ventana.anchor('n')

    # Variables del juego
    tiempo = 90
    objetivo = random.randint(100, 920)  # Ej: 700
    tolerancia = 20                      
    leds_anteriores = -1
    tiempo_inicio_rango = None
    juego_terminado = False

    print("Valor secreto Nivel 3:", objetivo)

    # Interfaz gráfica (mismo estilo con .grid que arce.py)
    tk.Label(ventana, text="Sintonizar la señal: girá el potenciómetro hasta encender los 4 LEDs.", font=("Arial", 11)).grid(row=0, column=0, columnspan=4, pady=15)

    # 4 LEDs visuales en pantalla que reflejan los 4 LEDs físicos del Arduino
    led1 = tk.Label(ventana, text="LED 1", width=6, height=2, font=("Arial", 12, "bold"), bg="gray", fg="white", relief="solid", borderwidth=2)
    led1.grid(row=1, column=0, padx=10, pady=15)

    led2 = tk.Label(ventana, text="LED 2", width=6, height=2, font=("Arial", 12, "bold"), bg="gray", fg="white", relief="solid", borderwidth=2)
    led2.grid(row=1, column=1, padx=10, pady=15)

    led3 = tk.Label(ventana, text="LED 3", width=6, height=2, font=("Arial", 12, "bold"), bg="gray", fg="white", relief="solid", borderwidth=2)
    led3.grid(row=1, column=2, padx=10, pady=15)

    led4 = tk.Label(ventana, text="LED 4", width=6, height=2, font=("Arial", 12, "bold"), bg="gray", fg="white", relief="solid", borderwidth=2)
    led4.grid(row=1, column=3, padx=10, pady=15)

    leds_ui = [led1, led2, led3, led4]

    mensaje_estado = tk.Label(ventana, text="Buscando señal...", font=("Arial", 13, "bold"), pady=15)
    mensaje_estado.grid(row=2, column=0, columnspan=4)

    mensaje_progreso = tk.Label(ventana, text="Estabilización: 0.0s / 3.0s", font=("Arial", 12), fg="blue")
    mensaje_progreso.grid(row=3, column=0, columnspan=4, pady=10)

    reloj = tk.Label(ventana, text=f"Tiempo: {tiempo}s", font=("Arial", 11))
    reloj.grid(row=4, column=0, columnspan=4, pady=15)

    def procesar_potenciometro(valor):
        nonlocal leds_anteriores, tiempo_inicio_rango

        distancia = abs(valor - objetivo)

        
        if distancia <= tolerancia:
            cant_leds = 4      # Dentro del rango correcto
        elif distancia <= 80:
            cant_leds = 3      # Muy cerca
        elif distancia <= 180:
            cant_leds = 2      # Cerca
        elif distancia <= 320:
            cant_leds = 1      # Lejos
        else:
            cant_leds = 0      # Muy lejos

       
        if cant_leds != leds_anteriores:
            arduino.write(f"LEDS:{cant_leds}\n".encode())
            leds_anteriores = cant_leds

            for i in range(4):
                if i < cant_leds:
                    leds_ui[i].config(bg="green" if cant_leds == 4 else "orange")
                else:
                    leds_ui[i].config(bg="gray")

        # Control de los 3 segundos dentro del rango
        if cant_leds == 4:
            if tiempo_inicio_rango is None:
                tiempo_inicio_rango = time.time()
            mensaje_estado.config(text="¡Señal encontrada! Mantené la perilla quieta...", fg="green")
        else:
            tiempo_inicio_rango = None
            mensaje_estado.config(text="Buscando señal...", fg="black")
            mensaje_progreso.config(text="Estabilización: 0.0s / 3.0s")

    def leer_arduino():
        nonlocal juego_terminado

        if juego_terminado:
            return

        if arduino.in_waiting > 0:
            entrada = arduino.readline().decode(errors="ignore").strip()

            if entrada.startswith("POT:"):
                try:
                    valor = int(entrada.split(":")[1])
                    procesar_potenciometro(valor)
                except ValueError:
                    pass

        
        if tiempo_inicio_rango is not None:
            transcurrido = time.time() - tiempo_inicio_rango
            if transcurrido >= 3.0:
                juego_terminado = True
                arduino.write(b"BUZZER:OK\n")
                arduino.write(b"LEDS:0\n")
                mensaje_estado.config(text="¡Señal estabilizada!", fg="green")
                mensaje_progreso.config(text="Estabilización: 3.0s / 3.0s")
                messagebox.showinfo("¡Ganaste!", "¡Completaste el nivel tres y escapaste!")
                arduino.close()
                ventana.destroy()
                return
            else:
                mensaje_progreso.config(text=f"Estabilización: {transcurrido:.1f}s / 3.0s")

        ventana.after(50, leer_arduino)

    def actualizar_tiempo():
        nonlocal tiempo, juego_terminado

        if juego_terminado:
            return

        reloj.config(text=f"Tiempo: {tiempo}s")

        if tiempo > 0:
            tiempo -= 1
            ventana.after(1000, actualizar_tiempo)
        else:
            juego_terminado = True
            arduino.write(b"BUZZER:ERROR\n")
            arduino.write(b"LEDS:0\n")
            arduino.close()
            ventana.destroy()
            messagebox.showinfo("Fin", "¡Se acabó el tiempo!")

    leer_arduino()
    actualizar_tiempo()
    ventana.mainloop()


if __name__ == "__main__":
    nivel3()