import pygame
from games.juego_base import JuegoBase
from games.resultado_juego import ResultadoJuego
from input.entradas import Entrada


class AtajaLaPelotita(JuegoBase):
    def __init__(self, pantalla):
        super().__init__(pantalla)

        # Inicializacion especifica del juego

    def iniciar(self):
        """Inicializa o reinicia el juego."""

        pass

    def manejar_entrada(self, entrada):
        """Procesa una entrada del jugador."""

        if entrada.jugador == 0 and entrada.entrada == Entrada.SELECT:
            self.terminado = True

    def actualizar(self):
        """Actualiza el estado del juego."""

        pass

    def dibujar(self):
        """Dibuja el juego."""

        self.pantalla.fill((0, 0, 0))

        fuente = pygame.font.Font(None, 64)

        texto = fuente.render(
            "ATAJA LA PELOTITA",
            True,
            (255, 255, 255)
        )

        rectangulo = texto.get_rect(
            center=(400, 250)
        )

        self.pantalla.blit(
            texto,
            rectangulo
        )

        texto_secundario = fuente.render(
            "Juego en construccion",
            True,
            (255, 255, 255)
        )

        rectangulo_secundario = texto_secundario.get_rect(
            center=(400, 350)
        )

        self.pantalla.blit(
            texto_secundario,
            rectangulo_secundario
        )

    def obtener_resultado(self):
        """Devuelve el resultado del juego."""

        return ResultadoJuego(
            juego="Ataja la Pelotita",
            puntaje=self.puntaje
        )