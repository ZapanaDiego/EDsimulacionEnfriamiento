import pyqtgraph as pg
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGroupBox

class ChartPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        group_box = QGroupBox("Gráficas Interactivas")
        gb_layout = QHBoxLayout()
        
        self.plot_temp = pg.PlotWidget(title="Temperatura vs Tiempo")
        self.plot_temp.setLabel('left', 'Temperatura', units='°C')
        self.plot_temp.setLabel('bottom', 'Tiempo', units='s')
        self.plot_temp.showGrid(x=True, y=True)
        self.curve_temp = self.plot_temp.plot(pen=pg.mkPen('r', width=2))
        
        self.plot_flux = pg.PlotWidget(title="Flujo Instantáneo (dT/dt)")
        self.plot_flux.setLabel('left', 'Tasa de Enfriamiento', units='°C/s')
        self.plot_flux.setLabel('bottom', 'Tiempo', units='s')
        self.plot_flux.showGrid(x=True, y=True)
        self.curve_flux = self.plot_flux.plot(pen=pg.mkPen('b', width=2))
        
        gb_layout.addWidget(self.plot_temp)
        gb_layout.addWidget(self.plot_flux)
        group_box.setLayout(gb_layout)
        
        layout.addWidget(group_box)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def update_charts(self, t_data, T_data, flux_data):
        """
        Actualiza los datos de las curvas.
        """
        self.curve_temp.setData(t_data, T_data)
        self.curve_flux.setData(t_data, flux_data)
