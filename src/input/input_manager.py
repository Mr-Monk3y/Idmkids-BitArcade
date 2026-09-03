import pygame
import serial

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
        }

        self.conexion_serial = None
        self.puerto_serial = None

        self.acciones_serial = {
            "A": Accion.A,
            "B": Accion.B,
            "SHAKE": Accion.SHAKE,
        }

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
        """Convierte un mensaje serial en una accion de jugador."""

        mensaje = mensaje.strip()

        partes = mensaje.split(":")

        if len(partes) != 2:
            return None

        jugador_texto = partes[0]
        accion_texto = partes[1].upper()

        if not jugador_texto.isdigit():
            return None

        jugador = int(jugador_texto)

        if jugador < 0 or jugador > 4:
            return None

        if accion_texto not in self.acciones_serial:
            return None

        accion = self.acciones_serial[accion_texto]

        return EntradaJugador(
            jugador,
            accion=accion
        )

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

    def obtener_entrada_serial_real(self):
        """Lee una entrada disponible desde el receptor."""

        if self.conexion_serial is None:
            return None

        if not self.conexion_serial.in_waiting:
            return None

        try:
            mensaje = self.conexion_serial.readline().decode().strip()

            if not mensaje:
                return None

            return self.obtener_entrada_serial(mensaje)

        except (serial.SerialException, UnicodeDecodeError):
            return None