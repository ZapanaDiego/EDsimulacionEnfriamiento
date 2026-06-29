import sys
import logging
from PyQt6.QtWidgets import QApplication
from config.settings import SimulationConfig
from view.main_window import MainWindow

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] (%(filename)s): %(message)s',
        handlers=[
            logging.FileHandler("simulation.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    setup_logging()
    logging.info("Iniciando Simulador Interactivo de Enfriamiento Térmico de CPU (GUI)...")
    
    # 1. Instanciar la configuración global
    config = SimulationConfig()
    
    # 2. Inicializar aplicación Qt
    app = QApplication(sys.argv)
    
    # 3. Crear y mostrar ventana principal
    window = MainWindow(config)
    window.show()
    
    # 4. Iniciar bucle de eventos
    exit_code = app.exec()
    logging.info(f"Aplicación cerrada con código: {exit_code}")
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
