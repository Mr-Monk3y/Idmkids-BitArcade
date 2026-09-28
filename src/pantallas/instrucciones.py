import os
import sys
import pygame

from input.entradas import Entrada


class Instrucciones:
    def __init__(self, pantalla):
        self.pantalla = pantalla

        self.fuente_titulo = pygame.font.Font(None, 64)
        self.fuente_texto = pygame.font.Font(None, 36)
        self.fuente_contador = pygame.font.Font(None, 80)
        self.fondo_pptfa = self._cargar_fondo_pptfa()

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

    def _cargar_fondo_pptfa(self):
        """Carga el mismo fondo del juego Piedra/Papel/Tijera/Fuego/Agua."""

        if hasattr(sys, "_MEIPASS"):
            ruta_assets = os.path.join(sys._MEIPASS, "assets")
        else:
            ruta_assets = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "assets"
            )

        ruta = os.path.join(
            ruta_assets,
            "p_p_t_f_a",
            "fondo.png"
        )

        try:
            return pygame.image.load(ruta).convert()

        except (pygame.error, FileNotFoundError):
            return None


    def _dibujar_flecha(self, centro, direccion, tamano=34):
        """Dibuja una flecha clara en cualquiera de las cuatro direcciones."""

        cx, cy = centro
        t = tamano

        puntos = [
            (cx, cy - t),
            (cx + t, cy),
            (cx + t // 3, cy),
            (cx + t // 3, cy + t),
            (cx - t // 3, cy + t),
            (cx - t // 3, cy),
            (cx - t, cy),
        ]

        base = pygame.Surface(
            (t * 2 + 6, t * 2 + 6),
            pygame.SRCALPHA
        )

        pts = [
            (x - cx + t + 3, y - cy + t + 3)
            for x, y in puntos
        ]

        # Interior blanco
        pygame.draw.polygon(
            base,
            (255, 255, 255),
            pts
        )

        # Borde oscuro para que contraste con el fondo
        pygame.draw.polygon(
            base,
            (20, 20, 30),
            pts,
            3
        )

        angulos = {
            "UP": 0,
            "LEFT": 90,
            "DOWN": 180,
            "RIGHT": -90
        }

        flecha = pygame.transform.rotate(
            base,
            angulos[direccion]
        )

        self.pantalla.blit(
            flecha,
            flecha.get_rect(center=centro)
        )


    def _dibujar_instrucciones_pptfa(self):
        """Pantalla especial de instrucciones para PPTFA."""

        ancho, alto = self.pantalla.get_size()

        # Mismo fondo que el juego
        if self.fondo_pptfa is not None:
            fondo = pygame.transform.scale(
                self.fondo_pptfa,
                (ancho, alto)
            )

            self.pantalla.blit(fondo, (0, 0))

        else:
            self.pantalla.fill((0, 0, 0))

        # Panel oscuro transparente.
        # Deja ver el fondo pero mantiene legibles el texto y las flechas.
        panel = pygame.Surface(
            (720, 510),
            pygame.SRCALPHA
        )

        panel.fill((0, 0, 0, 145))

        self.pantalla.blit(
            panel,
            panel.get_rect(
                center=(ancho // 2, alto // 2)
            )
        )

        fuente_titulo = pygame.font.Font(None, 48)
        fuente_opcion = pygame.font.Font(None, 30)
        fuente_info = pygame.font.Font(None, 25)

        # Título
        titulo1 = fuente_titulo.render(
            "PIEDRA PAPEL TIJERA",
            True,
            (255, 255, 255)
        )

        titulo2 = fuente_titulo.render(
            "FUEGO Y AGUA",
            True,
            (255, 255, 255)
        )

        self.pantalla.blit(
            titulo1,
            titulo1.get_rect(center=(400, 72))
        )

        self.pantalla.blit(
            titulo2,
            titulo2.get_rect(center=(400, 112))
        )

        # Flechas y acciones
        opciones = [
            ((245, 205), "LEFT", "PIEDRA"),
            ((555, 205), "RIGHT", "PAPEL"),
            ((245, 320), "UP", "TIJERA"),
            ((555, 320), "DOWN", "AGUA"),
        ]

        for centro, direccion, nombre in opciones:
            self._dibujar_flecha(
                centro,
                direccion,
                28
            )

            texto = fuente_opcion.render(
                nombre,
                True,
                (255, 255, 255)
            )

            self.pantalla.blit(
                texto,
                texto.get_rect(
                    center=(
                        centro[0],
                        centro[1] + 58
                    )
                )
            )

        # Shake / fuego
        fuego = fuente_opcion.render(
            "SACUDIR = FUEGO",
            True,
            (255, 255, 255)
        )

        self.pantalla.blit(
            fuego,
            fuego.get_rect(center=(400, 420))
        )

        # Explicación corta
        info = fuente_info.render(
            "Elegí al mismo tiempo que tu rival",
            True,
            (255, 255, 255)
        )

        self.pantalla.blit(
            info,
            info.get_rect(center=(400, 465))
        )

        # Contador
        contador = self.fuente_contador.render(
            str(max(0, self.tiempo_restante)),
            True,
            (255, 255, 255)
        )

        self.pantalla.blit(
            contador,
            contador.get_rect(center=(400, 535))
        )

    def dibujar(self):
        """Dibuja las instrucciones."""

        if self.juego_seleccionado == "Piedra, Papel, Tijera, Fuego y Agua":
            self._dibujar_instrucciones_pptfa()
            return

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