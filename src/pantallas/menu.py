import pygame

from input.entradas import Entrada


class Menu:
    def __init__(self, pantalla):
        self.pantalla = pantalla

        self.fuente_titulo = pygame.font.Font(None, 72)
        self.fuente_opcion = pygame.font.Font(None, 48)

        self.opciones = [
            "Carrera",
            "Bit Dice",
            "Piedra, Papel, Tijera, Fuego y Agua",
            "Ataja la Pelotita"
        ]

        self.opcion_seleccionada = 0

    def manejar_entrada(self, entrada):
        """Procesa una entrada del usuario."""

        if entrada.entrada == Entrada.UP:
            self.opcion_seleccionada -= 1

            if self.opcion_seleccionada < 0:
                self.opcion_seleccionada = len(self.opciones) - 1

        elif entrada.entrada == Entrada.DOWN:
            self.opcion_seleccionada += 1

            if self.opcion_seleccionada >= len(self.opciones):
                self.opcion_seleccionada = 0

        elif entrada.entrada == Entrada.SELECT:
            return self.opcion_seleccionada

        return None

    def dibujar(self):
        """Dibuja el menu."""
        self.pantalla.fill((0, 0, 0))

        titulo = self.fuente_titulo.render(
            "BIT ARCADE",
            True,
            (255, 255, 255)
        )

        rectangulo_titulo = titulo.get_rect(
            center=(400, 100)
        )

        self.pantalla.blit(titulo, rectangulo_titulo)

        for indice, opcion in enumerate(self.opciones):

            texto = self.fuente_opcion.render(
                opcion,
                True,
                (255, 255, 255)
            )

            rectangulo = texto.get_rect(
                center=(400, 220 + indice * 80)
            )

            self.pantalla.blit(texto, rectangulo)

            if indice == self.opcion_seleccionada:
                pygame.draw.rect(
                    self.pantalla,
                    (255, 255, 255),
                    rectangulo.inflate(30, 15),
                    2
                )