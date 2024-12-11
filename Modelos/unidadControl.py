# Clase Unidad de Control
import time
class UnidadControl:
    def __init__(self, pc, mar, mbr, ir, registros, memoria, alu, busControl, busDatos, busDirecciones):
        self.pc = pc
        self.mar = mar
        self.mbr = mbr
        self.ir = ir
        self.registros = registros
        self.memoria = memoria
        self.alu = alu
        self.busControl = busControl 
        self.busDatos = busDatos
        self.busDirecciones = busDirecciones


    def fetchInstruccion(self):
        #tomar el valor del PC que es la direccion de la proxima instruccion
        direccion = self.pc.get() #Se obtiene la direccion de memoria donde se encuentra la instruccion a ejecutar
        print(f"EL PC TIENE {direccion}")
      
        #la direccion del pc se carga en el MAR
        self.mar.set(direccion)
        print(f"EL MAR TIENE {self.mar.get()}")

        self.busDirecciones.set(self.mar.get()) #Se coloca en el bus de direcciones la Direccion de memoria donde se encuentra la instruccion a ejecutar (lo que tiene la MAR)
        print(f"EL BUS DE DIRECCIONES TIENE {self.busDirecciones.get()}")

        self.busControl.set("READ") #Se coloca en el bus de control la señal de lectura para que la memoria lea la instruccion
        print(f"EL BUS DE CONTROL TIENE {self.busControl.get()}")


        #enviar señal al bus de direcciones con la direccion para buscar la instruccion en memoria
        if self.busControl.get() == "READ":
            self.busDatos.set(self.memoria.leerInstruccion(direccion)) #Se coloca la instruccion en el bus de datos
            instruccion = self.busDatos.get() #Se obtiene la instruccion del bus de datos

        if instruccion is None:
            raise ValueError(f"La dirección {direccion} no contiene una instrucción válida")
            
        print(f"LA INSTRUCCION ES {instruccion}")

        #el dato leido se carga en el MBR
        self.mbr.set(instruccion)
        print(f"EL MBR TIENE {self.mbr.get()}")

        #enviar la instruccion al IR (se copia el contenido del MBR al IR)
        self.ir.set(instruccion)
        print(f"EL IR TIENE {self.ir.get()}")

        #incrementar el PC para apuntar a la siguiente instruccion
        self.pc.set(direccion + 1)
        print(f"EL PC TIENE {self.pc.get()}")


    def decodeInstruccion(self):
        #obtener la instruccion del IR
        instruccion = self.ir.get()

        #decodificar la instruccion
        partes = instruccion.split()
        operacion = partes[0]
        
        destino = partes[1]

        fuente = partes[2] if len(partes) > 2 else None


        return operacion, destino, fuente
    

    def fetchOperando(self, fuente):
        # Decodificar el modo de direccionamiento
        if fuente is not None:
            if fuente.startswith("#"):  # Direccionamiento inmediato
                valor = int(fuente[1:])
                direccion = None
            elif fuente.startswith("@"):  # Direccionamiento indirecto
                direccion1 = int(fuente[1:])
                direccion = self.memoria.leerDato(direccion1)
                valor = self.memoria.leerDato(self.memoria.leerDato(direccion1))
            elif fuente.isdigit():  # Direccionamiento directo
                direccion = int(fuente)
                valor = self.memoria.leerDato(direccion)
            elif fuente.startswith("%"):  # Direccionamiento basado en registro
                valor = self.registros[fuente[1:]].get()
                direccion = None
        else:
            valor = None
            direccion = None

        return valor, direccion
    

    def executeInstruccion(self, operacion, destino, fuente, valor, direccion):
        # Ejecución de la instrucción según su tipo
        if operacion == "MOV": #MOV: mueve un valor a un registro o a una direccion de memoria
                if direccion is not None:
                    self.mar.set(direccion)
                    self.busDirecciones.set(self.mar.get())

                    self.busControl.set("READ")

                    self.busDatos.set(valor)
                    self.mbr.set(self.busDatos.get())
                else:
                    self.mbr.set(valor)
                    
                    #self.memoria.escribirDato(int(destino), int(valor))

        elif operacion == "LOAD": #LOAD: carga un valor de una direccion de memoria a un registro
                if direccion is not None:
                    self.mar.set(direccion)
                    self.busDirecciones.set(self.mar.get())

                    self.busControl.set("READ")

                    self.busDatos.set(self.memoria.leerDato(direccion))
                    self.mbr.set(self.busDatos.get())   
                else:
                    #self.busDatos.set(valor)
                    self.mbr.set(valor)

                #self.registros[destino].set(valor)

        elif operacion == "STORE": #STORE: guarda un valor de un registro en una direccion de memoria
                if direccion is not None:
                    self.mar.set(direccion)
                    self.busDirecciones.set(self.mar.get())

                    self.busControl.set("READ")

                    self.busDatos.set(valor)
                    self.mbr.set(self.busDatos.get())
                else:
                    self.mbr.set(valor)
            
                #self.memoria.escribirDato(direccion, self.registros[fuente].get())

        elif operacion in {"ADD", "SUB", "MUL", "DIV", "AND", "OR", "NOT", "XOR"}: #operaciones aritmeticas Y logicas
                if direccion is not None:
                    self.mar.set(direccion)
                    self.busDirecciones.set(self.mar.get())

                    self.busControl.set("READ")

                    self.busDatos.set(valor)
                    self.mbr.set(self.busDatos.get())
                    
                    resultado = self.alu.operar(operacion, self.registros[destino].get(), valor)

                    self.alu.set(resultado)
                else:
                    self.mbr.set(valor)

                    resultado = self.alu.operar(operacion, self.registros[destino].get(), valor)
                    self.alu.set(resultado)

                #self.registros[destino].set(resultado)

        elif operacion == "JMP": #JMP: salto incondicional
                self.pc.set(int(destino))

        else:
                raise ValueError(f"Instrucción no reconocida: {operacion}")
        

        return operacion, destino, fuente, valor, direccion
    


    def writeBack(self, operacion, destino, fuente, valor, direccion):
        if operacion == "MOV":
            if destino not in self.registros:
                self.mar.set(destino)
                self.busDirecciones.set(self.mar.get())

                self.busControl.set("WRITE")

                self.busDatos.set(valor)
                self.mbr.set(self.busDatos.get())

                self.memoria.escribirDato(int(destino), valor)

            else:
                self.mar.set(destino)
                self.busDirecciones.set(0)

                self.busControl.set(0)

                self.busDatos.set(0)
                self.mbr.set(valor)
                self.registros[destino].set(valor)
               

        elif operacion == "LOAD":
            if destino not in self.registros:
                self.mar.set(destino)
                self.busDirecciones.set(self.mar.get())

                self.busControl.set("WRITE")

                self.busDatos.set(valor)
                self.mbr.set(self.busDatos.get())

                self.memoria.escribirDato(int(destino), valor)
            
            else:
                self.mar.set(destino)
                self.busDirecciones.set(0)

                self.busControl.set(0)

                self.busDatos.set(0)
                self.mbr.set(valor)

                self.registros[destino].set(valor)

        elif operacion == "STORE":
            if destino not in self.registros:
                direccion = int(destino)
                self.mar.set(direccion)
                self.busDirecciones.set(self.mar.get())

                self.busControl.set("WRITE")

                self.busDatos.set(valor)
                self.mbr.set(self.busDatos.get())

                self.memoria.escribirDato(direccion, valor)

            else:

                self.mar.set(direccion)
                self.busDirecciones.set(0)

                self.busControl.set(0)

                self.busDatos.set(0)
                self.mbr.set(valor)

                self.registros[destino].set(valor)

        elif operacion in {"ADD", "SUB", "MUL", "DIV", "AND", "OR", "NOT", "XOR"}:
            if destino not in self.registros:
        
                self.mar.set(destino)
                self.busDirecciones.set(self.mar.get())

                self.busControl.set("WRITE")

                self.busDatos.set(valor)

                self.mbr.set(self.busDatos.get())

                resultado = self.alu.operar(operacion, self.memoria.leerDato(int(destino)), valor)
                self.alu.set(resultado)

                self.memoria.escribirDato(int(destino), resultado)

            else:
                self.mar.set(destino)
                self.busDirecciones.set(0)

                self.busControl.set(0)

                self.busDatos.set(0)
                self.mbr.set(valor)

                resultado = self.alu.operar(operacion, self.registros[destino].get(), valor)
                self.alu.set(resultado)
                self.registros[destino].set(resultado)

        elif operacion == "JMP":
            pass

        else:
            raise ValueError(f"Instrucción no reconocida: {operacion}")
        



        
        
             
             

    


        
