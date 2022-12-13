from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QMessageBox
from os.path import join
from utils import data_json

window_name, base_class = uic.loadUiType(join(*data_json(
    "RUTA_PANTALLA_INICIO")))


class VentanaInicio(window_name, base_class):

    senal_enviar_login = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.estado = False
        self.init_gui()

    def init_gui(self):
        self.setWindowTitle("DCCasillas")
        self.botonInicio.clicked.connect(self.enviar_login)

    def keyPressEvent(self, event):
        """Si apreta Enter se envia al servidor"""
        if event.key() == Qt.Key_Return:
            self.enviar_login()

    def enviar_login(self):
        nombre_usuario = self.usuario.text().replace(" ", "")
        diccionario = {
            "comando": "validar_login",
            "nombre usuario": nombre_usuario,
        }
        self.senal_enviar_login.emit(diccionario)

    # revisa errores y en caso de que haya crea pop-ups, en caso contrario comienza el juego
    def mostrar_error(self, str):
        self.hacer_popup(str)

    # Codigo sacado de https://www.techwithtim.net/tutorials/pyqt5-tutorial/messageboxes/
    def hacer_popup(self, mensaje):
        msg = QMessageBox()
        msg.setWindowTitle("Mensaje de error")
        msg.setText(mensaje)
        x = msg.exec_()  # this will show our messagebox

    def mostrar(self):
        self.estado = True
        self.show()

    def ocultar(self):
        self.hide()

    def salir(self):
        self.estado = False
        self.close()
