import os
import sys
import pygame

from input.entradas import Entrada

ARCHIVO_FUENTE = "PressStart2P-Regular.ttf"

class Resultado:
    def __init__(self, pantalla):
        self.pantalla = pantalla

        if hasattr(sys, "_MEIPASS"):
            self.ruta_assets = os.path.join(sys._MEIPASS, "assets")
        else:
            self.ruta_assets = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")

        self.fuente_titulo = self.cargar_fuente(32)
        self.fuente_texto = self.cargar_fuente(16)
        self.fuente_contador = self.cargar_fuente(28)
        self.fuente_ayuda = self.cargar_fuente(9)

        self.fondo = self.cargar_fondo()

        self.resultado = None
        self.tiempo_inicial = 5
        self.tiempo_restante = self.tiempo_inicial

        self.reloj_contador = pygame.time.get_ticks()

    def cargar_fuente(self, tamano):
        """Carga la fuente pixelada."""

        ruta = os.path.join(self.ruta_assets, "fuentes", ARCHIVO_FUENTE)
        try:
            return pygame.font.Font(ruta, tamano)
        except FileNotFoundError:
            return pygame.font.Font(None, tamano)

    def cargar_fondo(self):
        """Carga el fondo de res."""

        ruta = os.path.join(self.ruta_assets, "resultado", "fondores.jpg")
        try:
            return pygame.image.load(ruta).convert()
        except (pygame.error, FileNotFoundError):
            return None
        

    def establecer_resultado(self, resultado):
        """Establece el resultado y reinicia el contador."""

        self.resultado = resultado

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
        """Procesa una entrada del usuario."""

        if entrada.jugador == 0 and entrada.entrada == Entrada.SELECT:
            return True

        return False

    def dibujar_fondo(self):
        """Escala el fondo para cubrir la pantalla"""
        ancho, alto = self.pantalla.get_size()
        if self.fondo is None:
            self.pantalla.fill((30,30,30))
            return
        ancho_fondo = self.fondo.get_width()
        alto_fondo = self.fondo.get_height()
        escala = max(ancho / ancho_fondo, alto / alto_fondo)
        nuevo_ancho = int(ancho_fondo * escala)
        nuevo_alto = int(alto_fondo * escala)
        fondo_escalado = pygame.transform.scale(self.fondo, (nuevo_ancho, nuevo_alto))
        x = (ancho - nuevo_ancho) // 2
        y = (alto - nuevo_alto) // 2
        self.pantalla.blit(fondo_escalado, (x,y))

    def dibujar(self):
        """Dibuja el resultado."""

        ancho, alto = self.pantalla.get_size()
        x_centro = ancho // 2

        self.dibujar_fondo()

        ancho_panel = min(650, int(ancho * 0.75))
        alto_panel = min(400, int(alto * 0.65))
        panel = pygame.Surface((ancho_panel, alto_panel), pygame.SRCALPHA)
        panel.fill((15,15,20,185))
        rect_panel = panel.get_rect(center=(x_centro, alto // 2))
        self.pantalla.blit(panel, rect_panel)
        pygame.draw.rect(self.pantalla, (255, 190, 80), rect_panel, 4)
        
        titulo = self.fuente_titulo.render("RESULTADO", False, (255, 255, 255))
        rect_titulo = titulo.get_rect(center=(x_centro, rect_panel.top + 60))
        self.pantalla.blit(titulo, rect_titulo)
        if self.resultado is None:
            return

        juego = self.fuente_texto.render(self.resultado.juego.upper(), False, (255, 255, 255))
        rect_juego = juego.get_rect(center=(x_centro, rect_panel.top + 135))
        self.pantalla.blit(juego, rect_juego)

        puntajes_jugadores = self.resultado.datos_adicionales.get("puntajes_jugadores")
        if puntajes_jugadores:
            cantidad = len(puntajes_jugadores)
            espacio = ancho_panel // (cantidad + 1)
            for i, puntos in enumerate(puntajes_jugadores):
                x_jugador = rect_panel.left + espacio * (i + 1)
                nombre = self.fuente_ayuda.render(f"JUGADOR {i + 1}", False, (255, 255, 255))
                self.pantalla.blit(nombre, nombre.get_rect(center=(x_jugador, rect_panel.top + 190)))
                puntaje = self.fuente_contador.render(str(puntos), False, (255, 210, 80))
                self.pantalla.blit(puntaje, puntaje.get_rect(center=(x_jugador, rect_panel.top + 230)))
                if self.resultado.ganador is not None:
                    if self.resultado.ganador == "Empate":
                        mensaje = "EMPATE"
                    else:
                        mensaje = f"GANA {self.resultado.ganador.upper()}"

                    ganador = self.fuente_texto.render(mensaje, False, (255, 255, 255))
                    self.pantalla.blit(ganador, ganador.get_rect(center=(x_centro, rect_panel.top + 285)))
        else:
            puntaje = self.fuente_texto.render(f"PUNTAJE: {self.resultado.puntaje}", False, (255, 255, 255))
            self.pantalla.blit(puntaje, puntaje.get_rect(center=(x_centro, rect_panel.top + 220)))

        ayuda = self.fuente_ayuda.render(f"VOLVIENDO AL MENU {max(0, self.tiempo_restante)}...", False, (255, 255,255))
        rect_ayuda = ayuda.get_rect(center=(x_centro, rect_panel.bottom - 35))
        self.pantalla.blit(ayuda, rect_ayuda)
