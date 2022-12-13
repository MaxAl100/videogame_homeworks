# Programa hecho completamente por Alejandro Held, excepto
# por los aspectos mencionados en el README

import cargar
import parametros
import menus

# función tomada de la actividad formativa 1 de este semestre


def get_input(inputt):
    entrada = input()
    if entrada not in {str(i) for i in range(inputt + 1)}:
        print("Error, opción invalida")
        entrada = get_input(inputt)
    return int(entrada)

# menú que aparece al comienzo de la aplicación


def main(usuarios, reclamos, encomiendas):

    respuesta = ""
    while respuesta != 4:
        print("---- Bienvenid@ a DCCorreos de Chile ----\n")
        print("** Menú de Inicio **\n")
        print("Selecciona una de las siguientes opciones:\n\n")
        print("[1] Iniciar sesión como usuario")
        print("[2] Registrarse como usuario")
        print("[3] Iniciar sesión como administrador")
        print("[4] Salir del programa")
        print("Indique su opción elegida: (input)")
        respuesta = get_input(4)

        if respuesta == 0:
            print("Error, opción invalida")

        if respuesta == 1:
            # ir hacia inicio de sesión
            print("-" * 10 + "Iniciar sesión" + "-"*10 + "\n")
            usuario = input("Inserte nombre de usuario: ")
            contraseña = input("Inserte su contraseña: ")
            encontrado = False

            for usuario_registrado in usuarios:
                if usuario == usuario_registrado.nombre:
                    encontrado = True
                    if contraseña == usuario_registrado.clave:
                        print("Usuario y contraseña correctos!\n")
                        menus.menu_usuario(
                            usuario_registrado, usuarios, encomiendas, reclamos)
                    else:
                        print("\n\nError, contraseña incorrecta\n")
                        print("Volviendo al menú principal\n\n")
            if encontrado is False:
                print("\n\nError, nombre de usuario inválido\n")
                print("Volviendo al menú principal\n\n")

        if respuesta == 2:
            seleccion = 1
            while seleccion == 1:
                # ir hacia registro
                print("-" * 10 + "Registrarse como usuario" + "-"*10 + "\n")
                usuario = input("Inserte nombre de usuario: ")
                contraseña = input("Inserte su contraseña: ")
                error_registrado = False

                if len(usuario) < parametros.MIN_CARACTERES:
                    print("Error, nombre de usuario muy corto.")
                    error_registrado = True
                if usuario.isalpha() is False:
                    print("Error, el nombre solo puede caracteres alfabéticos.")
                    error_registrado = True

                for usuario_registrado in usuarios:
                    if usuario == usuario_registrado.nombre:
                        print("Error, el nombre ya fue elegido por otro usuario.")
                        error_registrado = True
                print("\n")

                if error_registrado is False:
                    print("Usuario registrado correctamente\n")
                    with open("usuarios.csv", encoding='utf-8', mode="a+") as archivo:
                        archivo.write(f"{usuario},{contraseña}\n")
                    usuario_nuevo = cargar.User(usuario, contraseña)
                    usuarios.append(usuario_nuevo)
                    seleccion = 0
                else:
                    print(
                        "¿Desea reintentar el inicio de sesión?\n[0]: No\n[1]: Sí\n")
                    seleccion = get_input(1)

        if respuesta == 3:
            # ir hacia inicio de admin
            print("-" * 10 + "Iniciar sesión como Administrador" + "-"*10 + "\n")
            es_admin = 0
            while es_admin == 0:
                contraseña = input("\nInserte contraseña de Administrador: ")
                if contraseña == parametros.CONTRASENA_ADMIN:
                    es_admin = 1
                    print("¡Bienvenido Administrador!")
                else:
                    print("¡Contraseña incorrecta!\n¿Desea reintentarlo?")
                    print("[0] Repetir contraseña\n[1] Volver")
                    eleccion = get_input(1)
                    if eleccion == 0:
                        es_admin = 0
                    else:
                        es_admin = 2
            if es_admin == 1:
                print("Yendo a menú de administrador...")
                menus.menu_admin(encomiendas, reclamos)


# lo que hace correr todo, básicamente
if __name__ == "__main__":
    usuarios = cargar.cargar_usuarios("usuarios.csv")
    reclamos = cargar.cargar_reclamos("reclamos.csv")
    encomiendas = cargar.cargar_encomiendas("encomiendas.csv")
    main(usuarios, reclamos, encomiendas)
