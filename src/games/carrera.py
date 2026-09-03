from games.juego_base import JuegoBase
from games.resultado_juego import ResultadoJuego


class Carrera(JuegoBase):
    def __init__(self, pantalla):
        super().__init__(pantalla)

        # Inicializacion especifica del juego

    def iniciar(self):
        """Inicializa o reinicia el juego."""

        pass

    def manejar_entrada(self, entrada):
        """Procesa una entrada de un jugador."""

        pass

    def actualizar(self):
        """Actualiza el estado del juego."""

        pass

    def dibujar(self):
        """Dibuja el juego."""

        pass

    def obtener_resultado(self):
        """Devuelve el resultado del juego."""

        return ResultadoJuego(
            juego="Carrera",
            puntaje=self.puntaje
        )