from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from os.path import join
from utils import data_json

window_name, base_class = uic.loadUiType(join(*data_json(
    "RUTA_PANTALLA_FINAL")))


class VentanaFinal(window_name, base_class):

    senal_volver_menu_inicial = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.jugador_1 = [self.ficha_1, self.nombre_1,
                          self.base_1, self.color_1, self.victoria_1, self.orden_1]
        self.jugador_2 = [self.ficha_2, self.nombre_2,
                          self.base_2, self.color_2, self.victoria_2, self.orden_2]
        self.jugador_3 = [self.ficha_3, self.nombre_3,
                          self.base_3, self.color_3, self.victoria_3, self.orden_3]
        self.jugador_4 = [self.ficha_4, self.nombre_4,
                          self.base_4, self.color_4, self.victoria_4, self.orden_4]
        self.jugadores = [self.jugador_1, self.jugador_2,
                          self.jugador_3, self.jugador_4]
        self.boton_volver.clicked.connect(self.volver_menu_principal)

    def actualizar_ventana(self, dicci):
        self.ganador.setText(f"THE WINNER IS {dicci['ganador'].upper()}")
        jug = 0
        for key in dicci.keys():
            if key != "ganador":
                info = dicci[key]
                self.jugadores[jug][0].setPixmap(info[0].pixmap())
                self.jugadores[jug][1].setText(info[1].text())
                self.jugadores[jug][2].setText(info[2].text())
                self.jugadores[jug][3].setText(info[3].text())
                self.jugadores[jug][4].setText(info[4].text())
                self.jugadores[jug][5].setText(info[5].text())

                jug += 1

    def mostrar(self, *args):
        self.show()

    def volver_menu_principal(self):
        self.senal_volver_menu_inicial.emit()

    def ocultar(self):
        self.hide()
