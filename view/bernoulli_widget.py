import logging
import numpy as np
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from core.bernoulli_simulator import BernoulliSimulator
from view.components.bernoulli_input_panel import BernoulliInputPanel
from view.components.bernoulli_chart_panel import BernoulliChartPanel
from view.components.room_canvas import RoomCanvasPanel

class BernoulliWidget(QWidget):
    def __init__(self, config, parent_menu):
        super().__init__()
        self.config = config
        self.parent_menu = parent_menu
        self.setWindowTitle("Simulador de Enfriamiento Avanzado (Bernoulli)")
        self.resize(1300, 800)
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()
        
        # 1. Instanciar Componentes
        self.input_panel = BernoulliInputPanel(self.config)
        self.input_panel.setFixedWidth(300)
        
        self.chart_panel = BernoulliChartPanel()
        # Reutilizamos el RoomCanvasPanel de la arquitectura Newton
        self.room_canvas = RoomCanvasPanel()
        
        # 2. Layouts
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.input_panel)
        
        btn_back = QPushButton("Volver al Menú")
        btn_back.clicked.connect(self.go_back)
        left_layout.addWidget(btn_back)
        
        left_container = QWidget()
        left_container.setLayout(left_layout)
        left_container.setFixedWidth(320)
        
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.room_canvas, 1) # 1 parte arriba
        right_layout.addWidget(self.chart_panel, 2) # 2 partes abajo
        
        right_container = QWidget()
        right_container.setLayout(right_layout)
        
        main_layout.addWidget(left_container)
        main_layout.addWidget(right_container)
        
        self.setLayout(main_layout)
        
        # 3. Conectar Señales
        self.input_panel.run_requested.connect(self.execute_simulation)
        self.input_panel.temp_cpu_changed.connect(self.room_canvas.set_temperature)
        self.input_panel.wind_speed_changed.connect(self.room_canvas.set_wind_speed)
        
        # Inicializar estado visual
        self.room_canvas.set_temperature(self.config.T_initial_cpu)
        self.room_canvas.set_wind_speed(self.config.V_air)

    def execute_simulation(self):
        logging.info(f"Usuario solicitó ejecución (Bernoulli). Parámetros -> T_CPU={self.config.T_initial_cpu}, T_AIR={self.config.T_ambient}, K={self.config.cooling_constant_k}, Viento={self.config.V_air}, n={self.config.bernoulli_n}, Humedad={self.config.humidity_H}, K_nb={self.config.sensor_Knb}")
        
        # Instanciar simulador de Bernoulli
        simulator = BernoulliSimulator(self.config)
        
        try:
            simulator.solve_equation()
            t_data, T_data = simulator.get_results()
            
            # Cálculo de datos para gráficas
            diff = np.maximum(T_data - self.config.T_ambient, 0.0)
            
            # Recalcular k2 dinámico
            viento = self.config.V_air
            humedad = self.config.humidity_H
            sesgo = self.config.sensor_Knb
            k2_dynamic = (viento * (1.0 + humedad / 100.0) * sesgo) / 10000.0
            
            # Gráfica 2: Flujo Lineal vs Flujo Turbulento
            flux_lin_data = -self.config.cooling_constant_k * diff
            flux_turb_data = -k2_dynamic * (diff ** self.config.bernoulli_n)
            
            # Gráfica 3: Evolución de Turbulencia
            # Usamos V_air, H y K_nb para afectar visualmente la curva de turbulencia
            turb_evo_data = np.abs(flux_turb_data) * self.config.V_air * self.config.sensor_Knb * (1 + self.config.humidity_H/100.0)
            
            # Actualizar gráficos
            self.chart_panel.update_charts(t_data, T_data, flux_lin_data, flux_turb_data, turb_evo_data)
            
            # Actualizar canvas 2.5D
            self.room_canvas.set_temperature(T_data[-1])
            
        except Exception as e:
            print(f"Error al ejecutar la simulación de Bernoulli: {e}")

    def go_back(self):
        self.parent_menu.show()
        self.close()
