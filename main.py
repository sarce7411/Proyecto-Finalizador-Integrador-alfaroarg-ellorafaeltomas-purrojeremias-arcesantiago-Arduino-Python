import tkinter as tk
from tkinter import messagebox
import threading
import time

try:
    import serial
    MODO_SIMULACION = False
except ImportError:
    MODO_SIMULACION = True

PUERTO_SERIE = "/dev/ttyACM0"
BAUDIOS = 9600


class EscapeRoomApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Escape Room Electrónico - La Habitación Secreta")
        self.root.geometry("820x580")
        self.root.configure(bg="#0d1117")
        self.root.resizable(False, False)

        # Estado del juego
        self.nivel_actual = 1
        self.intentos = 3
        self.pistas_restantes = 2
        self.tiempo_restante = 177  # 02:57
        self.juego_activo = True

        # Definición de secuencias por nivel (Solo Botones)
        self.combinacion_nivel1 = ["B", "D", "A"]
        self.combinacion_nivel2 = ["A", "C", "B"]
        self.combinacion_nivel3 = ["C", "A", "D", "B"]

        self.ingresados = []

        self.arduino = None
        self.conectar_arduino()

        self.crear_interfaz()

        if MODO_SIMULACION or not self.arduino:
            self.root.bind("<Key>", self.simular_teclado)

        self.actualizar_cronometro()

    def conectar_arduino(self):
        global MODO_SIMULACION
        if not MODO_SIMULACION:
            try:
                self.arduino = serial.Serial(PUERTO_SERIE, BAUDIOS, timeout=1)
                time.sleep(2)
                self.hilo_escucha = threading.Thread(target=self.leer_puerto_serie, daemon=True)
                self.hilo_escucha.start()
                print("Conectado con éxito al Arduino.")
            except Exception as e:
                print(f"No se detectó el Arduino ({e}). Activando modo simulación.")
                MODO_SIMULACION = True

    def crear_interfaz(self):
        # 1. ENCABEZADO
        frame_top = tk.Frame(self.root, bg="#0d1117")
        frame_top.pack(fill="x", padx=25, pady=(15, 10))

        lbl_titulo = tk.Label(frame_top, text="ESCAPE ROOM", font=("Helvetica", 22, "bold"), fg="#00f0ff", bg="#0d1117")
        lbl_titulo.pack(side="left")

        lbl_sub = tk.Label(frame_top, text="  // LA HABITACIÓN SECRETA", font=("Helvetica", 12, "bold"), fg="#8b949e", bg="#0d1117")
        lbl_sub.pack(side="left", pady=(8, 0))

        frame_timer = tk.Frame(frame_top, bg="#161b22", highlightbackground="#30363d", highlightthickness=1, padx=12, pady=4)
        frame_timer.pack(side="right")

        tk.Label(frame_timer, text="TIEMPO RESTANTE", font=("Helvetica", 8, "bold"), fg="#8b949e", bg="#161b22").pack()
        self.lbl_tiempo = tk.Label(frame_timer, text="02:57", font=("Consolas", 22, "bold"), fg="#ff0055", bg="#161b22")
        self.lbl_tiempo.pack()

        # 2. PANEL PRINCIPAL (IZQUIERDA)
        self.frame_juego = tk.Frame(self.root, bg="#161b22", highlightbackground="#30363d", highlightthickness=1)
        self.frame_juego.place(x=25, y=95, width=510, height=360)

        self.lbl_nivel = tk.Label(self.frame_juego, text="NIVEL 1 DE 3", font=("Helvetica", 10, "bold"), fg="#00f0ff", bg="#161b22")
        self.lbl_nivel.pack(anchor="w", padx=20, pady=(15, 5))

        self.lbl_desafio_titulo = tk.Label(self.frame_juego, text="Desafío 1: Código Inicial", 
                                           font=("Helvetica", 15, "bold"), fg="#ffffff", bg="#161b22")
        self.lbl_desafio_titulo.pack(anchor="w", padx=20, pady=(0, 5))

        self.lbl_indicaciones = tk.Label(self.frame_juego, text="Ingresá la secuencia de 3 botones usando la botonera:", 
                                         font=("Helvetica", 10), fg="#8b949e", bg="#161b22")
        self.lbl_indicaciones.pack(anchor="w", padx=20, pady=(0, 15))

        # CONTENEDOR DE DÍGITOS
        self.frame_digits = tk.Frame(self.frame_juego, bg="#161b22")
        self.frame_digits.pack(pady=10)

        self.box_digits = []
        self.actualizar_boxes_display(3)

        # ESTADÍSTICAS
        frame_stats = tk.Frame(self.frame_juego, bg="#161b22")
        frame_stats.pack(fill="x", side="bottom", pady=20, padx=20)

        self.lbl_intentos = tk.Label(frame_stats, text=f"Intentos: {self.intentos} / 3", 
                                     font=("Helvetica", 10, "bold"), fg="#e3b341", bg="#161b22")
        self.lbl_intentos.pack(side="left")

        self.lbl_pistas = tk.Label(frame_stats, text=f"Pistas disponibles: {self.pistas_restantes}", 
                                   font=("Helvetica", 10, "bold"), fg="#58a6ff", bg="#161b22")
        self.lbl_pistas.pack(side="right")

        # 3. PANEL LATERAL DE ESTADO (DERECHA)
        frame_estado = tk.Frame(self.root, bg="#161b22", highlightbackground="#30363d", highlightthickness=1)
        frame_estado.place(x=555, y=95, width=240, height=360)

        tk.Label(frame_estado, text="PROGRESO", font=("Helvetica", 11, "bold"), fg="#8b949e", bg="#161b22").pack(anchor="w", padx=15, pady=(15, 10))

        self.lbl_st1 = tk.Label(frame_estado, text="[●] Desafío 1: Combinación", font=("Helvetica", 9, "bold"), fg="#00f0ff", bg="#161b22", justify="left")
        self.lbl_st1.pack(anchor="w", padx=15, pady=6)

        self.lbl_st2 = tk.Label(frame_estado, text="[ ] Desafío 2: Secuencia Media", font=("Helvetica", 9), fg="#484f58", bg="#161b22", justify="left")
        self.lbl_st2.pack(anchor="w", padx=15, pady=6)

        self.lbl_st3 = tk.Label(frame_estado, text="[ ] Desafío 3: Código Maestro", font=("Helvetica", 9), fg="#484f58", bg="#161b22", justify="left")
        self.lbl_st3.pack(anchor="w", padx=15, pady=6)

        tk.Frame(frame_estado, bg="#30363d", height=1).pack(fill="x", padx=15, pady=15)

        tk.Label(frame_estado, text="OBJETIVO GENERAL", font=("Helvetica", 9, "bold"), fg="#e3b341", bg="#161b22").pack(anchor="w", padx=15)
        tk.Label(frame_estado, text="Completá las 3 pruebas\nantes de que el tiempo\nllegue a 00:00 para escapar.", 
                 font=("Helvetica", 9), fg="#8b949e", bg="#161b22", justify="left").pack(anchor="w", padx=15, pady=(5, 0))

        # 4. PANEL INFERIOR DE PISTAS Y MENSAJES
        frame_bottom = tk.Frame(self.root, bg="#161b22", highlightbackground="#30363d", highlightthickness=1)
        frame_bottom.place(x=25, y=470, width=770, height=85)

        self.lbl_pista_txt = tk.Label(frame_bottom, text="PISTA: La combinación contiene los botones B, D y A.", 
                                      font=("Helvetica", 10, "bold"), fg="#e3b341", bg="#161b22", anchor="w")
        self.lbl_pista_txt.pack(side="left", padx=20, pady=15)

        self.lbl_mensaje_global = tk.Label(frame_bottom, text="SISTEMA LISTO", 
                                           font=("Consolas", 11, "bold"), fg="#00ff66", bg="#161b22", anchor="e")
        self.lbl_mensaje_global.pack(side="right", padx=20, pady=15)

    def actualizar_boxes_display(self, cantidad):
        for widget in self.frame_digits.winfo_children():
            widget.destroy()

        self.box_digits = []
        for i in range(cantidad):
            box = tk.Label(self.frame_digits, text="?", font=("Consolas", 32, "bold"), fg="#00ff66", bg="#0d1117", 
                           width=3, height=1, highlightbackground="#30363d", highlightthickness=2)
            box.pack(side="left", padx=8)
            self.box_digits.append(box)

    def leer_puerto_serie(self):
        while self.juego_activo:
            if self.arduino and self.arduino.in_waiting > 0:
                try:
                    linea = self.arduino.readline().decode('utf-8').strip()
                    if linea.startswith("BOTON:"):
                        boton = linea.split(":")[1]
                        self.root.after(0, self.procesar_boton, boton)
                except Exception:
                    pass

    def simular_teclado(self, event):
        tecla = event.char.upper()
        if tecla in ["A", "B", "C", "D"]:
            self.procesar_boton(tecla)

    def enviar_arduino(self, comando):
        if self.arduino and self.arduino.is_open:
            try:
                self.arduino.write(f"{comando}\n".encode('utf-8'))
            except Exception as e:
                print(f"Error al enviar datos: {e}")

    def procesar_boton(self, boton):
        if not self.juego_activo:
            return

        # Seleccionar la combinación según el nivel actual
        if self.nivel_actual == 1:
            meta = self.combinacion_nivel1
        elif self.nivel_actual == 2:
            meta = self.combinacion_nivel2
        elif self.nivel_actual == 3:
            meta = self.combinacion_nivel3

        self.ingresados.append(boton)

        for i in range(len(meta)):
            if i < len(self.ingresados):
                self.box_digits[i].config(text=self.ingresados[i], fg="#00f0ff")
            else:
                self.box_digits[i].config(text="?", fg="#00ff66")

        if len(self.ingresados) == len(meta):
            if self.ingresados == meta:
                self.enviar_arduino("BUZZER:OK")
                
                if self.nivel_actual == 1:
                    self.lbl_mensaje_global.config(text="¡NIVEL 1 SUPERADO!", fg="#00ff66")
                    self.lbl_st1.config(text="[V] Desafío 1: Combinación", fg="#00ff66")
                    self.root.after(1200, self.cargar_nivel_2)
                elif self.nivel_actual == 2:
                    self.lbl_mensaje_global.config(text="¡NIVEL 2 SUPERADO!", fg="#00ff66")
                    self.lbl_st2.config(text="[V] Desafío 2: Secuencia Media", fg="#00ff66")
                    self.root.after(1200, self.cargar_nivel_3)
                elif self.nivel_actual == 3:
                    self.ganar_juego()
            else:
                self.intentos -= 1
                self.lbl_intentos.config(text=f"Intentos: {self.intentos} / 3")
                self.enviar_arduino("BUZZER:ERROR")
                
                if self.intentos > 0:
                    self.lbl_mensaje_global.config(text="¡CÓDIGO ERRÓNEO!", fg="#ff0055")
                    self.ingresados = []
                    self.root.after(1000, self.resetear_boxes)
                else:
                    self.perder_juego("¡Sin intentos disponibles!")

    def resetear_boxes(self):
        for box in self.box_digits:
            box.config(text="?", fg="#00ff66")

    def cargar_nivel_2(self):
        self.nivel_actual = 2
        self.ingresados = []
        self.lbl_nivel.config(text="NIVEL 2 DE 3")
        self.lbl_desafio_titulo.config(text="Desafío 2: Secuencia Intermedia")
        self.lbl_indicaciones.config(text="Ingresá el código de 3 botones para desbloquear la puerta secundaria:")
        self.lbl_st2.config(fg="#00f0ff", text="[●] Desafío 2: Secuencia Media")
        self.lbl_pista_txt.config(text="PISTA: Secuencia del Nivel 2 -> [ A , C , B ]")
        self.lbl_mensaje_global.config(text="INGRESÁ CÓDIGO", fg="#00f0ff")
        self.actualizar_boxes_display(3)

    def cargar_nivel_3(self):
        self.nivel_actual = 3
        self.ingresados = []
        self.lbl_nivel.config(text="NIVEL 3 DE 3")
        self.lbl_desafio_titulo.config(text="Desafío 3: Código Maestro")
        self.lbl_indicaciones.config(text="Ingresá el código final de 4 botones para desactivar el sistema:")
        self.lbl_st3.config(fg="#00f0ff", text="[●] Desafío 3: Código Maestro")
        self.lbl_pista_txt.config(text="PISTA: Secuencia Final -> [ C , A , D , B ]")
        self.lbl_mensaje_global.config(text="ÚLTIMO CÓDIGO", fg="#00f0ff")
        self.actualizar_boxes_display(4)

    def actualizar_cronometro(self):
        if self.juego_activo and self.tiempo_restante > 0:
            minutos = self.tiempo_restante // 60
            segundos = self.tiempo_restante % 60
            self.lbl_tiempo.config(text=f"{minutos:02d}:{segundos:02d}")
            self.tiempo_restante -= 1
            self.root.after(1000, self.actualizar_cronometro)
        elif self.tiempo_restante <= 0:
            self.lbl_tiempo.config(text="00:00")
            self.perder_juego("¡Se acabó el tiempo!")

    def perder_juego(self, motivo):
        self.juego_activo = False
        messagebox.showerror("GAME OVER", f"{motivo}\nHas perdido el juego.")
        self.root.destroy()

    def ganar_juego(self):
        self.juego_activo = False
        self.lbl_st3.config(text="[V] Desafío 3: Código Maestro", fg="#00ff66")
        self.lbl_mensaje_global.config(text="¡ESCAPASTE CON ÉXITO!", fg="#00ff66")
        messagebox.showinfo("¡VICTORIA!", "¡Felicidades! Completaste todos los niveles y lograste escapar.")
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = EscapeRoomApp(root)
    root.mainloop()