import random
import pygame

# Colores básicos
WHITE = (235, 235, 235)
GRAY  = (60, 60, 70)
DARK  = (24, 24, 28)
YELL  = (240, 210, 60)

class Item:
    def __init__(self, name, quantity=1):
        self.name = name
        self.quantity = quantity

    def __str__(self):
        return f"{self.name} x{self.quantity}"

class InventorySlot:
    def __init__(self, item=None):
        self.item = item

class Inventory:
    def __init__(self, num_slots):
        self.slots = [InventorySlot() for _ in range(num_slots)]

    def add_item(self, name, quantity=1):
        # Apilar mismo ítem si ya existe
        for slot in self.slots:
            if slot.item and slot.item.name == name:
                slot.item.quantity += quantity
                return
        # Buscar hueco vacío
        for slot in self.slots:
            if not slot.item:
                slot.item = Item(name, quantity)
                return
        # Inventario lleno (silencioso en pygame; podrías devolver mensaje)
        return

    def rewardBE(self, player):
        """Recompensa básica tras victoria: oro + 1 ítem al azar."""
        monedas = random.randint(8, 40)
        player.oro += monedas

        items_basicos = ["Poción pequeña", "Cuerda", "Antorcha", "Pan duro", "Daga vieja"]
        item = random.choice(items_basicos)
        self.add_item(item, 1)

        msg = f"+{monedas} oro y obtuviste: {item}"
        return monedas, item, msg

# -------- Dibujo del inventario en Pygame --------
def draw_inventory_panel(surface, inv: Inventory, oro: int, font):
    # Panel lateral derecho
    panel_w = 360
    x = surface.get_width() - panel_w - 24
    y = 220
    h = 360

    pygame.draw.rect(surface, DARK, (x, y, panel_w, h))
    pygame.draw.rect(surface, GRAY, (x, y, panel_w, h), 2)

    surface.blit(font.render("Inventario [I para cerrar]", True, YELL), (x+12, y+10))
    surface.blit(font.render(f"Oro: {oro}", True, WHITE), (x+12, y+44))

    # Slots en grilla
    cols = 3
    slot_w, slot_h = 100, 80
    gap = 12
    start_x, start_y = x+12, y+80

    for idx, slot in enumerate(inv.slots):
        r = idx // cols
        c = idx % cols
        sx = start_x + c*(slot_w + gap)
        sy = start_y + r*(slot_h + gap)
        pygame.draw.rect(surface, (32,32,36), (sx, sy, slot_w, slot_h))
        pygame.draw.rect(surface, GRAY, (sx, sy, slot_w, slot_h), 2)

        if slot.item:
            name = slot.item.name
            qty  = slot.item.quantity
            txt1 = font.render(name[:12], True, WHITE)
            txt2 = font.render(f"x{qty}", True, WHITE)
            surface.blit(txt1, (sx+8, sy+10))
            surface.blit(txt2, (sx+8, sy+40))
