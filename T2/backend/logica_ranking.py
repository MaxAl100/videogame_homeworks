from PyQt5.QtCore import QObject, pyqtSignal

import parametros as p


def ayuda_orden(entrada):
    return(int(entrada[1]))


class LogicaRanking(QObject):

    senal_enviar_info = pyqtSignal(list)

    def __init__(self):
        super().__init__()

    # ordena la información del archivo para luego enviarla a la ventana

    def obtener_info(self):
        mejores = []

        with open(p.RUTA_PUNTAJE, encoding="utf-8") as file:
            jugadores = file.readlines()

        nuevo_jugadores = []

        for jugador in jugadores:
            jugador = jugador.strip("\n").split(",")
            nuevo_jugadores.append(jugador)

        jugadores = sorted(nuevo_jugadores, key=ayuda_orden, reverse=True)
        mejores = jugadores[0:5]

        self.senal_enviar_info.emit(mejores)
