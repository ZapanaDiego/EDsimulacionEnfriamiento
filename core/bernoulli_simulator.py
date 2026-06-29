import logging
import numpy as np
from scipy.integrate import solve_ivp
from .base_simulator import BaseSimulator

class BernoulliSimulator(BaseSimulator):
    """
    Implementación del Modelo Avanzado (Ecuación de Bernoulli).
    Modela enfriamiento turbulento/convección forzada.
    dT/dt = -k1*(T - T_m) - k2*(T - T_m)^n
    """

    def get_derivatives(self, t, T):
        """
        Define la ecuación diferencial no lineal de Bernoulli.
        """
        k1 = self.config.cooling_constant_k
        n = self.config.bernoulli_n
        T_m = self.config.T_ambient
        
        # Calcular k2 dinámico acoplando las variables atmosféricas
        viento = self.config.V_air
        humedad = self.config.humidity_H
        sesgo = self.config.sensor_Knb
        k2 = (viento * (1.0 + humedad / 100.0) * sesgo) / 10000.0
        
        # np.maximum evita evaluar bases negativas con exponentes fraccionarios
        # en caso de inestabilidades numéricas donde T cae por debajo de T_m
        diff = np.maximum(T - T_m, 0.0)
        
        dT_dt = -k1 * diff - k2 * (diff ** n)
        return dT_dt

    def solve_equation(self):
        """
        Utiliza scipy.integrate.solve_ivp para resolver la EDO numéricamente.
        """
        logging.info("Iniciando integración numérica (Bernoulli).")
        try:
            t_span = (self.config.time_start, self.config.time_end)
            t_eval = np.linspace(self.config.time_start, self.config.time_end, self.config.num_points)
            y0 = [self.config.T_initial_cpu]
            dt = (self.config.time_end - self.config.time_start) / self.config.num_points
            
            logging.info(f"--- Parámetros Físicos Bernoulli ---")
            logging.info(f"T_cpu inicial: {self.config.T_initial_cpu}°C")
            logging.info(f"T_ambient: {self.config.T_ambient}°C")
            logging.info(f"Constante k1: {self.config.cooling_constant_k}")
            
            # Calcular k2 dinámico para el log
            viento = self.config.V_air
            humedad = self.config.humidity_H
            sesgo = self.config.sensor_Knb
            k2_dynamic = (viento * (1.0 + humedad / 100.0) * sesgo) / 10000.0
            
            logging.info(f"Constante k2 dinámica: {k2_dynamic:.6f}")
            logging.info(f"Exponente n: {self.config.bernoulli_n}")
            logging.info(f"Velocidad Viento: {viento} m/s, Humedad: {humedad}%, Sesgo: {sesgo}")
            logging.info(f"Tiempo total: {self.config.time_end}s, dt ~ {dt:.3f}s")
    
            solution = solve_ivp(
                fun=self.get_derivatives,
                t_span=t_span,
                y0=y0,
                t_eval=t_eval,
                method='RK45'
            )
            
            logging.info(f"--- Auditoría SciPy (Bernoulli) ---")
            logging.info(f"Success: {solution.success}")
            logging.info(f"Mensaje: {solution.message}")
            logging.info(f"Evaluaciones de función (nfev): {solution.nfev}")
    
            if solution.success:
                if np.isnan(solution.y).any():
                    raise ValueError("Se detectaron valores NaN en la solución.")
                self.times = solution.t
                self.temperatures = solution.y[0]
                
                logging.info(f"--- Estadísticos de Salida (Bernoulli) ---")
                logging.info(f"Shape t: {self.times.shape}, Shape T: {self.temperatures.shape}")
                logging.info(f"Temp. Máxima: {np.max(self.temperatures):.2f}°C")
                logging.info(f"Temp. Mínima: {np.min(self.temperatures):.2f}°C")
                logging.info(f"Primeros 5 puntos (t, T): {list(zip(np.round(self.times[:5], 2), np.round(self.temperatures[:5], 2)))}")
                logging.info(f"Últimos 5 puntos (t, T): {list(zip(np.round(self.times[-5:], 2), np.round(self.temperatures[-5:], 2)))}")
                logging.info(f"Integración numérica (Bernoulli) completada con éxito. Puntos: {len(self.times)}")
            else:
                raise RuntimeError(f"Fallo al resolver la EDO de Bernoulli: {solution.message}")
        except Exception as e:
            logging.error(f"Error crítico en la integración (Bernoulli): {str(e)}", exc_info=True)
            raise
