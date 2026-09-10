import os
import random
import pygame
import sys

from games.juego_base import JuegoBase
from games.resultado_juego import ResultadoJuego
from input.entradas import Entrada
from input.acciones import Accion

def obtener_ruta_assets():
    """Obtiene la ruta de los recursos del juego."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(
            sys._MEIPASS,
            "assets",
            "juegos",
            "ataja_la_pelotita"
        )

    return os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "assets",
        "juegos",
        "ataja_la_pelotita"
    )

class AtajaLaPelotita(JuegoBase):
    def __init__(self, pantalla):
        super().__init__(pantalla)

        # Dimensiones de la pantalla
        self.ancho_pantalla = pantalla.get_width()
        self.alto_pantalla = pantalla.get_height()

        # Duración de la partida
        self.duracion = 30
        self.tiempo_inicio = 0
        self.tiempo_restante = self.duracion

        # Cuenta regresiva inicial
        self.duracion_cuenta_regresiva = 3000
        self.inicio_cuenta_regresiva = 0
        self.partida_comenzada = False

        # Selección temporal de cantidad de jugadores humanos
        self.seleccion_dos_jugadores = False

        # Jugadores
        self.cantidad_jugadores = 4
        self.jugadores_humanos = [1]

        # Tamaño lógico del jugador
        self.ancho_jugador = 80
        self.alto_jugador = 30

        # Tamaño de la hitbox
        self.ancho_hitbox = 60
        self.alto_hitbox = 75

        # Desplazamiento de la hitbox dentro del sprite
        self.desplazamiento_hitbox_x = 70
        self.desplazamiento_hitbox_y = 50

        self.velocidad_jugador = 6
        self.velocidad_salto = 14
        self.gravedad = 0.7
        self.posiciones_jugadores = []
        self.velocidades_y = []
        self.jugadores_en_suelo = []

        # Dirección visual de cada jugador
        self.direcciones_jugadores = []

        # Posición anterior para detectar movimiento
        self.posiciones_x_anteriores = []

        # Animaciones
        self.animaciones_jugadores = []
        self.animacion_actual = []
        self.frames_actuales = []
        self.relojes_animacion = []
        self.duracion_idle = 150
        self.duracion_caminar = 100
        self.duracion_salto = 120
        self.ancho_frame = 40
        self.alto_frame = 29

        # Tamaño visual del personaje
        self.ancho_sprite = 200
        self.alto_sprite = 145

        # Ruta de los recursos
        self.ruta_assets = obtener_ruta_assets()

        # Fondo
        self.archivo_fondo = "fondo.png"
        self.imagen_fondo = None

        # Archivos de los jugadores
        self.archivos_sprites = [
            "jugador_azul.png",
            "jugador_rojo.png",
            "jugador_verde.png",
            "jugador_amarillo.png"
        ]

        # Archivos de los objetos
        self.archivos_objetos = {
            "comun": "manzana.png",
            "grande": "sandia.png",
            "rapido": "kiwi.png",
            "especial": "frutilla.png"
        }

        self.imagenes_objetos = {}

        # Objetos
        self.objetos = []
        self.tipos_objetos = {
            "comun": {
                "valor": 1,
                "radio": 12,
                "velocidad": 4
            },
            "grande": {
                "valor": 2,
                "radio": 18,
                "velocidad": 3
            },
            "rapido": {
                "valor": 3,
                "radio": 10,
                "velocidad": 7
            },
            "especial": {
                "valor": 5,
                "radio": 14,
                "velocidad": 5
            }
        }

        self.intervalo_generacion = 700
        self.ultimo_objeto = 0

        # Puntajes
        self.puntajes = [0, 0, 0, 0]

        # Bots
        self.velocidad_bot = 3
        self.probabilidad_salto_bot = 0.08
        self.zonas_bots = {
            2: (0, 260),
            3: (270, 530),
            4: (540, 800)
        }

    def iniciar(self):
        """Inicializa o reinicia el juego."""
        self.terminado = False
        self.puntaje = 0
        self.tiempo_inicio = 0
        self.tiempo_restante = self.duracion
        self.puntajes = [0, 0, 0, 0]
        self.objetos = []

        # Iniciar cuenta regresiva
        self.inicio_cuenta_regresiva = pygame.time.get_ticks()
        self.partida_comenzada = False

        # El juego todavía no comenzó, por lo que no se
        # generan objetos durante la cuenta regresiva.
        self.ultimo_objeto = pygame.time.get_ticks()

        # Posiciones iniciales de los cuatro jugadores
        posiciones_iniciales = [
            (50, self.alto_pantalla - 250),
            (250, self.alto_pantalla - 250),
            (450, self.alto_pantalla - 250),
            (650, self.alto_pantalla - 250)
        ]

        self.posiciones_jugadores = [
            [x, y] for x, y in posiciones_iniciales
        ]

        self.velocidades_y = [0, 0, 0, 0]
        self.jugadores_en_suelo = [False, False, False, False]

        self.direcciones_jugadores = [
            "right",
            "right",
            "right",
            "right"
        ]

        self.posiciones_x_anteriores = [
            posicion[0] for posicion in self.posiciones_jugadores
        ]

        # Cargar las animaciones
        self.cargar_animaciones_jugadores()

        # Cargar las imágenes de los objetos
        self.cargar_imagenes_objetos()

        # Cargar el fondo
        ruta_fondo = os.path.join(
            self.ruta_assets,
            self.archivo_fondo
        )

        self.imagen_fondo = pygame.image.load(
            ruta_fondo
        ).convert()

        ahora = pygame.time.get_ticks()

        self.animacion_actual = [
            "idle",
            "idle",
            "idle",
            "idle"
        ]

        self.frames_actuales = [0, 0, 0, 0]
        self.relojes_animacion = [
            ahora,
            ahora,
            ahora,
            ahora
        ]

    def cargar_animaciones_jugadores(self):
        """Carga y separa los spritesheets de los cuatro jugadores."""
        self.animaciones_jugadores = []

        for archivo in self.archivos_sprites:
            ruta = os.path.join(
                self.ruta_assets,
                archivo
            )

            spritesheet = pygame.image.load(
                ruta
            ).convert_alpha()

            animaciones = {
                "idle": [],
                "walk_right": [],
                "walk_left": [],
                "jump_right": [],
                "jump_left": []
            }

            # Idle: fila 0, cuatro frames
            for columna in range(4):
                frame = spritesheet.subsurface(
                    pygame.Rect(
                        columna * 42,
                        0,
                        self.ancho_frame,
                        self.alto_frame
                    )
                ).copy()
                animaciones["idle"].append(frame)

            # Caminar hacia la derecha: fila 1, seis frames
            for columna in range(6):
                frame = spritesheet.subsurface(
                    pygame.Rect(
                        columna * 42,
                        31,
                        self.ancho_frame,
                        self.alto_frame
                    )
                ).copy()
                animaciones["walk_right"].append(frame)

            # Caminar hacia la izquierda: fila 2, seis frames
            for columna in range(6):
                frame = spritesheet.subsurface(
                    pygame.Rect(
                        columna * 42,
                        62,
                        self.ancho_frame,
                        self.alto_frame
                    )
                ).copy()
                animaciones["walk_left"].append(frame)

            # Saltar hacia la derecha: fila 3, cuatro frames
            for columna in range(4):
                frame = spritesheet.subsurface(
                    pygame.Rect(
                        columna * 42,
                        93,
                        self.ancho_frame,
                        self.alto_frame
                    )
                ).copy()
                animaciones["jump_right"].append(frame)

            # Saltar hacia la izquierda: fila 4, cuatro frames
            for columna in range(4):
                frame = spritesheet.subsurface(
                    pygame.Rect(
                        columna * 42,
                        124,
                        self.ancho_frame,
                        self.alto_frame
                    )
                ).copy()
                animaciones["jump_left"].append(frame)

            self.animaciones_jugadores.append(animaciones)

    def cargar_imagenes_objetos(self):
        """Carga las imágenes de los objetos que caen."""
        self.imagenes_objetos = {}

        for tipo, archivo in self.archivos_objetos.items():
            ruta = os.path.join(
                self.ruta_assets,
                archivo
            )

            imagen = pygame.image.load(
                ruta
            ).convert_alpha()

            self.imagenes_objetos[tipo] = imagen



    def manejar_entrada(self, entrada):
        """Procesa una entrada de un jugador."""
        if entrada is None:
            return

        jugador = entrada.jugador

        if jugador < 0 or jugador > self.cantidad_jugadores:
            return

        # Durante la cuenta regresiva, Z permite seleccionar dos jugadores humanos.
        if not self.partida_comenzada:
            return

        if jugador < 1 or jugador > self.cantidad_jugadores:
            return

        indice = jugador - 1

        # No permitir movimiento durante la cuenta regresiva
        if not self.partida_comenzada:
            return

        # Controles mediante teclado
        if entrada.entrada == Entrada.LEFT:
            self.posiciones_jugadores[indice][0] -= (
                self.velocidad_jugador
            )
            self.direcciones_jugadores[indice] = "left"

        elif entrada.entrada == Entrada.RIGHT:
            self.posiciones_jugadores[indice][0] += (
                self.velocidad_jugador
            )
            self.direcciones_jugadores[indice] = "right"

        elif entrada.entrada == Entrada.UP:
            if self.jugadores_en_suelo[indice]:
                self.velocidades_y[indice] = (
                    -self.velocidad_salto
                )
                self.jugadores_en_suelo[indice] = False

        # Controles mediante micro:bit
        elif jugador == 1 and entrada.accion == Accion.A:
            self.posiciones_jugadores[indice][0] -= (
                self.velocidad_jugador
            )
            self.direcciones_jugadores[indice] = "left"

        elif jugador == 1 and entrada.accion == Accion.B:
            self.posiciones_jugadores[indice][0] += (
                self.velocidad_jugador
            )
            self.direcciones_jugadores[indice] = "right"

        elif jugador == 1 and entrada.accion == Accion.SHAKE:
            if self.jugadores_en_suelo[indice]:
                self.velocidades_y[indice] = (
                    -self.velocidad_salto
                )
                self.jugadores_en_suelo[indice] = False

        # Mantener la hitbox del jugador dentro de la pantalla
        limite_x = (
            self.ancho_pantalla -
            self.ancho_jugador
        )

        if self.posiciones_jugadores[indice][0] < 0:
            self.posiciones_jugadores[indice][0] = 0

        if self.posiciones_jugadores[indice][0] > limite_x:
            self.posiciones_jugadores[indice][0] = limite_x

    def obtener_hitbox_jugador(self, indice):
        """Obtiene el rectángulo de colisión del jugador."""

        # Calcular la posición del sprite exactamente igual
        # que al momento de dibujarlo
        x_sprite = (
            self.posiciones_jugadores[indice][0]
            + self.ancho_jugador / 2
            - self.ancho_sprite / 2
        )

        y_sprite = (
            self.posiciones_jugadores[indice][1]
            + self.alto_jugador
            - self.alto_sprite
        )

        # La hitbox se ubica dentro del frame de 200x145
        return pygame.Rect(
            int(
                x_sprite +
                self.desplazamiento_hitbox_x
            ),
            int(
                y_sprite +
                self.desplazamiento_hitbox_y
            ),
            self.ancho_hitbox,
            self.alto_hitbox
        )

    def actualizar(self):
        """Actualiza continuamente el estado del juego."""
        if self.terminado:
            return

        ahora = pygame.time.get_ticks()

        # Esperar a que termine la cuenta regresiva
        if not self.partida_comenzada:
            tiempo_cuenta_regresiva = (
                ahora - self.inicio_cuenta_regresiva
            )

            # Durante la cuenta regresiva, permitir seleccionar dos jugadores.
            teclas = pygame.key.get_pressed()

            if teclas[pygame.K_z]:
                self.seleccion_dos_jugadores = True
                self.jugadores_humanos = [1, 2]

            if tiempo_cuenta_regresiva >= self.duracion_cuenta_regresiva:
                self.partida_comenzada = True
                self.tiempo_inicio = ahora
                self.tiempo_restante = self.duracion
                self.ultimo_objeto = ahora

            else:
                return

        # Actualizar tiempo
        tiempo_transcurrido = (
            ahora - self.tiempo_inicio
        ) / 1000

        self.tiempo_restante = max(
            0,
            self.duracion - tiempo_transcurrido
        )

        # Gravedad y salto
        for indice in range(self.cantidad_jugadores):
            self.velocidades_y[indice] += self.gravedad

            self.posiciones_jugadores[indice][1] += (
                self.velocidades_y[indice]
            )

            suelo = (
                self.alto_pantalla -
                self.alto_jugador
            )

            if self.posiciones_jugadores[indice][1] >= suelo:
                self.posiciones_jugadores[indice][1] = suelo
                self.velocidades_y[indice] = 0
                self.jugadores_en_suelo[indice] = True
            else:
                self.jugadores_en_suelo[indice] = False

        # Actualizar bots
        self.actualizar_bots()

        # Generar objetos
        if (
            ahora - self.ultimo_objeto
            >= self.intervalo_generacion
        ):
            self.generar_objeto()
            self.ultimo_objeto = ahora

        # Actualizar objetos
        self.actualizar_objetos()

        # Actualizar animaciones
        self.actualizar_animaciones()

        # Comprobar final de partida
        if self.tiempo_restante <= 0:
            self.tiempo_restante = 0
            self.terminado = True

    def generar_objeto(self):
        """Genera un nuevo objeto que cae desde la parte superior."""
        tipo = random.choice(
            list(self.tipos_objetos.keys())
        )

        datos = self.tipos_objetos[tipo]

        x = random.randint(
            datos["radio"],
            self.ancho_pantalla - datos["radio"]
        )

        objeto = {
            "x": x,
            "y": -datos["radio"],
            "tipo": tipo,
            "radio": datos["radio"],
            "valor": datos["valor"],
            "velocidad": datos["velocidad"]
        }

        self.objetos.append(objeto)

    def actualizar_objetos(self):
        """Actualiza la posición de los objetos y sus colisiones."""
        objetos_restantes = []

        for objeto in self.objetos:
            objeto["y"] += objeto["velocidad"]

            atrapado = False

            for indice in range(self.cantidad_jugadores):
                hitbox = self.obtener_hitbox_jugador(indice)

                punto_objeto = pygame.Vector2(
                    objeto["x"],
                    objeto["y"]
                )

                punto_mas_cercano = pygame.Vector2(
                    max(
                        hitbox.left,
                        min(
                            punto_objeto.x,
                            hitbox.right
                        )
                    ),
                    max(
                        hitbox.top,
                        min(
                            punto_objeto.y,
                            hitbox.bottom
                        )
                    )
                )

                distancia = punto_objeto.distance_to(
                    punto_mas_cercano
                )

                if distancia <= objeto["radio"]:
                    self.puntajes[indice] += (
                        objeto["valor"]
                    )
                    atrapado = True
                    break

            if atrapado:
                continue

            if (
                objeto["y"] - objeto["radio"]
                <= self.alto_pantalla
            ):
                objetos_restantes.append(objeto)

        self.objetos = objetos_restantes

    def obtener_objeto_objetivo(
        self,
        indice_jugador,
        objetivos_seleccionados
    ):
        """Busca el mejor objeto para que un bot intente atrapar."""
        jugador = indice_jugador + 1

        if jugador not in self.zonas_bots:
            return None

        zona_inicio, zona_fin = self.zonas_bots[jugador]

        jugador_x = (
            self.posiciones_jugadores[indice_jugador][0]
        )

        candidatos = []

        for indice_objeto, objeto in enumerate(self.objetos):
            if indice_objeto in objetivos_seleccionados:
                continue

            if objeto["x"] < zona_inicio:
                continue

            if objeto["x"] > zona_fin:
                continue

            distancia_horizontal = abs(
                objeto["x"] - jugador_x
            )

            if distancia_horizontal > 180:
                continue

            distancia_vertical = abs(
                objeto["y"] -
                self.posiciones_jugadores[indice_jugador][1]
            )

            prioridad = (
                distancia_horizontal +
                distancia_vertical * 0.35 -
                objeto["valor"] * 15
            )

            candidatos.append(
                (prioridad, indice_objeto)
            )

        if not candidatos:
            return None

        candidatos.sort(
            key=lambda candidato: candidato[0]
        )

        return candidatos[0][1]

    def mover_bot_hacia_objeto(
        self,
        indice_jugador,
        indice_objeto
    ):
        """Mueve un bot hacia su objetivo."""
        jugador = indice_jugador + 1

        zona_inicio, zona_fin = self.zonas_bots[jugador]

        jugador_x = (
            self.posiciones_jugadores[indice_jugador][0]
        )

        if indice_objeto is None:
            centro_zona = (
                zona_inicio + zona_fin
            ) / 2

            if jugador_x < centro_zona - 10:
                self.posiciones_jugadores[indice_jugador][0] += (
                    self.velocidad_bot
                )
                self.direcciones_jugadores[indice_jugador] = (
                    "right"
                )

            elif jugador_x > centro_zona + 10:
                self.posiciones_jugadores[indice_jugador][0] -= (
                    self.velocidad_bot
                )
                self.direcciones_jugadores[indice_jugador] = (
                    "left"
                )

            return

        objeto = self.objetos[indice_objeto]
        objetivo_x = objeto["x"]

        if jugador_x < objetivo_x - 8:
            self.posiciones_jugadores[indice_jugador][0] += (
                self.velocidad_bot
            )
            self.direcciones_jugadores[indice_jugador] = (
                "right"
            )

        elif jugador_x > objetivo_x + 8:
            self.posiciones_jugadores[indice_jugador][0] -= (
                self.velocidad_bot
            )
            self.direcciones_jugadores[indice_jugador] = (
                "left"
            )

        distancia_x = abs(
            objetivo_x - jugador_x
        )

        jugador_y = (
            self.posiciones_jugadores[indice_jugador][1]
        )

        if (
            distancia_x < 50
            and 350 < jugador_y < 530
            and self.jugadores_en_suelo[indice_jugador]
        ):
            if random.random() < self.probabilidad_salto_bot:
                self.velocidades_y[indice_jugador] = (
                    -self.velocidad_salto
                )
                self.jugadores_en_suelo[indice_jugador] = False

    def actualizar_bots(self):
        """Actualiza el movimiento de los jugadores controlados por computadora."""
        objetivos_seleccionados = set()

        for jugador in range(
            1,
            self.cantidad_jugadores + 1
        ):
            if jugador in self.jugadores_humanos:
                continue

            indice = jugador - 1

            indice_objeto = self.obtener_objeto_objetivo(
                indice,
                objetivos_seleccionados
            )

            if indice_objeto is not None:
                objetivos_seleccionados.add(
                    indice_objeto
                )

            self.mover_bot_hacia_objeto(
                indice,
                indice_objeto
            )

            # Mantener al bot dentro de su zona
            zona_inicio, zona_fin = (
                self.zonas_bots[jugador]
            )

            limite_izquierdo = zona_inicio

            limite_derecho = (
                zona_fin -
                self.ancho_jugador
            )

            if (
                self.posiciones_jugadores[indice][0]
                < limite_izquierdo
            ):
                self.posiciones_jugadores[indice][0] = (
                    limite_izquierdo
                )

            if (
                self.posiciones_jugadores[indice][0]
                > limite_derecho
            ):
                self.posiciones_jugadores[indice][0] = (
                    limite_derecho
                )

    def actualizar_animaciones(self):
        """Actualiza el estado y el frame de animación de cada jugador."""
        ahora = pygame.time.get_ticks()

        for indice in range(self.cantidad_jugadores):
            posicion_x_actual = (
                self.posiciones_jugadores[indice][0]
            )

            desplazamiento_x = (
                posicion_x_actual -
                self.posiciones_x_anteriores[indice]
            )

            # Determinar dirección según el movimiento real
            if desplazamiento_x > 0.1:
                self.direcciones_jugadores[indice] = (
                    "right"
                )
            elif desplazamiento_x < -0.1:
                self.direcciones_jugadores[indice] = (
                    "left"
                )

            # Determinar la animación
            if not self.jugadores_en_suelo[indice]:
                nombre_animacion = (
                    "jump_" +
                    self.direcciones_jugadores[indice]
                )
                duracion_frame = self.duracion_salto

            elif abs(desplazamiento_x) > 0.1:
                nombre_animacion = (
                    "walk_" +
                    self.direcciones_jugadores[indice]
                )
                duracion_frame = self.duracion_caminar

            else:
                nombre_animacion = "idle"
                duracion_frame = self.duracion_idle

            # Si cambió la animación, comenzar desde el primer frame
            if (
                self.animacion_actual[indice]
                != nombre_animacion
            ):
                self.animacion_actual[indice] = (
                    nombre_animacion
                )
                self.frames_actuales[indice] = 0
                self.relojes_animacion[indice] = ahora

            # Avanzar frame cuando corresponde
            elif (
                ahora -
                self.relojes_animacion[indice]
                >= duracion_frame
            ):
                frames = self.animaciones_jugadores[
                    indice
                ][nombre_animacion]

                self.frames_actuales[indice] += 1

                if (
                    self.frames_actuales[indice]
                    >= len(frames)
                ):
                    self.frames_actuales[indice] = 0

                self.relojes_animacion[indice] = ahora

            self.posiciones_x_anteriores[indice] = (
                posicion_x_actual
            )

    def obtener_sprite_jugador(self, indice):
        """Obtiene el frame actual del sprite del jugador."""
        nombre_animacion = (
            self.animacion_actual[indice]
        )

        frames = self.animaciones_jugadores[
            indice
        ][nombre_animacion]

        frame = frames[
            self.frames_actuales[indice]
        ]

        # Escalar manteniendo el estilo pixel art
        sprite = pygame.transform.scale(
            frame,
            (
                self.ancho_sprite,
                self.alto_sprite
            )
        )

        return sprite

    def dibujar(self):
        """Dibuja todos los elementos del juego."""
        self.pantalla.blit(self.imagen_fondo,(0, 0))

        # Suelo
        pygame.draw.rect(
            self.pantalla,
            (50, 50, 60),
            (
                0,
                self.alto_pantalla - 10,
                self.ancho_pantalla,
                10
            )
        )

        # Objetos
        for objeto in self.objetos:
            imagen = self.imagenes_objetos[objeto["tipo"]]

            rectangulo = imagen.get_rect(
                center=(
                    int(objeto["x"]),
                    int(objeto["y"])
                )
            )

            self.pantalla.blit(
                imagen,
                rectangulo
            )

        # Jugadores
        for indice in range(
            self.cantidad_jugadores
        ):
            sprite = self.obtener_sprite_jugador(
                indice
            )

            x = int(
                self.posiciones_jugadores[indice][0]
                + self.ancho_jugador / 2
                - self.ancho_sprite / 2
            )

            # El sprite queda apoyado sobre la misma base
            # que utiliza la hitbox del jugador.
            y = int(
                self.posiciones_jugadores[indice][1]
                + self.alto_jugador
                - self.alto_sprite
            )

            self.pantalla.blit(
                sprite,
                (x, y)
            )

        # Cuenta regresiva inicial
        if not self.partida_comenzada:
            tiempo_actual = pygame.time.get_ticks()
            tiempo_transcurrido = (
                tiempo_actual - self.inicio_cuenta_regresiva
            )

            segundos_restantes = 3 - (
                tiempo_transcurrido // 1000
            )

            fuente_cuenta = pygame.font.Font(
                None,
                100
            )

            texto_cuenta = fuente_cuenta.render(
                str(segundos_restantes),
                True,
                (255, 255, 255)
            )

            rectangulo_cuenta = texto_cuenta.get_rect(
                center=(
                    self.ancho_pantalla // 2,
                    self.alto_pantalla // 2
                )
            )

            self.pantalla.blit(
                texto_cuenta,
                rectangulo_cuenta
            )

            fuente_seleccion = pygame.font.Font(None,32)

            texto_seleccion = fuente_seleccion.render("Z: 2 jugadores",True,(255, 255, 255))

            rectangulo_seleccion = texto_seleccion.get_rect(
                center=(
                    self.ancho_pantalla // 2,
                    self.alto_pantalla // 2 + 90
                )
            )

            self.pantalla.blit(
                texto_seleccion,
                rectangulo_seleccion
            )

        # HUD
        fuente = pygame.font.Font(
            None,
            32
        )

        texto_tiempo = fuente.render(
            f"Tiempo: {int(self.tiempo_restante)}",
            True,
            (255, 255, 255)
        )

        self.pantalla.blit(
            texto_tiempo,
            (20, 20)
        )

        for indice in range(
            self.cantidad_jugadores
        ):
            texto_puntaje = fuente.render(
                f"J{indice + 1}: {self.puntajes[indice]}",
                True,
                (255, 255, 255)
            )

            self.pantalla.blit(
                texto_puntaje,
                (
                    180 + indice * 150,
                    20
                )
            )

    def obtener_resultado(self):
        """Devuelve el resultado de la partida."""
        puntaje_maximo = max(
            self.puntajes
        )

        ganador = (
            self.puntajes.index(
                puntaje_maximo
            ) + 1
        )

        return ResultadoJuego(
            juego="Ataja la Pelotita",
            puntaje=puntaje_maximo,
            ganador=ganador,
            datos_adicionales={
                "puntajes": self.puntajes
            }
        )