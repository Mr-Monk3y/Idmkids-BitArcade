import pygame

from input.entradas import Entrada


class Instrucciones:
    def __init__(self, pantalla):
        self.pantalla = pantalla

        self.fuente_titulo = pygame.font.Font(None, 64)
        self.fuente_texto = pygame.font.Font(None, 36)
        self.fuente_contador = pygame.font.Font(None, 80)

        self.juego_seleccionado = None

        self.titulo = ""
        self.texto = []

        self.tiempo_inicial = 10
        self.tiempo_restante = self.tiempo_inicial

        self.reloj_contador = pygame.time.get_ticks()

        self.instrucciones = {
            "Carrera": [
                "Aca van las instrucciones de Carrera."
            ],

            "Bit Dice": [
                "Aca van las instrucciones de Bit Dice."
            ],

            "Piedra, Papel, Tijera, Fuego y Agua": [
                "<- Piedra        -> Papel",
                "^ Tijera        v Agua",
                "SACUDIR: Fuego",
                "",
                "Ambos jugadores eligen al mismo tiempo.",
                "Cada elemento vence a dos de los demás.",
                "¡Gana tantas rondas como puedas!"
            ],

            "Ataja la Pelotita": [
                "Aca van las instrucciones de Ataja la Pelotita."
            ]
        }

    def establecer_juego(self, juego):
        """Establece el juego y carga sus instrucciones."""

        self.juego_seleccionado = juego

        self.titulo = juego

        self.texto = self.instrucciones.get(
            juego,
            ["No hay instrucciones disponibles."]
        )

        self.tiempo_restante = self.tiempo_inicial
        self.reloj_contador = pygame.time.get_ticks()

    def actualizar(self):
        """Actualiza el contador de las instrucciones."""

        tiempo_actual = pygame.time.get_ticks()

        if tiempo_actual - self.reloj_contador >= 1000:
            self.tiempo_restante -= 1
            self.reloj_contador = tiempo_actual

        return self.tiempo_restante <= 0

    def manejar_entrada(self, entrada):
        """Procesa una entrada del sistema."""

        if entrada.jugador == 0:

            if entrada.entrada == Entrada.SELECT:
                return True

            if entrada.entrada == Entrada.BACK:
                return True

        return False

    def dibujar(self):
        """Dibuja las instrucciones."""

        self.pantalla.fill((0, 0, 0))

        titulo = self.fuente_titulo.render(
            self.titulo,
            True,
            (255, 255, 255)
        )

        rectangulo_titulo = titulo.get_rect(
            center=(400, 100)
        )

        self.pantalla.blit(
            titulo,
            rectangulo_titulo
        )

        if self.juego_seleccionado == "Piedra, Papel, Tijera, Fuego y Agua":
            y_inicial = 210
            separacion = 38
            fuente_texto = pygame.font.Font(None, 30)

        else:
            y_inicial = 250
            separacion = 50
            fuente_texto = self.fuente_texto

        for indice, linea in enumerate(self.texto):

            texto = fuente_texto.render(linea, True, (255, 255, 255))
            rectangulo_texto = texto.get_rect(center=(400, y_inicial + indice * separacion))
            self.pantalla.blit(texto, rectangulo_texto)

        contador = self.fuente_contador.render(
            str(max(0, self.tiempo_restante)),
            True,
            (255, 255, 255)
        )

        if self.juego_seleccionado == "Piedra, Papel, Tijera, Fuego y Agua":
            posicion_contador = (400, 560)
        else:
            posicion_contador = (400, 500)

        rectangulo_contador = contador.get_rect(center=posicion_contador)

        self.pantalla.blit(
            contador,
            rectangulo_contador
        )