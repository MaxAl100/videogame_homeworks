import sys
from codigo import cargar
from codigo import clases
from codigo import parametros
import os
import beautifultable

# Este código es el principal del programa y es el que tiene que ser corrido para que corra todo.


# esta función sirve para recibir el input del usuario y dependiendo de lo que entregue, va a
# reaccionar de distintas maneras, continuando o pidiendo un valor nuevo

def get_input(opciones):
    entrada = input()
    if entrada.isnumeric():
        if entrada not in {str(i) for i in range(opciones + 1)}:
            print("Error, número invalido")
            return("a")
        else:
            return(int(entrada))
    else:
        if entrada.upper() != "X":
            print("Error, opción invalida")
            return("a")
        else:
            return("X")


# este es el menú principal del casino, donde se puede acceder a los juegos, bebestibles y ver la
# información del jugador seleccionado. Cada uno de estos está incluido también en esta gran función

def menu_principal(casino):
    eleccion_main = -1
    if casino.jugador.dinero > deuda:
        print(
            "Lo has logrado! Pagas tu deuda a BigCat y te vas del casino"
            " lo más rápido que puedes")
        sys.exit()
    while eleccion_main != 0:
        mini_eleccion = -1
        print("\n   *** Menú Principal ***   \n" + "-" * 30)
        print("[1] Opciones de juegos")
        print("[2] Comprar bebestible")
        print("[3] Ver estado jugador")
        print("[4] Ver show")
        print("[0] Volver\n[X] Salir")
        eleccion_main = get_input(4)
        if eleccion_main == "X":
            return(True)
        elif eleccion_main == 1:
            while mini_eleccion != 0 and mini_eleccion != "a":
                print("  *** Opciones de juego ***\n" + "-" * 30)
                i = 1
                for juego in casino.juegos:
                    print(f"[{i}] {juego.nombre}")
                    i += 1
                print("\n[0] Volver\n[X] Salir")
                mini_eleccion = get_input(len(casino.juegos))
                if mini_eleccion == "X":
                    sys.exit()
                elif mini_eleccion != 0 and mini_eleccion != "a":
                    # Esta es la opción de apostar
                    juego_elegido = casino.juegos[mini_eleccion - 1]
                    print("¿Cuanto dinero quieres apostar?")
                    print(
                        f"Mínimo: {juego_elegido.minimo}\nMáximo: {juego_elegido.maximo}")
                    dinero_apostado = input()
                    if dinero_apostado.isnumeric() is False:
                        print("Error, la cantidad debe ser un entero")
                    else:
                        dinero_apostado = int(dinero_apostado)

                        if casino.jugador.dinero < juego_elegido.minimo:
                            print(
                                "Error, el jugador no tiene suficiente dinero"
                                " para apostar en este juego")

                        elif dinero_apostado < juego_elegido.minimo:
                            print(
                                "Error, el dinero apostado debe ser más que el mínimo del juego")

                        elif dinero_apostado > juego_elegido.maximo:
                            print(
                                "Error, el dinero apostado debe ser menos que el máximo del juego")

                        else:
                            if dinero_apostado == 69:
                                print("Cantidad de dinero NICE")
                            else:
                                print("Cantidad de dinero aceptable!")
                            favorito = casino.jugador.juego_favorito
                            if favorito == juego_elegido.nombre:
                                fav = 1
                            else:
                                fav = 0
                            # y el resultado es calculada aquí:
                            casino.jugar(juego_elegido, dinero_apostado, fav)
                        if casino.jugador.dinero > deuda:
                            print(
                                "Lo has logrado! Pagas tu deuda a BigCat y te vas del casino"
                                " lo más rápido que puedes")
                            sys.exit()
                        mini_eleccion = "a"

        elif eleccion_main == 2:
            while mini_eleccion != 0:
                print("\n" + " " * 8 + "*" * 3 +
                      " Bebestibles " + "*" * 3 + " " * 8)
                table = beautifultable.BeautifulTable()
                table.columns.header = ["Nombre", "Tipo", "Precio"]
                lista_numeros = []
                i = 0
                for bebestible in casino.bebestibles:
                    i += 1
                    lista_numeros.append(str(i))
                    lista_bebestible = [bebestible.nombre,
                                        bebestible.tipo, f"${bebestible.precio}"]

                    table.rows.append(lista_bebestible)

                table.rows.header = lista_numeros
                print(table)
                print("\n[0] Volver\n[X] Salir")
                mini_eleccion = get_input(len(casino.bebestibles))
                if mini_eleccion == "X":
                    sys.exit()
                elif mini_eleccion != 0:
                    bebestible_elegido = casino.bebestibles[mini_eleccion - 1]
                    if casino.jugador.dinero > bebestible_elegido.precio:
                        casino.jugador.dinero -= bebestible_elegido.precio
                        if casino.jugador.personalidad.upper() != "BEBEDOR":
                            mult = 1
                        else:
                            mult = casino.jugador.cliente_recurrente()
                        bebestible_elegido.consumir(casino.jugador, mult)
                        print(
                            f"El jugador ha consumido {bebestible_elegido.nombre}!")
                    else:
                        print(
                            "El jugador no tiene suficiente dinero para este bebestible...")
        elif eleccion_main == 3:
            while mini_eleccion != 0:
                print("\n*** Ver estado del jugador ***\n" + "-" * 40)
                print(
                    f"Nombre: {casino.jugador.nombre}\nPersonalidad: {casino.jugador.personalidad}")
                print(
                    f"Energía: {casino.jugador.energia}\nSuerte: {casino.jugador.suerte}")
                print(
                    f"Dinero: {casino.jugador.dinero}\nFrustración: {casino.jugador.frustracion}")
                print(
                    f"Ego: {casino.jugador.ego}\nCarisma: {casino.jugador.carisma}")
                print(
                    f"Confianza: {casino.jugador.confianza}\n"
                    f"Juego favorito: {casino.jugador.juego_favorito}")
                print(f"Dinero faltante: {casino.dinero_faltante}")
                print("[0] Volver\n[X] Salir")
                mini_eleccion = get_input(1)
                if mini_eleccion == 1:
                    print("Error, número invalido")
                elif mini_eleccion == "X":
                    return(True)
        elif eleccion_main == 4:
            while mini_eleccion != 0:
                print("Ver show?")
                print(f"[1] Sí, ver show\n[0] Volver\n[X] Salir")
                print(f"El precio de ver un show es {parametros.DINERO_SHOW}")
                mini_eleccion = get_input(1)
                if mini_eleccion == 1:
                    casino.show.ver_show(casino.jugador)


# Esta función representa el primer menú que uno ve y permite empezar la partida y seleccionar un
# jugador para luego ser enviado al menú del casino

def main(jugadores, juegos, bebestibles, deuda, show):
    cierre = False
    eleccion_inicio = 0
    while eleccion_inicio != "X":
        jugadores = cargar.cargar_jugadores(
            os.path.join("registro", "jugadores.csv"))
        juegos = cargar.cargar_juegos(os.path.join("registro", "juegos.csv"))
        bebestibles = cargar.cargar_bebestibles(
            os.path.join("registro", "bebestibles.csv"))

        print("\n*** Menú de Inicio ***")
        print("-"*20)
        print("[1] Iniciar partida\n[X] Salir")
        eleccion_inicio = get_input(1)

        if eleccion_inicio == 0:
            print("Error, número invalido")

        elif eleccion_inicio == 1:
            eleccion_jug = -1

            while eleccion_jug != 0:
                print("\n" + " "*6 + "*" * 3 +
                      " Opciones de Jugador " + "*" * 3 + " " * 6)
                i = 1
                for jugador in jugadores:
                    print(f"[{i}] {jugador.nombre}: {jugador.personalidad}")
                    i += 1
                print("[0] Volver\n[X] Salir")
                eleccion_jug = get_input(len(jugadores))

                if eleccion_jug == "X":
                    cierre = True

                elif eleccion_jug == 0:
                    print("Volviendo al menú anterior")

                elif eleccion_jug != -1 and eleccion_jug != "a":
                    jugador_seleccionado = jugadores[int(eleccion_jug) - 1]
                    print(f"Has seleccionado a {jugador_seleccionado.nombre}!")
                    eleccion_jug = 0
                    casino = clases.Casino(jugador_seleccionado,
                                           bebestibles, juegos, deuda, show)
                    cierre = menu_principal(casino)

                if cierre is True:
                    eleccion_inicio = "X"
                    eleccion_jug = 0


# lo que hace correr todo, básicamente
if __name__ == "__main__":
    players = cargar.cargar_jugadores(
        os.path.join("registro", "jugadores.csv"))
    games = cargar.cargar_juegos(os.path.join("registro", "juegos.csv"))
    drinks = cargar.cargar_bebestibles(
        os.path.join("registro", "bebestibles.csv"))
    deuda = parametros.DEUDA_TOTAL
    show = clases.Show()
    main(players, games, drinks, deuda, show)

# con lo de arriba se mantiene la info si no se cierra la aplicación, pero se resetea
# cuando se cierra y vuelve a abrir. Si quisiera que se reseteara cada vez que se llega al menú
# de inicio, entonces tengo que setear players, games y drinks en el menú main
