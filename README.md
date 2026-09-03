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

`python main.py`

---

## 📁 Estructura del proyecto

El proyecto estará dividido en módulos para permitir que diferentes partes del sistema se desarrollen de forma independiente.

La estructura del proyecto se documentará a medida que avance el desarrollo.

---

## 👥 Equipo

Bit Arcade es desarrollado como un **proyecto grupal**.

## Notas:

Amplificar señal de radio en Micro:Bit
Imprimir controles? Tipo volante con agarraderas?

## Comentarios:

Algunas cosas:
1. Cada juego tiene un archivo propio en src/games/.
2. Traten de no cambiar mucho main.py, InputManager, JuegoBase, RegistroJuegos o de avisar porque toca a todos los juegos.
3. Hay una carpeta de assets para cada juego y pantalla de instrucciones.
4. Hay que instalar Python 3.11 o compatible.
5. Para instalar lo otro necesario hay que hacer desde cmd .venv\Scripts\activate.bat y luego pip install -r requirements.txt
6. Hay un make run
7. JuegoBase es la interfaz, ahi están las firmas
8. El main controla el flujo de la app
9. En __init__() van las variables de la clase
10. iniciar() se llama cada vez que empieza una nueva partida, deja el juego en su estado inicial.
11. manejar_entrada(entrada) procesa las acciones de los jugadores, recibe: jugador, entrada, accion. 
12. Las entradas de teclado usan entrada, las acciones de microbit usan accion. El juego decide qué significa cada acción física.
13. Para la  demo hagamos todo con los botones o el teclado, después cambiamos a microbit con acelerómetro y radio para los controles
14. El InputManager ya tiene configuradas teclas para cuatro jugadores, l juego solamente recibe EntradaJugador.
15. Puse para que se mande input cada 50 ms así podemos saber si algo se dejo apretado
16. actualizar() acá va la lógica que debe actualizarse continuamente durante el juego.
17. dibujar() todo lo visual del juego va acá.
18. obtener_resultado() al terminar la partida, el juego debe devolver un ResultadoJuego
19. Finalización del juego
20. Cuando el juego termina tiene que poner self.terminado = True el main lo ve y pasa a resltados
21. Con ESC vas al menu y con ENTER saltas el contador
