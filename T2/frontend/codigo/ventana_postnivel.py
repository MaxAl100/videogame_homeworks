from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal

import parametros as p

window_name, base_class = uic.loadUiType(p.RUTA_UI_VENTANA_POSTNIVEL)


class VentanaPostnivel(window_name, base_class):

    senal_salida = pyqtSignal()
    senal_otro_nivel = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ganado = False
        self.init_gui()

    def init_gui(self):
        self.boton_salir.clicked.connect(self.salir_juego)
        self.boton_siguiente.clicked.connect(self.siguiente_nivel)

    def salir_juego(self):
        self.senal_salida.emit()
        self.ganado = False
        self.guardar_puntos()
        self.hide()

    def siguiente_nivel(self):
        info = [int(self.casilla_nivel.text()) + 1,
                self.casilla_puntos_acum.text()]
        info2 = []
        if self.mundo == 0:
            info2.append(True)
            info2.append(False)
            info2.append(False)
        elif self.mundo == 1:
            info2.append(False)
            info2.append(True)
            info2.append(False)
        else:
            info2.append(False)
            info2.append(False)
            info2.append(True)
        info2.append(self.nombre)
        info.append(info2)
        self.senal_otro_nivel.emit(info)
        print("Pasando al siguiente nivel...")
        self.ganado = False
        self.hide()

    def mostrar_ventana(self, lista):
        self.nombre = lista[0]
        lista = lista[1:]
        self.puntos_acum = lista[4]
        self.casilla_nivel.setText(str(lista[0]))
        self.casilla_balas.setText(str(lista[1]))
        self.casilla_tiempo.setText(str(lista[2]) + " s")
        self.casilla_puntos_nivel.setText(str(lista[3]))
        self.casilla_puntos_acum.setText(str(lista[4]))
        self.mundo = lista[5]

        if self.ganado is False:
            self.boton_siguiente.setEnabled(False)
            self.casilla_info.setText(
                "No has logrado vencer a los aliens y el siguiente nivel no estará disponible...")
        else:
            self.boton_siguiente.setEnabled(True)
            self.casilla_info.setText(
                "Has logrado vencer a los aliens y puedes intentar el siguiente nivel!")

        self.show()

    def victoria(self):
        self.ganado = True

    def guardar_puntos(self):
        print("Añadiendo puntaje")
        with open(p.RUTA_PUNTAJE, encoding="utf-8", mode="a") as file:
            file.write(f"{self.nombre},{self.puntos_acum}\n")
