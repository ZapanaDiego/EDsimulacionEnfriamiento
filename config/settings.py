from dataclasses import dataclass

@dataclass
class SimulationConfig:
    """
    Configuración central de la simulación.
    Usar un dataclass permite tener una estructura inmutable o fácilmente instanciable
    con valores por defecto, facilitando inyectar dependencias en los simuladores.
    """
    T_ambient: float = 25.0       # Temperatura ambiente en grados Celsius
    T_initial_cpu: float = 90.0   # Temperatura inicial de la CPU al apagarse
    cooling_constant_k: float = 0.05 # Constante de enfriamiento k (Ley de Newton)
    cooling_constant_k2: float = 0.005 # Constante de acoplamiento no lineal k2 (Turbulencia)
    
    # Nuevas variables Bernoulli solicitadas
    bernoulli_n: float = 1.5      # Escala de turbulencia (Exponente n de Bernoulli)
    V_air: float = 5.0            # Velocidad Máxima del Viento
    humidity_H: float = 50.0      # Humedad
    sensor_Knb: float = 1.0       # Sesgo del Sensor Nano Banana
    
    time_start: float = 0.0       # Tiempo inicial de la simulación (segundos)
    time_end: float = 300.0       # Tiempo final de la simulación (segundos)
    num_points: int = 1000        # Número de puntos para la resolución de la ED
