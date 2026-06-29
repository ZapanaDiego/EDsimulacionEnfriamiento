import pyqtgraph as pg
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGroupBox

class BernoulliChartPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        group_box = QGroupBox("Gráficas Avanzadas (Bernoulli)")
        gb_layout = QHBoxLayout()
        
        # 1. T vs Tiempo
        self.plot_temp = pg.PlotWidget(title="Temperatura vs Tiempo")
        self.plot_temp.setLabel('left', 'Temperatura', units='°C')
        self.plot_temp.setLabel('bottom', 'Tiempo', units='s')
        self.plot_temp.showGrid(x=True, y=True)
        self.curve_temp = self.plot_temp.plot(pen=pg.mkPen('r', width=2))
        
        # 2. Componentes de Flujo (dT/dt)
        self.plot_flux = pg.PlotWidget(title="Componentes de Flujo")
        self.plot_flux.setLabel('left', 'Tasa (dT/dt)', units='°C/s')
        self.plot_flux.setLabel('bottom', 'Tiempo', units='s')
        self.plot_flux.showGrid(x=True, y=True)
        self.plot_flux.addLegend()
        self.curve_flux_lin = self.plot_flux.plot(pen=pg.mkPen('b', width=2), name="Disipación Constante")
        self.curve_flux_turb = self.plot_flux.plot(pen=pg.mkPen('g', width=2, style=pg.QtCore.Qt.PenStyle.DashLine), name="Efecto Turbulencia")
        
        # 3. Evolución de Turbulencia
        self.plot_turb = pg.PlotWidget(title="Evolución de Turbulencia")
        self.plot_turb.setLabel('left', 'Turbulencia', units='')
        self.plot_turb.setLabel('bottom', 'Tiempo', units='s')
        self.plot_turb.showGrid(x=True, y=True)
        self.curve_turb = self.plot_turb.plot(pen=pg.mkPen('m', width=2))
        
        gb_layout.addWidget(self.plot_temp)
        gb_layout.addWidget(self.plot_flux)
        gb_layout.addWidget(self.plot_turb)
        group_box.setLayout(gb_layout)
        
        layout.addWidget(group_box)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def update_charts(self, t_data, T_data, flux_lin_data, flux_turb_data, turb_evo_data):
        """
        Actualiza las 3 gráficas simultáneamente.
        """
        self.curve_temp.setData(t_data, T_data)
        self.curve_flux_lin.setData(t_data, flux_lin_data)
        self.curve_flux_turb.setData(t_data, flux_turb_data)
        self.curve_turb.setData(t_data, turb_evo_data)
