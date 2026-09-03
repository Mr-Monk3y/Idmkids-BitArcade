class ResultadoJuego:
    def __init__(
        self,
        juego,
        puntaje=0,
        ganador=None,
        datos_adicionales=None
    ):
        self.juego = juego
        self.puntaje = puntaje
        self.ganador = ganador

        if datos_adicionales is None:
            datos_adicionales = {}

        self.datos_adicionales = datos_adicionales