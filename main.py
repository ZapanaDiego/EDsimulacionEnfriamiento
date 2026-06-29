import sys
from PyQt6.QtWidgets import QApplication
from config.settings import SimulationConfig
from view.main_window import MainWindow

def main():
    print("Iniciando Simulador Interactivo de Enfriamiento Térmico de CPU (GUI)...")
    
    # 1. Instanciar la configuración global
    config = SimulationConfig()
    
    # 2. Inicializar aplicación Qt
    app = QApplication(sys.argv)
    
    # 3. Crear y mostrar ventana principal
    window = MainWindow(config)
    window.show()
    
    # 4. Iniciar bucle de eventos
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
