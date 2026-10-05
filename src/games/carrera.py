import os

import sys


import pygame


from games.juego_base import JuegoBase

from games.resultado_juego import ResultadoJuego

from games.carrera_core.game import Game


from input.entradas import Entrada

# ============================================================

# CONFIGURACIÓN

# ============================================================


COLORES = [
    "rojo",
    "azul",
    "verde",
    "amarillo",
]


RGB_COLORES = {
    "rojo": (235, 55, 70),
    "azul": (55, 135, 235),
    "verde": (60, 200, 105),
    "amarillo": (245, 205, 55),
}


SHOWROOM_FILES = {
    "rojo": "showroom_rojo.png",
    "azul": "showroom_azul.png",
    "verde": "showroom_verde.png",
    "amarillo": "showroom_amarillo.png",
}


class Carrera(JuegoBase):

    # ========================================================

    # ESTADOS INTERNOS

    # ========================================================

    SELECCION_J1 = "seleccion_j1"

    SELECCION_J2 = "seleccion_j2"

    CARGANDO = "cargando"

    CUENTA_REGRESIVA = "cuenta_regresiva"

    CARRERA = "carrera"

    def __init__(self, pantalla):

        super().__init__(pantalla)

        self.ancho, self.alto = self.pantalla.get_size()

        self.game = None

        self.estado = self.SELECCION_J1

        self.ultimo_tick = None

        # ----------------------------------------------------

        # Selección de autos

        # ----------------------------------------------------

        self.indice_seleccion = 0

        self.color_j1 = None

        self.color_j2 = None

        # ----------------------------------------------------

        # Loading

        # ----------------------------------------------------

        self.loading_timer = 0.0

        self.loading_duration = 1.6

        # ----------------------------------------------------

        # Luces F1

        # ----------------------------------------------------

        self.countdown_timer = 0.0

        self.light_interval = 1.0

        self.all_lights_hold = 1.15

        self.countdown_total = self.light_interval * 5 + self.all_lights_hold

        # ----------------------------------------------------

        # Serial / micro:bit

        # ----------------------------------------------------

        self.serial_activo = {
            1: False,
            2: False,
        }

        # Evita que LEFT/RIGHT mantenido recorra

        # los autos a 60 FPS en el showroom.

        self.seleccion_bloqueada = {
            1: False,
            2: False,
        }

        # ----------------------------------------------------

        # Recursos

        # ----------------------------------------------------

        self.font_cache = {}

        self.showroom_images = self._cargar_showroom_images()

        self.select_sound = self._cargar_sonido("select.wav")

        self.confirm_sound = self._cargar_sonido("confirm.wav")

        self.f1_sound = self._cargar_sonido("f1lights.wav")

        if self.select_sound:

            self.select_sound.set_volume(0.65)

        if self.confirm_sound:

            self.confirm_sound.set_volume(0.75)

        if self.f1_sound:

            self.f1_sound.set_volume(0.85)

    # ========================================================

    # RUTAS / ASSETS

    # ========================================================

    def _ruta_assets(self):

        if hasattr(sys, "_MEIPASS"):

            return os.path.join(
                sys._MEIPASS,
                "assets",
                "juegos",
                "carrera",
            )

        return os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "assets",
                "juegos",
                "carrera",
            )
        )

    def _ruta_imagen(self, filename):

        return os.path.join(
            self._ruta_assets(),
            "imagenes",
            filename,
        )

    def _ruta_audio(self, filename):

        return os.path.join(
            self._ruta_assets(),
            "audio",
            filename,
        )

    # ========================================================

    # RECURSOS

    # ========================================================

    def _font(self, size):

        if size not in self.font_cache:

            self.font_cache[size] = pygame.font.Font(
                None,
                size,
            )

        return self.font_cache[size]

    def _cargar_showroom_images(self):

        images = {}

        for color, filename in SHOWROOM_FILES.items():

            path = self._ruta_imagen(filename)

            if not os.path.exists(path):

                print(f"[Carrera][Showroom] " f"No se encontró: {path}")

                continue

            try:

                image = pygame.image.load(path).convert_alpha()

                images[color] = image

            except pygame.error as error:

                print(f"[Carrera][Showroom] " f"Error cargando {filename}: {error}")

        return images

    def _cargar_sonido(self, filename):

        path = self._ruta_audio(filename)

        if not os.path.exists(path):

            print(f"[Carrera][Audio] " f"No se encontró: {path}")

            return None

        try:

            return pygame.mixer.Sound(path)

        except pygame.error as error:

            print(f"[Carrera][Audio] " f"Error cargando {filename}: {error}")

            return None

    # ========================================================

    # INICIO

    # ========================================================

    def iniciar(self):

        self.terminado = False

        self.puntaje = 0

        self.game = None

        self.estado = self.SELECCION_J1

        self.indice_seleccion = 0

        self.color_j1 = None

        self.color_j2 = None

        self.loading_timer = 0.0

        self.countdown_timer = 0.0

        self.serial_activo = {
            1: False,
            2: False,
        }

        self.seleccion_bloqueada = {
            1: False,
            2: False,
        }

        self.ultimo_tick = pygame.time.get_ticks()

        self._reproducir_musica(
            "showroom.ogg",
            volumen=0.45,
        )

    # ========================================================

    # INPUT

    # ========================================================

    def manejar_entrada(self, entrada):
        """

        Entrada proveniente del teclado.

        """

        jugador = entrada.jugador

        if jugador not in (1, 2):

            return

        # Si el jugador ya está enviando datos por micro:bit,

        # el teclado deja de controlarlo.

        if self.serial_activo[jugador]:

            return

        self._procesar_entrada(entrada)

    def manejar_entrada_serial(self, entrada):
        """

        Entrada proveniente de micro:bit.

        """

        jugador = entrada.jugador

        if jugador not in (1, 2):

            return

        self.serial_activo[jugador] = True

        self._procesar_entrada(entrada)

    def _procesar_entrada(self, entrada):

        if self.estado == self.SELECCION_J1:

            self._entrada_seleccion_j1(entrada)

        elif self.estado == self.SELECCION_J2:

            self._entrada_seleccion_j2(entrada)

        elif self.estado == self.CARRERA:

            self._entrada_carrera(entrada)

    # ========================================================

    # SELECCIÓN J1

    # ========================================================

    def _entrada_seleccion_j1(self, entrada):

        if entrada.jugador != 1:

            return

        # Cuando se suelta la dirección, habilitamos

        # el próximo cambio de auto.

        if entrada.entrada == Entrada.NONE:

            self.seleccion_bloqueada[1] = False

            return

        if entrada.entrada == Entrada.LEFT:

            if self.seleccion_bloqueada[1]:

                return

            self.indice_seleccion -= 1

            self.indice_seleccion %= len(COLORES)

            self.seleccion_bloqueada[1] = True

            self._reproducir(self.select_sound)

        elif entrada.entrada == Entrada.RIGHT:

            if self.seleccion_bloqueada[1]:

                return

            self.indice_seleccion += 1

            self.indice_seleccion %= len(COLORES)

            self.seleccion_bloqueada[1] = True

            self._reproducir(self.select_sound)

        elif entrada.entrada == Entrada.UP:

            self.color_j1 = COLORES[self.indice_seleccion]

            self._reproducir(self.confirm_sound)

            self.indice_seleccion = 0

            # J2 empieza con la selección desbloqueada.

            self.seleccion_bloqueada[2] = False

            self.estado = self.SELECCION_J2

    def _colores_disponibles_j2(self):
        """
        Devuelve los colores disponibles para J2,
        excluyendo el auto elegido por J1.
        """
        return [color for color in COLORES if color != self.color_j1]

    # ========================================================

    # SELECCIÓN J2

    # ========================================================

    def _entrada_seleccion_j2(self, entrada):

        if entrada.jugador != 2:

            return

        disponibles = self._colores_disponibles_j2()

        # Cuando se suelta la dirección, habilitamos

        # el próximo cambio de auto.

        if entrada.entrada == Entrada.NONE:

            self.seleccion_bloqueada[2] = False

            return

        if entrada.entrada == Entrada.LEFT:

            if self.seleccion_bloqueada[2]:

                return

            self.indice_seleccion -= 1

            self.indice_seleccion %= len(disponibles)

            self.seleccion_bloqueada[2] = True

            self._reproducir(self.select_sound)

        elif entrada.entrada == Entrada.RIGHT:

            if self.seleccion_bloqueada[2]:

                return

            self.indice_seleccion += 1

            self.indice_seleccion %= len(disponibles)

            self.seleccion_bloqueada[2] = True

            self._reproducir(self.select_sound)

        elif entrada.entrada == Entrada.UP:

            self.color_j2 = disponibles[self.indice_seleccion]

            self._reproducir(self.confirm_sound)

            self._preparar_carrera()

    # ========================================================

    # PREPARAR CARRERA

    # ========================================================

    def _preparar_carrera(self):
        self._detener_musica(500)

        self.game = Game(
            self.pantalla,
            player_1_color=self.color_j1,
            player_2_color=self.color_j2,
        )

        self.loading_timer = 0.0

        self.estado = self.CARGANDO

        # Frenamos cualquier dirección que haya quedado

        # activa durante la selección.

        self.game.set_player_direction(1, "none")

        self.game.set_player_direction(2, "none")

    # ========================================================

    # INPUT DURANTE CARRERA

    # ========================================================

    def _entrada_carrera(self, entrada):

        if self.game is None:

            return

        jugador = entrada.jugador

        if entrada.entrada == Entrada.LEFT:

            self.game.set_player_direction(
                jugador,
                "left",
            )

        elif entrada.entrada == Entrada.RIGHT:

            self.game.set_player_direction(
                jugador,
                "right",
            )

        elif entrada.entrada == Entrada.NONE:

            self.game.set_player_direction(
                jugador,
                "none",
            )

    # UP se usa solamente para confirmar en showroom.

    # DOWN no tiene uso en la carrera.

    # ========================================================

    # UPDATE

    # ========================================================

    def actualizar(self):

        ahora = pygame.time.get_ticks()

        if self.ultimo_tick is None:

            self.ultimo_tick = ahora

            return

        dt = (ahora - self.ultimo_tick) / 1000.0

        self.ultimo_tick = ahora

        # Evita saltos gigantes si se pierde el foco,

        # se mueve la ventana, etc.

        dt = min(dt, 0.05)

        # ----------------------------------------------------

        # Debounce del showroom para teclado

        # ----------------------------------------------------

        teclas = pygame.key.get_pressed()

        if self.estado == self.SELECCION_J1:

            if not teclas[pygame.K_a] and not teclas[pygame.K_d]:

                self.seleccion_bloqueada[1] = False

        elif self.estado == self.SELECCION_J2:

            if not teclas[pygame.K_LEFT] and not teclas[pygame.K_RIGHT]:

                self.seleccion_bloqueada[2] = False

        # ----------------------------------------------------

        # Loading

        # ----------------------------------------------------

        if self.estado == self.CARGANDO:

            self.loading_timer += dt

            if self.loading_timer >= self.loading_duration:

                self.estado = self.CUENTA_REGRESIVA

                self.countdown_timer = 0.0

                self._reproducir(self.f1_sound)

            return

        # ----------------------------------------------------

        # Countdown F1

        # ----------------------------------------------------

        if self.estado == self.CUENTA_REGRESIVA:

            self.countdown_timer += dt

            if self.countdown_timer >= self.countdown_total:

                self.estado = self.CARRERA

                # Arranca la música de la carrera.

                self._reproducir_musica(
                    "race.ogg",
                    volumen=0.40,
                )

                # Reiniciamos el tick para que la carrera

                # no herede ningún salto temporal.

                self.ultimo_tick = pygame.time.get_ticks()

            return

        # ----------------------------------------------------

        # Carrera

        # ----------------------------------------------------

        if self.estado != self.CARRERA:

            return

        if self.game is None:

            return

        self.game.update(dt)

        # El teclado no manda NONE cuando se suelta una tecla.

        # InputManager vuelve a mandar LEFT/RIGHT cada frame

        # mientras la tecla siga presionada.

        #

        # Por eso reseteamos teclado al terminar el frame.

        # Con micro:bit no, porque manda NONE explícitamente.

        for jugador in (1, 2):

            if not self.serial_activo[jugador]:

                self.game.set_player_direction(
                    jugador,
                    "none",
                )

        if self.game.race.finished:

            self._finalizar_carrera()

    # ========================================================

    # FINAL

    # ========================================================

    def _finalizar_carrera(self):
        if self.terminado:
            return

        self._detener_musica(600)

        self.terminado = True

        winner = self.game.race.winner

        if winner is not None:
            self.puntaje = winner.player_id
        else:
            self.puntaje = 0

    # ========================================================

    # DRAW

    # ========================================================

    def dibujar(self):

        if self.estado == self.SELECCION_J1:

            self._dibujar_showroom(
                jugador=1,
                colores=COLORES,
            )

        elif self.estado == self.SELECCION_J2:

            self._dibujar_showroom(
                jugador=2,
                colores=self._colores_disponibles_j2(),
            )

        elif self.estado == self.CARGANDO:

            self._dibujar_loading()

        elif self.estado == self.CUENTA_REGRESIVA:

            self._dibujar_countdown()

        elif self.estado == self.CARRERA:

            if self.game is not None:

                self.game.draw()

        self._dibujar_crt()

    # ========================================================

    # SHOWROOM

    # ========================================================

    def _dibujar_showroom(self, jugador, colores):

        self.pantalla.fill((8, 10, 16))

        # ----------------------------------------------------

        # Título

        # ----------------------------------------------------

        titulo = self._font(52).render(
            f"JUGADOR {jugador}",
            True,
            (245, 245, 245),
        )

        self.pantalla.blit(
            titulo,
            titulo.get_rect(
                center=(
                    self.ancho // 2,
                    55,
                )
            ),
        )

        subtitulo = self._font(28).render(
            "ELEGÍ TU AUTO",
            True,
            (45, 225, 220),
        )

        self.pantalla.blit(
            subtitulo,
            subtitulo.get_rect(
                center=(
                    self.ancho // 2,
                    100,
                )
            ),
        )

        # ----------------------------------------------------

        # Auto seleccionado

        # ----------------------------------------------------

        color = colores[self.indice_seleccion]

        image = self.showroom_images.get(color)

        if image is not None:

            max_w = int(self.ancho * 0.55)

            max_h = int(self.alto * 0.47)

            escala = min(
                max_w / image.get_width(),
                max_h / image.get_height(),
            )

            nuevo_w = int(image.get_width() * escala)

            nuevo_h = int(image.get_height() * escala)

            image_scaled = pygame.transform.smoothscale(
                image,
                (
                    nuevo_w,
                    nuevo_h,
                ),
            )

            rect = image_scaled.get_rect(
                center=(
                    self.ancho // 2,
                    int(self.alto * 0.47),
                )
            )

            self.pantalla.blit(
                image_scaled,
                rect,
            )

        # ----------------------------------------------------

        # Nombre / color

        # ----------------------------------------------------

        rgb = RGB_COLORES[color]

        nombre = self._font(42).render(
            color.upper(),
            True,
            rgb,
        )

        self.pantalla.blit(
            nombre,
            nombre.get_rect(
                center=(
                    self.ancho // 2,
                    int(self.alto * 0.76),
                )
            ),
        )

        # ----------------------------------------------------

        # Indicadores de colores

        # ----------------------------------------------------

        total = len(colores)

        espacio = 46

        inicio_x = self.ancho // 2 - ((total - 1) * espacio) // 2

        y = int(self.alto * 0.84)

        for i, opcion in enumerate(colores):

            x = inicio_x + i * espacio

            radio = 14

            if i == self.indice_seleccion:

                radio = 19

            pygame.draw.circle(
                self.pantalla,
                RGB_COLORES[opcion],
                (x, y),
                radio,
            )

            if i == self.indice_seleccion:

                pygame.draw.circle(
                    self.pantalla,
                    (245, 245, 245),
                    (x, y),
                    radio + 4,
                    2,
                )

        # ----------------------------------------------------

        # Instrucciones

        # ----------------------------------------------------

        instrucciones = self._font(22).render(
            "IZQUIERDA / DERECHA   •   ARRIBA PARA CONFIRMAR",
            True,
            (130, 135, 150),
        )

        self.pantalla.blit(
            instrucciones,
            instrucciones.get_rect(
                center=(
                    self.ancho // 2,
                    self.alto - 35,
                )
            ),
        )

    # ========================================================

    # LOADING

    # ========================================================

    def _dibujar_loading(self):

        self.pantalla.fill((8, 10, 16))

        texto = self._font(54).render(
            "PREPARANDO CARRERA",
            True,
            (245, 245, 245),
        )

        self.pantalla.blit(
            texto,
            texto.get_rect(
                center=(
                    self.ancho // 2,
                    self.alto // 2 - 30,
                )
            ),
        )

        puntos = int(self.loading_timer * 4) % 4

        loading = self._font(40).render(
            "." * puntos,
            True,
            (45, 225, 220),
        )

        self.pantalla.blit(
            loading,
            loading.get_rect(
                center=(
                    self.ancho // 2,
                    self.alto // 2 + 40,
                )
            ),
        )

    # ========================================================

    # CUENTA REGRESIVA F1

    # ========================================================

    def _dibujar_countdown(self):

        self.pantalla.fill((8, 10, 16))

        titulo = self._font(48).render(
            "PREPARATE",
            True,
            (245, 245, 245),
        )

        self.pantalla.blit(
            titulo,
            titulo.get_rect(
                center=(
                    self.ancho // 2,
                    105,
                )
            ),
        )

        luces_encendidas = min(
            5,
            int(self.countdown_timer / self.light_interval) + 1,
        )

        separacion = 90

        inicio_x = self.ancho // 2 - (separacion * 2)

        y = self.alto // 2

        for i in range(5):

            x = inicio_x + i * separacion

            # Carcasa

            pygame.draw.circle(
                self.pantalla,
                (45, 45, 55),
                (x, y),
                34,
            )

            pygame.draw.circle(
                self.pantalla,
                (105, 105, 115),
                (x, y),
                34,
                3,
            )

            # Luz roja

            if i < luces_encendidas:

                pygame.draw.circle(
                    self.pantalla,
                    (255, 55, 55),
                    (x, y),
                    26,
                )

        if self.countdown_timer < self.light_interval * 5:

            status_text = "PREPARATE"

            status_color = (
                180,
                180,
                190,
            )

        elif self.countdown_timer < self.countdown_total:

            status_text = "..."

            status_color = (
                255,
                65,
                65,
            )

        else:

            status_text = "¡YA!"

            status_color = (
                60,
                235,
                130,
            )

        status = self._font(48).render(
            status_text,
            True,
            status_color,
        )

        self.pantalla.blit(
            status,
            status.get_rect(
                center=(
                    self.ancho // 2,
                    int(self.alto * 0.73),
                )
            ),
        )

        hint = self._font(22).render(
            "NO HACE FALTA ACELERAR",
            True,
            (110, 115, 130),
        )

        self.pantalla.blit(
            hint,
            hint.get_rect(
                center=(
                    self.ancho // 2,
                    self.alto - 45,
                )
            ),
        )

    # ========================================================

    # CRT

    # ========================================================

    def _dibujar_crt(self):

        overlay = pygame.Surface(
            (
                self.ancho,
                self.alto,
            ),
            pygame.SRCALPHA,
        )

        # Scanlines

        for y in range(
            0,
            self.alto,
            4,
        ):

            pygame.draw.line(
                overlay,
                (0, 0, 0, 20),
                (0, y),
                (self.ancho, y),
            )

        # Viñeta lateral

        pygame.draw.rect(
            overlay,
            (0, 0, 0, 22),
            (
                0,
                0,
                15,
                self.alto,
            ),
        )

        pygame.draw.rect(
            overlay,
            (0, 0, 0, 22),
            (
                self.ancho - 15,
                0,
                15,
                self.alto,
            ),
        )

        self.pantalla.blit(
            overlay,
            (0, 0),
        )

    # ========================================================
    # AUDIO
    # ========================================================

    def _reproducir(self, sonido):
        if sonido is not None:
            sonido.play()

    def _reproducir_musica(self, filename, volumen=0.45):
        path = self._ruta_audio(filename)

        if not os.path.exists(path):
            print(f"[Carrera][Música] " f"No se encontró: {path}")
            return

        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(volumen)
            pygame.mixer.music.play(-1)

        except pygame.error as error:
            print(f"[Carrera][Música] " f"Error cargando {filename}: {error}")

    def _detener_musica(self, fade_ms=400):
        pygame.mixer.music.fadeout(fade_ms)

    def detener(self):
        pygame.mixer.music.stop()

        if self.game is not None:
            self.game.set_player_direction(1, "none")
            self.game.set_player_direction(2, "none")

    # ========================================================
    # RESULTADO
    # ========================================================

    def obtener_resultado(self):
        return ResultadoJuego(
            juego="Carrera",
            puntaje=self.puntaje,
        )
