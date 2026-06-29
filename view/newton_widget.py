import numpy as np
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from core.newton_simulator import NewtonSimulator
from view.components.input_panel import InputPanel
from view.components.chart_panel import ChartPanel
from view.components.room_canvas import RoomCanvasPanel

class NewtonWidget(QWidget):
    def __init__(self, config, parent_menu):
        super().__init__()
        self.config = config
        self.parent_menu = parent_menu
        self.setWindowTitle("Simulador de Enfriamiento Lineal (Newton)")
        self.resize(1100, 750)
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()
        
        # 1. Instanciar Componentes
        self.input_panel = InputPanel(self.config)
        self.input_panel.setFixedWidth(250)
        
        self.chart_panel = ChartPanel()
        self.room_canvas = RoomCanvasPanel()
        
        # 2. Layouts
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.input_panel)
        
        btn_back = QPushButton("Volver al Menú")
        btn_back.clicked.connect(self.go_back)
        left_layout.addWidget(btn_back)
        
        left_container = QWidget()
        left_container.setLayout(left_layout)
        left_container.setFixedWidth(270)
        
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
        
        # Inicializar estado visual
        self.room_canvas.set_temperature(self.config.T_initial_cpu)

    def execute_simulation(self):
        # 1. Instanciar simulador
        simulator = NewtonSimulator(self.config)
        
        # 2. Resolver ED
        try:
            simulator.solve_equation()
            t_data, T_data = simulator.get_results()
            
            # 3. Calcular flujo instantáneo (dT/dt)
            # dT/dt = -k * (T - T_ambient)
            flux_data = -self.config.cooling_constant_k * (T_data - self.config.T_ambient)
            
            # 4. Actualizar gráficos
            self.chart_panel.update_charts(t_data, T_data, flux_data)
            
            # 5. Opcional: Actualizar el canvas a la temp final
            # Para una animación en tiempo real se requeriría un QTimer,
            # por ahora actualizamos a la temp final.
            self.room_canvas.set_temperature(T_data[-1])
            
        except Exception as e:
            print(f"Error al ejecutar la simulación: {e}")

    def go_back(self):
        self.parent_menu.show()
        self.close()
