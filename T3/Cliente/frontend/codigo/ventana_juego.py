from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from os.path import join
from utils import data_json

window_name, base_class = uic.loadUiType(
    join(*data_json("RUTA_PANTALLA_JUEGO")))


class VentanaJuego(window_name, base_class):

    senal_info_inicio = pyqtSignal(list)
    senal_lanzamiento_dado = pyqtSignal(dict)
    senal_actualizar_tablero = pyqtSignal(list, dict, dict)
    senal_fin_juego = pyqtSignal(str)
    senal_info_ventana_final = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.lanzar_dado.clicked.connect(self.pedir_lanzamiento_dado)
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
        self.en_turno = 1
        self.puede_lanzar = False
        self.delimitar_coordenadas()
        self.juntar_fichas()
        self.colores = []

    def juntar_fichas(self):
        self.fichas = dict()
        self.fichas["rojo"] = [self.rojo_1, self.rojo_2]
        self.fichas["azul"] = [self.azul_1, self.azul_2]
        self.fichas["verde"] = [self.verde_1, self.verde_2]
        self.fichas["amarillo"] = [self.amarillo_1, self.amarillo_2]

    def delimitar_coordenadas(self):
        self.coordenadas_principales = [[0, 80], [100, 80], [200, 80], [300, 80], [400, 80],
                                        [500, 80], [500, 180], [
                                            500, 280], [500, 380],
                                        [500, 480], [500, 580], [400, 580], [
                                            300, 580], [200, 580], [100, 580], [0, 580], [0, 480],
                                        [0, 380], [0, 280], [0, 180]]
        self.coordenadas_rojas = [[100, 480], [100, 380], [100, 280]]
        self.coordenadas_azul = [[100, 180], [200, 180], [300, 180]]
        self.coordenadas_verdes = [[400, 480], [300, 480], [200, 480]]
        self.coordenadas_amarillas = [[400, 180], [400, 280], [400, 380]]
        self.coordenadas_colores = dict()
        self.coordenadas_colores["rojo"] = self.coordenadas_rojas
        self.coordenadas_colores["azul"] = self.coordenadas_azul
        self.coordenadas_colores["verde"] = self.coordenadas_verdes
        self.coordenadas_colores["amarillo"] = self.coordenadas_amarillas

    def datos_inicio(self, info):
        i = 0
        self.colores = []
        for info_jug in info:
            a_editar = self.jugadores[i]
            a_editar[1].setText(info_jug[0])
            a_editar[0].setPixmap(self.obtener_pixmap_color(info_jug[1]))
            self.colores.append(info_jug[1])
            i += 1
        self.cant_jugadores = i
        while i < 4:
            a_editar = self.jugadores[i]
            a_editar[0].setPixmap(self.obtener_pixmap_color("estrella"))
            a_editar[1].setText("")
            a_editar[2].setText("")
            a_editar[3].setText("")
            a_editar[4].setText("")
            a_editar[5].setText("")
            i += 1
        self.turno_actual.setText(
            f"Turno del jugador: {self.jugador_1[1].text()}")
        for color in self.fichas.keys():
            if color not in self.colores:
                for imagen in self.fichas[color]:
                    imagen.setPixmap(self.obtener_pixmap_color(""))
            else:
                for imagen in self.fichas[color]:
                    imagen.setPixmap(self.obtener_pixmap_color(color))

    def obtener_pixmap_color(self, color):
        if color == "rojo":
            pixeles = QPixmap(join(*data_json("RUTA_ROJA_SIMPLE")))
        elif color == "rojo_2":
            pixeles = QPixmap(join(*data_json("RUTA_ROJA_DOBLE")))
        elif color == "azul":
            pixeles = QPixmap(join(*data_json("RUTA_AZUL_SIMPLE")))
        elif color == "azul_2":
            pixeles = QPixmap(join(*data_json("RUTA_AZUL_DOBLE")))
        elif color == "verde":
            pixeles = QPixmap(join(*data_json("RUTA_VERDE_SIMPLE")))
        elif color == "verde_2":
            pixeles = QPixmap(join(*data_json("RUTA_VERDE_DOBLE")))
        elif color == "amarillo":
            pixeles = QPixmap(join(*data_json("RUTA_AMARILLA_SIMPLE")))
        elif color == "amarillo_2":
            pixeles = QPixmap(join(*data_json("RUTA_AMARILLA_DOBLE")))
        elif color == "estrella":
            pixeles = QPixmap(join(*data_json("RUTA_ESTRELLA")))
        else:
            pixeles = QPixmap()
        return(pixeles)

    def pedir_lanzamiento_dado(self):
        info = {"comando": "lanzar_dado",
                "turno": self.en_turno
                }
        self.senal_lanzamiento_dado.emit(info)
        self.lanzar_dado.setEnabled(False)
        self.puede_lanzar = False

    def poder_lanzar_dado(self):
        if self.puede_lanzar is False:
            self.puede_lanzar = True
            self.lanzar_dado.setEnabled(True)
        else:
            self.puede_lanzar = False
            self.lanzar_dado.setEnabled(False)

    def no_poder_lanzar(self):
        self.puede_lanzar = False
        self.lanzar_dado.setEnabled(False)

    def resultado_dado(self, resul, jug):
        siguiente = self.jugadores[jug % self.cant_jugadores][1]
        self.num_dado.setText(f"Numero obtenido: {resul}")
        self.en_turno = (self.en_turno + 1) % self.cant_jugadores
        self.turno_actual.setText(
            f"Turno del jugador: {siguiente.text()}")

    def jugador_menos(self, info):
        i = 0
        for info_jug in info:
            a_editar = self.jugadores[i]
            a_editar[1].setText(info_jug[0])
            a_editar[0].setPixmap(self.obtener_pixmap_color(info_jug[1]))
            i += 1
        self.cant_jugadores = i
        while i < 4:
            a_editar = self.jugadores[i]
            a_editar[0].setPixmap(self.obtener_pixmap_color("estrella"))
            a_editar[1].setText("")
            a_editar[2].setText("")
            a_editar[3].setText("")
            a_editar[4].setText("")
            a_editar[5].setText("")
            i += 1

    def actualizar_tablero(self, tablero, finales, stats):
        azul_juntos = False
        verde_juntos = False
        rojo_juntos = False
        amarillo_juntos = False
        pos = 0
        for casilla in tablero:
            if len(casilla) == 2:
                if "rojo" in casilla[0]:
                    rojo_juntos = True
                elif "azul" in casilla[0]:
                    azul_juntos = True
                elif "verde" in casilla[0]:
                    verde_juntos = True
                else:
                    amarillo_juntos = True
            elif casilla != []:
                ficha = casilla[0]
                color = ficha[:-2]
                self.fichas[color][int(ficha[-1]) -
                                   1].move(self.coordenadas_principales[pos][0],
                                           self.coordenadas_principales[pos][1])
            pos += 1
        for color in finales.keys():
            pos_color = 0
            for casilla in finales[color]:
                if casilla != []:
                    num = int(casilla[0][-1])
                    self.fichas[color][num-1].move(self.coordenadas_colores[color]
                                                   [pos_color][0],
                                                   self.coordenadas_colores[color][pos_color][1])
                pos_color += 1
        for jug in self.jugadores:
            try:
                nombre = jug[1].text()
                estadisticas = stats[nombre]
                jug[2].setText(f"Fichas en base: {estadisticas[0]}")
                jug[3].setText(f"Fichas en color: {estadisticas[1]}")
                jug[4].setText(f"Fichas en victoria: {estadisticas[2]}")
            except KeyError as k:
                pass

        if "azul" in self.colores:
            if azul_juntos is True:
                self.fichas["azul"][0].setPixmap(self.obtener_pixmap_color(""))
                self.fichas["azul"][1].setPixmap(
                    self.obtener_pixmap_color("azul_2"))
                self.fichas["azul"][1].resize(100, 100)
            else:
                self.fichas["azul"][0].setPixmap(
                    self.obtener_pixmap_color("azul"))
                self.fichas["azul"][1].setPixmap(
                    self.obtener_pixmap_color("azul"))
                self.fichas["azul"][1].resize(60, 100)
        if "verde" in self.colores:
            if verde_juntos is True:
                self.fichas["verde"][0].setPixmap(
                    self.obtener_pixmap_color(""))
                self.fichas["verde"][1].setPixmap(
                    self.obtener_pixmap_color("verde_2"))
                self.fichas["verde"][1].resize(100, 100)
            else:
                self.fichas["verde"][0].setPixmap(
                    self.obtener_pixmap_color("verde"))
                self.fichas["verde"][1].setPixmap(
                    self.obtener_pixmap_color("verde"))
                self.fichas["verde"][1].resize(60, 100)
        if "rojo" in self.colores:
            if rojo_juntos is True:
                self.fichas["rojo"][0].setPixmap(self.obtener_pixmap_color(""))
                self.fichas["rojo"][1].setPixmap(
                    self.obtener_pixmap_color("rojo_2"))
                self.fichas["rojo"][1].resize(100, 100)
            else:
                self.fichas["rojo"][0].setPixmap(
                    self.obtener_pixmap_color("rojo"))
                self.fichas["rojo"][1].setPixmap(
                    self.obtener_pixmap_color("rojo"))
                self.fichas["rojo"][1].resize(60, 100)
        if "amarillo" in self.colores:
            if amarillo_juntos is True:
                self.fichas["amarillo"][0].setPixmap(
                    self.obtener_pixmap_color(""))
                self.fichas["amarillo"][1].setPixmap(
                    self.obtener_pixmap_color("amarillo_2"))
                self.fichas["amarillo"][1].resize(100, 100)
            else:
                self.fichas["amarillo"][0].setPixmap(
                    self.obtener_pixmap_color("amarillo"))
                self.fichas["amarillo"][1].setPixmap(
                    self.obtener_pixmap_color("amarillo"))
                self.fichas["amarillo"][1].resize(60, 100)
        pass

    def fin_juego(self, ganador):
        info = dict()
        info["ganador"] = ganador
        info["jugador_1"] = self.jugador_1
        info["jugador_2"] = self.jugador_2
        info["jugador_3"] = self.jugador_3
        info["jugador_4"] = self.jugador_4
        self.senal_info_ventana_final.emit(info)
        self.ocultar()

    def mostrar(self):
        self.show()

    def ocultar(self):
        self.hide()
