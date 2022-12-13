from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMessageBox, QButtonGroup

import parametros as p

window_name, base_class = uic.loadUiType(p.RUTA_UI_VENTANA_PRINCIPAL)


class VentanaPrincipal(window_name, base_class):

    senal_info = pyqtSignal(list)
    senal_comienzo_juego = pyqtSignal(list)
    senal_nueva_partida = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_gui()

    def init_gui(self):
        self.comenzar_caza.clicked.connect(self.intento_jugar)
        self.setWindowTitle("A cazar aliens!")

        # parte de la solución para desclickear los radiobuttons
        self.grupo = QButtonGroup()
        self.grupo.addButton(self.opc1)
        self.grupo.addButton(self.opc2)
        self.grupo.addButton(self.opc3)

    # muestra la ventana
    def mostrar_ventana(self):
        self.show()

    # manda info para intentar comenzar el juego a través de una señal
    def intento_jugar(self):
        info = []
        info.append(self.nombre.text())

        self.botones = []
        self.botones.append(self.opc1.isChecked())
        self.botones.append(self.opc2.isChecked())
        self.botones.append(self.opc3.isChecked())
        info.append(self.botones)

        self.senal_info.emit(info)

    # revisa errores y en caso de que haya crea pop-ups, en caso contrario comienza el juego
    def revision_info(self, lista):
        if len(lista) == 0:
            self.comienzo_juego()
        else:
            for error in lista:
                self.hacer_popup(error)

    # Codigo sacado de https://www.techwithtim.net/tutorials/pyqt5-tutorial/messageboxes/
    def hacer_popup(self, mensaje):
        msg = QMessageBox()
        msg.setWindowTitle("Mensaje de error")
        msg.setText(mensaje)
        x = msg.exec_()  # this will show our messagebox

    # función de comenzar juego y limpia los campos llenados
    # ademas envia cierta info
    def comienzo_juego(self):
        print("Comenzando juego, de veras esta vez")
        # sacado de pagina, link en mi whatsapp personal
        self.grupo.setExclusive(False)
        self.opc1.setChecked(False)
        self.opc2.setChecked(False)
        self.opc3.setChecked(False)
        self.grupo.setExclusive(True)
        self.botones.append(self.nombre.text())
        self.senal_nueva_partida.emit()
        self.senal_comienzo_juego.emit(self.botones)
        self.botones = []
        self.nombre.setText("")
        self.hide()
