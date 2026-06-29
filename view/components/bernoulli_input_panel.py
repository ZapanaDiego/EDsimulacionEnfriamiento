from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QPushButton, QGroupBox, QScrollArea
from PyQt6.QtCore import Qt, pyqtSignal

class BernoulliInputPanel(QWidget):
    run_requested = pyqtSignal()
    temp_cpu_changed = pyqtSignal(float)
    wind_speed_changed = pyqtSignal(float) # Nueva señal
    
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)
        
        group_box = QGroupBox("Controles Avanzados")
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
        
        # 4. Velocidad Viento V_air (0 - 20)
        self.lbl_v_air = QLabel(f"Velocidad Viento: {self.config.V_air} m/s")
        self.slider_v_air = self.create_slider(0, 20, int(self.config.V_air), self.on_v_air_changed)
        
        # 5. Escala Turbulencia n (1.0 - 3.0 -> mapeado a 10 - 30)
        self.lbl_n = QLabel(f"Escala Turbulencia (n): {self.config.bernoulli_n}")
        self.slider_n = self.create_slider(10, 30, int(self.config.bernoulli_n * 10), self.on_n_changed)
        
        # 6. Humedad H (0 - 100)
        self.lbl_h = QLabel(f"Humedad (H): {self.config.humidity_H}%")
        self.slider_h = self.create_slider(0, 100, int(self.config.humidity_H), self.on_h_changed)
        
        # 7. Sesgo Nano Banana K_nb (0.0 - 5.0 -> mapeado a 0 - 50)
        self.lbl_knb = QLabel(f"Sesgo Nano Banana (K_nb): {self.config.sensor_Knb}")
        self.slider_knb = self.create_slider(0, 50, int(self.config.sensor_Knb * 10), self.on_knb_changed)
        
        self.btn_run = QPushButton("Ejecutar Bernoulli")
        self.btn_run.setStyleSheet("background-color: #2196F3; color: white; padding: 10px; font-weight: bold;")
        self.btn_run.clicked.connect(self.run_requested.emit)
        
        gb_layout.addWidget(self.lbl_t_cpu)
        gb_layout.addWidget(self.slider_t_cpu)
        gb_layout.addWidget(self.lbl_t_air)
        gb_layout.addWidget(self.slider_t_air)
        gb_layout.addWidget(self.lbl_k)
        gb_layout.addWidget(self.slider_k)
        
        gb_layout.addWidget(self.lbl_v_air)
        gb_layout.addWidget(self.slider_v_air)
        gb_layout.addWidget(self.lbl_n)
        gb_layout.addWidget(self.slider_n)
        gb_layout.addWidget(self.lbl_h)
        gb_layout.addWidget(self.slider_h)
        gb_layout.addWidget(self.lbl_knb)
        gb_layout.addWidget(self.slider_knb)
        
        gb_layout.addStretch()
        gb_layout.addWidget(self.btn_run)
        
        group_box.setLayout(gb_layout)
        layout.addWidget(group_box)
        
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

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
        
    def on_v_air_changed(self, value):
        self.lbl_v_air.setText(f"Velocidad Viento: {value} m/s")
        self.config.V_air = float(value)
        self.config.cooling_constant_k2 = 0.001 * float(value)
        # Emitir señal para la animación
        self.wind_speed_changed.emit(float(value))

    def on_n_changed(self, value):
        n_val = value / 10.0
        self.lbl_n.setText(f"Escala Turbulencia (n): {n_val}")
        self.config.bernoulli_n = n_val

    def on_h_changed(self, value):
        self.lbl_h.setText(f"Humedad (H): {value}%")
        self.config.humidity_H = float(value)

    def on_knb_changed(self, value):
        knb_val = value / 10.0
        self.lbl_knb.setText(f"Sesgo Nano Banana (K_nb): {knb_val}")
        self.config.sensor_Knb = knb_val
