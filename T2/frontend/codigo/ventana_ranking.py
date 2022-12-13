from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QTableWidgetItem

import parametros as p

window_name, base_class = uic.loadUiType(p.RUTA_UI_VENTANA_RANKING)


class VentanaRanking(window_name, base_class):

    senal_volver_menu = pyqtSignal()
    senal_pedir_info = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_gui()

    def init_gui(self):
        self.pushButton.clicked.connect(self.volver_a_menu)
        self.setWindowTitle("A cazar aliens!")

    def mostrar_ventana(self):
        self.show()
        self.senal_pedir_info.emit()

    # recibe la info y actualiza la tabla
    def actualizar_info(self, lista):
        fila = 0
        for minilista in lista:
            self.tabla_ranking.setItem(fila, 0, QTableWidgetItem(minilista[0]))
            self.tabla_ranking.setItem(fila, 1, QTableWidgetItem(minilista[1]))
            fila += 1

    # para que la ventana inicio se abra nuevamente cuando se cierre esta ventana
    def closeEvent(self, event):
        self.senal_volver_menu.emit()
        event.accept()

    def volver_a_menu(self):
        self.senal_volver_menu.emit()
        self.hide()
