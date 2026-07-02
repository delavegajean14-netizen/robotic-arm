import tkinter as tk
from tkinter import ttk, messagebox
import serial
import time
import math
import threading

# configuración física en cm
L1 = 5.0   # Brazo (cm)
L2 = 8.0   # Antebrazo (cm)
L3 = 4.0   # Efector final (cm)
H_BASE = 1.5 
OFFSETS = [90, 90, 90, 90] # Posición central

class RobotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Control Maestro - Brazo Robótico")
        self.root.geometry("480x780") # tamaño de la ventana 
        self.arduino = None
        
        self.rutina = [] 
        self.detener_rutina = False # marcador para detener el bucle
        
        self.crear_interfaz()

    def crear_interfaz(self):
        style = ttk.Style()
        style.theme_use('clam')
        self.root.configure(bg="#f0f2f5")

        # sección 1: conexiones seriales
        frame_conn = ttk.LabelFrame(self.root, text=" Conexión Serial ", padding=10)
        frame_conn.pack(fill="x", padx=15, pady=10)

        self.entry_puerto = ttk.Entry(frame_conn, width=12)
        self.entry_puerto.insert(0, "COM16")
        self.entry_puerto.pack(side="left", padx=5)

        self.btn_conectar = ttk.Button(frame_conn, text="Conectar", command=self.conectar_serial)
        self.btn_conectar.pack(side="left", padx=5)

        self.lbl_estado = ttk.Label(frame_conn, text="● Desconectado", foreground="red")
        self.lbl_estado.pack(side="right", padx=10)

        # sección 2: control manual (FK) 
        frame_fk = ttk.LabelFrame(self.root, text=" Control de Articulaciones (Grados) ", padding=10)
        frame_fk.pack(fill="x", padx=15, pady=5)

        self.sliders = []
        nombres = ["Base (Q0)", "Hombro (Q1)", "Codo (Q2)", "Muñeca (Q3)"]
        for i, nombre in enumerate(nombres):
            row = ttk.Frame(frame_fk)
            row.pack(fill="x", pady=2)
            ttk.Label(row, text=nombre, width=12).pack(side="left")
            
            slider = ttk.Scale(row, from_=-90, to=90, orient="horizontal")
            slider.set(0)
            slider.pack(side="left", fill="x", expand=True, padx=5)
            
            val_label = ttk.Label(row, text="0°", width=5)
            val_label.pack(side="right")
            
            slider.bind("<ButtonRelease-1>", lambda e: self.enviar_desde_sliders())
            slider.configure(command=lambda v, l=val_label: l.configure(text=f"{int(float(v))}°"))
            self.sliders.append(slider)

        # botón de reset
        ttk.Button(frame_fk, text="⟲ Resetear a Posición Inicial", command=self.reset_posicion).pack(pady=10)

        # sección 3: cinemática inversa 
        frame_ik = ttk.LabelFrame(self.root, text=" Posicionamiento Cartesiano (cm) ", padding=10)
        frame_ik.pack(fill="x", padx=15, pady=5)

        inputs = ttk.Frame(frame_ik)
        inputs.pack()
        
        self.coords = {}
        for i, eje in enumerate(['X', 'Y', 'Z']):
            ttk.Label(inputs, text=f"{eje}:").grid(row=0, column=i*2, padx=2)
            ent = ttk.Entry(inputs, width=6)
            ent.insert(0, "7.0" if eje != 'Y' else "5.0")
            ent.grid(row=0, column=i*2+1, padx=5)
            self.coords[eje] = ent

        ttk.Button(frame_ik, text="Calcular y Posicionar", command=self.ejecutar_ik).pack(pady=10)

        # sección 4: ruinas de movimiento 
        frame_rutina = ttk.LabelFrame(self.root, text=" Secuencia Automática ", padding=10)
        frame_rutina.pack(fill="x", padx=15, pady=5)

        # controles de edición de rutina
        btn_edit_frame = ttk.Frame(frame_rutina)
        btn_edit_frame.pack(fill="x", pady=5)
        ttk.Button(btn_edit_frame, text="✚ Guardar Pos.", command=self.guardar_posicion).pack(side="left", padx=5, expand=True)
        ttk.Button(btn_edit_frame, text="✖️ Borrar Todo", command=self.borrar_rutina).pack(side="left", padx=5, expand=True)
        
        self.lbl_pasos = ttk.Label(frame_rutina, text="Pasos guardados: 0", font=("Arial", 9, "italic"))
        self.lbl_pasos.pack(pady=2)

        # controles de reproducción
        btn_play_frame = ttk.Frame(frame_rutina)
        btn_play_frame.pack(fill="x", pady=5)
        
        self.btn_play_once = ttk.Button(btn_play_frame, text="▶️ 1 Vez", command=lambda: self.iniciar_reproduccion(bucle=False))
        self.btn_play_once.pack(side="left", padx=2, expand=True)
        
        self.btn_play_loop = ttk.Button(btn_play_frame, text="🔁 Bucle", command=lambda: self.iniciar_reproduccion(bucle=True))
        self.btn_play_loop.pack(side="left", padx=2, expand=True)
        
        self.btn_stop = ttk.Button(btn_play_frame, text="⏹️ Detener", command=self.detener_reproduccion, state="disabled")
        self.btn_stop.pack(side="left", padx=2, expand=True)

        # sección 5: log de eventos
        self.txt_log = tk.Text(self.root, height=5, font=("Consolas", 8), bg="#ffffff")
        self.txt_log.pack(padx=15, pady=10, fill="both")

    # metodo de la iterfaz y comunicación 
    def log(self, msg):
        self.txt_log.insert(tk.END, f">> {msg}\n")
        self.txt_log.see(tk.END)

    def conectar_serial(self):
        if self.arduino and self.arduino.is_open:
            self.arduino.close()
            self.btn_conectar.config(text="Conectar")
            self.lbl_estado.config(text="● Desconectado", foreground="red")
            return
        try:
            puerto = self.entry_puerto.get()
            self.arduino = serial.Serial(puerto, 115200, timeout=0.1)
            time.sleep(2) 
            self.btn_conectar.config(text="Desconectar")
            self.lbl_estado.config(text="● Conectado", foreground="green")
            self.log(f"Conectado a {puerto}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir {self.entry_puerto.get()}")

    def enviar_desde_sliders(self):
        angulos = [s.get() for s in self.sliders]
        self.enviar_a_arduino(angulos)

    def enviar_a_arduino(self, angulos):
        fisicos = [
            int(angulos[0] + OFFSETS[0]),
            int(-angulos[1] + OFFSETS[1]), 
            int(angulos[2] + OFFSETS[2]),
            int(angulos[3] + OFFSETS[3])
        ]
        fisicos = [max(0, min(180, a)) for a in fisicos]
        cmd = f"{fisicos[0]},{fisicos[1]},{fisicos[2]},{fisicos[3]}\n"
        
        if self.arduino and self.arduino.is_open:
            try:
                self.arduino.write(cmd.encode())
                self.log(f"Enviado: {cmd.strip()}")
            except:
                self.log("Error al escribir en serial.")
        else:
            self.log(f"Simulación: {cmd.strip()}")

    def ejecutar_ik(self):
        try:
            x = float(self.coords['X'].get())
            y = float(self.coords['Y'].get()) - H_BASE
            z = float(self.coords['Z'].get())
            
            r = math.sqrt(x*2 + z*2)
            L_ext = L2 + L3
            
            cos_q2 = (r*2 + y2 - L12 - L_ext*2) / (2 * L1 * L_ext)
            if not (-1 <= cos_q2 <= 1):
                raise ValueError("Fuera de alcance")

            q2_rad = math.acos(cos_q2)
            q1_rad = math.atan2(y, r) - math.atan2(L_ext * math.sin(q2_rad), L1 + L_ext * math.cos(q2_rad))
            q0_rad = math.atan2(z, x)

            q0, q1, q2 = math.degrees(q0_rad), math.degrees(q1_rad), math.degrees(q2_rad)
            
            self.sliders[0].set(q0)
            self.sliders[1].set(q1)
            self.sliders[2].set(q2)
            self.enviar_a_arduino([q0, q1, q2, 0])
            
        except ValueError:
            messagebox.showwarning("Inalcanzable", "Las coordenadas están fuera del rango.")

    def reset_posicion(self):
        """Devuelve el brazo a la posición inicial (0 grados matemáticos = 90 grados físicos)"""
        for slider in self.sliders:
            slider.set(0)
        self.enviar_desde_sliders()
        self.log("Brazo reseteado a la posición de inicio.")

    # métodos de la rutina de movimiento
    def guardar_posicion(self):
        pos_actual = [s.get() for s in self.sliders]
        self.rutina.append(pos_actual)
        self.lbl_pasos.config(text=f"Pasos guardados: {len(self.rutina)}")
        self.log(f"Posición guardada: {pos_actual}")

    def borrar_rutina(self):
        self.rutina.clear()
        self.lbl_pasos.config(text="Pasos guardados: 0")
        self.log("Rutina borrada.")

    def iniciar_reproduccion(self, bucle=False):
        if not self.rutina:
            messagebox.showwarning("Aviso", "No hay pasos guardados en la rutina.")
            return
            
        # configurar botones
        self.btn_play_once.config(state="disabled")
        self.btn_play_loop.config(state="disabled")
        self.btn_stop.config(state="normal")
        
        self.detener_rutina = False
        modo = "BUCLE" if bucle else "1 VEZ"
        self.log(f"--- Iniciando Rutina ({modo}) ---")
        
        # iniciamos hilo
        hilo = threading.Thread(target=self._hilo_reproduccion, args=(bucle,), daemon=True)
        hilo.start()

    def detener_reproduccion(self):
        """Activa la bandera para que el hilo se detenga"""
        self.detener_rutina = True
        self.btn_stop.config(state="disabled")
        self.log("Deteniendo... (espera a que termine el movimiento actual)")

    def _hilo_reproduccion(self, bucle):
        ciclo_actual = 1
        
        while not self.detener_rutina:
            self.log(f"Ejecutando ciclo {ciclo_actual}...")
            
            for i, pos in enumerate(self.rutina):
                if self.detener_rutina:
                    break # salir del for si presionan Stop
                    
                # mover y actualizar UI
                self.root.after(0, self.actualizar_sliders_desde_hilo, pos)
                self.enviar_a_arduino(pos)
                
                # tiempo de espera entre pasos (puedes ajustarlo si el robot es más rápido)
                time.sleep(1.5) 
                
            if not bucle:
                break # salir del while si no es bucle
                
            ciclo_actual += 1
            
        self.log("--- Rutina Finalizada / Detenida ---")
        
        # restaurar botones al terminar usando el hilo principal
        self.root.after(0, self.restaurar_botones_play)

    def actualizar_sliders_desde_hilo(self, pos):
        for i in range(4):
            self.sliders[i].set(pos[i])

    def restaurar_botones_play(self):
        self.btn_play_once.config(state="normal")
        self.btn_play_loop.config(state="normal")
        self.btn_stop.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = RobotGUI(root)
    root.mainloop()