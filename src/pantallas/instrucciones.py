import os
import sys
import pygame

from input.entradas import Entrada

ARCHIVO_FUENTE = "PressStart2P-Regular.ttf"


class Instrucciones:
    def __init__(self, pantalla):
        self.pantalla = pantalla

        self.fuente_titulo = pygame.font.Font(None, 64)
        self.fuente_texto = pygame.font.Font(None, 36)
        self.fuente_contador = pygame.font.Font(None, 80)
        self.fondo_pptfa = self._cargar_fondo_pptfa()
        self.fondo_lluvia_frutas = self._cargar_fondo_lluvia_frutas()
        self.objetos_lluvia_frutas = self._cargar_objetos_lluvia_frutas()

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

    def cargar_fuente(self, ruta_assets, tamano):
        """Carga la fuente pixelada; si no está el archivo usa la de pygame."""
        ruta = os.path.join(ruta_assets, "fuentes", ARCHIVO_FUENTE)

        try:
            return pygame.font.Font(ruta, tamano)
        except FileNotFoundError:
            return pygame.font.Font(None, int(tamano * 1.5))

    def _cargar_fondo_pptfa(self):
        """Carga el mismo fondo del juego Piedra/Papel/Tijera/Fuego/Agua."""

        if hasattr(sys, "_MEIPASS"):
            self.ruta_assets = os.path.join(sys._MEIPASS, "assets")
        else:
            self.ruta_assets = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "assets"
            )

        ruta = os.path.join(
            self.ruta_assets,
            "p_p_t_f_a",
            "fondo.png"
        )

        try:
            return pygame.image.load(ruta).convert()

        except (pygame.error, FileNotFoundError):
            return None

    def _cargar_fondo_lluvia_frutas(self):
        """Carga el fondo utilizado por Lluvia de Frutas."""

        ruta = os.path.join(
            self.ruta_assets,
            "juegos",
            "ataja_la_pelotita",
            "fondo.png"
        )

        try:
            return pygame.image.load(ruta).convert()

        except (pygame.error, FileNotFoundError):
            return None


    def _cargar_objetos_lluvia_frutas(self):
        """Carga las imágenes de los objetos de Lluvia de Frutas."""

        archivos = {
            "comun": "manzana.png",
            "grande": "sandia.png",
            "rapido": "kiwi.png",
            "especial": "frutilla.png",
            "malo": "podrida.png"
        }

        imagenes = {}

        for nombre, archivo in archivos.items():
            ruta = os.path.join(
                self.ruta_assets,
                "juegos",
                "ataja_la_pelotita",
                archivo
            )

            try:
                imagenes[nombre] = pygame.image.load(
                    ruta
                ).convert_alpha()

            except (pygame.error, FileNotFoundError):
                imagenes[nombre] = None

        return imagenes

    def _dibujar_flecha(self, centro, direccion, tamano=7):
        """Dibuja una flecha estilo pixel art."""

        cx, cy = centro
        p = tamano

        # Forma base: flecha apuntando hacia arriba.
        # Cada posición representa un "píxel" grande.
        bloques = [
            (0, -3),

            (-1, -2),
            (0, -2),
            (1, -2),

            (-2, -1),
            (-1, -1),
            (0, -1),
            (1, -1),
            (2, -1),

            (-1, 0),
            (0, 0),
            (1, 0),

            (-1, 1),
            (0, 1),
            (1, 1),

            (-1, 2),
            (0, 2),
            (1, 2),

            (-1, 3),
            (0, 3),
            (1, 3),
        ]

        # Superficie transparente donde armamos la flecha.
        superficie = pygame.Surface(
            (p * 9, p * 9),
            pygame.SRCALPHA
        )

        centro_superficie = p * 4

        # Dibujamos la flecha bloque por bloque.
        for x, y in bloques:
            pygame.draw.rect(
                superficie,
                (255, 255, 255),
                (
                    centro_superficie + x * p,
                    centro_superficie + y * p,
                    p,
                    p
                )
            )

        # La flecha original apunta hacia arriba.
        # La rotamos según la dirección necesaria.
        angulos = {
            "UP": 0,
            "LEFT": 90,
            "DOWN": 180,
            "RIGHT": -90
        }

        superficie = pygame.transform.rotate(
            superficie,
            angulos[direccion]
        )

        rect = superficie.get_rect(center=(cx, cy))
        self.pantalla.blit(superficie, rect)


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

        fuente_titulo = self.cargar_fuente(self.ruta_assets, 22)
        fuente_opcion = self.cargar_fuente(self.ruta_assets, 14)
        fuente_info = self.cargar_fuente(self.ruta_assets, 10)
        fuente_fuego = self.cargar_fuente(self.ruta_assets, 16)

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
                7
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
        fuego = fuente_fuego.render(
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

        fuente_contador = self.cargar_fuente(
            self.ruta_assets,
            32
        )

        # Contador
        contador = fuente_contador.render(
            str(max(0, self.tiempo_restante)),
            True,
            (255, 255, 255)
        )

        self.pantalla.blit(
            contador,
            contador.get_rect(center=(400, 535))
        )

    def _dibujar_instrucciones_lluvia_frutas(self):
        """Pantalla especial de instrucciones para Lluvia de Frutas."""

        ancho, alto = self.pantalla.get_size()

        # Mismo fondo que el juego.
        if self.fondo_lluvia_frutas is not None:
            fondo = pygame.transform.scale(
                self.fondo_lluvia_frutas,
                (ancho, alto)
            )

            self.pantalla.blit(fondo, (0, 0))

        else:
            self.pantalla.fill((0, 0, 0))

        # Panel oscuro transparente.
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

        # Fuente pixelada.
        fuente_titulo = self.cargar_fuente(
            self.ruta_assets,
            22
        )

        # Título visible del juego.
        titulo = fuente_titulo.render(
            "LLUVIA DE FRUTAS",
            True,
            (255, 255, 255)
        )

        self.pantalla.blit(
            titulo,
            titulo.get_rect(
                center=(400, 80)
            )
        )

        # Controles.
        fuente_control = self.cargar_fuente(
            self.ruta_assets,
            12
        )

        controles = [
            ((230, 185), "LEFT", "MOVERSE"),
            ((400, 185), "UP", "SALTAR"),
            ((570, 185), "RIGHT", "MOVERSE"),
        ]

        for centro, direccion, nombre in controles:
            self._dibujar_flecha(
                centro,
                direccion,
                7
            )

            texto = fuente_control.render(
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

        # Explicación de los objetos.
        fuente_info = self.cargar_fuente(
            self.ruta_assets,
            10
        )

        texto_objetivo = fuente_info.render(
            "ATRAPA LOS OBJETOS Y SUMA PUNTOS",
            True,
            (255, 255, 255)
        )

        self.pantalla.blit(
            texto_objetivo,
            texto_objetivo.get_rect(
                center=(400, 285)
            )
        )

        fuente_puntos = self.cargar_fuente(
            self.ruta_assets,
            14
        )

        # Objetos y sus puntajes.
        objetos = [
            ("comun", 1),
            ("grande", 2),
            ("rapido", 3),
            ("especial", 5),
            ("malo", -3),
        ]

        posiciones_x = [
            200,
            300,
            400,
            500,
            600
        ]

        for (tipo, puntos), x in zip(
            objetos,
            posiciones_x
        ):
            imagen = self.objetos_lluvia_frutas[tipo]

            if imagen is not None:
                imagen = pygame.transform.scale(
                    imagen,
                    (64, 64)
                )

                self.pantalla.blit(
                    imagen,
                    imagen.get_rect(
                        center=(x, 345)
                    )
                )

            if puntos > 0:
                texto_puntos = f"+{puntos}"
            else:
                texto_puntos = str(puntos)

            superficie_puntos = fuente_puntos.render(
                texto_puntos,
                True,
                (255, 255, 255)
            )

            self.pantalla.blit(
                superficie_puntos,
                superficie_puntos.get_rect(
                    center=(x, 395)
                )
            )

        # Objetivo final.
        fuente_objetivo = self.cargar_fuente(
            self.ruta_assets,
            15
        )

        objetivo = fuente_objetivo.render(
            "¡CONSEGUI EL MAYOR PUNTAJE!",
            True,
            (255, 255, 255)
        )

        self.pantalla.blit(
            objetivo,
            objetivo.get_rect(
                center=(400, 460)
            )
        )

        fuente_contador = self.cargar_fuente(
            self.ruta_assets,
            32
        )

        # Contador.
        contador = fuente_contador.render(
            str(max(0, self.tiempo_restante)),
            True,
            (255, 255, 255)
        )

        self.pantalla.blit(
            contador,
            contador.get_rect(
                center=(400, 530)
            )
        )

    def _dibujar_instrucciones_bit_dice(self):
        """Pantalla especial de instrucciones para Bit Dice."""

        ancho, alto = self.pantalla.get_size()

        # Fondo negro.
        self.pantalla.fill((0, 0, 0))

        # Fuentes pixeladas.
        fuente_titulo = self.cargar_fuente(
            self.ruta_assets,
            24
        )

        fuente_texto = self.cargar_fuente(
            self.ruta_assets,
            12
        )

        fuente_destacada = self.cargar_fuente(
            self.ruta_assets,
            14
        )

        fuente_contador = self.cargar_fuente(
            self.ruta_assets,
            32
        )

        # Título.
        titulo = fuente_titulo.render(
            "BIT DICE",
            True,
            (255, 255, 255)
        )

        self.pantalla.blit(
            titulo,
            titulo.get_rect(
                center=(ancho // 2, 75)
            )
        )

        # Primera instrucción.
        texto_memoriza = fuente_texto.render(
            "MEMORIZA LA SECUENCIA",
            True,
            (255, 255, 255)
        )

        self.pantalla.blit(
            texto_memoriza,
            texto_memoriza.get_rect(
                center=(ancho // 2, 155)
            )
        )

        # Flechas que representan la secuencia.
        direcciones = [
            ((250, 235), "LEFT"),
            ((350, 235), "UP"),
            ((450, 235), "RIGHT"),
            ((550, 235), "DOWN"),
        ]

        for centro, direccion in direcciones:
            self._dibujar_flecha(
                centro,
                direccion,
                10
            )

        # Segunda instrucción.
        texto_repetir = fuente_texto.render(
            "Y REPETILA EN ORDEN",
            True,
            (255, 255, 255)
        )

        self.pantalla.blit(
            texto_repetir,
            texto_repetir.get_rect(
                center=(ancho // 2, 325)
            )
        )

        # Explicación de la dificultad.
        texto_ronda = fuente_texto.render(
            "CADA RONDA SUMA UN PASO",
            True,
            (255, 255, 255)
        )

        self.pantalla.blit(
            texto_ronda,
            texto_ronda.get_rect(
                center=(ancho // 2, 390)
            )
        )

        # Objetivo final.
        texto_objetivo = fuente_destacada.render(
            "¡LLEGA LO MAS LEJOS!",
            True,
            (255, 255, 255)
        )

        self.pantalla.blit(
            texto_objetivo,
            texto_objetivo.get_rect(
                center=(ancho // 2, 460)
            )
        )

        # Cuenta regresiva.
        contador = fuente_contador.render(
            str(max(0, self.tiempo_restante)),
            True,
            (255, 255, 255)
        )

        self.pantalla.blit(
            contador,
            contador.get_rect(
                center=(ancho // 2, 535)
            )
        )

    def dibujar(self):
        """Dibuja las instrucciones."""

        if self.juego_seleccionado == "Piedra, Papel, Tijera, Fuego y Agua":
            self._dibujar_instrucciones_pptfa()
            return

        if self.juego_seleccionado == "Ataja la Pelotita":
            self._dibujar_instrucciones_lluvia_frutas()
            return

        if self.juego_seleccionado == "Bit Dice":
            self._dibujar_instrucciones_bit_dice()
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