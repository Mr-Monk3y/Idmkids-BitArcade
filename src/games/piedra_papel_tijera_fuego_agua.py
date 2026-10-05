import os
import sys
import pygame
from games.juego_base import JuegoBase
from games.resultado_juego import ResultadoJuego
from input.entradas import Entrada
from input.acciones import Accion

ANCHO_LIENZO = 272
ALTO_LIENZO = 160

TAM_SPRITE = 64

ARCHIVO_FUENTE = "PressStart2P-Regular.ttf"

BLANCO = (255, 255, 255)


def obtener_ruta_assets():
    """Devuelve la carpeta src/assets (funciona también dentro del .exe)."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, "assets")

    return os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "assets"
    )


class PiedraPapelTijeraFuegoAgua(JuegoBase):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        self.jugada_j1 = None
        self.jugada_j2 = None
        self.puntos_j1 = 0
        self.puntos_j2 = 0
        self.ganador_ronda = None
        self.ronda_resuelta = False
        self.tiempo_fin_ronda = None
        self.ultimo_shake = {1: 0, 2: 0}
        self.gana = {"piedra" : ["tijera", "fuego"],
                     "papel" : ["piedra", "agua"],
                     "tijera" : ["papel", "agua"],
                     "fuego" : ["papel", "tijera"],
                     "agua" : ["piedra", "fuego"]}

        ruta_assets = obtener_ruta_assets()
        ruta_juego = os.path.join(ruta_assets, "p_p_t_f_a")

        self.lienzo = pygame.Surface((ANCHO_LIENZO, ALTO_LIENZO))

        self.texto = self.cargar_fuente(ruta_assets, 8)
        self.texto_estado = self.cargar_fuente(ruta_assets, 7)
        self.texto_grande = self.cargar_fuente(ruta_assets, 16)

        # Fondo
        self.fondo = pygame.image.load(
            os.path.join(ruta_juego, "fondo.png")
        ).convert()

        # Por si todavía queda el fondo viejo de 800x600
        if self.fondo.get_size() != (ANCHO_LIENZO, ALTO_LIENZO):
            self.fondo = pygame.transform.scale(
                self.fondo,
                (ANCHO_LIENZO, ALTO_LIENZO)
            )

        # Sprites
        archivos = {
            "piedra": "roca.png",
            "papel": "papel.png",
            "tijera": "tijera.png",
            "fuego": "fuego.png",
            "agua": "agua.png"
        }

        self.imagenes = {}

        for nombre, archivo in archivos.items():
            imagen = pygame.image.load(
                os.path.join(ruta_juego, archivo)
            ).convert_alpha()

            self.imagenes[nombre] = pygame.transform.scale(
                imagen,
                (TAM_SPRITE, TAM_SPRITE)
            )

    def cargar_fuente(self, ruta_assets, tamano):
        """Carga la fuente pixelada; si no está el archivo usa la de pygame."""
        ruta = os.path.join(ruta_assets, "fuentes", ARCHIVO_FUENTE)

        try:
            return pygame.font.Font(ruta, tamano)
        except FileNotFoundError:
            return pygame.font.Font(None, int(tamano * 1.5))

    def iniciar(self):
        """Inicializa o reinicia el juego"""

        self.terminado = False
        self.puntaje = 0
        self.jugada_j1 = None
        self.jugada_j2 = None
        self.puntos_j1 = 0
        self.puntos_j2 = 0
        self.ganador_ronda = None
        self.ronda_resuelta = False

    def manejar_entrada(self, entrada):
        """Procesa micro:bit; SHAKE elige fuego y descarta rebotes repetidos."""

        if entrada.entrada == Entrada.FINISH:
            self.terminado = True
            return
        
        if self.ronda_resuelta or entrada.jugador not in (1, 2):
            return

        jugada = None

        if entrada.accion == Accion.SHAKE:
            ahora = pygame.time.get_ticks()

            if ahora - self.ultimo_shake[entrada.jugador] < 700:
                return

            self.ultimo_shake[entrada.jugador] = ahora
            jugada = "fuego"

        elif entrada.entrada == Entrada.LEFT:
            jugada = "piedra"

        elif entrada.entrada == Entrada.RIGHT:
            jugada = "papel"

        elif entrada.entrada == Entrada.UP:
            jugada = "tijera"

        elif entrada.entrada == Entrada.DOWN:
            jugada = "agua"

        if jugada is None:
            return

        if entrada.jugador == 1:
            self.jugada_j1 = jugada
        else:
            self.jugada_j2 = jugada

        if self.jugada_j1 is not None and self.jugada_j2 is not None:
            self.det_ronda()

    def manejar_entrada_serial(self, entrada):
        """Procesa una entrada proveniente de un microbit."""
        self.manejar_entrada(entrada)

    def det_ronda(self):
        """Determina quién ganó la ronda."""
        if self.jugada_j1 is None or self.jugada_j2 is None: return
        if self.jugada_j1 == self.jugada_j2: self.ganador_ronda = "Empate"
        elif self.jugada_j2 in self.gana[self.jugada_j1]:
            self.ganador_ronda = "Jugador 1"
            self.puntos_j1 += 1
        else:
            self.ganador_ronda = "Jugador 2"
            self.puntos_j2 += 1

        self.ronda_resuelta = True
        self.tiempo_fin_ronda = pygame.time.get_ticks()

    def actualizar(self):
        """Actualiza el estado del juego."""
        if self.ronda_resuelta and self.tiempo_fin_ronda is not None:

            tiempo_actual = pygame.time.get_ticks()

            if tiempo_actual - self.tiempo_fin_ronda >= 2000:
                self.jugada_j1 = None
                self.jugada_j2 = None
                self.ganador_ronda = None
                self.ronda_resuelta = False
                self.tiempo_fin_ronda = None

    def escribir(self, fuente, mensaje, centro):
        """Dibuja texto centrado en el lienzo (sin suavizado, para que quede pixelado)."""
        superficie = fuente.render(mensaje, False, BLANCO)
        self.lienzo.blit(superficie, superficie.get_rect(center=centro))

    def escribir_con_fondo(self, fuente, texto, posicion):
        """Escribe texto con un fondo negro translúcido."""

        superficie_texto = fuente.render(
            texto,
            False,
            (255, 255, 255)
        )

        # Un pequeño margen alrededor del texto
        padding_x = 3
        padding_y = 2

        ancho = superficie_texto.get_width() + padding_x * 2
        alto = superficie_texto.get_height() + padding_y * 2

        # Panel transparente
        panel = pygame.Surface(
            (ancho, alto),
            pygame.SRCALPHA
        )

        panel.fill((0, 0, 0, 140))

        # Centrar el panel en la posición indicada
        rect_panel = panel.get_rect(center=posicion)
        self.lienzo.blit(panel, rect_panel)

        # Centrar el texto encima
        rect_texto = superficie_texto.get_rect(center=posicion)
        self.lienzo.blit(superficie_texto, rect_texto)

    def dibujar(self):
        """Dibuja el juego."""

        # Posiciones dentro del lienzo de 272x160
        x_j1 = ANCHO_LIENZO // 4        # 68
        x_j2 = ANCHO_LIENZO * 3 // 4    # 204
        x_centro = ANCHO_LIENZO // 2    # 136

        self.lienzo.blit(self.fondo, (0, 0))

        self.escribir(self.texto, "PIEDRA PAPEL TIJERA", (x_centro, 8))
        self.escribir(self.texto, "FUEGO Y AGUA", (x_centro, 18))

        self.escribir(self.texto, "JUGADOR 1", (x_j1, 30))
        self.escribir(self.texto, "JUGADOR 2", (x_j2, 30))

        self.escribir(self.texto_grande, str(self.puntos_j1), (x_j1, 43))
        self.escribir(self.texto_grande, str(self.puntos_j2), (x_j2, 43))

        if not self.ronda_resuelta:

            estado_j1 = "ELIGIENDO..." if self.jugada_j1 is None else "¡LISTO!"
            estado_j2 = "ELIGIENDO..." if self.jugada_j2 is None else "¡LISTO!"

            self.escribir_con_fondo(
                self.texto_estado,
                estado_j1,
                (x_j1, 84)
            )

            self.escribir_con_fondo(
                self.texto_estado,
                estado_j2,
                (x_j2, 84)
            )

        else:

            imagen_j1 = self.imagenes[self.jugada_j1]
            imagen_j2 = self.imagenes[self.jugada_j2]

            self.lienzo.blit(imagen_j1, imagen_j1.get_rect(center=(x_j1, 84)))
            self.lienzo.blit(imagen_j2, imagen_j2.get_rect(center=(x_j2, 84)))

            self.escribir(self.texto, self.jugada_j1.upper(), (x_j1, 124))
            self.escribir(self.texto, self.jugada_j2.upper(), (x_j2, 124))

            if self.ganador_ronda == "Empate":
                mensaje = "¡EMPATE!"
            else:
                mensaje = f"¡GANA {self.ganador_ronda.upper()}!"

            self.escribir(self.texto, mensaje, (x_centro, 148))

        self.presentar()

    def presentar(self):
        """Agranda el lienzo 272x160 y lo centra en la pantalla del juego."""
        ancho, alto = self.pantalla.get_size()

        escala = min(ancho / ANCHO_LIENZO, alto / ALTO_LIENZO)
        tamano = (int(ANCHO_LIENZO * escala), int(ALTO_LIENZO * escala))

        # transform.scale usa "vecino más cercano": los píxeles quedan nítidos
        agrandado = pygame.transform.scale(self.lienzo, tamano)

        self.pantalla.fill((0, 0, 0))
        self.pantalla.blit(
            agrandado,
            ((ancho - tamano[0]) // 2, (alto - tamano[1]) // 2)
        )

    def obtener_resultado(self):
        """Devuelve el resultado del juego."""

        if self.puntos_j1 > self.puntos_j2:
            ganador = "Jugador 1"
        elif self.puntos_j2 > self.puntos_j1:
            ganador = "Jugador 2"
        else:
            ganador = "Empate"

        return ResultadoJuego(juego="Piedra, Papel, Tijera, Fuego y Agua", 
                              ganador = ganador, 
                              datos_adicionales = {"puntajes_jugadores": [self.puntos_j1, self.puntos_j2]})