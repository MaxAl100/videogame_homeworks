from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

import parametros as p

window_name, base_class = uic.loadUiType(p.RUTA_UI_VENTANA_JUEGO)


class VentanaJuego(window_name, base_class):

    senal_comienzo_juego = pyqtSignal(list)
    senal_pausa = pyqtSignal()
    senal_tecla = pyqtSignal(list)
    senal_volver_menu = pyqtSignal()
    senal_salir_juego = pyqtSignal()
    senal_disparo = pyqtSignal()
    senal_cia = pyqtSignal()
    senal_ovni = pyqtSignal()
    senal_colision_estrella = pyqtSignal()
    senal_colision_bomba = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.keylist = []
        self.init_gui()

    def init_gui(self):
        self.setWindowTitle("A cazar aliens!")
        self.setMaximumWidth(p.ANCHO_JUEGO)
        self.setMaximumHeight(p.ALTO_JUEGO + 120)
        self.setMinimumWidth(p.ANCHO_JUEGO)
        self.setMinimumHeight(p.ALTO_JUEGO + 120)
        self.boton_pausa.clicked.connect(self.pausar)
        self.boton_salir.clicked.connect(self.salir_del_juego)
        self.firstrelease = True

    def mostrar_ventana(self):
        self.tdog_alien.move(-100, -100)
        self.tdog_normal.move(170, 390)
        self.show()

    def cambiar_fondo(self, mundo):
        if mundo == 0:
            self.pix_fondo = QPixmap(p.RUTA_FONDO_1)
            self.pix_tdog = QPixmap(p.RUTA_TDOG_ALIEN1)
        elif mundo == 1:
            self.pix_fondo = QPixmap(p.RUTA_FONDO_2)
            self.pix_tdog = QPixmap(p.RUTA_TDOG_ALIEN2)
        else:
            self.pix_fondo = QPixmap(p.RUTA_FONDO_3)
            self.pix_tdog = QPixmap(p.RUTA_TDOG_ALIEN3)
        self.tdog_alien.setPixmap(self.pix_tdog)
        self.tdog_alien.setScaledContents(True)
        self.tdog_alien.resize(80, 100)
        self.imagen_fondo.setPixmap(self.pix_fondo)
        self.imagen_fondo.setScaledContents(True)
        self.imagen_fondo.resize(p.ANCHO_JUEGO, p.ALTO_JUEGO)
        self.imagen_fondo.move(0, 0)

    def comenzar_juego(self, lista):
        self.mostrar_ventana()
        self.senal_comienzo_juego.emit(lista)

    def recepcion_datos(self, lista):
        self.casilla_nivel.setText(str(lista[0]))
        self.casilla_puntaje.setText(str(lista[1]))
        self.casilla_matados.setText(str(lista[2]))
        self.casilla_pormatar.setText(str(lista[3]))
        self.casilla_balas.setText("x " + str(lista[4]))

    def actualizar_tiempo(self, tiempo):
        if tiempo >= 0:
            self.casilla_tiempo.setText(str(tiempo/1000) + " s")

    def pausar(self):
        self.senal_pausa.emit()

    def salir_del_juego(self):
        self.senal_salir_juego.emit()

        self.senal_volver_menu.emit()
        self.hide()

    def keyPressEvent(self, event):
        if event.text() == p.TECLA_PAUSA:
            self.pausar()
        elif event.key() == 16777249:
            self.senal_disparo.emit()
        else:
            # info_emision = []
            astr = event.text()
            if event.text() == p.TECLA_ABAJO:
                astr = "D"
                # info_emision.append("D")
                # self.senal_tecla.emit("D")
            elif event.text() == p.TECLA_ARRIBA:
                astr = "U"
                # info_emision.append("U")
                # self.senal_tecla.emit("U")
            elif event.text() == p.TECLA_DERECHA:
                astr = "R"
                # info_emision.append("R")
                # self.senal_tecla.emit("R")
            elif event.text() == p.TECLA_IZQUIERDA:
                astr = "L"
                # info_emision.append("L")
                # self.senal_tecla.emit("L")
            # self.senal_tecla.emit(info_emision)


# inspirado de: https://stackoverflow.com/questions/7176951/
# how-to-get-multiple-key-presses-in-single-event
            self.firstrelease = True
            # astr = str(event.text())
            self.keylist.append(astr)

    def keyReleaseEvent(self, event):
        if self.firstrelease is True:
            self.processmultikeys(self.keylist)

        self.firstrelease = False

        del self.keylist[-1]

    def processmultikeys(self, keyspressed):
        self.senal_tecla.emit(keyspressed)
        fase_cia = 0
        fase_ovni = 0

        for key in keyspressed:
            if key in ["c", "i", "L"]:
                fase_cia += 1
            if key in ["o", "v", "n", "i"]:
                fase_ovni += 1

        if fase_cia == 3:
            self.senal_cia.emit()
        if fase_ovni == 4:
            self.senal_ovni.emit()

    def actualizar_aliens(self, aliens):
        for alien in aliens:
            alien.label_alien.setParent(self)
            alien.label_alien.setVisible(True)
            alien.label_alien.move(alien.pos_alien.x(), alien.pos_alien.y())

    def actualizar_mira(self, mira):

        mira.label_mira.setParent(self)
        mira.label_mira.setVisible(True)
        mira.label_mira.resize(p.WIDTH_MIRA, p.HEIGHT_MIRA)
        mira.label_mira.move(mira.pos_mira.x(), mira.pos_mira.y())
        mira.label_mira.raise_()

    def mostrar_explosion(self, explosion):
        if explosion.fase == 1:
            print(f"Estoy en fase {explosion.fase}")
            explosion.label_explosion_1.setParent(self)
            explosion.label_explosion_1.setVisible(True)
        elif explosion.fase == 2:
            print(f"Estoy en fase {explosion.fase}")
            explosion.label_explosion_2.setParent(self)
            explosion.label_explosion_2.setVisible(True)
        elif explosion.fase == 3:
            print(f"Estoy en fase {explosion.fase}")
            explosion.label_explosion_3.setParent(self)
            explosion.label_explosion_3.setVisible(True)

    def victoria(self):
        self.tdog_normal.move(-100, -100)
        self.tdog_alien.move(170, 390)

    def mover_estrella(self, ubic):
        self.estrella_muerte.move(ubic[0], ubic[1])

    def mover_bomba_hielo(self, ubic):
        self.bomba_hielo.move(ubic[0], ubic[1])

    def revision_colision_especiales(self, ubic):
        print("Revisando colisiones con eventos especiales")
        if self.estrella_muerte.x() < ubic[0] < self.estrella_muerte.x() + 100:
            if self.estrella_muerte.y() < ubic[1] < self.estrella_muerte.y() + 100:
                self.senal_colision_estrella.emit()
        if self.bomba_hielo.x() < ubic[0] < self.bomba_hielo.x() + 100:
            if self.bomba_hielo.y() < ubic[1] < self.bomba_hielo.y() + 100:
                self.senal_colision_bomba.emit()

    def pasar_a_postnivel(self, *args):
        self.hide()
