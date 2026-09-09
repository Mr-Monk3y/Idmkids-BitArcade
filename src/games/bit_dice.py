import random
import time
from enum import Enum

import pygame

from games.juego_base import JuegoBase
from games.resultado_juego import ResultadoJuego
from input.entradas import Entrada


DIRECCIONES = [Entrada.UP, Entrada.DOWN, Entrada.LEFT, Entrada.RIGHT]

# Bit Dice es un juego individual: solo escucha al control del jugador 1.
JUGADOR_ACTIVO = 1

COLOR_FONDO = (0, 0, 0)
COLOR_TEXTO = (255, 255, 255)
COLOR_AYUDA = (170, 170, 170)

COLOR_BASE = {
    Entrada.UP: (255, 210, 63),
    Entrada.DOWN: (255, 61, 129),
    Entrada.LEFT: (61, 139, 255),
    Entrada.RIGHT: (0, 229, 195),
}

COLOR_ENCENDIDO = {
    Entrada.UP: (255, 228, 136),
    Entrada.DOWN: (255, 133, 179),
    Entrada.LEFT: (138, 184, 255),
    Entrada.RIGHT: (123, 245, 227),
}

# Tiempos de la animacion (segundos)
PAUSA_ANTES_DE_MOSTRAR = 0.5
DURACION_FLASH_SECUENCIA = 0.48
PAUSA_ENTRE_FLASHES = 0.62
DURACION_FLASH_JUGADOR = 0.15
PAUSA_TRAS_ACIERTO = 0.8


class EstadoBitDice(Enum):
    MOSTRANDO = 1   # se esta reproduciendo la secuencia
    ESPERANDO = 2   # el jugador tiene que repetirla
    PAUSA = 3       # pausa corta entre nivel y nivel


class BitDice(JuegoBase):
    def __init__(self, pantalla):
        super().__init__(pantalla)

        self.fuente_titulo = pygame.font.Font(None, 64)
        self.fuente_stat = pygame.font.Font(None, 48)
        self.fuente_mensaje = pygame.font.Font(None, 36)
        self.fuente_ayuda = pygame.font.Font(None, 24)

        self.secuencia = []
        self.paso_jugador = 0
        self.estado = EstadoBitDice.MOSTRANDO
        self.mensaje = ""

        self.indice_mostrado = 0
        self.proximo_flash = 0
        self.pausa_hasta = 0

        self.direccion_encendida = None
        self.encendida_hasta = 0

    def iniciar(self):
        """Inicializa o reinicia el juego."""

        self.terminado = False
        self.puntaje = 0

        self.secuencia = []
        self.direccion_encendida = None

        self._agregar_paso()

    def _agregar_paso(self):
        """Suma un paso a la secuencia y arranca su reproduccion."""

        self.secuencia.append(random.choice(DIRECCIONES))
        self.paso_jugador = 0
        self.estado = EstadoBitDice.MOSTRANDO
        self.indice_mostrado = 0
        self.proximo_flash = time.time() + PAUSA_ANTES_DE_MOSTRAR
        self.mensaje = "Mira bien..."

    def _encender(self, direccion, duracion):
        self.direccion_encendida = direccion
        self.encendida_hasta = time.time() + duracion

    def manejar_entrada(self, entrada):
        """Procesa una entrada de un jugador."""

        if entrada.jugador != JUGADOR_ACTIVO:
            return

        if entrada.entrada not in DIRECCIONES:
            return

        if self.estado != EstadoBitDice.ESPERANDO:
            return  # ignorar entradas mientras se muestra la secuencia o en pausa

        direccion = entrada.entrada
        self._encender(direccion, DURACION_FLASH_JUGADOR)

        if direccion == self.secuencia[self.paso_jugador]:
            self.paso_jugador += 1

            if self.paso_jugador == len(self.secuencia):
                self.puntaje = len(self.secuencia)
                self.mensaje = "¡Bien! Siguiente nivel"
                self.estado = EstadoBitDice.PAUSA
                self.pausa_hasta = time.time() + PAUSA_TRAS_ACIERTO

        else:
            self.puntaje = len(self.secuencia) - 1
            self.mensaje = f"Fallaste en el nivel {len(self.secuencia)}"
            self.terminado = True

    def actualizar(self):
        """Actualiza el estado del juego."""

        ahora = time.time()

        if self.direccion_encendida and ahora >= self.encendida_hasta:
            self.direccion_encendida = None

        if self.estado == EstadoBitDice.PAUSA:
            if ahora >= self.pausa_hasta:
                self._agregar_paso()

        elif self.estado == EstadoBitDice.MOSTRANDO:
            if not self.direccion_encendida and ahora >= self.proximo_flash:
                if self.indice_mostrado < len(self.secuencia):
                    self._encender(
                        self.secuencia[self.indice_mostrado],
                        DURACION_FLASH_SECUENCIA
                    )
                    self.proximo_flash = ahora + PAUSA_ENTRE_FLASHES
                    self.indice_mostrado += 1
                else:
                    self.estado = EstadoBitDice.ESPERANDO
                    self.mensaje = "¡Tu turno!"

    def dibujar(self):
        """Dibuja el juego."""

        self.pantalla.fill(COLOR_FONDO)

        ancho = self.pantalla.get_width()

        titulo = self.fuente_titulo.render("Bit Dice", True, COLOR_TEXTO)
        self.pantalla.blit(titulo, titulo.get_rect(center=(ancho // 2, 70)))

        nivel = self.fuente_stat.render(
            f"Nivel {len(self.secuencia)}", True, COLOR_TEXTO
        )
        self.pantalla.blit(nivel, nivel.get_rect(center=(ancho // 2, 130)))

        mensaje = self.fuente_mensaje.render(self.mensaje, True, COLOR_TEXTO)
        self.pantalla.blit(mensaje, mensaje.get_rect(center=(ancho // 2, 190)))

        cx, cy = ancho // 2, 380
        tam = 100
        separacion = 20

        self._dibujar_flecha(Entrada.UP, (cx, cy - tam - separacion // 2), tam)
        self._dibujar_flecha(Entrada.DOWN, (cx, cy + tam + separacion // 2), tam)
        self._dibujar_flecha(Entrada.LEFT, (cx - tam - separacion // 2, cy), tam)
        self._dibujar_flecha(Entrada.RIGHT, (cx + tam + separacion // 2, cy), tam)

        ayuda = self.fuente_ayuda.render(
            "Inclina el control hacia el lado que corresponda",
            True,
            COLOR_AYUDA
        )
        self.pantalla.blit(
            ayuda,
            ayuda.get_rect(center=(ancho // 2, self.pantalla.get_height() - 40))
        )

    def _dibujar_flecha(self, direccion, centro, tamano):
        encendida = self.direccion_encendida == direccion
        color = COLOR_ENCENDIDO[direccion] if encendida else COLOR_BASE[direccion]

        rectangulo = pygame.Rect(0, 0, tamano, tamano)
        rectangulo.center = centro
        pygame.draw.rect(self.pantalla, color, rectangulo, border_radius=16)

        cx, cy = centro
        s = tamano * 0.22
        oscuro = (0, 0, 0)

        if direccion == Entrada.UP:
            puntos = [(cx, cy - s), (cx - s, cy + s * 0.6), (cx + s, cy + s * 0.6)]
        elif direccion == Entrada.DOWN:
            puntos = [(cx, cy + s), (cx - s, cy - s * 0.6), (cx + s, cy - s * 0.6)]
        elif direccion == Entrada.LEFT:
            puntos = [(cx - s, cy), (cx + s * 0.6, cy - s), (cx + s * 0.6, cy + s)]
        else:
            puntos = [(cx + s, cy), (cx - s * 0.6, cy - s), (cx - s * 0.6, cy + s)]

        pygame.draw.polygon(self.pantalla, oscuro, puntos)

    def obtener_resultado(self):
        """Devuelve el resultado del juego."""

        return ResultadoJuego(
            juego="Bit Dice",
            puntaje=self.puntaje
        )
