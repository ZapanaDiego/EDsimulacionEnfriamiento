import logging
import random
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox
from PyQt6.QtCore import Qt, QPointF, QTimer, QLineF
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPolygonF, QLinearGradient

class RoomCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(400, 300)
        self.current_temp = 25.0
        self.max_temp = 100.0
        self.min_temp = 20.0
        
        # Animación de Viento
        self.wind_speed = 0.0
        self.wind_particles = self.init_particles(30)
        
        # Timer para ~30 FPS (33 ms)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(33)

    def init_particles(self, count):
        particles = []
        for _ in range(count):
            particles.append({
                'x': random.uniform(0, 800), # Espacio amplio inicial
                'y': random.uniform(0, 600),
                'speed_factor': random.uniform(0.5, 1.5),
                'length': random.uniform(20, 60),
                'opacity': random.randint(50, 180)
            })
        logging.debug(f"Sistema de partículas inicializado. Cantidad: {count}")
        return particles

    def set_temperature(self, temp):
        self.current_temp = temp

    def set_wind_speed(self, speed):
        self.wind_speed = speed

    def get_laptop_color(self):
        ratio = (self.current_temp - self.min_temp) / (self.max_temp - self.min_temp)
        ratio = max(0.0, min(1.0, ratio))
        r = int(ratio * 255)
        b = int((1 - ratio) * 255)
        return QColor(r, 50, b)
        
    def update_animation(self):
        if self.wind_speed > 0:
            self.update_particles()
        self.update() # Forzar repintado continuo

    def update_particles(self):
        width = self.width() if self.width() > 0 else 400
        height = self.height() if self.height() > 0 else 300
        
        for p in self.wind_particles:
            # Movimiento isométrico aproximado (diagonal: de izquierda superior a derecha inferior)
            dx = self.wind_speed * p['speed_factor'] * 2.5
            dy = self.wind_speed * p['speed_factor'] * 0.6
            
            p['x'] += dx
            p['y'] += dy
            
            # Reaparición cuando sale de pantalla
            if p['x'] > width or p['y'] > height:
                p['x'] = random.uniform(-200, -50)
                p['y'] = random.uniform(-100, height * 0.8)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width = self.width()
        height = self.height()
        
        # Fondo (Pared)
        bg_grad = QLinearGradient(0, 0, 0, height)
        bg_grad.setColorAt(0.0, QColor(220, 220, 230))
        bg_grad.setColorAt(1.0, QColor(180, 180, 190))
        painter.fillRect(0, 0, width, height, bg_grad)
        
        # Dibujar escritorio (Polígono isométrico)
        desk_poly = QPolygonF([
            QPointF(width * 0.1, height * 0.7),
            QPointF(width * 0.9, height * 0.7),
            QPointF(width * 1.0, height * 1.0),
            QPointF(width * 0.0, height * 1.0)
        ])
        
        desk_grad = QLinearGradient(0, height * 0.7, 0, height)
        desk_grad.setColorAt(0.0, QColor(120, 80, 50))
        desk_grad.setColorAt(1.0, QColor(80, 50, 30))
        painter.setBrush(QBrush(desk_grad))
        painter.setPen(QPen(Qt.GlobalColor.black, 1))
        painter.drawPolygon(desk_poly)
        
        # Dibujar Laptop Base (Polígono)
        laptop_color = self.get_laptop_color()
        laptop_grad = QLinearGradient(width * 0.3, height * 0.75, width * 0.7, height * 0.85)
        laptop_grad.setColorAt(0.0, laptop_color.lighter(120))
        laptop_grad.setColorAt(1.0, laptop_color.darker(120))
        
        base_poly = QPolygonF([
            QPointF(width * 0.35, height * 0.75),
            QPointF(width * 0.65, height * 0.75),
            QPointF(width * 0.75, height * 0.85),
            QPointF(width * 0.25, height * 0.85)
        ])
        painter.setBrush(QBrush(laptop_grad))
        painter.drawPolygon(base_poly)
        
        # Pantalla de la laptop
        screen_poly = QPolygonF([
            QPointF(width * 0.35, height * 0.75),
            QPointF(width * 0.65, height * 0.75),
            QPointF(width * 0.60, height * 0.50),
            QPointF(width * 0.40, height * 0.50)
        ])
        painter.setBrush(QBrush(QColor(30, 30, 30))) # Pantalla apagada
        painter.drawPolygon(screen_poly)
        
        # Texto de temperatura
        painter.setPen(QPen(Qt.GlobalColor.white))
        font = painter.font()
        font.setPointSize(12)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(int(width * 0.45), int(height * 0.82), f"{self.current_temp:.1f}°C")
        
        # Dibujar Partículas de Viento
        if self.wind_speed > 0:
            for p in self.wind_particles:
                color = QColor(200, 230, 255, p['opacity']) # Celeste translúcido
                pen = QPen(color, 2, Qt.PenStyle.SolidLine)
                pen.setCapStyle(Qt.PenCapStyle.RoundCap)
                painter.setPen(pen)
                
                # La línea va desde (x, y) hacia atrás en el ángulo del movimiento
                dx = p['length']
                dy = p['length'] * 0.24 # Aproximadamente proporcional al dx/dy de update_particles
                p1 = QPointF(p['x'], p['y'])
                p2 = QPointF(p['x'] - dx, p['y'] - dy)
                painter.drawLine(QLineF(p1, p2))

class RoomCanvasPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        group_box = QGroupBox("Entorno Virtual (2.5D)")
        gb_layout = QVBoxLayout()
        self.canvas = RoomCanvas()
        gb_layout.addWidget(self.canvas)
        group_box.setLayout(gb_layout)
        layout.addWidget(group_box)
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)
        
    def set_temperature(self, temp):
        self.canvas.set_temperature(temp)
        
    def set_wind_speed(self, speed):
        self.canvas.set_wind_speed(speed)
