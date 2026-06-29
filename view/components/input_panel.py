from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QPushButton, QGroupBox
from PyQt6.QtCore import Qt, pyqtSignal

class InputPanel(QWidget):
    # Definimos señales que este componente emitirá
    run_requested = pyqtSignal()
    temp_cpu_changed = pyqtSignal(float)
    
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        group_box = QGroupBox("Controles")
        gb_layout = QVBoxLayout()
        
        # 1. T_CPU (0 - 150)
        self.lbl_t_cpu = QLabel(f"T. Inicial CPU: {self.config.T_initial_cpu}°C")
        self.slider_t_cpu = self.create_slider(0, 150, int(self.config.T_initial_cpu), self.on_t_cpu_changed)
        
        # 2. T_AIR (0 - 50)
        self.lbl_t_air = QLabel(f"T. Ambiente: {self.config.T_ambient}°C")
        self.slider_t_air = self.create_slider(0, 50, int(self.config.T_ambient), self.on_t_air_changed)
        
        # 3. K (0.01 - 0.20 -> mapeado a 1 - 20)
        self.lbl_k = QLabel(f"Constante K: {self.config.cooling_constant_k}")
        self.slider_k = self.create_slider(1, 20, int(self.config.cooling_constant_k * 100), self.on_k_changed)
        
        self.btn_run = QPushButton("Ejecutar")
        self.btn_run.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-weight: bold;")
        self.btn_run.clicked.connect(self.run_requested.emit)
        
        gb_layout.addWidget(self.lbl_t_cpu)
        gb_layout.addWidget(self.slider_t_cpu)
        gb_layout.addWidget(self.lbl_t_air)
        gb_layout.addWidget(self.slider_t_air)
        gb_layout.addWidget(self.lbl_k)
        gb_layout.addWidget(self.slider_k)
        gb_layout.addStretch()
        gb_layout.addWidget(self.btn_run)
        
        group_box.setLayout(gb_layout)
        layout.addWidget(group_box)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def create_slider(self, min_val, max_val, init_val, callback):
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(init_val)
        slider.valueChanged.connect(callback)
        return slider

    def on_t_cpu_changed(self, value):
        self.lbl_t_cpu.setText(f"T. Inicial CPU: {value}°C")
        self.config.T_initial_cpu = float(value)
        self.temp_cpu_changed.emit(float(value))

    def on_t_air_changed(self, value):
        self.lbl_t_air.setText(f"T. Ambiente: {value}°C")
        self.config.T_ambient = float(value)

    def on_k_changed(self, value):
        k_val = value / 100.0
        self.lbl_k.setText(f"Constante K: {k_val}")
        self.config.cooling_constant_k = k_val
