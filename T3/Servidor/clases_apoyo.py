from abc import ABC, abstractmethod


class Pieza():
    def __init__(self, inicial, nombre, jugador):
        self.inicio = inicial
        self.posicion = inicial
        self.nombre = nombre
        self.jugador = jugador
        self.en_color = False
        self.pos_color = None
        self.en_victoria = False
        self.pos_anterior = None
        self.pos_color_anterior = None
        self.revisado_color = False

    def mover(self, cant):
        if self.en_victoria is False:
            if self.en_color is False:
                # En este caso pasa por su casilla de inicio, por lo que debe empezar a ir en sus
                # casillas finales
                if self.posicion < self.inicio and (self.posicion + cant) >= self.inicio:
                    self.en_color = True
                    self.pos_anterior = self.posicion
                    self.pos_color = self.posicion + cant - self.inicio
                    if self.pos_color == 2:
                        self.en_victoria = True
                else:
                    # En este caso pasa por una esquina que no es suya, por lo que debe moverse uno
                    # extra por como simule el tablero
                    self.pos_anterior = self.posicion
                    if self.posicion//5 != (self.posicion+cant)//5:
                        self.posicion += (cant+1)
                    else:
                        self.posicion += cant
                    self.posicion = self.posicion % 20
            else:
                self.pos_color_anterior = self.pos_color
                # En este caso no llega al final
                if self.pos_color + cant < 2:
                    self.pos_color += cant
                # En este caso llega al final
                elif self.pos_color + cant == 2:
                    self.pos_color = self.pos_color + cant
                    self.en_victoria = True
                else:
                    # rebote implementado aquí
                    self.pos_color = self.pos_color + cant
                    if self.pos_color != 2:
                        while self.pos_color//2 > 0:
                            self.pos_color = self.pos_color - 2

    def __repr__(self):
        if self.en_victoria is True:
            texto = f"Soy {self.nombre} y estoy en la casilla de victoria"
        elif self.en_color is True:
            texto = (f"Soy {self.nombre} y estoy en las casillas finales, me queda"
                     f" {2-self.pos_color} para ganar")
        else:
            texto = f"Soy {self.nombre} y estoy en la casilla {self.posicion}"
        return(texto)


class Jugador(ABC):
    def __init__(self, nombre, coord_tablero, tablero, parent):
        self.nombre = nombre
        self.color = None
        self.coord_tablero = coord_tablero
        self.tablero = tablero
        self.parent = parent
        self.final = [None, None, None]
        self.ganador = False

    @abstractmethod
    def mover_pieza(self, cant):
        pass

    def __repr__(self) -> str:
        return(f"{self.nombre} con el color {self.color}")

    def revisar_victoria(self):
        if self.pieza_1.en_victoria is True and self.pieza_2.en_victoria is True:
            self.ganador = True

    def fin_juego(self):
        self.pieza_1.posicion = self.pieza_1.inicio
        self.pieza_2.posicion = self.pieza_2.inicio


class JugadorRojo(Jugador):

    def __init__(self, nombre, coord_tablero, tablero, parent):
        super().__init__(nombre, coord_tablero, tablero, parent)
        self.color = "rojo"
        self.pieza_1 = Pieza(15, "rojo_1", nombre)
        self.pieza_2 = Pieza(15, "rojo_2", nombre)

    def mover_pieza(self, cant):
        self.parent.parent.log(
            f"El jugador {self.nombre} ha avanzado {cant} casillas")
        if self.pieza_1.en_victoria is False:
            self.pieza_1.mover(cant)
            self.tablero.actualizar_tablero(self.pieza_1)
        else:
            self.pieza_2.mover(cant)
            self.tablero.actualizar_tablero(self.pieza_2)
        self.revisar_victoria()


class JugadorAzul(Jugador):

    def __init__(self, nombre, coord_tablero, tablero, parent):
        super().__init__(nombre, coord_tablero, tablero, parent)
        self.color = "azul"
        # En esto pongo 20 para que me funcione el código de encontrar el comienzo de las casillas
        # de color
        self.pieza_1 = Pieza(20, "azul_1", nombre)
        self.pieza_2 = Pieza(20, "azul_2", nombre)

    def mover_pieza(self, cant):
        self.parent.parent.log(
            f"El jugador {self.nombre} ha avanzado {cant} casillas")
        if self.pieza_1.en_victoria is False:
            self.pieza_1.mover(cant)
            self.tablero.actualizar_tablero(self.pieza_1)
        else:
            self.pieza_2.mover(cant)
            self.tablero.actualizar_tablero(self.pieza_2)
        self.revisar_victoria()


class JugadorVerde(Jugador):

    def __init__(self, nombre, coord_tablero, tablero, parent):
        super().__init__(nombre, coord_tablero, tablero, parent)
        self.color = "verde"
        self.pieza_1 = Pieza(10, "verde_1", nombre)
        self.pieza_2 = Pieza(10, "verde_2", nombre)

    def mover_pieza(self, cant):
        self.parent.parent.log(
            f"El jugador {self.nombre} ha avanzado {cant} casillas")
        if self.pieza_1.en_victoria is False:
            self.pieza_1.mover(cant)
            self.tablero.actualizar_tablero(self.pieza_1)
        else:
            self.pieza_2.mover(cant)
            self.tablero.actualizar_tablero(self.pieza_2)
        self.revisar_victoria()


class JugadorAmarillo(Jugador):

    def __init__(self, nombre, coord_tablero, tablero, parent):
        super().__init__(nombre, coord_tablero, tablero, parent)
        self.color = "amarillo"
        self.pieza_1 = Pieza(5, "amarillo_1", nombre)
        self.pieza_2 = Pieza(5, "amarillo_2", nombre)

    def mover_pieza(self, cant):
        self.parent.parent.log(
            f"El jugador {self.nombre} ha avanzado {cant} casillas")
        if self.pieza_1.en_victoria is False:
            self.pieza_1.mover(cant)
            self.tablero.actualizar_tablero(self.pieza_1)
        else:
            self.pieza_2.mover(cant)
            self.tablero.actualizar_tablero(self.pieza_2)
        self.revisar_victoria()


class Tablero():

    def __init__(self, parent, *jugs):
        self.parent = parent
        self.tablero = []
        for _ in range(20):
            self.tablero.append([])
        self.jugadores = []
        for jug in jugs:
            self.jugadores.append(jug)
        self.rectas_finales = dict()

    def agregar_jugador(self, jug):
        self.jugadores.append(jug)

    def sacar_jugador(self, jug):
        self.jugadores.remove(jug)

    def posiciones_iniciales(self):
        for jug in self.jugadores:
            ubic = jug.pieza_1.posicion
            ubic_2 = jug.pieza_2.posicion
            self.tablero[ubic % 20].append(jug.pieza_1)
            self.tablero[ubic_2 % 20].append(jug.pieza_2)
            self.rectas_finales[jug.color] = [[], [], []]

    def actualizar_tablero(self, pieza):
        sacar = (pieza.pos_anterior) % 20
        poner = pieza.posicion
        if pieza.en_color is False:
            if sacar == (pieza.inicio % 20):
                self.tablero[sacar].remove(pieza)
            else:
                self.tablero[sacar] = []
            if self.tablero[poner] == []:
                self.tablero[poner].append(pieza)
            else:
                pieza_a_sacar = self.tablero[poner][0]
                pieza_a_sacar.posicion = pieza_a_sacar.inicio
                self.tablero[pieza_a_sacar.inicio % 20].append(pieza_a_sacar)
                self.tablero[poner] = [pieza]
                self.parent.parent.log(
                    f"La pieza {pieza.jugador} ha comido a la pieza {pieza_a_sacar.jugador}")
        else:
            if pieza.revisado_color is False:
                pieza.revisado_color = True
                for key in self.rectas_finales.keys():
                    if pieza.nombre[:-2] in key:
                        self.rectas_finales[key][pieza.pos_color].append(pieza)
                self.tablero[sacar].remove(pieza)
            else:
                for key in self.rectas_finales.keys():
                    if pieza.nombre[:-2] in key:
                        self.rectas_finales[key][pieza.pos_color_anterior].remove(
                            pieza)
                        self.rectas_finales[key][pieza.pos_color].append(pieza)

    def info_a_enviar(self):
        for jug in self.jugadores:
            if jug.ganador is True:
                info_a_entregar = {"comando": "fin_juego",
                                   "ganador": jug.nombre}
                for jug in self.jugadores:
                    jug.fin_juego()
                return(info_a_entregar)
        info_a_entregar = dict()
        tablero_simple = []
        for pos in self.tablero:
            if pos == []:
                tablero_simple.append([])
            else:
                contenido_celda = []
                for contenido in pos:
                    contenido_celda.append(contenido.nombre)
                tablero_simple.append(contenido_celda)
        rectas_finales_simple = dict()
        for key in self.rectas_finales.keys():
            recta = self.rectas_finales[key]
            esta_recta = []
            for pos in recta:
                if pos == []:
                    esta_recta.append([])
                else:
                    esta_recta.append([pos[0].nombre])
            rectas_finales_simple[key] = esta_recta

        caracteristicas_jugadores = dict()
        for jug in self.jugadores:
            en_base = 0
            if jug.pieza_1.posicion == jug.pieza_1.inicio:
                en_base += 1
            if jug.pieza_2.posicion == jug.pieza_2.inicio:
                en_base += 1
            en_color = 0
            if jug.pieza_1.en_color is True:
                en_color += 1
            if jug.pieza_2.en_color is True:
                en_color += 1
            en_victoria = 0
            if jug.pieza_1.en_victoria is True:
                en_victoria += 1
            if jug.pieza_2.en_victoria is True:
                en_victoria += 1
            en_color = en_color - en_victoria
            caracteristicas_jugadores[jug.nombre] = [
                en_base, en_color, en_victoria]

        info_a_entregar = {"comando": "actualizar_tablero",
                           "tablero": tablero_simple,
                           "rectas_finales": rectas_finales_simple,
                           "estadisticas_jugadoras": caracteristicas_jugadores}
        return(info_a_entregar)

    def __repr__(self) -> str:
        info = ""
        for key in self.rectas_finales:
            info = info + f"{key}: {self.rectas_finales[key]}\n"
        return(f"Tablero {self.tablero}\nRectas finales: {info}")
