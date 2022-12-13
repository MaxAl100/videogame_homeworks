import main
import parametros
import datetime
import cargar

# codigo tomado de
# https://stackoverflow.com/questions/4719438/editing-specific-line-in-text-file-in-python
# para reemplazar lineas en un archivo (lo podría haber hecho yo, pero decidí buscarlo en google)
# para ser más eficiente con mi tiempo


def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()

# el menú del usuario donde se ven las distintas funcionalidades


def menu_usuario(usuario_ingresado, usuarios, encomiendas, reclamos):
    encomiendas_realizadas = 0

    respuesta = ""
    while respuesta != 5:
        print("** Menú de usuario **\n\n")
        print("[1] Hacer una encomienda")
        print("[2] Revisar estado de encomiendas realizadas")
        print("[3] Realizar reclamos")
        print("[4] Ver el estado de los pedidos personales")
        print("[5] Cerrar Sesión")
        print("Indique su opción elegida: (input)\n")
        respuesta = main.get_input(5)

        if respuesta == 0:
            print("Error, opción invalida")

        if respuesta == 1:
            # realizar encomienda, paso a paso
            paso = 1
            print("Comienzo realización pedido...")
            while paso < 5:
                if paso == 1:
                    nombre = input("Insertar nombre del artículo: ")
                    if "," in nombre:
                        print(
                            "El nombre no puede incluir comas(',').\n¿Desea continuar?\n")
                        print("[0] Continuar\n[1] Cancelar encomienda")
                        eleccion = main.get_input(1)
                        if eleccion == 1:
                            print("Encomienda cancelada.\n\n")
                            paso = 6
                    else:
                        paso += 1
                        print("Nombre seleccionado correctamente.")

                if paso == 2:
                    destinatario = input("Insertar nombre del destinatario: ")
                    usuario_encontrado = False
                    for usuario in usuarios:
                        if usuario.nombre == destinatario:
                            usuario_encontrado = True

                    if usuario_encontrado is False:
                        print(
                            "Error, el destinatario tiene que ser usuario de DCCorreos de Chile\n")
                        print("¿Desea continuar?\n")
                        print("[0] Continuar\n[1] Cancelar encomienda")
                        eleccion = main.get_input(1)
                        if eleccion == 1:
                            print("Encomienda cancelada.\n\n")
                            paso = 6
                    else:
                        if destinatario == usuario_ingresado.nombre:
                            print("Error, el destinatario no puede ser usted mismo")
                            print("¿Desea continuar?\n")
                            print("[0] Continuar\n[1] Cancelar encomienda")
                            eleccion = main.get_input(1)
                            if eleccion == 1:
                                print("Encomienda cancelada.\n\n")
                                paso = 6
                        else:
                            print("Destinatario seleccionado.")
                            paso += 1

                if paso == 3:
                    if "," in nombre:
                        print(
                            "El peso no puede incluir comas(','). Utilice puntos('.') para dividir"
                            " los kilos de los gramos\n¿Desea continuar?\n")
                        print("[0] Continuar\n[1] Cancelar encomienda")
                        eleccion = main.get_input(1)
                        if eleccion == 1:
                            print("Encomienda cancelada.\n\n")
                            paso = 6
                    peso = input("Insertar peso del artículo en kg: ")
                    tiene_letras = False
                    for digit in peso:
                        if digit not in "1234567890.":
                            tiene_letras = True
                    if tiene_letras is False:

                        if float(peso) > float(parametros.MAX_PESO):
                            print("Error, el artículo pesa demasiado.\n")
                            print("¿Desea continuar?\n")
                            print("[0] Continuar\n[1] Cancelar encomienda")
                            eleccion = main.get_input(1)
                            if eleccion == 1:
                                print("Encomienda cancelada.\n\n")
                                paso = 6

                        elif float(peso) < 0.01:
                            print(
                                "Error, peso es muy pequeño. Si pesa menos "
                                "que 10 gramos, redondear a este valor (0.01 kg).")
                            print("¿Desea continuar?\n")
                            print("[0] Continuar\n[1] Cancelar encomienda")
                            eleccion = main.get_input(1)
                            if eleccion == 1:
                                print("Encomienda cancelada.\n\n")
                                paso = 6
                        else:
                            print("Peso registrado correctamente.")
                            paso += 1
                    else:
                        print("Error, el peso tiene que ser un valor numérico")

                if paso == 4:
                    destino = input(
                        "Insertar dirección de destino del artículo: ")
                    if "," in destino:
                        print(
                            "El destino no puede incluir comas(',').\n¿Desea continuar?\n")
                        print("[0] Continuar\n[1] Cancelar encomienda")
                        eleccion = main.get_input(1)
                        if eleccion == 1:
                            print("Encomienda cancelada.\n\n")
                            paso = 6
                    else:
                        paso += 1
                        print("Destino seleccionado correctamente.")
                        fecha = str(datetime.datetime.now())
                        fecha = fecha.split(" ")
                        fecha_c = ""
                        for letter in fecha[0]:
                            if letter == "-":
                                fecha_c = fecha_c + "/"
                            else:
                                fecha_c = fecha_c + letter
                        fecha[1] = fecha[1].split(".")
                        fecha_c = fecha_c + " " + str(fecha[1][0])

                        # además de añadir la encomienda al archivo, se agrega a la lista con
                        # encomiendas de la clase Encomienda
                        estado = "Emitida"
                        texto = f"\n{nombre},{destinatario},{peso},{destino},{fecha_c},{estado}"
                        with open("encomiendas.csv", encoding='utf-8', mode="a+") as archivo:
                            archivo.write(texto)

                        encomienda = cargar.Encomienda(
                            nombre, destinatario, peso, destino, fecha_c, estado)
                        encomiendas.append(encomienda)
                        print("La encomienda ha sido registrada correctamente.")
                        encomiendas_realizadas += 1

        if respuesta == 2:
            # revisar estado encomienda
            print("Revisando estado de encomiendas realizadas\n")
            for i in range(encomiendas_realizadas):
                print(
                    f"Nombre: {encomiendas[-i-1].nombre}, Estado: {encomiendas[-i-1].estado}\n")
            print("\n")

        if respuesta == 3:
            # realizar reclamos
            print("Realizar reclamos: ")
            titulo = input("Inserte el título del reclamo: ")
            print("Inserte la descripción del reclamo: ")
            descripcion = input()
            reclamo = cargar.Reclamo(
                usuario_ingresado.nombre, titulo, descripcion)
            with open("reclamos.csv", encoding='utf-8', mode="a") as archivo:
                archivo.write(
                    f"{usuario_ingresado.nombre},{titulo},{descripcion}\n")
            reclamos.append(reclamo)

        if respuesta == 4:
            # visualizar pedidos dirigidos a este usuario
            print("Visualización de pedidos personales:")
            for encomienda in encomiendas:
                if encomienda.receptor == usuario_ingresado.nombre:
                    print(f"{encomienda}\n")

        if respuesta == 5:
            # cerrar sesión
            print("Cerrando Sesión\nVolviendo al menú principal\n")
            break


def menu_admin(encomiendas, reclamos):
    respuesta = ""
    while respuesta != 3:
        print("** Menú de administrador **\n\n")
        print("[1] Actualizar encomiendas")
        print("[2] Revisar reclamos")
        print("[3] Cerrar sesión")
        print("Indique su opción elegida: (input)\n")
        respuesta = main.get_input(3)

        if respuesta == 0:
            print("Error, opción invalida")

        if respuesta == 1:
            print("Visualización de encomiendas:")
            seleccion = ""

            while seleccion != 0:
                print("  |" + " " * 7 + "Nombre articulo" + " " * 7 + "  |" + " " * 4 + "Receptor" +
                      " " * 5 + "|  Peso  |" + " " * 5 + "Destino" + " " * 5 + "|" + " " * 7 +
                      "Estado" + " " * 7 + "|")
                for i in range(len(encomiendas)):
                    enc = encomiendas[i]
                    print(
                        f"[{i+1}] {enc.nombre: ^30.30s} {enc.receptor: ^18.18s} {enc.peso: ^5.5s}"
                        f" {enc.destino: ^15.15s} {enc.estado: ^26.26}")
                print("[0]: Volver al menú anterior")
                print(
                    "Elija cual encomienda actualizar o si prefiere volver al menú anterior")
                seleccion = main.get_input(len(encomiendas))

                if seleccion != 0:
                    enc = encomiendas[seleccion - 1]
                    state = encomiendas[seleccion - 1].estado
                    if state == "Emitida":
                        print("Actualizando encomienda...")
                        encomiendas[seleccion -
                                    1].estado = "Revisada por agencia"
                        texto_nuevo = (
                            f"{enc.nombre},{enc.receptor},{enc.peso},{enc.destino},{enc.fecha},"
                            "Revisada por agencia\n")
                    elif state == "Revisada por agencia":
                        print("Actualizando encomienda...")
                        encomiendas[seleccion - 1].estado = "En camino"
                        texto_nuevo = (
                            f"{enc.nombre},{enc.receptor},{enc.peso},{enc.destino},{enc.fecha},"
                            "En camino\n")
                    elif state == "En camino":
                        print("Actualizando encomienda...")
                        encomiendas[seleccion - 1].estado = "En destino"
                        texto_nuevo = f"{enc.nombre},{enc.receptor},{enc.peso},{enc.destino},"
                        f"{enc.fecha},En destino\n"
                    else:
                        print("Error, opción invalida")

                    replace_line("encomiendas.csv", seleccion, texto_nuevo)

                    print(
                        "¿Desea actualizar más encomiendas?\n\n[0]: No\n[1]: Sí\n")
                    seleccion = main.get_input(1)

        if respuesta == 2:
            print("Visualización de reclamos:")
            seleccion = ""

            while seleccion != 0:
                for i in range(len(reclamos)):
                    print(f"[{i+1}]: {reclamos[i].titulo}")
                print("[0]: Volver al menú anterior")
                print("Elija cual reclamo ver o si prefiere volver al menú anterior")
                seleccion = main.get_input(len(reclamos))
                if seleccion != 0:
                    print(f"Título: {reclamos[seleccion - 1].titulo}")
                    print(f"Usuario: {reclamos[seleccion - 1].usuario}")
                    print(
                        f"Descripción: {reclamos[seleccion - 1].descripcion}")

                    print(
                        "¿Desea visualisar otro reclamo?\n\n[0]: No\n[1]: Sí\n")
                    seleccion = main.get_input(1)

        if respuesta == 3:
            # cerrar sesión
            print("Cerrando Sesión\nVolviendo al menú principal\n")
            break
