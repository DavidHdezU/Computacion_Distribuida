import simpy


class Canal():
    """Clase Abstracta que modela el comportamiento que cualquier canal debe 
    tomar."""

    def __init__(self, env: simpy.Environment, capacidad=simpy.core.Infinity):
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
        raise NotImplementedError('Get_canales de Canal no implementado')


class CanalGeneral(Canal):
    """Implementacion de un canal para el caso general."""

    def envia(self, mensaje, vecinos):
        """Envia un mensaje a los canales de entrada de los vecinos."""
        raise NotImplementedError('Envia de CanalGeneral no implementado')