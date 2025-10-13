import random
from inventario import Inventory

class Personaje:
    def __init__(self, nombre):
        self.nombre = nombre
        self.nivel = 1
        self.xp = 0
        self.vida = 100

        self.fuerza = self.rolear_stats()
        self.destreza = self.rolear_stats()
        self.inteligencia = self.rolear_stats()
        self.defensa = self.rolear_stats()

        self.clase = "Aventurero"
        self.atributo_ataque = "fuerza"

        self.oro = 0
        self.inv = Inventory(num_slots=8)

    def rolear_stats(self):
        # 6d6, quitando el mínimo (como tu versión)
        dados = [random.randint(1, 6) for _ in range(6)]
        dados.remove(min(dados))
        return sum(dados)

    def max_xp(self):
        return self.xp >= 100

    def level_up_once(self):
        if self.max_xp():
            self.nivel += 1
            self.xp -= 100
            # Bonus de stats por nivel
            self.fuerza += 1
            self.destreza += 1
            self.inteligencia += 1
            self.defensa += 1
            self.vida += 5  # pequeña curación/bono
            return True
        return False

    def level_up_all(self):
        """Sube varios niveles si acumula >100 XP varias veces.
           Devuelve (niveles_subidos, mensajes)"""
        msgs = []
        count = 0
        while self.max_xp():
            self.level_up_once()
            count += 1
            msgs.append(f"Subís al nivel {self.nivel}. ¡Felicitaciones!")
        return count, msgs

class Guerrero(Personaje):
    def __init__(self, base):
        self.__dict__.update(base.__dict__)
        self.clase = "Guerrero"
        self.fuerza += 3
        self.defensa += 2
        self.atributo_ataque = "fuerza"

class Mago(Personaje):
    def __init__(self, base):
        self.__dict__.update(base.__dict__)
        self.clase = "Mago"
        self.inteligencia += 4
        self.vida -= 10
        self.atributo_ataque = "inteligencia"

class Picaro(Personaje):
    def __init__(self, base):
        self.__dict__.update(base.__dict__)
        self.clase = "Pícaro"
        self.destreza += 4
        self.fuerza -= 1
        self.atributo_ataque = "destreza"
