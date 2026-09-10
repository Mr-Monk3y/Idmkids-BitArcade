import pygame
from games.juego_base import JuegoBase
from games.resultado_juego import ResultadoJuego
from input.entradas import Entrada


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
        self.gana = {"piedra" : ["tijera", "fuego"], 
                     "papel" : ["piedra", "agua"],
                     "tijera" : ["papel", "agua"],
                     "fuego" : ["papel", "tijera"],
                     "agua" : ["piedra", "fuego"]}
        self.texto = pygame.font.Font(None, 40)
        self.texto_grande = pygame.font.Font(None, 60)

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
        """Procesa una entrada de un jugador."""
        if self.ronda_resuelta:
            return

        jugada = None

        if entrada.entrada == Entrada.LEFT:
            jugada = "piedra"

        elif entrada.entrada == Entrada.RIGHT:
            jugada = "papel"

        elif entrada.entrada == Entrada.UP:
            jugada = "tijera"

        elif entrada.entrada == Entrada.DOWN:
            jugada = "agua"

        elif entrada.entrada == Entrada.SELECT:
            jugada = "fuego"

        if jugada is None:
            return

        if entrada.jugador == 1:
            self.jugada_j1 = jugada

        elif entrada.jugador == 2:
            self.jugada_j2 = jugada

        if self.jugada_j1 is not None and self.jugada_j2 is not None:
            self.det_ronda()

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

    def dibujar(self):
        """Dibuja el juego."""

        self.pantalla.fill((0,0,0))

        titulo = self.texto_grande.render("Piedra, Papel, Tijera, Fuego y Agua", True, (255, 255, 255))
        titulo_rect = titulo.get_rect(center=(self.pantalla.get_width() // 2, 70))
        self.pantalla.blit(titulo, titulo_rect)
        
        marcador = self.texto.render(f"Jugador 1: {self.puntos_j1}      Jugador 2: {self.puntos_j2}", True, (255, 255, 255))
        marcador_rect = marcador.get_rect(center=(self.pantalla.get_width() // 2, 140))
        self.pantalla.blit(marcador, marcador_rect)
        
        texto_j1 = self.jugada_j1 if self.jugada_j1 else "Esperando..."
        texto_j2 = self.jugada_j2 if self.jugada_j2 else "Esperando..."
        jugada1 = self.texto.render(f"Jugador 1: {texto_j1}", True, (255, 255, 255))
        jugada2 = self.texto.render(f"Jugador 2: {texto_j2}", True, (255, 255, 255))
        
        ancho = self.pantalla.get_width()

        jugada1_rect = jugada1.get_rect(center=(ancho // 4, 250))
        jugada2_rect = jugada2.get_rect(center=(3 * ancho // 4, 250))
        
        self.pantalla.blit(jugada1, jugada1_rect)
        self.pantalla.blit(jugada2, jugada2_rect)

        if self.ganador_ronda is not None:

            if self.ganador_ronda == "Empate":
                mensaje = "¡Empate!"
            else:
                mensaje = f"¡Gana {self.ganador_ronda}!"

            resultado = self.texto_grande.render(
                mensaje,
                True,
                (255, 255, 255)
            )

            resultado_rect = resultado.get_rect(
                center=(self.pantalla.get_width() // 2, 400)
            )

            self.pantalla.blit(resultado, resultado_rect)

    def obtener_resultado(self):
        """Devuelve el resultado del juego."""

        return ResultadoJuego(
            juego="Piedra, Papel, Tijera, Fuego y Agua",
            puntaje=self.puntaje
        )