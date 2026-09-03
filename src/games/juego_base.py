from abc import ABC, abstractmethod


class JuegoBase(ABC):
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.terminado = False
        self.puntaje = 0

    @abstractmethod
    def iniciar(self):
        """Inicializa o reinicia el juego."""
        pass

    @abstractmethod
    def manejar_entrada(self, entrada):
        """Procesa una entrada de un jugador."""
        pass

    @abstractmethod
    def actualizar(self):
        """Actualiza el estado del juego."""
        pass

    @abstractmethod
    def dibujar(self):
        """Dibuja el juego."""
        pass

    @abstractmethod
    def obtener_resultado(self):
        """Devuelve el resultado del juego."""
        pass