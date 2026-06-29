# 🌡️ Simulador Interactivo de Enfriamiento Térmico de CPU (GUI)

## 📖 Descripción General

Es una aplicación científica interactiva desarrollada en Python con una interfaz gráfica moderna (PyQt / PyQtGraph) que modela y simula la disipación térmica de un procesador a lo largo del tiempo. 

Bajo el capó, el simulador compara dos enfoques físicos distintos mediante la resolución numérica de Ecuaciones Diferenciales Ordinarias (EDOs) utilizando el solver de calidad industrial `solve_ivp` (método de Runge-Kutta de orden 4 y 5) de la librería SciPy. Adicionalmente, cuenta con un impresionante **sistema visual de partículas 2.5D en tiempo real** para emular el flujo de aire aerodinámico sobre el escritorio.

---

## 🚀 Instalación y Ejecución

Sigue las instrucciones correspondientes a tu sistema operativo para ejecutar el simulador localmente.

### 🐧 Linux (Bash)
```bash
# 1. Clonar el repositorio
git clone https://github.com/ZapanaDiego/EDsimulacionEnfriamiento.git
cd EDsimulacionEnfriamiento

# 2. Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependencias
pip install numpy scipy PyQt6 pyqtgraph

# 4. Ejecutar la simulación
python main.py
```

### 🪟 Windows (PowerShell/CMD)
```powershell
# 1. Clonar el repositorio
git clone https://github.com/ZapanaDiego/EDsimulacionEnfriamiento.git
cd EDsimulacionEnfriamiento

# 2. Crear y activar entorno virtual
python -m venv venv
.\venv\Scripts\activate

# 3. Instalar dependencias
pip install numpy scipy PyQt6 pyqtgraph

# 4. Ejecutar la simulación
python main.py
```

---

## 🧮 Modelos Físicos y Variables Térmicas

El usuario puede interactuar con dos simuladores completamente distintos a través de paneles de control intuitivos. Las EDOs se resuelven en tiempo real y los datos se proyectan en gráficas dinámicas.

### A) Ley de Enfriamiento de Newton (Modelo Lineal)
Modela la disipación bajo convección natural simple.

**Ecuación Diferencial:**
$$ \frac{dT}{dt} = -k_1 (T - T_{\text{ambient}}) $$

| Variable | Descripción |
| :--- | :--- |
| **T_CPU Inicial (°C)** | Temperatura de partida del silicio tras apagarse. |
| **T_AIR (°C)** | Temperatura ambiente de la habitación (la asíntota térmica). |
| **K ($k_1$)** | Constante de conductividad térmica del disipador base. |

### B) Modelo de Convección Turbulenta de Bernoulli (Modelo No Lineal Acoplado)
Modela la disipación térmica en un entorno complejo con convección forzada, flujos turbulentos y variables exóticas atmosféricas.

**Ecuación Diferencial:**
$$ \frac{dT}{dt} = -k_1 (T - T_{\text{ambient}}) - k_2 (T - T_{\text{ambient}})^n $$

**Acoplamiento Físico de $k_2$:**
La constante $k_2$ es **dinámica** y se calcula en tiempo real mediante el acoplamiento de las variables atmosféricas para prevenir la inestabilidad de Euler y escalar la turbulencia en rangos microscópicos:
$$ k_2 = \frac{\text{Viento} \cdot \left(1.0 + \frac{\text{Humedad}}{100.0}\right) \cdot K_{nb}}{10000} $$

| Variable | Descripción |
| :--- | :--- |
| **T_CPU Inicial y T_AIR** | Condiciones de frontera (iguales al modelo lineal). |
| **K ($k_1$)** | Coeficiente de enfriamiento lineal base. |
| **Viento (m/s)** | Velocidad del flujo de aire sobre el disipador (controla la animación 2.5D). |
| **Humedad (%)** | Humedad relativa del aire que altera la densidad del fluido de disipación. |
| **Escala de Turbulencia ($n$)** | Exponente de restricción física que rige la no linealidad (rango estricto de `1.1` a `1.7`). |
| **$K_{nb}$ (Sesgo del Sensor)** | Multiplicador de eficiencia del disipador o ruido de hardware (Sensor Nano Banana). |

---

## 🔬 Sistema de Auditoría y Logging Científico

Este proyecto está construido bajo rigurosos estándares de ingeniería de software. Toda la integración matemática cuenta con un sistema robusto de instrumentación. Al ejecutar, se generará (o anexará) de forma automática un archivo `simulation.log` en la raíz del proyecto.

Este volcado centralizado registra detalladamente:
- **Marcas de Tiempo (Timestamps)** y el archivo origen exacto del log.
- **Parámetros Físicos Exactos:** Una captura de las variables de entrada instantes antes de iniciar la integración numérica.
- **Auditoría del Solver de SciPy:** 
  - Estado del cálculo numérico convergente (`success`).
  - Número de evaluaciones de la función (`nfev`) para medir la carga y complejidad de cómputo.
- **Estadísticas de Salida Numérica:** 
  - Tamaño de las matrices resultantes (Tensores de tiempo y temperatura).
  - Temperatura Máxima y Mínima alcanzadas (para control de violaciones de frontera térmica).
  - Volcado tabular `(t, T)` con muestreo de los primeros y últimos 5 puntos de la curva de integración.
- **Control de Excepciones:** Captura de *Tracebacks* críticos y detección de números no convergentes o inestabilidades de Euler (`NaN`).
