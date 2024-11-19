import pygame
import sys
import os
import pickle

from attributs import attributs, VIDE

pygame.init()

TITLE = "Tile Map System"
BG_COLOR = (255, 255, 255)

# constantes pour le zoom
MIN_ZOOM = 0.2
MAX_ZOOM = 10

#Paramétres de la map
TILE_SIZE = 64
GAME_SCREEN_WIDTH = 25 * TILE_SIZE
GAME_SCREEN_HEIGHT = 14 * TILE_SIZE
WIDTH_MAP = GAME_SCREEN_WIDTH * 3
HEIGHT_MAP = GAME_SCREEN_HEIGHT * 2

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

if os.path.isfile("map.png"):
    map_surface = pygame.image.load("map.png")
else:
    map_surface = pygame.Surface((WIDTH_MAP, HEIGHT_MAP))
    map_surface.fill((255, 255, 255))

FOLDER_PATH = "collisions"

def main():

    # Set up des images
    images = {}
    for file in os.listdir(FOLDER_PATH):
        if os.path.isfile(os.path.join(FOLDER_PATH, file)):
            images[file] = pygame.transform.scale(pygame.image.load(os.path.join(FOLDER_PATH, file)), (TILE_SIZE, TILE_SIZE))

    TILE_MAP_FILE_NAME = "map.txt"
    TILE_MAP_RELOADABLE_FILE_NAME = "map_reload.txt"
    TILE_MAP_IMAGE_FILE_NAME = "map.png"
    TILE_MAP = load_map(TILE_MAP_RELOADABLE_FILE_NAME)

    screen = pygame.display.set_mode(size=(SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    FPS = 30
    fpsClock = pygame.time.Clock()

    # variables pour le zoom
    zoom_factor = 1
    zoom_speed = 0.1

    # offset de la souris
    offset_x = 0
    offset_y = 0
    dragging = False
    last_mouse_pos = None

    menu = Menu(images)
    menu.draw(screen)

    placing_tile = False

    # loop de jeu    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_q:
                    pygame.image.save(map_surface, TILE_MAP_IMAGE_FILE_NAME)
                    save_map(TILE_MAP_FILE_NAME, TILE_MAP)
                    save_map(TILE_MAP_RELOADABLE_FILE_NAME, TILE_MAP, False)
                if event.key == pygame.K_z:
                    zoom_factor = 1
                if event.key == pygame.K_a:
                    menu.visible = not menu.visible
                    if not menu.visible:
                        menu.dragging = -1
            
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for img in menu.collisionRects:
                        if img["rect"].collidepoint(event.pos):
                            menu.dragging = img["key"]
                    dragging = True
                    last_mouse_pos = pygame.mouse.get_pos()
                elif event.button == 2:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    menu.dragging = get_tile_from_map(TILE_MAP, (mouse_x - offset_x, mouse_y - offset_y), zoom_factor) or VIDE
                elif event.button == 3:
                    if menu.dragging != -1:
                        placing_tile = True
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
                elif event.button == 3:
                    placing_tile = False
            
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
                    zoom_factor = min(zoom_factor + zoom_speed, MAX_ZOOM)
                    
                elif event.y < 0:
                    zoom_factor = max(zoom_factor - zoom_speed, MIN_ZOOM)
        
        screen.fill(BG_COLOR)

        if placing_tile:
            x, y = pygame.mouse.get_pos()
            add_tile_to_map(TILE_MAP, images, menu.dragging, (x - offset_x, y - offset_y), zoom_factor)

        draw_tile_map(screen, TILE_MAP, images, zoom_factor, offset_x, offset_y)

        menu.draw(screen)

        pygame.draw.rect(screen, (0, 0, 0), (offset_x, offset_y, WIDTH_MAP * zoom_factor, HEIGHT_MAP * zoom_factor), 10)
        
        pygame.display.update()

        fpsClock.tick(FPS)

    pygame.quit()
    sys.exit()

# dessiner la map
def draw_tile_map(screen, TILE_MAP, images, zoom_factor=1, offset_x=0, offset_y=0):
    scaled_tile_size = TILE_SIZE * zoom_factor
    scaled_images = {}
    if zoom_factor != 1:
        for img in images:
            scaled_images[img] = pygame.transform.scale(images[img], (scaled_tile_size, scaled_tile_size))
    else:
        scaled_images = images
    for y, row in enumerate(TILE_MAP):
        for x, tile in enumerate(row):
            if not tile in images:
                print("Il manque le fichier image: " + tile)
                pygame.quit()
                sys.exit()
            screen_coords = (x * scaled_tile_size + offset_x, y * scaled_tile_size + offset_y)
            if -TILE_SIZE < screen_coords[0] < SCREEN_WIDTH and -TILE_SIZE < screen_coords[1] < SCREEN_HEIGHT:
                tile_img = scaled_images[tile]
                screen.blit(tile_img, screen_coords)
    
    for x in range(0, WIDTH_MAP, GAME_SCREEN_WIDTH):
        screen_coords = (x * zoom_factor + offset_x, offset_y)
        screen_coords_end = (x * zoom_factor + offset_x, HEIGHT_MAP * zoom_factor + offset_y)
        pygame.draw.line(screen, (100, 100, 100, 200), screen_coords, screen_coords_end)

    for y in range(0, HEIGHT_MAP, GAME_SCREEN_HEIGHT):
        screen_coords = (offset_x, y * zoom_factor + offset_y)
        screen_coords_end = (WIDTH_MAP * zoom_factor + offset_x, y * zoom_factor + offset_y)
        pygame.draw.line(screen, (100, 100, 100, 200), screen_coords, screen_coords_end)
    


def add_tile_to_map(TILE_MAP, images, key, coords, zoom_factor=1):
    x, y = coords
    scaled_tile = int(TILE_SIZE * zoom_factor)
    cell_x = int(x // scaled_tile)
    cell_y = int(y // scaled_tile)
    if 0 <= cell_x < WIDTH_MAP / TILE_SIZE and 0 <= cell_y < HEIGHT_MAP / TILE_SIZE:
        map_surface.fill((255, 255, 255), (cell_x * TILE_SIZE, cell_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        map_surface.blit(images[key], (cell_x * TILE_SIZE, cell_y * TILE_SIZE))
        TILE_MAP[cell_y][cell_x] = key

def get_tile_from_map(TILE_MAP, coords, zoom_factor=1):
    x, y = coords
    scaled_tile = int(TILE_SIZE * zoom_factor)
    cell_x = int(x // scaled_tile)
    cell_y = int(y // scaled_tile)
    if 0 < cell_x < WIDTH_MAP / TILE_SIZE - 1 and 0 < cell_y < HEIGHT_MAP / TILE_SIZE - 1:
        return TILE_MAP[cell_y][cell_x]


class Menu:
    def __init__(self, images: dict):
        self.menu_image = pygame.image.load("menu.png")
        self.menu_image.set_alpha(200)
        self.edit_image = pygame.image.load("edit.png")
        self.export_image = pygame.image.load("export.png")
        self.zoom_image = pygame.image.load("zoom.png")
        self.visible = True

        self.collisionRects = []

        self.dragging = -1

        self.collisionList = images
    
    def draw(self, screen: pygame.Surface):
        screen.blit(self.edit_image, (0, 0))
        screen.blit(self.export_image, (70, 0))
        screen.blit(self.zoom_image, (150, 0))

        offset_y = 50
        offset_x = 0
        y = 0
        if self.visible:
            screen.blit(self.menu_image, (0, offset_y))
            self.collisionRects = []
            for key in self.collisionList:
                img: pygame.Surface = self.collisionList[key]
                rect = screen.blit(img, (offset_x, offset_y + y))
                if y + img.get_height() < self.menu_image.get_height():
                    y += img.get_height()
                else:
                    offset_x += 50
                    y = img.get_height()
                rect = screen.blit(img, (offset_x, offset_y + y - img.get_height()))
                self.collisionRects.append({"image": img, "rect": rect, "key": key})

            if self.dragging != -1:
                screen.blit(self.collisionList[self.dragging], pygame.mouse.get_pos())


def load_map(file_name):
    if os.path.isfile(file_name):
        with open(file_name, "rb") as f:
            TILE_MAP = pickle.load(f)
    else:
        TILE_MAP = [[VIDE for _ in range(WIDTH_MAP // TILE_SIZE)] for _ in range(HEIGHT_MAP // TILE_SIZE)]
    return TILE_MAP

def save_map(file_name, TILE_MAP, reloadable=True):
    tile_map = TILE_MAP
    if reloadable:
        tile_map = [map(appliquer_attributs, row) for row in TILE_MAP]
    with open(file_name, "wb") as f:
        pickle.dump(tile_map, f)

def appliquer_attributs(tile_name):
    return attributs[tile_name]

if __name__ == "__main__":
    main()