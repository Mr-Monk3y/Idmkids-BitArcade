import pygame

from input.input_manager import InputManager

from pantallas.estado import Estado
from pantallas.menu import Menu
from pantallas.instrucciones import Instrucciones
from pantallas.juego import Juego
from pantallas.resultado import Resultado


# Configuracion de la ventana
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
TITULO_VENTANA = "Bit Arcade"


def main():
    pygame.init()

    icono = pygame.image.load("src/assets/icono.png")
    pygame.display.set_icon(icono)

    pantalla = pygame.display.set_mode(
        (ANCHO_PANTALLA, ALTO_PANTALLA)
    )

    pygame.display.set_caption(TITULO_VENTANA)

    reloj = pygame.time.Clock()

    input_manager = InputManager()
    input_manager.conectar_serial("COM5")

    menu = Menu(pantalla)
    instrucciones = Instrucciones(pantalla)
    juego = Juego(pantalla)
    resultado = Resultado(pantalla)

    estado_actual = Estado.MENU

    ejecutando = True

    while ejecutando:

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                ejecutando = False
                continue

            entrada = input_manager.obtener_evento(evento)

            if entrada is None:
                continue

            if estado_actual == Estado.MENU:

                opcion = menu.manejar_entrada(entrada)

                if opcion is not None:

                    juego_seleccionado = menu.opciones[opcion]

                    instrucciones.establecer_juego(
                        juego_seleccionado
                    )

                    juego.establecer_juego(
                        juego_seleccionado
                    )

                    estado_actual = Estado.INSTRUCCIONES

            elif estado_actual == Estado.INSTRUCCIONES:

                avanzar = instrucciones.manejar_entrada(entrada)

                if avanzar:
                    estado_actual = Estado.JUEGO

            elif estado_actual == Estado.JUEGO:

                terminar = juego.manejar_entrada(entrada)

                if terminar:
                    resultado.establecer_resultado(
                        juego.juego_seleccionado,
                        0
                    )

                    estado_actual = Estado.RESULTADO

            elif estado_actual == Estado.RESULTADO:

                volver = resultado.manejar_entrada(entrada)

                if volver:
                    estado_actual = Estado.MENU
            
        entrada_serial = input_manager.obtener_entrada_serial_real()

        if entrada_serial is not None:

            if estado_actual == Estado.MENU:

                opcion = menu.manejar_entrada(entrada_serial)

                if opcion is not None:

                    juego_seleccionado = menu.opciones[opcion]

                    instrucciones.establecer_juego(
                        juego_seleccionado
                    )

                    juego.establecer_juego(
                        juego_seleccionado
                    )

                    estado_actual = Estado.INSTRUCCIONES

            elif estado_actual == Estado.INSTRUCCIONES:

                avanzar = instrucciones.manejar_entrada(
                    entrada_serial
                )

                if avanzar:
                    estado_actual = Estado.JUEGO

            elif estado_actual == Estado.JUEGO:

                terminar = juego.manejar_entrada(
                    entrada_serial
                )

                if terminar:
                    resultado.establecer_resultado(
                        juego.juego_seleccionado,
                        0
                    )

                    estado_actual = Estado.RESULTADO

            elif estado_actual == Estado.RESULTADO:

                volver = resultado.manejar_entrada(
                    entrada_serial
                )

                if volver:
                    estado_actual = Estado.MENU

        if estado_actual == Estado.INSTRUCCIONES:

            if instrucciones.actualizar():
                estado_actual = Estado.JUEGO

        elif estado_actual == Estado.JUEGO:

            if juego.actualizar():
                resultado.establecer_resultado(
                    juego.juego_seleccionado,
                    0
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