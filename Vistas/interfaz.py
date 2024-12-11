# Clase Interfaz Gráfica

from tkinter import ttk
import tkinter as tk
from Modelos.computador import Computador
class Interfaz:
    def __init__(self, computador):
        self.computador = computador
        self.root = tk.Tk()
        self.root.title("Simulador de Computador")
        self.root.geometry("900x600")  # Ajusta el tamaño de la ventana
        self.root.configure(bg="#f0f0f0")  # Fondo claro
        self.estilo_interfaz()
        self.crear_interfaz()
        self.instrucciones_pendientes = []

    def estilo_interfaz(self):
        # Configurar estilos globales
        estilo = ttk.Style()
        estilo.theme_use("clam")  # Tema moderno
        estilo.configure("TLabel", background="#ccccff", font=("Arial", 10))  # Lila claro
        estilo.configure("TFrame", background="#ffcc99")  # Naranja claro
        estilo.configure("TLabelframe", background="#99ccff", font=("Arial", 12, "bold"))  # Azul claro
        estilo.configure("TLabelframe.Label", background="#99ccff", font=("Arial", 12, "bold"))  # Azul claro
        estilo.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#ffcc00")  # Amarillo
        estilo.configure("TButton", background="#66ff66", font=("Arial", 10))  # Verde claro


    def crear_interfaz(self):
        # Panel de registros
        frame_registros = ttk.LabelFrame(self.root, text="Registros", padding=10)
        frame_registros.grid(row=0, column=0, padx=10, pady=10, sticky="n")
        self.registros_labels = {}
        for i, (nombre, registro) in enumerate(self.computador.registros.items()):
            label = ttk.Label(frame_registros, text=f"{nombre}: {registro.get()}")
            label.grid(row=i, column=0, sticky="w", pady=2)
            self.registros_labels[nombre] = label

        # Panel de componentes principales
        frame_componentes = ttk.LabelFrame(self.root, text="Componentes Principales", padding=10)
        frame_componentes.grid(row=0, column=1, padx=10, pady=10, sticky="n")
        self.componentes_labels = {
            "ALU": ttk.Label(frame_componentes, text=f"ALU: {self.computador.alu.get()}"),
            "PC": ttk.Label(frame_componentes, text=f"PC: {self.computador.pc.get()}"),
            "MAR": ttk.Label(frame_componentes, text=f"MAR: {self.computador.mar.get()}"),
            "MBR": ttk.Label(frame_componentes, text=f"MBR: {self.computador.mbr.get()}"),
            "IR": ttk.Label(frame_componentes, text=f"IR: {self.computador.ir.get()}")
        }
        for i, (nombre, label) in enumerate(self.componentes_labels.items()):
            label.grid(row=i, column=0, sticky="w", pady=2)

        #Panel para el bus del sistema
        frame_bus = ttk.LabelFrame(self.root, text="Bus del Sistema", padding=10)
        frame_bus.grid(row=0, column=3, padx=10, pady=10, sticky="n")
        self.bus_labels = {
            "BusControl": ttk.Label(frame_bus, text=f"Bus de Control: {self.computador.buscontrol.get()}"),
            "BusDatos": ttk.Label(frame_bus, text=f"Bus de Datos: {self.computador.busdatos.get()}"),
            "BusDirecciones": ttk.Label(frame_bus, text=f"Bus de Direcciones: {self.computador.busdirecciones.get()}")
        }
        for i, (nombre, label) in enumerate(self.bus_labels.items()):
            label.grid(row=i, column=0, sticky="w", pady=2)



         # Textos que indican el ciclo de instruccion
        frame_estados = ttk.LabelFrame(self.root, text="Ciclo de Instrucción", padding=10)
        frame_estados.grid(row=0, column=2, padx=10, pady=10, sticky="n")

        self.fetch_label = ttk.Label(frame_estados, text="Fetch")
        self.fetch_label.grid(row=0, column=1, sticky="w", pady=2)
        
        self.decode_label = ttk.Label(frame_estados, text="Decode")
        self.decode_label.grid(row=1, column=1, sticky="w", pady=2)
        
        self.fetch_operando_label = ttk.Label(frame_estados, text="Fetch Operando")
        self.fetch_operando_label.grid(row=2, column=1, sticky="w", pady=2)
        
        self.execute_label = ttk.Label(frame_estados, text="Execute")
        self.execute_label.grid(row=3, column=1, sticky="w", pady=2)

        self.write_label = ttk.Label(frame_estados, text="Write")
        self.write_label.grid(row=4, column=1, sticky="w", pady=2)

        # Panel de memoriaDatos
        frame_memoria = ttk.LabelFrame(self.root, text="Memoria Datos", padding=10)
        frame_memoria.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky="ew")
        self.memoria_tabla = ttk.Treeview(frame_memoria, columns=("Posición", "Valor"), show="headings", height=8)
        self.memoria_tabla.heading("Posición", text="Posición")
        self.memoria_tabla.heading("Valor", text="Valor")
        self.memoria_tabla.pack(fill="both", expand=True)
        self.actualizar_memoriaDatos()

        # Panel de memoriaInstrucciones
        frame_memoria_instrucciones = ttk.LabelFrame(self.root, text="Memoria de Instrucciones", padding=10)
        frame_memoria_instrucciones.grid(row=1, column=2, padx=10, pady=10, columnspan=2, sticky="ew")
        self.memoria_tablaInstrucciones = ttk.Treeview(frame_memoria_instrucciones, columns=("Posición", "Valor"), show="headings", height=8)
        self.memoria_tablaInstrucciones.heading("Posición", text="Posición")
        self.memoria_tablaInstrucciones.heading("Valor", text="Valor")
        self.memoria_tablaInstrucciones.pack(fill="both", expand=True)
        self.actualizar_memoriaInstrucciones()

        # Panel de control
        frame_control = ttk.LabelFrame(self.root, text="Control", padding=10)
        frame_control.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="ew")
        self.instrucciones_text = tk.Text(frame_control, height=5, width=50, font=("Arial", 10))
        self.instrucciones_text.grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(frame_control, text="Ejecutar", command=self.ejecutar_instrucciones).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame_control, text="Nuevo Programa", command=self.nuevo_programa).grid(row=0, column=2, padx=5, pady=5)

    def nuevo_programa(self):
        self.instrucciones_text.delete("1.0", tk.END)
        self.instrucciones_pendientes = []
        self.computador.pc.set(0)
        self.computador.mar.set(0)
        self.computador.mbr.set(0)
        self.computador.ir.set(0)
        self.computador.buscontrol.set(0)
        self.computador.busdatos.set(0)
        self.computador.busdirecciones.set(0)
        self.computador.alu.set(0)
        for registro in self.computador.registros.values():
            registro.set(0)
        for i in range(len(self.computador.memoria.memoriaDatos)):
            self.computador.memoria.escribirDato(i, 0)
        for i in range(len(self.computador.memoria.memoriaInstrucciones)):
            self.computador.memoria.escribirInstruccion(i, 0)

         # Resetear color de todos los ciclos
        self.fetch_label.config(foreground="black")
        self.decode_label.config(foreground="black")
        self.fetch_operando_label.config(foreground="black")
        self.execute_label.config(foreground="black")
        self.write_label.config(foreground="black")

        self.actualizar_interfaz()


    def actualizar_memoriaDatos(self):
        for i in self.memoria_tabla.get_children():
            self.memoria_tabla.delete(i)
        for pos, valor in enumerate(self.computador.memoria.memoriaDatos):
            self.memoria_tabla.insert("", "end", values=(pos, valor))

    def actualizar_memoriaInstrucciones(self):
        for i in self.memoria_tablaInstrucciones.get_children():
            self.memoria_tablaInstrucciones.delete(i)
        for pos, valor in enumerate(self.computador.memoria.memoriaInstrucciones):
            self.memoria_tablaInstrucciones.insert("", "end", values=(pos, valor))

    def iniciar(self):
        self.root.mainloop()

    def ejecutar_instrucciones(self):
        instrucciones = self.instrucciones_text.get("1.0", tk.END).strip().split("\n")
        #Poner instrucciones en la memoria de instrucciones
        for i, instruccion in enumerate(instrucciones):
            self.computador.memoria.escribirInstruccion(i, instruccion)
        self.computador.pc.set(0)
        self.actualizar_memoriaInstrucciones()
        self.instrucciones_pendientes = instrucciones
        longitud = len(instrucciones)
        self.ejecutar_siguiente_instruccion(longitud)


    def fetchInstruccion(self):
        self.computador.fetchInstruccion()

    def decodeInstruccion(self):
        return self.computador.decodeInstruccion()
    
    def fetchOperando(self, fuente):
        return self.computador.fetchOperando(fuente)
    
    def executeInstruccion(self, operacion, destino, fuente, valor, direccion):
        self.computador.ejecutar_instruccion(operacion, destino, fuente, valor, direccion)

    def writeInstruccion(self, operacion, destino, fuente, valor, direccion):
        self.computador.writeBack(operacion, destino, fuente, valor, direccion)


    def ejecutar_siguiente_instruccion(self, longitud):
        if longitud == self.computador.pc.get():
            self.instrucciones_text.delete("1.0", tk.END)
            self.instrucciones_text.insert(tk.END, "Ejecución finalizada con exito")
            self.actualizar_interfaz()
            return
        
        
        if self.instrucciones_pendientes:
            instruccionPC = self.computador.pc.get()
            print(f"Ejecutando instrucción: {self.computador.memoria.leerInstruccion(instruccionPC)}")

            # FETCH DE LA INSTRUCCIÓN
            self.fetchInstruccion()
            #pintar de verde el texto fetch 
            self.cambiar_color_ciclo("fetch")

            self.actualizar_interfaz()

            # Esperar 3 segundos antes de DECODE
            self.root.after(3000, lambda: self.decode_step(longitud))

    def decode_step(self, longitud):
        # DECODE DE LA INSTRUCCIÓN
        operacion, destino, fuente = self.decodeInstruccion()
        self.cambiar_color_ciclo("decode")
        self.actualizar_interfaz()

        # Guardar resultados temporalmente para siguientes pasos
        self.operacion = operacion
        self.destino = destino
        self.fuente = fuente

        # Esperar 3 segundos antes de FETCH OPERANDO
        self.root.after(3000, lambda: self.fetch_operando_step(longitud))

    def fetch_operando_step(self, longitud):
        # FETCH DEL OPERANDO
        valor, direccion = self.fetchOperando(self.fuente)
        self.valor = valor
        self.direccion = direccion
        self.cambiar_color_ciclo("fetch_operando")
        self.actualizar_interfaz()

        # Esperar 3 segundos antes de EXECUTE
        self.root.after(3000, lambda: self.execute_step(longitud))

    def execute_step(self, longitud):
        # EJECUCIÓN DE LA INSTRUCCIÓN
        self.executeInstruccion(self.operacion, self.destino, self.fuente, self.valor, self.direccion)
        self.cambiar_color_ciclo("execute")
        self.actualizar_interfaz()

        # Esperar 3 segundos antes de WRITE
        self.root.after(3000, lambda: self.write_step(longitud))

    def write_step(self, longitud):
        self.writeInstruccion(self.operacion, self.destino, self.fuente, self.valor, self.direccion)
        self.cambiar_color_ciclo("write")

        # Retrasar la ejecución de la siguiente instrucción, si hay más, si no terminar y mostrar mensaje en pantalla
        self.instrucciones_pendientes.pop(0)
        if self.instrucciones_pendientes:
            self.actualizar_interfaz()
            self.root.after(3000, lambda: self.ejecutar_siguiente_instruccion(longitud))
        else:
            self.instrucciones_text.delete("1.0", tk.END)
            self.instrucciones_text.insert(tk.END, "Ejecución finalizada con exito")
            self.actualizar_interfaz()

    def actualizar_interfaz(self):
        # Actualizar registros
        for nombre, registro in self.computador.registros.items():
            print(nombre, registro.get())
            self.registros_labels[nombre].config(text=f"{nombre}: {registro.get()}")
        # Actualizar componentes principales
        for nombre, componente in self.componentes_labels.items():
            componente.config(text=f"{nombre}: {getattr(self.computador, nombre.lower()).get()}")

        # Actualizar bus del sistema
        for nombre, bus in self.bus_labels.items():
            bus.config(text=f"{nombre}: {getattr(self.computador, nombre.lower()).get()}")

        # Actualizar memoria
        self.actualizar_memoriaDatos()
        self.actualizar_memoriaInstrucciones()


    def cambiar_color_ciclo(self, ciclo):
        # Resetear color de todos los ciclos
        self.fetch_label.config(foreground="black")
        self.decode_label.config(foreground="black")
        self.fetch_operando_label.config(foreground="black")
        self.execute_label.config(foreground="black")
        self.write_label.config(foreground="black")

        # Cambiar color basado en la fase actual
        if ciclo == "fetch":
            self.fetch_label.config(foreground="blue")
        elif ciclo == "decode":
            self.decode_label.config(foreground="green")
        elif ciclo == "fetch_operando":
            self.fetch_operando_label.config(foreground="orange")
        elif ciclo == "execute":
            self.execute_label.config(foreground="red")
        elif ciclo == "write":
            self.write_label.config(foreground="purple")

    