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
        # Definir el rango de tiempo y las condiciones iniciales
        t_span = (self.config.time_start, self.config.time_end)
        t_eval = np.linspace(self.config.time_start, self.config.time_end, self.config.num_points)
        y0 = [self.config.T_initial_cpu]

        # Resolver la ecuación
        # solve_ivp requiere una función con firma f(t, y)
        solution = solve_ivp(
            fun=self.get_derivatives,
            t_span=t_span,
            y0=y0,
            t_eval=t_eval,
            method='RK45' # Método de Runge-Kutta de orden 4(5) (estándar)
        )

        if solution.success:
            self.times = solution.t
            self.temperatures = solution.y[0] # y es un array 2D, tomamos la primera fila
        else:
            raise RuntimeError(f"Fallo al resolver la EDO: {solution.message}")
