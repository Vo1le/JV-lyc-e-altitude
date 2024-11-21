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
NUM_LAYERS = 5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

FOLDER_PATH = "collisions"
TILE_MAP_FILE_NAME = "map.txt"
TILE_MAP_RELOADABLE_FILE_NAME = "map_reload.txt"
TILE_MAP_IMAGE_FILE_NAME = "map.png"

FONT = pygame.font.Font(size=32)

if os.path.isfile(TILE_MAP_IMAGE_FILE_NAME):
    map_surface = pygame.image.load(TILE_MAP_IMAGE_FILE_NAME)
else:
    map_surface = pygame.Surface((WIDTH_MAP, HEIGHT_MAP))
    map_surface.fill((255, 255, 255))

def main():

    # Set up des images
    images = {}
    for file in os.listdir(FOLDER_PATH):
        if os.path.isfile(os.path.join(FOLDER_PATH, file)):
            images[file] = pygame.transform.scale(pygame.image.load(os.path.join(FOLDER_PATH, file)), (TILE_SIZE, TILE_SIZE))
    images_faded = {}
    for image_name in images:
        img: pygame.Surface = images[image_name].copy()
        img.set_alpha(100.0)
        images_faded[image_name] = img
    
    layers = load_map(TILE_MAP_RELOADABLE_FILE_NAME)
    current_layer = 0

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

    map_sauvegarde = True

    historique_changements = []
    changements_max = 10
    dernier_tuile_placee_coords = False

    # loop de jeu    
    running = True
    while running:
        touches_appuyes = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    dialogue_quitter(layers, map_sauvegarde, images)
                if event.key == pygame.K_q:
                    map_sauvegarde = True
                    save_map_image(layers, images)
                    pygame.image.save(map_surface, TILE_MAP_IMAGE_FILE_NAME)
                    save_map(TILE_MAP_FILE_NAME, layers)
                    save_map(TILE_MAP_RELOADABLE_FILE_NAME, layers, False)
                if event.key == pygame.K_a:
                    menu.visible = not menu.visible
                    if not menu.visible:
                        menu.dragging = -1
                if event.key == pygame.K_UP:
                    current_layer = min(current_layer + 1, NUM_LAYERS - 1)
                elif event.key == pygame.K_DOWN:
                    current_layer = max(current_layer - 1, 0)
                if touches_appuyes[pygame.K_LCTRL] or touches_appuyes[pygame.K_RCTRL]:
                    if event.key == pygame.K_z:
                        if len(historique_changements) > 0:
                            changement = historique_changements[0]
                            add_tile_to_map(layers[current_layer], images, changement["tuile"], changement["pos"], zoom_factor)
                            historique_changements.pop(0)
                else:
                    if event.key == pygame.K_z:
                        zoom_factor = 1

            
            if event.type == pygame.QUIT:
                dialogue_quitter(layers, map_sauvegarde, images)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for img in menu.collisionRects:
                        if img["rect"].collidepoint(event.pos):
                            menu.dragging = img["key"]
                    dragging = True
                    last_mouse_pos = pygame.mouse.get_pos()
                elif event.button == 2:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    menu.dragging = get_tile_from_map(layers[current_layer], (mouse_x - offset_x, mouse_y - offset_y), zoom_factor) or VIDE
                elif event.button == 3:
                    if menu.dragging != -1:
                        placing_tile = True
                        map_sauvegarde = False
            
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
            coords = (x - offset_x, y - offset_y)
            if dernier_tuile_placee_coords != coords:
                dernier_tuile_placee_coords = coords
                tuile = get_tile_from_map(layers[current_layer], coords, zoom_factor) or VIDE
                if tuile != menu.dragging:
                    changement = {
                        "pos": coords,
                        "tuile": tuile
                    }
                    historique_changements.insert(0, changement)
                    if len(historique_changements) > changements_max:
                        historique_changements.pop()
                    add_tile_to_map(layers[current_layer], images, menu.dragging, coords, zoom_factor)
        else:
            dernier_tuile_placee_coords = False

        for i, layer in enumerate(layers):
            using_images = images
            if i != current_layer:
                using_images = images_faded
            draw_tile_map(screen, layer, using_images, zoom_factor, offset_x, offset_y)

        for x in range(0, WIDTH_MAP, GAME_SCREEN_WIDTH):
            screen_coords = (x * zoom_factor + offset_x, offset_y)
            screen_coords_end = (x * zoom_factor + offset_x, HEIGHT_MAP * zoom_factor + offset_y)
            pygame.draw.line(screen, (100, 100, 100, 200), screen_coords, screen_coords_end)

        for y in range(0, HEIGHT_MAP, GAME_SCREEN_HEIGHT):
            screen_coords = (offset_x, y * zoom_factor + offset_y)
            screen_coords_end = (WIDTH_MAP * zoom_factor + offset_x, y * zoom_factor + offset_y)
            pygame.draw.line(screen, (100, 100, 100, 200), screen_coords, screen_coords_end)

        menu.draw(screen)

        pygame.draw.rect(screen, (0, 0, 0), (offset_x, offset_y, WIDTH_MAP * zoom_factor, HEIGHT_MAP * zoom_factor), 10)
        
        current_layer_img = FONT.render("couche: " + str(current_layer), True, (0, 100, 100))

        screen.blit(current_layer_img, (SCREEN_WIDTH - 100, 10))

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


def add_tile_to_map(TILE_MAP, images, key, coords, zoom_factor=1):
    x, y = coords
    scaled_tile = int(TILE_SIZE * zoom_factor)
    cell_x = int(x // scaled_tile)
    cell_y = int(y // scaled_tile)
    if 0 <= cell_x < WIDTH_MAP / TILE_SIZE and 0 <= cell_y < HEIGHT_MAP / TILE_SIZE:
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

        self.initialized_rects = False

        self.offset_y = 50
        self.vide_color = (100, 100, 100)
    
    def draw(self, screen: pygame.Surface):
        screen.blit(self.edit_image, (0, 0))
        screen.blit(self.export_image, (70, 0))
        screen.blit(self.zoom_image, (150, 0))

        offset_x = 0
        y = 0
        if self.visible:
            screen.blit(self.menu_image, (0, self.offset_y))
            if not self.initialized_rects:
                self.collisionRects = []
            for key in self.collisionList:
                img: pygame.Surface = self.collisionList[key]
                rect = screen.blit(img, (offset_x, self.offset_y + y))
                if y + img.get_height() < self.menu_image.get_height():
                    y += img.get_height()
                else:
                    offset_x += 50
                    y = img.get_height()
                if key == VIDE:
                    pygame.draw.rect(screen, self.vide_color, pygame.rect.Rect(offset_x, self.offset_y + y - img.get_height(), TILE_SIZE, TILE_SIZE))
                rect = screen.blit(img, (offset_x, self.offset_y + y - img.get_height()))
                if not self.initialized_rects:
                    self.collisionRects.append({"image": img, "rect": rect, "key": key})

            if self.dragging != -1:
                if self.dragging == VIDE:
                    pygame.draw.rect(screen, self.vide_color, pygame.rect.Rect(pygame.mouse.get_pos(), (TILE_SIZE, TILE_SIZE)))
                screen.blit(self.collisionList[self.dragging], pygame.mouse.get_pos())
            
            self.initialized_rects = True


def load_map(file_name):
    if os.path.isfile(file_name):
        with open(file_name, "rb") as f:
            TILE_MAP = pickle.load(f)
    else:
        TILE_MAP = [[[VIDE for _ in range(WIDTH_MAP // TILE_SIZE)] for _ in range(HEIGHT_MAP // TILE_SIZE)] for _ in range(NUM_LAYERS)]
    return TILE_MAP

def save_map(file_name, TILE_MAP, reloadable=True):
    tile_map = TILE_MAP
    if reloadable:
        tile_map = [[map(appliquer_attributs, row) for row in layer] for layer in TILE_MAP]
    with open(file_name, "wb") as f:
        pickle.dump(tile_map, f)

def save_map_image(TILE_MAP, images):
    map_surface.fill((255, 255, 255))
    for layer in TILE_MAP:
        for y, row in enumerate(layer):
            for x, tile in enumerate(row):
                map_surface.blit(images[tile], (x * TILE_SIZE, y * TILE_SIZE))

def appliquer_attributs(tile_name):
    return attributs[tile_name]

def dialogue_quitter(TILE_MAP, map_sauvegarde, images):
    pygame.quit()
    print("\n\n")
    if not map_sauvegarde:
        s = ""
        for i in range(5):
            s = input("Vous avez quitté l'éditeur de niveau sans sauvegarder, voulez vous le faire maintenant? (oui/non) ").lower()
            if s == "oui":
                save_map_image(TILE_MAP, images)
                pygame.image.save(map_surface, TILE_MAP_IMAGE_FILE_NAME)
                save_map(TILE_MAP_FILE_NAME, TILE_MAP)
                save_map(TILE_MAP_RELOADABLE_FILE_NAME, TILE_MAP, False)
                break
            print()
            if s == "non":
                break
            else:
                print("Réponse doit etre soit oui soit non, tentatives restantes avant termination du program:", 4 - i)
    sys.exit()

if __name__ == "__main__":
    main()