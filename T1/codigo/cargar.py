from encodings import utf_8
from codigo import clases

# En este código creo tres funciones distintas que cargan los archivos y los convierten en listas
# incluyendo a instancias de las clases apropiadas. Además se tiene un orden de información para
# evitar problemas si cambian de orden los datos en la primera (y todas las demás) líneas


def cargar_jugadores(ruta_archivo):
    with open(ruta_archivo, encoding="utf_8", mode="r+") as archivo:
        players = archivo.readlines()

    correct_players = []

    for jugador in players:
        jugador = jugador.strip().split(",")
        correct_players.append(jugador)

    linea_guia = correct_players[0]
    info = ["nombre", "personalidad", "energia", "suerte", "dinero",
            "frustracion", "ego", "carisma", "confianza", "juego favorito"]
    orden_info = []

    num1 = 0

    for info_ordenada in info:
        num2 = 0
        for dato in linea_guia:
            if dato == info_ordenada:
                orden_info.append(num2)

            num2 += 1

        num1 += 1

    correct_players = correct_players[1:]

    lista_jugadores = []

    for player in correct_players:
        player_data = []
        for indice in orden_info:
            player_data.append(player[indice])
        if player_data[1].upper() == "LUDOPATA":
            char = clases.JugadorLudopata(player_data)
        elif player_data[1].upper() == "BEBEDOR":
            char = clases.JugadorBebedor(player_data)
        elif player_data[1].upper() == "CASUAL":
            char = clases.JugadorCasual(player_data)
        else:
            char = clases.JugadorTacano(player_data)

        lista_jugadores.append(char)

    return(lista_jugadores)


def cargar_juegos(ruta_archivo):
    with open(ruta_archivo, encoding="utf_8", mode="r+") as archivo:
        juegos = archivo.readlines()

    juegos_correctos = []

    for juego in juegos:
        juego = juego.strip().split(",")
        juegos_correctos.append(juego)

    linea_guia = juegos_correctos[0]
    info = ["nombre", "esperanza", "apuesta minima", "apuesta maxima"]
    orden_info = []

    num1 = 0

    for info_ordenada in info:
        num2 = 0
        for dato in linea_guia:
            if dato == info_ordenada:
                orden_info.append(num2)
            num2 += 1
        num1 += 1

    juegos_correctos = juegos_correctos[1:]

    lista_juegos = []

    for juego in juegos_correctos:
        info_juego = []
        for indice in orden_info:
            info_juego.append(juego[indice])
        game = clases.Juego(info_juego)
        lista_juegos.append(game)

    return(lista_juegos)


def cargar_bebestibles(ruta_archivo):
    with open(ruta_archivo, encoding="utf_8", mode="r+") as archivo:
        bebestibles = archivo.readlines()

    bebestibles_correcto = []

    for bebes in bebestibles:
        bebes = bebes.strip().split(",")
        bebestibles_correcto.append(bebes)

    linea_guia = bebestibles_correcto[0]
    info = ["nombre", "tipo", "precio"]
    orden_info = []

    num1 = 0

    for info_ordenada in info:
        num2 = 0
        for dato in linea_guia:
            if dato == info_ordenada:
                orden_info.append(num2)
            num2 += 1
        num1 += 1

    bebestibles_correcto = bebestibles_correcto[1:]

    lista_bebestibles = []

    for drink in bebestibles_correcto:
        drink_info = []
        for indice in orden_info:
            drink_info.append(drink[indice])
        if drink_info[1].upper == "JUGO":
            bebida = clases.Jugo(drink_info)
        elif drink_info[1].upper == "GASEOSA":
            bebida = clases.Gaseosa(drink_info)
        else:
            bebida = clases.BrebajeMágico(drink_info)

        lista_bebestibles.append(bebida)

    return(lista_bebestibles)
