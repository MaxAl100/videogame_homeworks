from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap

import parametros as p

window_name, base_class = uic.loadUiType(p.RUTA_UI_VENTANA_INICIO)


class VentanaInicio(window_name, base_class):

    senal_ver_rankings = pyqtSignal()
    senal_iniciar_juego = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_gui()

    def init_gui(self):
        self.setWindowTitle("A cazar aliens!")
        self.setMaximumSize(700, 600)

        # imagen del logo
        pixeles = QPixmap(p.RUTA_LOGO)
        self.label_imagen.setMaximumSize(640, 480)
        self.label_imagen.setPixmap(pixeles)
        self.label_imagen.setScaledContents(True)

        # unir los botones para que me funcionen, ya que desde designer no me funciona
        self.pushButton1.clicked.connect(self.empezar_juego)
        self.pushButton2.clicked.connect(self.ver_rankings)

    def mostrar_ventana(self):
        self.show()

    # funciones de los botones:

    def empezar_juego(self):
        print("Empezando juego")
        self.senal_iniciar_juego.emit()
        self.hide()

    def ver_rankings(self):
        print("Viendo rankings")
        self.senal_ver_rankings.emit()
        self.hide()
