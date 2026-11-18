import tkinter as tk
from tkinter import messagebox
import serial
import time

from secrandom import generar

PUERTO_SERIE = "COM3"
BAUDIOS = 9600

nivel = 1
arduino = serial.Serial(PUERTO_SERIE, BAUDIOS, timeout=1)

ventana = tk.Tk()
ventana.geometry("600x400")
ventana.title("Escape Room")
ventana.anchor('n')

secuencia = generar()

tiempo = 90

texto_nivel = tk.Label(ventana, text="Nivel 1 de 3")
texto_nivel.grid(row=5, column=0, columnspan=3)

reloj = tk.Label(ventana, text=f"Tiempo: {tiempo}s")
reloj.grid(row=4, column=0, columnspan=3)

tk.Label(ventana, text="Ingrese la secuencia generada.").grid(row=0, columnspan=3)

caja1 = tk.Label(
    ventana,
    text="",
    width=3,
    height=2,
    font=("Arial", 24),
    relief="solid",
    borderwidth=2
)
caja1.grid(row=1, column=0, padx=5, pady=10)

caja2 = tk.Label(
    ventana,
    text="",
    width=3,
    height=2,
    font=("Arial", 24),
    relief="solid",
    borderwidth=2
)
caja2.grid(row=1, column=1, padx=5, pady=10)

caja3 = tk.Label(
    ventana,
    text="",
    width=3,
    height=2,
    font=("Arial", 24),
    relief="solid",
    borderwidth=2
)
caja3.grid(row=1, column=2, padx=5, pady=10)

cajas = [caja1, caja2, caja3]
posicion = 0

mensaje_final = tk.Label(ventana, text="", pady=40, font=(10))
mensaje_final.grid(row=3, columnspan=3)

def siguiente_nivel():
    global nivel, secuencia, posicion

    nivel += 1
    secuencia = generar()
    posicion = 0

    for caja in cajas:
        caja.config(text="")

    mensaje_final.config(text="")
    texto_nivel.config(text=f"Nivel {nivel} de 3")

def verificar():
    global nivel
    global posicion
    gano = False
    if caja1.cget("text") == secuencia[0]:
        if caja2.cget("text") == secuencia[1]:
            if caja3.cget("text") == secuencia[2]:
                mensaje_final.config(text="Ganaste!")
                gano = True
            else:
                mensaje_final.config(text="Acertaste las primeras 2 letras.")
        else:
            mensaje_final.config(text="Acertaste la primera letra.")
    else:
        if caja1.cget("text") == secuencia[0]:
            v1 = True
        else:
            v1 = False

        if caja2.cget("text") == secuencia[1]:
            v2 = True
        else:
            v2 = False

        if caja3.cget("text") == secuencia[2]:
            v3 = True
        else:
            v3 = False

        if v1 == True and v2 == True:
            mensaje_final.config(text="Acertaste la primer y tercera letra.")
        if v1 == True and v3 == True:
            mensaje_final.config(text="Acertaste la primer y tercer letra.")
        if v2 == True and v3 == True:
            mensaje_final.config(text="Acertaste la segunda y tercera letra.")
        elif v2 == True and v3 == False:
            mensaje_final.config(text="Acertaste la segunda letra.")
        elif v3 == True and v2 == False:
            mensaje_final.config(text="Acertaste la tercer letra.")
        elif v3 == False and v2 == False:
            mensaje_final.config(text="No le pegaste a una.")


    if gano:
        arduino.write(b"BUZZER:OK\n")
        if nivel < 3:
            messagebox.showinfo("Nivel superado", f"¡Superaste el nivel {nivel}!")
            siguiente_nivel()

        else:
            messagebox.showinfo("Victoria", "¡Completaste los tres niveles!")
            arduino.close()
            ventana.destroy()
    else:
        arduino.write(b"BUZZER:ERROR\n")
        for caja in cajas:
            caja.config(text="")
        posicion = 0
        

b_confirmar = tk.Button(text="Confirmar", command=verificar, height=2, width=10, font=("Arial"), bg="green", fg="white").grid(row=2, columnspan=3)

def mostrar_letra(letra):
    global posicion
    
    if posicion < len(cajas):
        cajas[posicion].config(text=letra)
        posicion += 1

def leer_arduino():
    if arduino.in_waiting > 0:
        entrada = arduino.readline().decode().strip()

        if entrada == "BOTON:A":
            mostrar_letra("A")
        elif entrada == "BOTON:B":
            mostrar_letra("B")
        elif entrada == "BOTON:C":
            mostrar_letra("C")
        elif entrada == "BOTON:D":
            mostrar_letra("D")

    ventana.after(50, leer_arduino)

def actualizar_tiempo():
    global tiempo

    reloj.config(text=f"Tiempo: {tiempo}")

    if tiempo > 0:
        tiempo -= 1
        ventana.after(1000, actualizar_tiempo)
        
    else:
        arduino.write(b"BUZZER:ERROR\n")
        ventana.destroy()
        messagebox.showinfo("Fin", "¡Se acabó el tiempo!")
        
leer_arduino()
actualizar_tiempo()
ventana.mainloop()