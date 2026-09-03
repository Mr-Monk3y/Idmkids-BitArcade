from games.carrera import Carrera
from games.bit_dice import BitDice
from games.piedra_papel_tijera_fuego_agua import PiedraPapelTijeraFuegoAgua
from games.ataja_la_pelotita import AtajaLaPelotita


class RegistroJuegos:
    def __init__(self, pantalla):
        self.pantalla = pantalla

        self.juegos = {
            "Carrera": Carrera,
            "Bit Dice": BitDice,
            "Piedra, Papel, Tijera, Fuego y Agua": PiedraPapelTijeraFuegoAgua,
            "Ataja la Pelotita": AtajaLaPelotita,
        }

    def crear_juego(self, nombre):
        """Crea el juego correspondiente al nombre seleccionado."""

        if nombre not in self.juegos:
            return None

        clase_juego = self.juegos[nombre]

        return clase_juego(self.pantalla)