import random

class Monstruo:
    def __init__(self, nombre, vida, fuerza, defensa, xp):
        self.nombre = nombre
        self.vida = vida
        self.fuerza = fuerza
        self.defensa = defensa
        self.xp = xp

# --- Básicos ---
class Goblin(Monstruo):
    def __init__(self):
        super().__init__("Goblin", vida=30, fuerza=5, defensa=2, xp=15)

class RataGigante(Monstruo):
    def __init__(self):
        super().__init__("Rata Gigante", vida=25, fuerza=4, defensa=1, xp=12)

class Esqueleto(Monstruo):
    def __init__(self):
        super().__init__("Esqueleto", vida=35, fuerza=6, defensa=3, xp=18)

class Zombi(Monstruo):
    def __init__(self):
        super().__init__("Zombi", vida=40, fuerza=5, defensa=2, xp=20)

class Murcielago(Monstruo):
    def __init__(self):
        super().__init__("Murciélago", vida=22, fuerza=3, defensa=1, xp=10)

# --- Medios ---
class Ogro(Monstruo):
    def __init__(self):
        super().__init__("Ogro", vida=70, fuerza=15, defensa=8, xp=40)

class HombreLobo(Monstruo):
    def __init__(self):
        super().__init__("Hombre Lobo", vida=60, fuerza=18, defensa=6, xp=42)

class Troll(Monstruo):
    def __init__(self):
        super().__init__("Troll", vida=85, fuerza=20, defensa=10, xp=48)

class Espectro(Monstruo):
    def __init__(self):
        super().__init__("Espectro", vida=65, fuerza=17, defensa=5, xp=44)

class Basilisco(Monstruo):
    def __init__(self):
        super().__init__("Basilisco", vida=75, fuerza=19, defensa=9, xp=46)

# --- Selección aleatoria ---
def selectBE():
    pool = [Goblin, RataGigante, Esqueleto, Zombi, Murcielago]
    cls = random.choice(pool)
    return cls()

def selectME():
    pool = [Ogro, HombreLobo, Troll, Espectro, Basilisco]
    cls = random.choice(pool)
    return cls()
