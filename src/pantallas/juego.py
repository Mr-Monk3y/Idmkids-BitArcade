import pygame

from input.entradas import Entrada


class Juego:
    def __init__(self, pantalla):
        self.pantalla = pantalla

        self.fuente = pygame.font.Font(None, 64)
        self.fuente_contador = pygame.font.Font(None, 80)

        self.juego_seleccionado = None

        self.tiempo_inicial = 30
        self.tiempo_restante = self.tiempo_inicial

        self.reloj_contador = pygame.time.get_ticks()

    def establecer_juego(self, juego):
        """Establece el juego seleccionado y reinicia el contador."""
        self.juego_seleccionado = juego

        self.tiempo_restante = self.tiempo_inicial
        self.reloj_contador = pygame.time.get_ticks()

    def actualizar(self):
        """Actualiza el contador del juego."""
        tiempo_actual = pygame.time.get_ticks()

        if tiempo_actual - self.reloj_contador >= 1000:
            self.tiempo_restante -= 1
            self.reloj_contador = tiempo_actual

        return self.tiempo_restante <= 0

    def manejar_entrada(self, entrada):
        """Procesa una entrada del sistema."""

        if entrada.jugador == 0 and entrada.entrada == Entrada.SELECT:
            return True

        return False

    def dibujar(self):
        """Dibuja el juego."""
        self.pantalla.fill((0, 0, 0))

        texto = self.fuente.render(
            self.juego_seleccionado,
            True,
            (255, 255, 255)
        )

        rectangulo = texto.get_rect(
            center=(400, 250)
        )

        self.pantalla.blit(texto, rectangulo)

        contador = self.fuente_contador.render(
            str(max(0, self.tiempo_restante)),
            True,
            (255, 255, 255)
        )

        rectangulo_contador = contador.get_rect(
            center=(400, 400)
        )

        self.pantalla.blit(contador, rectangulo_contador)