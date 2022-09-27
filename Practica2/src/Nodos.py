import Canales
import math
import simpy

BACK_YES_MSG = "BACK_YES"
BACK_NO_MSG = "BACK_NO"
GO_MSG = "GO"

class Nodo:
    """Representa un nodo basico.

    Atributos:
    id_nodo -- identificador del nodo
    vecinos -- lista con los ids de nuestros vecinos
    canales -- tupla de la forma (canal_entrada, canal_salida)
    """
    def __init__(self, id_nodo: int, vecinos: list, canales: tuple):
        """Constructor basico de un Nodo."""
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canales = canales

    def __str__(self):
        """Regresa la representacion en cadena del nodo."""
        return f"Nodo: {self.id_nodo}, vecinos: {self.vecinos}, canales: {self.canales}"
    
    def get_id(self) -> int:
        """Regresa el identificador del nodo."""
        return self.id_nodo
    
    def get_vecinos(self) -> list:
        """Regresa la lista de vecinos del nodo."""
        return self.vecinos

    def get_canal_entrada(self) -> simpy.Store:
        """Regresa el canal de entrada del nodo."""
        return self.canales[0]

    def get_canal_salida(self) -> Canales.Canal:
        """Regresa el canal de salida del nodo."""
        return self.canales[1]

class NodoBFS(Nodo):
    """Nodo que implementa el algoritmo del ejercicio 1.

    Atributos adicionales:
    padre -- id del nodo que sera su padre en el arbol
    nivel -- entero que representa la distancia del nodo a la raiz
    hijos -- lista de ids de los nodos hijos del nodo
    msjs_esperados -- numero de mensajes que espera el nodo
    """
    def __init__(self, id_nodo: int, vecinos: list, canales: tuple):
        """Constructor para el nodo 'bfs'."""
        super().__init__(id_nodo, vecinos, canales)
        self.nivel = math.inf
        self.padre = None
        self.hijos = []
    

    def bfs(self, env: simpy.Environment):
        """Algoritmo de BFS."""
        if self.id_nodo == 0:
            self.padre = self.id_nodo
            self.nivel = 0
            self.msjs_esperados = len(self.vecinos)
            
            mensaje = (GO_MSG, self.nivel, self.id_nodo)
            yield env.timeout(1)
            
            self.canales[1].envia(mensaje, self.vecinos)
            
        while True:
            msg, d, mensajero = yield self.canales[0].get()
            
            if msg == GO_MSG:
                if self.nivel > d+1:
                    self.padre = mensajero
                    self.nivel = d+1
                    
                    expect_msg_list = [v for v in self.vecinos if v != mensajero]
                    self.msjs_esperados = len(expect_msg_list)
                    
                    if self.msjs_esperados == 0: # Caso en el que es hoja
                        mensaje = (BACK_YES_MSG, self.nivel, self.id_nodo)
                        self.canales[1].envia(mensaje, [self.padre])
                    else:
                        mensaje = (GO_MSG, d+1, self.id_nodo)
                        self.canales[1].envia(mensaje, expect_msg_list)
                        
                else:
                    mensaje = (BACK_NO_MSG, d+1, self.id_nodo)
                    self.canales[1].envia(mensaje, [mensajero])
                    
            else:
                if d == self.nivel+1:
                    if msg == BACK_YES_MSG:
                        self.hijos.append(mensajero)
                        
                    self.msjs_esperados -=1
                    
                    if self.msjs_esperados == 0:
                        if self.padre != self.id_nodo:
                            mensaje = (BACK_YES_MSG, self.nivel, self.id_nodo)
                            self.canales[1].envia(mensaje, [self.padre])
                    
                    
                        
                        
                        
                        

            
                    
                    
                    
                    
                    
                        
                        
                        
                        
                        
                        
                
                
                
                
                
                