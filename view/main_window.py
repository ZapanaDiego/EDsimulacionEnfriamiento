from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt
from .newton_widget import NewtonWidget
from .bernoulli_widget import BernoulliWidget

class MainWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.setWindowTitle("Simulador de Enfriamiento Térmico")
        self.setFixedSize(400, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        title = QLabel("Seleccione el Modelo de Simulación")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        btn_newton = QPushButton("Ejecutar Simulación Lineal (Newton)")
        btn_newton.setFixedSize(300, 50)
        btn_newton.clicked.connect(self.open_newton_sim)
        layout.addWidget(btn_newton)

        btn_bernoulli = QPushButton("Ejecutar Simulación Avanzada (Bernoulli)")
        btn_bernoulli.setFixedSize(300, 50)
        btn_bernoulli.clicked.connect(self.open_bernoulli_sim)
        layout.addWidget(btn_bernoulli)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_newton_sim(self):
        self.newton_window = NewtonWidget(self.config, self)
        self.newton_window.show()
        self.hide()

    def open_bernoulli_sim(self):
        self.bernoulli_window = BernoulliWidget(self.config, self)
        self.bernoulli_window.show()
        self.hide()
