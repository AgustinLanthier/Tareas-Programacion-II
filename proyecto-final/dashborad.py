#dashboar.py
from ascii_art import ascii_monstruos

def menu(jugador, enemigo):
    ancho = 16
    distancia = ' ' * 5
    borde = '═' * (ancho )
    borde2 = '━' * (ancho)
    # Variables jugador
    nombre_jugador = jugador.nombre.center(ancho)
    lvl_jugador = f"Lvl: {jugador.xp}".ljust(ancho)
    clase_jugador =f"Clase: {jugador.clase}".ljust(ancho)
    xp_jugador = f"Xp: {jugador.xp}".ljust(ancho)
    hp_jugador = f"HP: {jugador.vida}".ljust(ancho)
    frz_jugador = f"Frz: {jugador.fuerza}".ljust(ancho)
    dst_jugador = f"Dst: {jugador.destreza}".ljust(ancho)
    int_jugador = f"Int: {jugador.inteligencia}".ljust(ancho)
    def_jugador = f"Def: {jugador.defensa}".ljust(ancho)
    # Variables Enemigo
    nombre_enemigo = enemigo.nombre.center(ancho )
    hp_enemigo = f"HP: {enemigo.vida}".ljust(ancho)
    frz_enemigo = f"Frz: {enemigo.fuerza}".ljust(ancho)
    def_enemigo = f"Def: {enemigo.defensa}".ljust(ancho)
    xp_enemigo = f"Xp: {enemigo.xp}".ljust(ancho)

    jugador_box = [
        f"╔{borde}╗",
        f"║{nombre_jugador}║",
        f"║{borde2}║",
        f"║{lvl_jugador}║",
        f"║{clase_jugador}║",
        f"║{xp_jugador}║",
        f"║{hp_jugador}║",
        f"║{frz_jugador}║",
        f"║{dst_jugador}║",
        f"║{int_jugador}║",
        f"║{def_jugador}║",
        f"╚{borde}╝",
        f"╔{borde}╗",
        f"║ Tu turno:      ║",
        f"║ 1. Atacar      ║",
        f"║ 2. Esquivar    ║",
        f"║ 3. Bloquear    ║",
        f"╚{borde}╝",
    ]

    enemigo_box = [
        f"╔{borde}╗",
        f"║{nombre_enemigo}║",
        f"║{borde2}║",
        f"║{hp_enemigo}║",
        f"║{frz_enemigo}║",
        f"║{def_enemigo}║",
        f"║{xp_enemigo}║",
        f"╚{borde}╝"
    ]
    
    # Obtener el ASCII del monstruo según su nombre, o cadena vacía si no existe
    # .get() busca la clave (nombre del enemigo) en el diccionario ascii_monstruos
    # .strip("\n") elimina saltos de línea al principio o final para evitar líneas vacías
    # .split("\n") divide la cadena en una lista, separando por cada salto de línea
    ascii_lines = ascii_monstruos.get(enemigo.nombre, "").strip("\n").split("\n")

    # Calcular la cantidad máxima de líneas que vamos a imprimir
    # Toma el máximo largo entre las listas jugador_box, ascii_lines y enemigo_box
    max_lines = max(len(jugador_box), len(ascii_lines), len(enemigo_box))

    # Calcular el ancho máximo de las líneas ASCII
    # Recorre todas las líneas del ASCII y obtiene la longitud (cantidad de caracteres) de cada una
    # Devuelve el valor más grande (línea más ancha) para poder alinear bien el texto
    # Si ascii_lines está vacío, ancho_ascii queda 0 para evitar errores
    ancho_ascii = max(len(l) for l in ascii_lines) if ascii_lines else 0

# Recorrer desde la primera hasta la última línea que hay que imprimir
    for i in range(max_lines):
    # Si la línea existe en jugador_box, la usamos, si no, ponemos espacios para mantener la alineación
        if i < len(jugador_box):
            j_line = jugador_box[i]
        else:
            j_line = " " * (ancho + 2)
    # Igual para la línea del ASCII, si no existe línea, poner espacios en blanco con el ancho adecuado
        if i < len(ascii_lines):
            a_line = ascii_lines[i]
        else:
            a_line = " " * ancho_ascii

        if i < len(enemigo_box):
            e_line = enemigo_box[i]
        else:
            e_line = " " * (ancho + 2)

        # imprimir las tres partes separadas por espacio (distancia)
        print(f"{j_line}{distancia}{a_line}{distancia}{e_line}")
    