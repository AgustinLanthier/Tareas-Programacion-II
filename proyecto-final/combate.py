import random

def tirar_d20():
    return random.randint(1, 20)

def interpretar_tirada(tirada):
    if tirada == 1:
        return "critico_fallo"
    elif tirada == 20:
        return "critico_exito"
    elif tirada >= 10:
        return "exito"
    else:
        return "fallo"

def combate_turno(jugador, enemigo, accion):
    """
    Conserva la lógica original:
    - Atacar: solo daña al enemigo.
    - Esquivar/Bloquear: resuelven el daño que recibe el jugador.
    - No hay contraataque del enemigo en el mismo turno de 'Atacar' (igual que tu versión).
    """
    if jugador.vida <= 0 or enemigo.vida <= 0:
        return "El combate ya terminó."

    tirada = tirar_d20()
    res = interpretar_tirada(tirada)

    if accion == "atacar":
        atributo = getattr(jugador, jugador.atributo_ataque)
        if res == "critico_exito":
            dano = max(0, atributo * 2 - enemigo.defensa)
        elif res == "exito":
            dano = max(0, atributo - enemigo.defensa)
        elif res == "fallo":
            dano = max(0, int(atributo/2) - enemigo.defensa)
        else:
            dano = 0
        enemigo.vida -= dano
        return f"{jugador.nombre} ataca (d20={tirada}:{res}) → {dano} daño a {enemigo.nombre}"

    elif accion == "esquivar":
        if res == "critico_exito":
            # Evita todo el daño
            return f"{jugador.nombre} esquiva perfecto (d20={tirada}:{res}). No recibe daño."
        elif res == "exito":
            dano = max(0, enemigo.fuerza - jugador.destreza)
            jugador.vida -= dano
            return f"{jugador.nombre} esquiva parcial (d20={tirada}:{res}). Recibe {dano} daño."
        elif res == "fallo":
            jugador.vida -= enemigo.fuerza
            return f"{jugador.nombre} falla esquiva (d20={tirada}:{res}). Recibe {enemigo.fuerza} daño."
        else:  # critico_fallo
            jugador.vida -= enemigo.fuerza + 5
            return f"{jugador.nombre} tropieza (d20={tirada}:{res}). Recibe {enemigo.fuerza + 5} daño."

    elif accion == "bloquear":
        if res == "critico_exito":
            return f"{jugador.nombre} bloquea perfecto (d20={tirada}:{res}). Sin daño."
        elif res == "exito":
            dano = max(0, enemigo.fuerza - jugador.defensa)
            jugador.vida -= dano
            return f"{jugador.nombre} bloquea parcial (d20={tirada}:{res}). Recibe {dano} daño."
        elif res == "fallo":
            dano = max(0, int(enemigo.fuerza * 0.75))
            jugador.vida -= dano
            return f"{jugador.nombre} bloquea mal (d20={tirada}:{res}). Recibe {dano} daño."
        else:  # critico_fallo
            jugador.vida -= enemigo.fuerza + 5
            return f"{jugador.nombre} falla bloqueo (d20={tirada}:{res}). Recibe {enemigo.fuerza + 5} daño."

    return "Acción no válida."
