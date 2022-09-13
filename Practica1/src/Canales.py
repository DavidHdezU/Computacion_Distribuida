import simpy


class Canal():
    """Clase Abstracta que modela el comportamiento que cualquier canal debe 
    tomar."""

    def __init__(self, env: simpy.Environment, capacidad):
        """Constructor de la clase."""
        self.env = env
        self.capacidad = capacidad
        self.canales = []

    def envia(self, mensaje, vecinos):
        """Metodo abstracto.
        
        Envia un mensaje a los canales de entrada de los vecinos.
        """
        pass

    def crea_canal_de_entrada(self) -> simpy.Store:
        """Creamos un objeto Store en el un nodo recibirá los mensajes."""
        canal = simpy.Store(self.env, capacity=self.capacidad)
        self.canales.append(canal)
        return canal

    def get_canales(self) -> list:
        """Regresa la lista con los canales."""
        return self.canales


class CanalGeneral(Canal):
    """Implementacion de un canal para el caso general."""

    def envia(self, mensaje, vecinos):
        """Envia un mensaje a los canales de entrada de los vecinos."""
        eventos = []
        
        for i in range(len(self.canales)):
            if i in vecinos:
                eventos.append(self.canales[i].put(mensaje))
                
        return self.env.all_of(events=eventos)
        
        