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
        k2 = self.config.cooling_constant_k2
        n = self.config.bernoulli_n
        T_m = self.config.T_ambient
        
        # np.maximum evita evaluar bases negativas con exponentes fraccionarios
        # en caso de inestabilidades numéricas donde T cae por debajo de T_m
        diff = np.maximum(T - T_m, 0.0)
        
        dT_dt = -k1 * diff - k2 * (diff ** n)
        return dT_dt

    def solve_equation(self):
        """
        Utiliza scipy.integrate.solve_ivp para resolver la EDO numéricamente.
        """
        t_span = (self.config.time_start, self.config.time_end)
        t_eval = np.linspace(self.config.time_start, self.config.time_end, self.config.num_points)
        y0 = [self.config.T_initial_cpu]

        solution = solve_ivp(
            fun=self.get_derivatives,
            t_span=t_span,
            y0=y0,
            t_eval=t_eval,
            method='RK45'
        )

        if solution.success:
            self.times = solution.t
            self.temperatures = solution.y[0]
        else:
            raise RuntimeError(f"Fallo al resolver la EDO de Bernoulli: {solution.message}")
