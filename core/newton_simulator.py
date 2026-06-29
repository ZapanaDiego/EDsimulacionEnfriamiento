import logging
import numpy as np
from scipy.integrate import solve_ivp
from .base_simulator import BaseSimulator

class NewtonSimulator(BaseSimulator):
    """
    Implementación del Modelo Lineal (Ley de Enfriamiento de Newton).
    Hereda de BaseSimulator e implementa los métodos abstractos.
    dT/dt = -k * (T - T_ambient)
    """

    def get_derivatives(self, t, T):
        """
        Define la ecuación diferencial ordinaria (EDO) de Newton.
        """
        k = self.config.cooling_constant_k
        T_a = self.config.T_ambient
        
        dT_dt = -k * (T - T_a)
        return dT_dt

    def solve_equation(self):
        """
        Utiliza scipy.integrate.solve_ivp para resolver la EDO numéricamente.
        """
        logging.info("Iniciando integración numérica (Newton).")
        try:
            # Definir el rango de tiempo y las condiciones iniciales
            t_span = (self.config.time_start, self.config.time_end)
            t_eval = np.linspace(self.config.time_start, self.config.time_end, self.config.num_points)
            y0 = [self.config.T_initial_cpu]
            dt = (self.config.time_end - self.config.time_start) / self.config.num_points
            
            logging.info(f"--- Parámetros Físicos Newton ---")
            logging.info(f"T_cpu inicial: {self.config.T_initial_cpu}°C")
            logging.info(f"T_ambient: {self.config.T_ambient}°C")
            logging.info(f"Constante k1: {self.config.cooling_constant_k}")
            logging.info(f"Tiempo total: {self.config.time_end}s, dt ~ {dt:.3f}s")
    
            # Resolver la ecuación
            # solve_ivp requiere una función con firma f(t, y)
            solution = solve_ivp(
                fun=self.get_derivatives,
                t_span=t_span,
                y0=y0,
                t_eval=t_eval,
                method='RK45' # Método de Runge-Kutta de orden 4(5) (estándar)
            )
            
            logging.info(f"--- Auditoría SciPy (Newton) ---")
            logging.info(f"Success: {solution.success}")
            logging.info(f"Mensaje: {solution.message}")
            logging.info(f"Evaluaciones de función (nfev): {solution.nfev}")
    
            if solution.success:
                if np.isnan(solution.y).any():
                    raise ValueError("Se detectaron valores NaN en la solución.")
                self.times = solution.t
                self.temperatures = solution.y[0] # y es un array 2D, tomamos la primera fila
                
                logging.info(f"--- Estadísticos de Salida (Newton) ---")
                logging.info(f"Shape t: {self.times.shape}, Shape T: {self.temperatures.shape}")
                logging.info(f"Temp. Máxima: {np.max(self.temperatures):.2f}°C")
                logging.info(f"Temp. Mínima: {np.min(self.temperatures):.2f}°C")
                logging.info(f"Primeros 5 puntos (t, T): {list(zip(np.round(self.times[:5], 2), np.round(self.temperatures[:5], 2)))}")
                logging.info(f"Últimos 5 puntos (t, T): {list(zip(np.round(self.times[-5:], 2), np.round(self.temperatures[-5:], 2)))}")
                logging.info(f"Integración numérica (Newton) completada con éxito. Puntos: {len(self.times)}")
            else:
                raise RuntimeError(f"Fallo al resolver la EDO: {solution.message}")
        except Exception as e:
            logging.error(f"Error crítico en la integración (Newton): {str(e)}", exc_info=True)
            raise
