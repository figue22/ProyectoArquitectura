# Clase ALU
class ALU:
    def __init__(self):
        self.operacion = None
        self.op1 = None
        self.op2 = None
        self.resultado = 0



    def operar(self, operacion, op1, op2):
        if operacion == "ADD":
            self.operacion = operacion
            self.op1 = op1
            self.op2 = op2
            self.resultado = op1 + op2
            return self.resultado
        
        elif operacion == "SUB":
            self.operacion = operacion
            self.op1 = op1
            self.op2 = op2
            self.resultado = op1 - op2
            return self.resultado
        
        elif operacion == "MUL":
            self.operacion = operacion
            self.op1 = op1
            self.op2 = op2
            self.resultado = op1 * op2
            return self.resultado
        
        elif operacion == "DIV":
            self.operacion = operacion
            self.op1 = op1
            self.op2 = op2
            self.resultado = op1 // op2
            return self.resultado
    
        elif operacion == "AND":
            self.operacion = operacion
            self.op1 = op1
            self.op2 = op2
            self.resultado = op1 & op2
            return self.resultado
        
        elif operacion == "OR":
            self.operacion = operacion
            self.op1 = op1
            self.op2 = op2
            self.resultado = op1 | op2
            return self.resultado
    
        
        elif operacion == "NOT":
            self.operacion = operacion
            self.op1 = op1
            self.op2 = None
            self.resultado = ~op1
            return self.resultado
        
        elif operacion == "XOR":
            self.operacion = operacion
            self.op1 = op1
            self.op2 = op2
            self.resultado = op1 ^ op2
            return self.resultado
        
        else:
            raise ValueError("Operación no válida")
        

    def getOperacion(self):
        return self.operacion
    
    def getOp1(self):
        return self.op1
    
    def getOp2(self):
        return self.op2
    
    def get(self):
        return self.resultado
    
    def set(self, resultado):
        self.resultado = resultado
    

        