from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtGui import QPixmap
from os.path import join
from utils import data_json

window_name, base_class = uic.loadUiType(join(*data_json(
    "RUTA_PANTALLA_ESPERA")))


class VentanaEspera(window_name, base_class):

    senal_pedir_actualizacion = pyqtSignal(dict)
    senal_pedir_comienzo_juego = pyqtSignal(dict)
    senal_comenzar_juego = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.grupos = dict()
        self.boton_iniciar.clicked.connect(self.iniciar_partida)
        self.crear_grupos()

    # para editar las cosas más fácilmente
    def crear_grupos(self):
        lista_1 = [self.nombre_1, self.color_1, self.imagen_1]
        lista_2 = [self.nombre_2, self.color_2, self.imagen_2]
        lista_3 = [self.nombre_3, self.color_3, self.imagen_3]
        lista_4 = [self.nombre_4, self.color_4, self.imagen_4]
        self.grupos[1] = lista_1
        self.grupos[2] = lista_2
        self.grupos[3] = lista_3
        self.grupos[4] = lista_4

    # actualizar a tiempo real. Lo hice para ver qué tan dificil sería implementar el bonus.
    def iniciar_actualizacion(self):
        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.pedir_actualizacion)
        self.timer.start()

    def detener_actualizacion(self):
        self.timer.stop()

    def pedir_actualizacion(self):
        diccionario = {
            "comando": "actualizar_sala_espera",
        }
        self.senal_pedir_actualizacion.emit(diccionario)

    # actualiza los datos
    def actualizar_info_jugadores(self, jugadores):
        jug = 1

        for jugador in jugadores:
            rellenar = self.grupos[jug]
            if len(jugador) > 1:
                rellenar[0].setText(jugador[0])
                rellenar[1].setText(jugador[1])
                self.cambiar_imagen(rellenar[2], jugador[1])
            else:
                rellenar[0].setText(f"No hay jugador {jug} conectado")
                rellenar[1].setText(f"No hay jugador {jug} conectado")
                self.cambiar_imagen(rellenar[2], "estrella")
            jug += 1

    # para acceder a las imágenes rápidamente
    def cambiar_imagen(self, label, color):
        if color == "rojo":
            pixeles = QPixmap(join(*data_json("RUTA_ROJA_SIMPLE")))
        elif color == "azul":
            pixeles = QPixmap(join(*data_json("RUTA_AZUL_SIMPLE")))
        elif color == "verde":
            pixeles = QPixmap(join(*data_json("RUTA_VERDE_SIMPLE")))
        elif color == "amarillo":
            pixeles = QPixmap(join(*data_json("RUTA_AMARILLA_SIMPLE")))
        else:
            pixeles = QPixmap(join(*data_json("RUTA_ESTRELLA")))
        label.setPixmap(pixeles)
        label.setScaledContents(True)

    # en caso de que un jugador se vaya, el siguiente va a ser admin llamando a esta función
    def cambiar_estado_admin(self):
        if self.boton_iniciar.isEnabled() is False:
            self.boton_iniciar.setEnabled(True)
        else:
            self.boton_iniciar.setEnabled(False)

    def desactivar_admin(self):
        self.boton_iniciar.setEnabled(False)

    def iniciar_partida(self):
        info = dict()
        info["comando"] = "empezar_partida"
        self.senal_pedir_comienzo_juego.emit(info)

    def falta_jugadores(self):
        self.texto_error.setText(
            "No hay suficientes jugadores para empezar la partida")

    def mostrar(self):
        self.show()

    def ocultar(self):
        self.hide()
