#  Bit Arcade

Bit Arcade es un sistema de juegos estilo arcade controlado mediante controles inalámbricos con **micro:bit**.

El sistema consiste en una computadora que ejecuta los juegos y uno o más controles inalámbricos. Cada control detecta su inclinación y envía la entrada correspondiente a la computadora.

El proyecto se desarrolla utilizando **Python + Pygame**.

---

## 🛠️ Requisitos

Antes de trabajar en el proyecto, instalar:

- **Python 3**
- **Git**
- **Visual Studio Code** u otro IDE de preferencia

El proyecto también utilizará paquetes de Python, que se instalarán mediante `pip`.

---

## ⚙️ Configuración

### 📥 Clonar el repositorio

`git clone <URL_DEL_REPOSITORIO>`
`cd bit-arcade`

### 🐍 Crear un entorno virtual

`python -m venv .venv`

### ▶️ Activar el entorno virtual

**Windows:** `.venv\Scripts\activate`

**Linux/macOS:** `source .venv/bin/activate`

### 📦 Instalar las dependencias

`pip install -r requirements.txt`

---

## 🎮 Ejecutar el proyecto

Para ejecutar Bit Arcade:

`make run`

---

## 📁 Estructura del proyecto

El proyecto está dividido en módulos para permitir que diferentes partes del sistema se desarrollen de forma independiente.

---

## 👥 Equipo

Bit Arcade fue desarrollado como un **proyecto grupal**.


## Comentarios:

1. Cada juego tiene un archivo propio en src/games/.
2. Hay una carpeta de assets para cada juego y pantalla de instrucciones.
3. JuegoBase es la interfaz, ahi están las firmas
4. El main controla el flujo de la app
5. En __init__() van las variables de la clase
6. iniciar() se llama cada vez que empieza una nueva partida, deja el juego en su estado inicial.
7. manejar_entrada(entrada) procesa las acciones de los jugadores, recibe: jugador, entrada, accion. 
8. Las entradas de teclado usan entrada, las acciones de microbit usan serial. El juego decide qué significa cada acción física.
9. actualizar() acá va la lógica que debe actualizarse continuamente durante el juego.
10. dibujar() todo lo visual del juego va acá.
11. obtener_resultado() al terminar la partida, el juego debe devolver un ResultadoJuego
12. Cuando el juego termina tiene que poner self.terminado = True el main lo ve y pasa a resltados
13. Con ESC vas al menu y con ENTER saltas el contador
14. El puerto COM está hardcodeado para hallarlo usar:
15. powershell "Get-CimInstance Win32_SerialPort | Select-Object DeviceID,Name" para CMD
16. Get-CimInstance Win32_SerialPort | Select-Object DeviceID,Name powershell
17. wmic path Win32_SerialPort get DeviceID,Name otro
