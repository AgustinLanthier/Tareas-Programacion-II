import pygame
import sys
import pj
import monstruos
import combate
from inventario import draw_inventory_panel

pygame.init()

# -------- Ventana & Fuente --------
WIDTH, HEIGHT = 960, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dungeon RPG (Pygame)")

FONT = pygame.font.Font(None, 32)
BIG  = pygame.font.Font(None, 48)
SMALL= pygame.font.Font(None, 24)

# -------- Colores --------
BLACK = (10, 10, 12)
WHITE = (235, 235, 235)
GRAY  = (60, 60, 70)
YELL  = (240, 210, 60)
RED   = (210, 60, 60)
GREEN = (60, 190, 100)
BLUE  = (80, 140, 220)

# -------- Estados del juego --------
TITLE, NAME, CLASS, BATTLE, REWARD, GAMEOVER = range(6)

# -------- Utilidades de UI --------
def draw_centered_text(surface, text, font, color, y):
    img = font.render(text, True, color)
    x = WIDTH // 2 - img.get_width() // 2
    surface.blit(img, (x, y))

def draw_box(surface, x, y, w, h, border=2, color=GRAY):
    pygame.draw.rect(surface, color, (x, y, w, h), border)

def draw_stats(surface, jugador, enemigo):
    # Panel jugador
    x, y, w, h = 30, HEIGHT-150, 420, 120
    pygame.draw.rect(surface, (30,30,36), (x, y, w, h))
    draw_box(surface, x, y, w, h, 2)

    lines = [
        f"{jugador.nombre} — {jugador.clase}  (Lvl {jugador.nivel})",
        f"HP: {max(0, jugador.vida)}   XP: {jugador.xp}   Oro: {jugador.oro}",
        f"Fuerza: {jugador.fuerza}  Destreza: {jugador.destreza}  Int: {jugador.inteligencia}  Def: {jugador.defensa}"
    ]
    for i, line in enumerate(lines):
        surface.blit(FONT.render(line, True, WHITE), (x+12, y+10 + i*34))

    # Panel enemigo
    ex, ey, ew, eh = WIDTH-450, 40, 420, 110
    pygame.draw.rect(surface, (30,30,36), (ex, ey, ew, eh))
    draw_box(surface, ex, ey, ew, eh, 2)

    elines = [
        f"{enemigo.nombre}",
        f"HP: {max(0, enemigo.vida)}   Fuerza: {enemigo.fuerza}   Def: {enemigo.defensa}   XP al derrotar: {enemigo.xp}"
    ]
    for i, line in enumerate(elines):
        surface.blit(FONT.render(line, True, WHITE), (ex+12, ey+10 + i*40))

def draw_message_log(surface, log):
    x, y, w, h = 30, 40, 520, 260
    pygame.draw.rect(surface, (24,24,28), (x, y, w, h))
    draw_box(surface, x, y, w, h, 2)
    surface.blit(FONT.render("Eventos", True, YELL), (x+12, y+8))
    # Últimas 6 líneas
    to_show = log[-6:]
    for i, line in enumerate(to_show):
        surface.blit(SMALL.render(line, True, WHITE), (x+12, y+40 + i*28))

def draw_actions_help(surface):
    txt = "Acciones: [1] Atacar   [2] Esquivar   [3] Bloquear   [I] Inventario"
    draw_centered_text(surface, txt, FONT, BLUE, HEIGHT-36)

def text_input(surface, prompt, current):
    draw_centered_text(surface, prompt, FONT, WHITE, HEIGHT//2-60)
    box_w = 520
    x = WIDTH//2 - box_w//2
    pygame.draw.rect(surface, (24,24,28), (x, HEIGHT//2-10, box_w, 52))
    draw_box(surface, x, HEIGHT//2-10, box_w, 52, 2)
    surface.blit(BIG.render(current or "", True, WHITE), (x+12, HEIGHT//2-4))

def class_selection(surface, options, selected_idx):
    draw_centered_text(surface, "Elegí tu clase con ← → y Enter", FONT, WHITE, HEIGHT//2-120)
    gap = 240
    start_x = WIDTH//2 - (gap*(len(options)-1))//2
    for i, name in enumerate(options):
        cx = start_x + i*gap
        col = YELL if i == selected_idx else WHITE
        pygame.draw.circle(surface, col, (cx, HEIGHT//2), 6, 0)
        draw_centered_text(surface, name, BIG, col, HEIGHT//2+20)

def new_enemy(player_level):
    # Aumenta la dificultad alternando entre básicos y medios
    import random
    if player_level <= 2:
        return monstruos.selectBE()
    else:
        return random.choice([monstruos.selectBE(), monstruos.selectME()])

def reward_screen(surface, messages):
    draw_centered_text(surface, "¡Victoria! Recompensas:", BIG, GREEN, HEIGHT//2-120)
    for i, m in enumerate(messages):
        draw_centered_text(surface, m, FONT, WHITE, HEIGHT//2-40 + i*34)
    draw_centered_text(surface, "Pulsa Enter para continuar…", SMALL, BLUE, HEIGHT//2+130)

def game_over_screen(surface):
    draw_centered_text(surface, "Has sido derrotado…", BIG, RED, HEIGHT//2-20)
    draw_centered_text(surface, "Pulsa Enter para reiniciar", FONT, WHITE, HEIGHT//2+40)

def main():
    clock = pygame.time.Clock()

    # --- Variables de estado global ---
    state = TITLE
    name_buffer = ""
    class_idx = 0
    classes = ["Guerrero", "Mago", "Pícaro"]
    show_inventory = False

    jugador = None
    enemigo  = None
    message_log = []
    reward_messages = []

    while True:
        # ----------------- Input -----------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if state == TITLE:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    state = NAME

            elif state == NAME:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if name_buffer.strip():
                            base = pj.Personaje(name_buffer.strip())
                            # por defecto guerrero; se ajusta en CLASS
                            jugador = pj.Guerrero(base)
                            state = CLASS
                        else:
                            name_buffer = ""
                    elif event.key == pygame.K_BACKSPACE:
                        name_buffer = name_buffer[:-1]
                    else:
                        ch = event.unicode
                        if ch and ch.isprintable() and len(name_buffer) < 20:
                            name_buffer += ch

            elif state == CLASS:
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        class_idx = (class_idx - 4) % len(classes)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        class_idx = (class_idx + 4) % len(classes)
                    elif event.key == pygame.K_RETURN:
                        # aplicar clase elegida
                        base = pj.Personaje(jugador.nombre)
                        if classes[class_idx] == "Guerrero":
                            jugador = pj.Guerrero(base)
                        elif classes[class_idx] == "Mago":
                            jugador = pj.Mago(base)
                        else:
                            jugador = pj.Picaro(base)

                        enemigo = new_enemy(jugador.nivel)
                        message_log = [f"¡Un {enemigo.nombre} aparece!"]
                        state = BATTLE

            elif state == BATTLE:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i:
                        show_inventory = not show_inventory
                    elif event.key == pygame.K_1:
                        msg = combate.combate_turno(jugador, enemigo, "atacar")
                        message_log.append(msg)
                    elif event.key == pygame.K_2:
                        msg = combate.combate_turno(jugador, enemigo, "esquivar")
                        message_log.append(msg)
                    elif event.key == pygame.K_3:
                        msg = combate.combate_turno(jugador, enemigo, "bloquear")
                        message_log.append(msg)

                        # nada más — el daño se aplicó dentro del turno

                    # Chequear fin de combate
                    if enemigo and enemigo.vida <= 0:
                        # Recompensa por victoria
                        jugador.xp += enemigo.xp
                        lvlups, level_msgs = jugador.level_up_all()  # puede subir varios niveles
                        rw_gold, rw_item, rw_msg = jugador.inv.rewardBE(jugador)  # actualiza oro + inv
                        reward_messages = [
                            f"Derrotaste al {enemigo.nombre} (+{enemigo.xp} XP).",
                            *level_msgs,
                            rw_msg
                        ]
                        state = REWARD

                    if jugador and jugador.vida <= 0:
                        state = GAMEOVER

            elif state == REWARD:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    # Nuevo enemigo y a pelear
                    enemigo = new_enemy(jugador.nivel)
                    message_log.append(f"¡Un {enemigo.nombre} aparece!")
                    state = BATTLE

            elif state == GAMEOVER:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    # Reiniciar todo
                    name_buffer = ""
                    class_idx = 0
                    show_inventory = False
                    jugador = None
                    enemigo = None
                    message_log = []
                    reward_messages = []
                    state = TITLE

        # ----------------- Render -----------------
        screen.fill(BLACK)

        if state == TITLE:
            draw_centered_text(screen, "Dungeon RPG", BIG, YELL, HEIGHT//2-40)
            draw_centered_text(screen, "Pulsa Enter para comenzar", FONT, WHITE, HEIGHT//2+20)

        elif state == NAME:
            draw_centered_text(screen, "Escribí el nombre de tu personaje y Enter", FONT, WHITE, HEIGHT//2-100)
            text_input(screen, "Nombre:", name_buffer)

        elif state == CLASS:
            draw_centered_text(screen, f"Elegí la clase para {jugador.nombre}", BIG, YELL, HEIGHT//2-180)
            class_selection(screen, classes, class_idx)

        elif state == BATTLE and jugador and enemigo:
            draw_stats(screen, jugador, enemigo)
            draw_message_log(screen, message_log)
            draw_actions_help(screen)
            if show_inventory:
                draw_inventory_panel(screen, jugador.inv, jugador.oro, FONT)

        elif state == REWARD:
            reward_screen(screen, reward_messages)

        elif state == GAMEOVER:
            game_over_screen(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
