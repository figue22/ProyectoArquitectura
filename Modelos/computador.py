# Clase Computador
from Modelos.alu import ALU
from Modelos.registro import Registro
from Modelos.memoria import Memoria
from Modelos.unidadControl import UnidadControl
from Modelos.bus import Bus



class Computador:
    def __init__(self):
        self.registros = {f"R{i}": Registro(f"R{i}") for i in range(4)}
        self.pc = Registro("PC")
        self.mar = Registro("MAR")
        self.mbr = Registro("MBR")
        self.ir = Registro("IR")
        self.memoria = Memoria(256)
        self.alu = ALU()
        self.busdatos = Bus("busdatos")
        self.busdirecciones = Bus("busdirecciones")
        self.buscontrol = Bus("buscontrol")
        self.unidad_control = UnidadControl(self.pc, self.mar, self.mbr, self.ir, self.registros, self.memoria, self.alu, self.buscontrol, self.busdatos, self.busdirecciones)


    def fetchInstruccion(self):
        self.unidad_control.fetchInstruccion()

    def decodeInstruccion(self):
        return self.unidad_control.decodeInstruccion()
    
    def fetchOperando(self, fuente):
        return self.unidad_control.fetchOperando(fuente)
    
    def ejecutar_instruccion(self, operacion, destino, fuente, valor, direccion):
        self.unidad_control.executeInstruccion(operacion, destino, fuente, valor, direccion)

    def writeBack(self, operacion, destino, fuente, valor, direccion):
        self.unidad_control.writeBack(operacion, destino, fuente, valor, direccion)


    def estado_actual(self):
        estado = "Estado del Computador\n"
        estado += f"PC: {self.pc.get()}\n"
        estado += f"MAR: {self.mar.get()}, MBR: {self.mbr.get()}, IR: {self.ir.get()}\n"
        estado += "Registros:\n"
        for nombre, registro in self.registros.items():
            estado += f"  {nombre}: {registro.get()}\n"
        estado += "Memoria:\n"
        for i, valor in enumerate(self.memoria.datos):
            if valor != 0:  # Solo muestra posiciones de memoria no vacías
                estado += f"  Dirección {i}: {valor}\n"
        estado += "------\n"
        return estado
