import pygame
import os
import sys

from input.input_manager import InputManager

from games.registro_juegos import RegistroJuegos

from pantallas.estado import Estado
from pantallas.menu import Menu
from pantallas.instrucciones import Instrucciones
from pantallas.resultado import Resultado
from input.entradas import Entrada


# Configuracion de la ventana
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
TITULO_VENTANA = "Bit Arcade"


def main():
    pygame.init()

    if hasattr(sys, "_MEIPASS"):
        ruta_icono = os.path.join(
            sys._MEIPASS,
            "assets",
            "icono.png"
        )
    else:
        ruta_icono = os.path.join(
            os.path.dirname(__file__),
            "assets",
            "icono.png"
        )

    icono = pygame.image.load(ruta_icono)
    pygame.display.set_icon(icono)

    pantalla = pygame.display.set_mode(
        (ANCHO_PANTALLA, ALTO_PANTALLA)
    )

    pygame.display.set_caption(TITULO_VENTANA)

    reloj = pygame.time.Clock()

    input_manager = InputManager()

    menu = Menu(pantalla)
    instrucciones = Instrucciones(pantalla)
    registro_juegos = RegistroJuegos(pantalla)
    juego = None
    resultado = Resultado(pantalla)

    estado_actual = Estado.MENU
    juego_seleccionado = None

    ejecutando = True

    def procesar_entrada(entrada):
        """Procesa una entrada independientemente de su origen."""

        nonlocal estado_actual
        nonlocal juego_seleccionado
        nonlocal juego

        if estado_actual == Estado.MENU:

            opcion = menu.manejar_entrada(entrada)

            if opcion is not None:

                juego_seleccionado = menu.opciones[opcion]

                instrucciones.establecer_juego(
                    juego_seleccionado
                )

                juego = registro_juegos.crear_juego(
                    juego_seleccionado
                )

                juego.iniciar()

                estado_actual = Estado.INSTRUCCIONES

        elif estado_actual == Estado.INSTRUCCIONES:

            if entrada.jugador == 0:
                if entrada.entrada == Entrada.BACK:
                    estado_actual = Estado.MENU
                    return

            avanzar = instrucciones.manejar_entrada(entrada)

            if avanzar:
                estado_actual = Estado.JUEGO

        elif estado_actual == Estado.JUEGO:

            if entrada.jugador == 0:
                if entrada.entrada == Entrada.BACK:
                    estado_actual = Estado.MENU
                    return

            juego.manejar_entrada(entrada)

            if juego.terminado:
                resultado.establecer_resultado(
                    juego.obtener_resultado()
                )

                estado_actual = Estado.RESULTADO

        elif estado_actual == Estado.RESULTADO:

            if entrada.jugador == 0:
                if entrada.entrada == Entrada.BACK:
                    estado_actual = Estado.MENU
                    return

            volver = resultado.manejar_entrada(entrada)

            if volver:
                estado_actual = Estado.MENU

    while ejecutando:

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                ejecutando = False
                continue

            entrada = input_manager.obtener_evento(evento)

            if entrada is not None:
                procesar_entrada(entrada)

        if estado_actual == Estado.JUEGO:
            entradas_mantenidas = (
                input_manager.obtener_entradas_teclado_mantenidas()
            )

            for entrada in entradas_mantenidas:
                procesar_entrada(entrada)

        if estado_actual == Estado.MENU:
            pass

        elif estado_actual == Estado.INSTRUCCIONES:

            if instrucciones.actualizar():
                estado_actual = Estado.JUEGO

        elif estado_actual == Estado.JUEGO:

            juego.actualizar()

            if juego.terminado:
                resultado.establecer_resultado(
                    juego.obtener_resultado()
                )

                estado_actual = Estado.RESULTADO

        elif estado_actual == Estado.RESULTADO:

            if resultado.actualizar():
                estado_actual = Estado.MENU

        if estado_actual == Estado.MENU:
            menu.dibujar()

        elif estado_actual == Estado.INSTRUCCIONES:
            instrucciones.dibujar()

        elif estado_actual == Estado.JUEGO:
            juego.dibujar()

        elif estado_actual == Estado.RESULTADO:
            resultado.dibujar()

        pygame.display.flip()

        reloj.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()