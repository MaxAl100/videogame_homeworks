from PyQt5.QtCore import QObject, pyqtSignal

import parametros as p


class LogicaPrincipal(QObject):

    senal_correccion = pyqtSignal(list)

    def __init__(self):
        super().__init__()

    # aqui llega la señal con la info y es revisada para luego enviar una lista con
    # los errores presentes
    def verificar_info(self, lista):
        errores = []

        nombre = lista[0]
        eleccion = lista[1]

        if nombre == "":
            errores.append("Nombre no puede ser vacío")
        elif nombre.isalnum() is False:
            errores.append("Nombre tiene que ser alfanumérico")

        i = 0
        elegido = -1
        for opcion in eleccion:
            if opcion is True:
                elegido = i
            i += 1

        if elegido == -1:
            errores.append("Tiene que elegir un mapa en el cual cazar aliens")
        self.senal_correccion.emit(errores)
