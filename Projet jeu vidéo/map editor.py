import pygame
import sys

pygame.init()

TITLE = "Title Map System"
BG_COLOR = (255, 255, 255)


TITLE_MAP = [
    "XXXXXXXXXXXXXXXX",
    "X              X",
    "X              X",
    "X              X",
    "X              X",
    "X              X",
    "X              X",
    "X              X",
    "X              X",
    "X              X",
    "XXXXXXXXXXXXXXXX"
]

#Paramétres de la map
TILE_SIZE = 100
index = 1
width_map = 0
while len(TITLE_MAP[len(TITLE_MAP) - index]) - index != 0:
    if len(TITLE_MAP[len(TITLE_MAP) - index]) > width_map:
        width_map = len(TITLE_MAP[len(TITLE_MAP) - index])
        index += 1
    else :
        index += 1
print(width_map)
width_map = width_map * TILE_SIZE

map_surface = pygame.Surface((width_map, len(TITLE_MAP)*TILE_SIZE))

# Set up des images
img = {
    "X": pygame.image.load("wall.png"),
    " ": pygame.image.load("vide.jpg")
}
screen = pygame.display.set_mode(size=(800,600))
pygame.display.set_caption(TITLE)

# Zoom
MIN_ZOOM = 0
MAX_ZOOM = 100
zoom_factor = 1

# offset de la souris
offset_x = 0
offset_y = 0
dragging = False
last_mouse_pos = None

# dessiner la map
def draw_title_map():
    for y, row in enumerate(TITLE_MAP):
        for x, tile in enumerate(row):
            Img = img[tile]
            scaled_tile_size = TILE_SIZE * zoom_factor
            scaled_image = pygame.transform.scale(Img, ( TILE_SIZE,  TILE_SIZE))
            screen.blit(scaled_image, (x * scaled_tile_size + offset_x, y * scaled_tile_size + offset_y))
            map_surface.blit(scaled_image, (x * TILE_SIZE, y * TILE_SIZE))


# loop de jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                dragging = True
                last_mouse_pos = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if last_mouse_pos:
                    dx = mouse_x - last_mouse_pos[0]
                    dy = mouse_y - last_mouse_pos[1]
                    offset_x += dx
                    offset_y += dy
                last_mouse_pos = (mouse_x, mouse_y)
        elif event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                zoom_factor = min(zoom_factor + 0.1, MAX_ZOOM)
                
            elif event.y < 0:
                zoom_factor = max(zoom_factor - 0.1, MIN_ZOOM)
    
    screen.fill(BG_COLOR)
    pygame.Surface.fill(map_surface,BG_COLOR)

    draw_title_map()    
    
    pygame.image.save(map_surface, "map.png")
    pygame.display.flip()

pygame.quit()
sys.exit()