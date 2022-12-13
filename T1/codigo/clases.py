import random
from codigo import parametros
import abc


class ExcepcionRecursos(Exception):
    def __init__(self, nombre_recurso):
        super().__init__(
            f"No hay suficiente {nombre_recurso} para completar la acción")

# un montón de propiedades para que no se salgan de los límites, además el Jugador como tal es
# abstracto, ya que no quiero que exista un jugador sin habilidad


class Jugador(abc.ABC):

    def __init__(self, args):
        self.nombre = args[0]
        self.personalidad = args[1]
        self._energia = int(args[2])
        self._suerte = int(args[3])
        self._dinero = int(args[4])
        self._frustracion = int(args[5])
        self._ego = int(args[6])
        self.juegos_jugados = []
        self._carisma = int(args[7])
        self._confianza = int(args[8])
        self.juego_favorito = args[9]

    @property
    def dinero(self):
        return(self._dinero)

    @dinero.setter
    def dinero(self, d):
        if d >= 0:
            self._dinero = d
            print(f"El dinero del jugador ahora es {self._dinero}")
        else:
            raise ExcepcionRecursos("dinero")

    @property
    def energia(self):
        return(self._energia)

    @energia.setter
    def energia(self, e):
        if e > 100:
            self._energia = 100
        elif e < 0:
            raise ExcepcionRecursos("energía")
        else:
            self._energia = e
        print(f"La energía es ahora {self._energia}")

    @property
    def suerte(self):
        return(self._suerte)

    @suerte.setter
    def suerte(self, s):
        if s > 50:
            self._suerte = 50
        elif s < 0:
            self._suerte = 0
        else:
            self._suerte = s
        print(f"La suerte es ahora {self._suerte}")

    @property
    def frustracion(self):
        return(self._frustracion)

    @frustracion.setter
    def frustracion(self, f):
        if f > 100:
            self._frustracion = 100
        elif f < 0:
            self._frustracion = 0
        else:
            self._frustracion = f
        print(f"La frustracion es ahora {self._frustracion}")

    @property
    def ego(self):
        return(self._ego)

    @ego.setter
    def ego(self, e):
        if e > 15:
            self._ego = 15
        elif e < 0:
            self._ego = 0
        else:
            self._ego = e
        print(f"El ego es ahora {self._ego}")

    @property
    def carisma(self):
        return(self._carisma)

    @carisma.setter
    def carisma(self, c):
        if c > 50:
            self._carisma = 50
        elif c < 0:
            self._carisma = 0
        else:
            self._carisma = c
        print(f"El carisma es ahora {self._carisma}")

    @property
    def confianza(self):
        return(self._confianza)

    @confianza.setter
    def confianza(self, c):
        if c > 30:
            self._confianza = 30
        elif c < 0:
            self._confianza = 0
        else:
            self._confianza = c
        print(f"La confianza es {self._confianza}")

    def comprar_bebestible(self, bebestible):
        if self.dinero > bebestible.costo:
            self.dinero -= bebestible.costo
            print(
                f"El jugador {self.nombre} ha comprado y consumido {bebestible.nombre}")
            bebestible.consumir(self)
            return(True)
        else:
            print(
                f"El jugador {self.nombre} no tiene suficiente dinero"
                f" para comprar {bebestible.nombre}")
            return(False)

    def apostar(self, cantidad, juego):
        try:
            self.juegos_jugados.append(juego.nombre)
            self.energia -= round((self.ego + self.frustracion) * 0.15)
            es_favorito = False
            if juego.nombre == self.juego_favorito:
                es_favorito = True

            fav = 0
            if es_favorito:
                fav = 1

            valor_mult = (self.suerte * 15 - cantidad * 0.4 +
                          self.confianza * 3 * fav + self.carisma * 2)

            prob_ganar = min(1, max(0, valor_mult/1000))

            return(prob_ganar)
        except ExcepcionRecursos as err:
            print(f"Error: {err}")
            return("ERROR")


# luego en cada una de las clases siguiente aplico la habilidad específica de distintas maneras,
# algunas de manera más elegante y otras de manera más a lo que funcione (bebedor :/)

class JugadorLudopata(Jugador):

    def ludopatia(self, victoria):
        print("El jugador ha aumentado su ego y suerte!")
        self.ego += 2
        self.suerte += 3
        if victoria is False:
            print("Pero al perder aumentó su frustración...")
            self.frustracion += 5


class JugadorTacano(Jugador):

    def tacano_extremo(self, cantidad, victoria):
        if cantidad < parametros.PORCENTAJE_APUESTA_TACANO:
            print("El jugador ha activado su poder especial!")
            if victoria is True:
                print(f"Y ha ganado {parametros.BONIFICACION_TACANO}!")
                self.dinero += parametros.BONIFICACION_TACANO

            else:
                print("Pero no ha ganado...")


class JugadorBebedor(Jugador):

    def cliente_recurrente(self):
        mult = parametros.MULTIPLICADOR_BONIFICACION_BEBEDOR
        mult = round(mult)
        print(f"El jugador activó su habilidad y multiplica los beneficios del bebestible en"
              f" {mult}!")
        return(mult)


class JugadorCasual(Jugador):

    def suerte_principiante(self, juego):
        jugado = False
        for game in self.juegos_jugados:
            if juego.nombre == game:
                jugado = True

        if jugado is False:
            print(
                f"El jugador {self.nombre} nunca ha jugado {juego.nombre} y gana suerte"
                " de principiante!")
            self.suerte += parametros.BONIFICACION_SUERTE_CASUAL


# todos los juegos son similares, por lo que no cree una clase abstracta de juego
class Juego():

    def __init__(self, lista):
        self.nombre = lista[0]
        self.esperanza = int(lista[1])
        self.minimo = int(lista[2])
        self.maximo = int(lista[3])

    def entregar_resultados(self, jugador, resultado):
        if resultado is True:
            print("El jugador ha ganado!")
            jugador.ego += parametros.EGO_GANAR
            jugador.carisma += parametros.CARISMA_GANAR
            jugador.frustracion -= parametros.FRUSTRACION_GANAR

        else:
            print("El jugador ha perdido...")
            jugador.frustracion += parametros.FRUSTRACION_PERDER
            jugador.confianza -= parametros.CONFIANZA_PERDER

        pass

    def probabilidad_de_ganar(self, jugador, prob_jugador, fav_jugador, apuesta):
        win = False
        valor_mult = apuesta - (50 * fav_jugador - self.esperanza * 30)
        prob_ganar = min(1, prob_jugador - (valor_mult)/10000)
        if random.random() < prob_ganar:
            win = True
        self.entregar_resultados(jugador, win)
        return(win)


# los bebestibles sí tienen diferencias y por eso hice una clase abstracta. Además la última clase
# hereda de dos bebestibles distintos, útil para que cumpla su objetivo

class Bebestibles(abc.ABC):
    def __init__(self, lista):
        self.nombre = lista[0]
        self.tipo = lista[1]
        self.precio = int(lista[2])

    @abc.abstractmethod
    def consumir(self, mult, jugador):
        pass


class Jugo(Bebestibles):

    def consumir(self, jugador, mult):
        largo = len(self.nombre)

        if largo <= 4:
            jugador.ego += mult * 4
        elif largo <= 7:
            jugador.suerte += mult * 7
        else:
            jugador.frustracion -= mult * 10
            jugador.ego += mult * 11


class Gaseosa(Bebestibles):

    def consumir(self, jugador, mult):
        pers = jugador.personalidad

        if pers == "tacano" or pers == "ludopata":
            jugador.frustracion -= mult * 5
        else:
            jugador.frustracion += mult * 5

        jugador.ego += mult * 6


class BrebajeMágico(Jugo, Gaseosa):

    def consumir(self, jugador, mult):
        jugador.carisma += mult * 5
        Jugo.consumir(self, jugador, mult)
        Gaseosa.consumir(self, jugador, mult)


# El casino es la clase principal que hace funcionar todo, ya que tiene las distintas clases
# incluidas aquí para que todo funcione bien entre sí

class Casino():

    def __init__(self, jugador, bebestibles, juegos, dinero_faltante, show):
        self.jugador = jugador
        self.bebestibles = bebestibles
        self.juegos = juegos
        self.dinero_faltante = dinero_faltante
        self.show = show

    def evento_especial(self):
        if random.random() < parametros.PROBABILIDAD_EVENTO:
            seleccion = random.randint(0, len(self.bebestibles))
            if self.jugador.personalidad.upper() == "BEBEDOR":
                mult = self.jugador.cliente_recurrente()
            else:
                mult = 1
            self.bebestibles[seleccion-1].consumir(self.jugador, mult)
            print("El evento especial ha sucedido!")
            print(
                f"El jugador ha consumido {self.bebestibles[seleccion-1].nombre}!")
        else:
            print("El evento especial no ha sucedido...")

    def jugar(self, juego, apuesta, fav):
        if self.jugador.dinero > apuesta:
            if self.jugador.personalidad.upper() == "CASUAL":
                self.jugador.suerte_principiante(juego)
            prob_ganar = self.jugador.apostar(apuesta, juego)
            if prob_ganar != "ERROR":
                victoria = juego.probabilidad_de_ganar(
                    self.jugador, prob_ganar, fav, apuesta)

                if self.jugador.personalidad.upper() == "LUDOPATA":
                    self.jugador.ludopatia(victoria)
                elif self.jugador.personalidad.upper() == "TACANO":
                    self.jugador.tacano_extremo(apuesta, victoria)

                if victoria is True:
                    self.jugador.dinero += apuesta
                else:
                    self.jugador.dinero -= apuesta
                self.evento_especial()
        else:
            print(
                f"Error, el jugador no tiene suficiente dinero para apostar {apuesta}")
        pass


class Show():
    def __init__(self):

        pass

    def ver_show(self, jugador):
        if jugador.dinero < parametros.DINERO_SHOW:
            print("El jugador no tiene suficiente dinero para ver un show...")
            print(f"El precio para ver un show es {parametros.DINERO_SHOW}")
        else:
            print("El jugador vio un show!")
            jugador.dinero -= parametros.DINERO_SHOW
            jugador.energia += parametros.ENERGIA_SHOW
            jugador.frustracion -= parametros.FRUSTRACION_SHOW
