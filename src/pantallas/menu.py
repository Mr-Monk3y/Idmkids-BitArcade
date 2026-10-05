import os
import sys
import pygame

from input.entradas import Entrada

ARCHIVO_FUENTE = "PressStart2P-Regular.ttf"

class Menu:
    def __init__(self, pantalla):
        self.pantalla = pantalla

        if hasattr(sys, "_MEIPASS"):
            self.ruta_assets = os.path.join(sys._MEIPASS, "assets")
        else:
            self.ruta_assets = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
        
        self.fuente_titulo = self.cargar_fuente(36)
        self.fuente_opcion = self.cargar_fuente(18)
        self.fuente_ayuda = self.cargar_fuente(10)

        self.fondo = self.cargar_fondo()

        self.opciones = [
            "Carrera",
            "Bit Dice",
            "Piedra, Papel, Tijera, Fuego y Agua",
            "Ataja la Pelotita"
        ]

        self.opcion_seleccionada = 0

    def cargar_fuente(self, tamano):
        """Carga la fuente pixelada."""
        ruta = os.path.join(self.ruta_assets, "fuentes", ARCHIVO_FUENTE)
        try:
            return pygame.font.Font(ruta, tamano)
        except FileNotFoundError:
            return pygame.font.Font(None, tamano)

    def cargar_fondo(self):
        """Carga el fondo pixel art del menu"""
        ruta = os.path.join(self.ruta_assets, "menu", "fondo.jpg")
        try:
            return pygame.image.load(ruta).convert()
        except (pygame.error, FileNotFoundError):
            return None

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

    def dibujar_fondo(self):
        """Escala el fondo para cubrir toda la pantalla sin deformarlo."""
        ancho, alto = self.pantalla.get_size()

        if self.fondo is None:
            self.pantalla.fill((30, 140, 200))
            return

        ancho_fondo = self.fondo.get_width()
        alto_fondo = self.fondo.get_height()
        escala = max(ancho/ancho_fondo, alto/alto_fondo)
        nuevo_ancho = int(ancho_fondo * escala)
        nuevo_alto = int(alto_fondo * escala)
        fondo_escalado = pygame.transform.scale(self.fondo, (nuevo_ancho, nuevo_alto))
        x = (ancho - nuevo_ancho) // 2
        y = (alto - nuevo_alto) // 2
        self.pantalla.blit(fondo_escalado, (x,y))
        

    def dibujar(self):
        """Dibuja el menu."""
        ancho, alto = self.pantalla.get_size()
        x_centro = ancho // 2
        self.dibujar_fondo()

        titulo = self.fuente_titulo.render("BIT ARCADE", False, (255,255,255))
        rectangulo_titulo = titulo.get_rect(center=(x_centro, int(alto * 0.16)))
        sombra = self.fuente_titulo.render("BIT ARCADE", False, (20,60,90))
        rectangulo_sombra = sombra.get_rect(center=(x_centro + 4, int(alto * 0.16) + 4))
        self.pantalla.blit(sombra, rectangulo_sombra)
        self.pantalla.blit(titulo, rectangulo_titulo)

        ancho_panel = min(720, int(ancho * 0.75))
        alto_panel = min(390, int(alto * 0.58))
        panel = pygame.Surface((ancho_panel, alto_panel), pygame.SRCALPHA)
        panel.fill((8,25,45,165))
        rectangulo_panel = panel.get_rect(center=(x_centro, int(alto * 0.57)))
        self.pantalla.blit(panel, rectangulo_panel)
        pygame.draw.rect(self.pantalla, (255, 255, 255), rectangulo_panel, 3)
        

        cantidad_opciones = len(self.opciones)
        y_inicio = rectangulo_panel.top + 70
        y_fin = rectangulo_panel.bottom - 50
        espacio = (y_fin - y_inicio) // max(1, cantidad_opciones -1)

        for indice, opcion in enumerate(self.opciones):
            y = y_inicio + indice * espacio
            if indice == self.opcion_seleccionada:
                color = (255, 210, 80)
            else:
                color = (255, 255, 255)

            if opcion == "Ataja la Pelotita":
                nombre_visible = "Lluvia de Frutas"
            else:
                nombre_visible = opcion

            if opcion == "Piedra, Papel, Tijera, Fuego y Agua":
                linea1 = self.fuente_opcion.render("PIEDRA, PAPEL, TIJERA", False, color)
                linea2 = self.fuente_opcion.render("FUEGO Y AGUA", False, color)
                rect1 = linea1.get_rect(center=(x_centro, y - 12))
                rect2 = linea2.get_rect(center=(x_centro, y + 12))
                self.pantalla.blit(linea1, rect1)
                self.pantalla.blit(linea2, rect2)
                if indice == self.opcion_seleccionada:
                    rectangulo = rect1.union(rect2)
                    pygame.draw.rect(self.pantalla, (255, 210, 80), rectangulo.inflate(30,14), 2)
            else:
                texto = self.fuente_opcion.render(opcion.upper(), False, color)
                rectangulo = texto.get_rect(center=(x_centro, y))
                self.pantalla.blit(texto, rectangulo)

                if indice == self.opcion_seleccionada:
                    pygame.draw.rect(self.pantalla, (255, 210, 80), rectangulo.inflate(30, 18), 2)


        ayuda = self.fuente_ayuda.render("ARRIBA / ABAJO PARA ELEGIR", False, (255, 255, 255))

        rect_ayuda = ayuda.get_rect(center=(x_centro, int(alto * 0.94)))

        self.pantalla.blit(ayuda, rect_ayuda)
