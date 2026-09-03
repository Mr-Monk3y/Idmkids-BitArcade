import pygame

from input.entradas import Entrada


class Resultado:
    def __init__(self, pantalla):
        self.pantalla = pantalla

        self.fuente_titulo = pygame.font.Font(None, 64)
        self.fuente_texto = pygame.font.Font(None, 48)
        self.fuente_contador = pygame.font.Font(None, 64)

        self.juego_seleccionado = None

        self.puntaje = 0

        self.tiempo_inicial = 5
        self.tiempo_restante = self.tiempo_inicial

        self.reloj_contador = pygame.time.get_ticks()

    def establecer_resultado(self, juego, puntaje):
        """Establece los datos del resultado y reinicia el contador."""
        self.juego_seleccionado = juego
        self.puntaje = puntaje

        self.tiempo_restante = self.tiempo_inicial
        self.reloj_contador = pygame.time.get_ticks()

    def actualizar(self):
        """Actualiza el contador del resultado."""
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
        """Dibuja el resultado."""
        self.pantalla.fill((0, 0, 0))

        titulo = self.fuente_titulo.render(
            "RESULTADO",
            True,
            (255, 255, 255)
        )

        rectangulo_titulo = titulo.get_rect(
            center=(400, 100)
        )

        self.pantalla.blit(titulo, rectangulo_titulo)

        juego = self.fuente_texto.render(
            self.juego_seleccionado,
            True,
            (255, 255, 255)
        )

        rectangulo_juego = juego.get_rect(
            center=(400, 220)
        )

        self.pantalla.blit(juego, rectangulo_juego)

        puntaje = self.fuente_texto.render(
            f"Puntaje: {self.puntaje}",
            True,
            (255, 255, 255)
        )

        rectangulo_puntaje = puntaje.get_rect(
            center=(400, 320)
        )

        self.pantalla.blit(puntaje, rectangulo_puntaje)

        contador = self.fuente_contador.render(
            str(max(0, self.tiempo_restante)),
            True,
            (255, 255, 255)
        )

        rectangulo_contador = contador.get_rect(
            center=(400, 430)
        )

        self.pantalla.blit(contador, rectangulo_contador)