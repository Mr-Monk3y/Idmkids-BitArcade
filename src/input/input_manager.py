import pygame
import serial
from serial.tools import list_ports

from input.entrada import EntradaJugador
from input.entradas import Entrada
from input.acciones import Accion


class InputManager:
    def __init__(self):
        self.teclas = {
            # Jugador 1
            pygame.K_a: EntradaJugador(1, Entrada.LEFT),
            pygame.K_d: EntradaJugador(1, Entrada.RIGHT),
            pygame.K_w: EntradaJugador(1, Entrada.UP),
            pygame.K_s: EntradaJugador(1, Entrada.DOWN),

            # Jugador 2
            pygame.K_LEFT: EntradaJugador(2, Entrada.LEFT),
            pygame.K_RIGHT: EntradaJugador(2, Entrada.RIGHT),
            pygame.K_UP: EntradaJugador(2, Entrada.UP),
            pygame.K_DOWN: EntradaJugador(2, Entrada.DOWN),

            # Jugador 3
            pygame.K_j: EntradaJugador(3, Entrada.LEFT),
            pygame.K_l: EntradaJugador(3, Entrada.RIGHT),
            pygame.K_i: EntradaJugador(3, Entrada.UP),
            pygame.K_k: EntradaJugador(3, Entrada.DOWN),

            # Jugador 4
            pygame.K_f: EntradaJugador(4, Entrada.LEFT),
            pygame.K_h: EntradaJugador(4, Entrada.RIGHT),
            pygame.K_t: EntradaJugador(4, Entrada.UP),
            pygame.K_g: EntradaJugador(4, Entrada.DOWN),

            # Entradas generales
            pygame.K_RETURN: EntradaJugador(0, Entrada.SELECT),
            pygame.K_ESCAPE: EntradaJugador(0, Entrada.BACK),
            pygame.K_e: EntradaJugador(0, Entrada.FINISH),
        }

        self.conexion_serial = None
        self.puerto_serial = None

    def detectar_microbit(self):
        """Busca automáticamente una micro:bit conectada por USB."""

        puertos = list_ports.comports()

        for puerto in puertos:
            if puerto.vid == 3368 and puerto.pid == 516:
                print(f"Micro:bit encontrada en {puerto.device}")
                return puerto.device

        print("No se encontró ninguna micro:bit conectada")
        return None

    def obtener_evento(self, evento):
        """Obtiene una entrada a partir de un evento de Pygame."""

        entrada = self.obtener_entrada_teclado(evento)

        if entrada is not None:
            return entrada

        return None

    def obtener_entrada_teclado(self, evento):
        """Convierte un evento de teclado en una entrada de jugador."""

        if evento.type != pygame.KEYDOWN:
            return None

        if evento.key not in self.teclas:
            return None

        return self.teclas[evento.key]

    def obtener_entradas_teclado_mantenidas(self):
        """Obtiene las entradas de las teclas de movimiento mantenidas."""

        teclas_mantenidas = pygame.key.get_pressed()

        entradas = []

        teclas_movimiento = (
            pygame.K_a,
            pygame.K_d,
            pygame.K_w,
            pygame.K_s,
            pygame.K_LEFT,
            pygame.K_RIGHT,
            pygame.K_UP,
            pygame.K_DOWN,
            pygame.K_j,
            pygame.K_l,
            pygame.K_i,
            pygame.K_k,
            pygame.K_f,
            pygame.K_h,
            pygame.K_t,
            pygame.K_g,
        )

        for tecla in teclas_movimiento:

            if teclas_mantenidas[tecla]:
                entradas.append(self.teclas[tecla])

        return entradas

    def obtener_entrada_serial(self, mensaje):
        """Convierte un mensaje del receptor en una entrada de jugador."""
        mensaje = mensaje.strip()

        partes = mensaje.split(":")
        if len(partes) != 2:
            return None

        jugador_texto = partes[0]
        accion_texto = partes[1].upper()

        # El identificador debe tener el formato P1, P2, P3 o P4.
        if len(jugador_texto) != 2:
            return None

        if jugador_texto[0] != "P":
            return None

        if not jugador_texto[1].isdigit():
            return None

        jugador = int(jugador_texto[1])

        if jugador < 1 or jugador > 4:
            return None

        entradas_movimiento = {
            "LEFT": Entrada.LEFT,
            "RIGHT": Entrada.RIGHT,
            "UP": Entrada.UP,
            "DOWN": Entrada.DOWN,
            "NONE": Entrada.NONE,
        }

        if accion_texto in entradas_movimiento:
            return EntradaJugador(
                jugador,
                entrada=entradas_movimiento[accion_texto]
            )

        if accion_texto == "SHAKE":
            return EntradaJugador(
                jugador,
                accion=Accion.SHAKE
            )

        if accion_texto == "BACK":
            return EntradaJugador(
            0,
            entrada=Entrada.BACK
        )

        return None

    def conectar_serial(self, puerto, velocidad=115200):
        """Intenta conectar con el receptor por puerto serial."""

        try:
            self.conexion_serial = serial.Serial(
                puerto,
                velocidad,
                timeout=0
            )

            self.puerto_serial = puerto

            print(f"Receptor conectado en {puerto}")

            return True

        except serial.SerialException:
            self.conexion_serial = None
            self.puerto_serial = None

            print(f"No se pudo conectar al puerto {puerto}")

            return False

    def obtener_entradas_serial_reales(self):
        """Lee todas las entradas disponibles desde el receptor."""
        entradas = []

        if self.conexion_serial is None:
            return entradas

        while self.conexion_serial.in_waiting:
            try:
                mensaje = (
                    self.conexion_serial.readline()
                    .decode()
                    .strip()
                )

                if not mensaje:
                    continue

                print("MICROBIT:", mensaje)
                
                entrada = self.obtener_entrada_serial(mensaje)

                if entrada is not None:
                    entradas.append(entrada)

            except (serial.SerialException, UnicodeDecodeError):
                break

        return entradas