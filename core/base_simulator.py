from abc import ABC, abstractmethod
import numpy as np

class BaseSimulator(ABC):
    """
    Clase abstracta que define el contrato (interfaz) para cualquier simulador de enfriamiento.
    Esta arquitectura permite el Principio de Abierto/Cerrado (SOLID): el sistema está abierto
    a la extensión (ej. agregar BernoulliSimulator) pero cerrado a la modificación.
    """
    
    def __init__(self, config):
        """
        Inicializa el simulador con la configuración provista.
        Se usa inyección de dependencias para que el simulador no esté fuertemente acoplado
        a variables globales.
        """
        self.config = config
        # Aquí almacenaremos los resultados de la simulación
        self.times = np.array([])
        self.temperatures = np.array([])

    @abstractmethod
    def get_derivatives(self, t, T):
        """
        Método abstracto para definir la Ecuación Diferencial (dT/dt).
        Cada modelo matemático específico deberá implementar su propia ecuación.
        """
        pass

    @abstractmethod
    def solve_equation(self):
        """
        Resuelve la ecuación diferencial a lo largo del tiempo definido en la configuración.
        """
        pass

    def get_results(self):
        """
        Método común para todos los simuladores. Retorna los resultados.
        No es abstracto porque la lógica de devolver datos es la misma para todos.
        """
        if len(self.times) == 0 or len(self.temperatures) == 0:
            raise ValueError("La simulación no ha sido resuelta aún. Llama a solve_equation() primero.")
        return self.times, self.temperatures
