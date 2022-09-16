import Canales
import simpy


BACK_MSG = "BACK"
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


class NodoVecinos(Nodo):
    """Nodo que implementa el algoritmo del ejercicio 1.

    Atributos adicionales:
    vecinos_de_vecinos -- lista con los ids de los vecinos de nuestros vecinos
    """
    def __init__(self, id_nodo: int, vecinos: list, canales: tuple):
        """Constructor para el nodo 'vecinos'."""
        super().__init__(id_nodo, vecinos, canales)
        self.vecinos_de_vecinos = []

    def conoce_vecinos(self, env: simpy.Environment):
        """Algoritmo para conocer a los vecinos de mis vecinos."""
        self.canales[1].envia(self.vecinos, self.vecinos)

        while True:
            vecinos_de_v = yield self.canales[0].get()
            for v in vecinos_de_v:
                if self.vecinos_de_vecinos.count(v) == 0:
                    self.vecinos_de_vecinos.append(v)

class NodoArbolGenerador(Nodo):
    """Nodo que implementa el algoritmo del ejercicio 2.

    Atributos adicionales:
    madre -- id del nodo madre dentro del arbol
    hijas -- lista de nodos hijas del nodo actual
    """
    def __init__(self, id_nodo: int, vecinos: list, canales: tuple):
        """Constructor para el nodo arbol generador."""
        super().__init__(id_nodo, vecinos, canales)

        

    def genera_arbol(self, env: simpy.Environment):
        """Algoritmo para producir el arbol generador."""
        
        if self.id_nodo == 0:
            self.padre = self.id_nodo
            self.msg_expected = len(self.vecinos) 
            
            mensaje = (GO_MSG, self.id_nodo, None) # Tipo de mensaje, mensajero, val_set
            
            yield env.timeout(1)
            
            self.canales[1].envia(mensaje, self.vecinos) # Para este caso el canal de salida no es de tipo simpy.Store, creemos que esto esto es confuso
        else:
            self.padre = None
        
        self.hijos = set()
        
        while True:
            msg, mensajero, val_set = yield self.canales[0].get()
            yield env.timeout(1)
            
            if msg == GO_MSG:
                if self.padre is None:
                    self.padre = mensajero
                    self.msg_expected = len(self.vecinos)-1
                    
                    if self.msg_expected == 0:
                        mensaje = (BACK_MSG, self.id_nodo, self.id_nodo)

                        self.canales[1].envia(mensaje, [mensajero])
                
                    else:
                        mensaje = (GO_MSG, self.id_nodo, None)
                        destinatarios = [v for v in self.vecinos if v != mensajero]
                        
                        self.canales[1].envia(mensaje, destinatarios)
                        
                else:
                    mensaje = (BACK_MSG, self.id_nodo, None)
                    self.canales[1].envia(mensaje, [mensajero])
            
            else: # Recibimos BACK
                self.msg_expected -= 1
                
                if val_set is not None:
                    self.hijos.add(mensajero)
                    
                if self.msg_expected == 0:
                    if self.padre != self.id_nodo: # Checar si no es el nodo distinguido
                        mensaje = (BACK_MSG, self.id_nodo, self.id_nodo)
                        
                        self.canales[1].envia(mensaje, [self.padre])


class NodoBroadcast(Nodo):
    """Nodo que implementa el algoritmo del ejercicio 3.

    Atributos adicionales:
    mensaje -- cadena con el mensaje que se distribuye
    """
    def __init__(self, id_nodo: int, vecinos: list, canales: tuple):
        """Constructor para el nodo broadcast."""
        
        super().__init__(id_nodo, vecinos, canales)

    def broadcast(self, env: simpy.Environment):
        """Algoritmo de broadcast."""
        
        if self.id_nodo == 0:
            self.mensaje = "Hello"
            
            yield env.timeout(1)
            self.canales[1].envia(self.mensaje, self.vecinos)
            
        else:
            self.mensaje = None
            
        while True:
            self.mensaje = yield self.canales[0].get()
            
            self.canales[1].envia(self.mensaje, self.vecinos)

class NodoConvergecast(Nodo):
    """Nodo que implementa el algoritmo convergecast.

    Atributos adicionales:
    value -- valor que el nodo quiere hacer llegar al nodo distinguido
    """
    def __init__(self, id_nodo: int, vecinos: list, canales: tuple):
        """Constructor para el nodo broadcast."""
        
        super().__init__(id_nodo, vecinos, canales)
        self.value = self.id_nodo
        self.padre = None

    def convergecast(self, env: simpy.Environment):
        """Algoritmo de convergecast."""
        
        if self.id_nodo == 0: 
            self.padre = self.id_nodo
            
            yield env.timeout(1)
            self.canales[1].envia(("MSG_PADRE", self.id_nodo), self.vecinos)
            
        while True:
            mensaje = yield self.canales[0].get()

            if(mensaje[0] == "MSG_PADRE"): ## Mensaje que ayuda a que los nodos hijos conozcan a su padre
                self.padre = mensaje[1]
                

                if self.vecinos: ## Si el nodo no es hoja se manda a sus hijos su identidad para que conozcan a su padre
                    nuevo_mensaje = ("MSG_PADRE", self.id_nodo)
                    self.canales[1].envia(nuevo_mensaje, self.vecinos)

                else: ## Nodo hoja comienza a mandar el valor para el convergecast a su padre
                    nuevo_mensaje = ("MSG_VALUE", self.value)
                    self.canales[1].envia(nuevo_mensaje, [self.padre])
            
            else: ## Mensaje convergecast
                if self.padre != self.id_nodo: # Si no es la raiz manda valor para el convergecast al padre
                    self.value = mensaje[1] + self.value
                    nuevo_mensaje = ("MSG_VALUE", self.value)
                    self.canales[1].envia(nuevo_mensaje, [self.padre])
                else: # Si es la raiz actualiza su valor con la informacion recibida y termina entonces el convergecast
                    self.value = mensaje[1] + self.value
