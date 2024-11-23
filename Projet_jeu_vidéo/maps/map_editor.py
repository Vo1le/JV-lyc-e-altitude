import pygame
import sys
import os
import pickle
from math import ceil, floor
from attributs import *

pygame.init()

TITLE = "Tile Map System"
BG_COLOR = (255, 255, 255)

# constantes pour le zoom
MIN_ZOOM = 0.2
MAX_ZOOM = 5

#Paramétres de la map
NUM_LAYERS = 5

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700

FOLDER_PATH = "collisions"
TILE_MAP_FOLDER_NAME = "tilemaps"
TILE_MAP_FILE_NAME = "map.txt"
TILE_MAP_RELOADABLE_FILE_NAME = "map_reload.txt"
TILE_MAP_IMAGE_FILE_NAME = "map.png"

FONT = pygame.font.Font(size=32)

HELP_BACKGROUND = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
HELP_BACKGROUND.fill(pygame.Color(200, 200, 100))
HELP_BACKGROUND.set_alpha(150)

if os.path.isfile(TILE_MAP_IMAGE_FILE_NAME):
    map_surface = pygame.image.load(TILE_MAP_IMAGE_FILE_NAME)
else:
    map_surface = pygame.Surface((WIDTH_MAP, HEIGHT_MAP))
    map_surface.fill((255, 255, 255))

def main():

    screen = pygame.display.set_mode(size=(SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    FPS = 30
    fpsClock = pygame.time.Clock()

    # Set up des images
    images = {}
    for file in os.listdir(FOLDER_PATH):
        if os.path.isfile(os.path.join(FOLDER_PATH, file)):
            images[file] = pygame.transform.scale(pygame.image.load(os.path.join(FOLDER_PATH, file)), (TILE_SIZE, TILE_SIZE))
    for file in os.listdir(TILE_MAP_FOLDER_NAME):
        if os.path.isfile(os.path.join(TILE_MAP_FOLDER_NAME, file)):
            if file in tile_maps.keys():
                img = pygame.image.load(os.path.join(TILE_MAP_FOLDER_NAME, file)).convert_alpha()
                size = tile_maps[file]["tile_size"]
                for i, atlas in enumerate(tile_maps[file]["attributs"]):
                    for y, row in enumerate(atlas):
                        for x, _ in enumerate(row):
                            surface = pygame.Surface((size, size)).convert_alpha()
                            surface.fill(pygame.Color(0, 0, 0, 0))
                            surface.blit(img, (0, 0), (x * size, y * size, size, size))
                            img_name = file + "::" + str(i) + "::" + str(x) + ";" + str(y)
                            images[img_name] = pygame.transform.scale(surface, (TILE_SIZE, TILE_SIZE))
            else:
                print("tile map " + file + " n'est pas décrite dans attributs.py")
    images_faded = {}
    for image_name in images:
        img: pygame.Surface = images[image_name].copy()
        img.set_alpha(100.0)
        images_faded[image_name] = img
    
    layers = load_map(TILE_MAP_RELOADABLE_FILE_NAME)
    current_layer = 0

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
    placing_rect = False
    placing_rect_position = pygame.Vector2(0, 0)

    show_help = True

    map_sauvegarde = True

    historique_changements = []
    changements_max = 10
    dernier_tuile_placee_coords = False

    # loop de jeu    
    running = True
    while running:
        touches_appuyes = pygame.key.get_pressed()
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    dialogue_quitter(layers, map_sauvegarde, images)
                elif event.key == pygame.K_q:
                    map_sauvegarde = True
                    save_map_image(layers, images)
                    pygame.image.save(map_surface, TILE_MAP_IMAGE_FILE_NAME)
                    save_map(TILE_MAP_FILE_NAME, layers)
                    save_map(TILE_MAP_RELOADABLE_FILE_NAME, layers, False)
                elif event.key == pygame.K_a:
                    menu.visible = not menu.visible
                    if not menu.visible:
                        menu.dragging = -1
                elif event.key == pygame.K_UP:
                    current_layer = min(current_layer + 1, NUM_LAYERS - 1)
                elif event.key == pygame.K_DOWN:
                    current_layer = max(current_layer - 1, 0)
                elif event.key == pygame.K_e:
                    menu.dragging = VIDE
                elif event.key == pygame.K_h:
                    show_help = not show_help
                if touches_appuyes[pygame.K_LCTRL] or touches_appuyes[pygame.K_RCTRL]:
                    if event.key == pygame.K_z:
                        if len(historique_changements) > 0:
                            changement = historique_changements[0]
                            if type(changement) is list:
                                for change in changement:
                                    add_tile_to_map(layers[change["layer"]], change["tuile"], change["pos"], zoom_factor)
                            else:
                                add_tile_to_map(layers[changement["layer"]], changement["tuile"], changement["pos"], zoom_factor)
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
                    menu.dragging = get_tile_from_map(layers[current_layer], (x - offset_x, y - offset_y), zoom_factor) or VIDE
                elif event.button == 3:
                    if menu.dragging != -1:
                        placing_tile = True
                        map_sauvegarde = False
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
                elif event.button == 3:
                    placing_tile = False
                    if not type(placing_rect) is bool and menu.dragging != -1 and not (placing_rect.width == 0 or placing_rect.height == 0):
                        placing_rect.width /= zoom_factor
                        placing_rect.height /= zoom_factor
                        scaled_tile_size = TILE_SIZE
                        x = placing_rect.left
                        changements = []
                        while x < placing_rect.right:
                            y = placing_rect.top
                            while y < placing_rect.bottom:
                                coords = (x, y)
                                changement = {
                                    "pos": (x * zoom_factor, y * zoom_factor),
                                    "tuile": get_tile_from_map(layers[current_layer], coords, 1),
                                    "layer": current_layer
                                }
                                changements.append(changement)
                                add_tile_to_map(layers[current_layer], menu.dragging, coords, 1)
                                y += scaled_tile_size
                            x += scaled_tile_size
                        historique_changements.insert(0, changements)
                        if len(historique_changements) > changements_max:
                            historique_changements.pop()

            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    if last_mouse_pos:
                        dx = x - last_mouse_pos[0]
                        dy = y - last_mouse_pos[1]
                        offset_x += dx
                        offset_y += dy
                    last_mouse_pos = (x, y)
            
            elif event.type == pygame.MOUSEWHEEL:
                if menu.rect.collidepoint(x, y):
                    if event.y > 0:
                        menu.y_scroll = min(menu.y_scroll + menu.scroll_speed, menu.offset_y * 2)
                    elif event.y < 0:
                        menu.y_scroll -= menu.scroll_speed
                else:
                    if event.y > 0:
                        zoom_factor = min(zoom_factor + zoom_speed, MAX_ZOOM)
                    elif event.y < 0:
                        zoom_factor = max(zoom_factor - zoom_speed, MIN_ZOOM)
        
        if touches_appuyes[pygame.K_LSHIFT]:
            global_mouse_x = (x - offset_x) / zoom_factor
            global_mouse_y = (y - offset_y) / zoom_factor
            scaled_tile_size = TILE_SIZE * zoom_factor
            if type(placing_rect) is bool:
                coords = (floor(global_mouse_x / TILE_SIZE) * TILE_SIZE, floor(global_mouse_y / TILE_SIZE) * TILE_SIZE)
                placing_rect = pygame.Rect(coords, (scaled_tile_size, scaled_tile_size))
                placing_rect_position = pygame.Vector2(coords)
            func_x = ceil
            func_y = ceil
            if global_mouse_x < placing_rect_position.x:
                func_x = floor
            if global_mouse_y < placing_rect_position.y:
                func_y = floor
            placing_rect.size = (abs(func_x((global_mouse_x - placing_rect_position.x) / TILE_SIZE) * scaled_tile_size), abs(func_y((global_mouse_y - placing_rect_position.y) / TILE_SIZE) * scaled_tile_size))
            if global_mouse_x < placing_rect_position.x:
                placing_rect.left = placing_rect_position.x - placing_rect.width / zoom_factor
            else:
                placing_rect.left = placing_rect_position.x
            if global_mouse_y < placing_rect_position.y:
                placing_rect.top = placing_rect_position.y - placing_rect.height / zoom_factor
            else:
                placing_rect.top = placing_rect_position.y
        else:
            placing_rect = False

        screen.fill(BG_COLOR)

        if placing_tile and type(placing_rect) is bool:
            coords = (x - offset_x, y - offset_y)
            if dernier_tuile_placee_coords != coords:
                dernier_tuile_placee_coords = coords
                tuile = get_tile_from_map(layers[current_layer], coords, zoom_factor) or VIDE
                if tuile != menu.dragging:
                    changement = {
                        "pos": coords,
                        "tuile": tuile,
                        "layer": current_layer
                    }
                    historique_changements.insert(0, changement)
                    if len(historique_changements) > changements_max:
                        historique_changements.pop()
                    add_tile_to_map(layers[current_layer], menu.dragging, coords, zoom_factor)
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

        pygame.draw.rect(screen, (0, 0, 0), (offset_x, offset_y, WIDTH_MAP * zoom_factor, HEIGHT_MAP * zoom_factor), 10)

        if not type(placing_rect) is bool:
            s = pygame.Surface((placing_rect.size[0], placing_rect.size[1]))
            s.set_alpha(100)
            s.fill((100, 100, 100))
            screen.blit(s, (placing_rect.left * zoom_factor + offset_x, placing_rect.top * zoom_factor + offset_y))
        
        menu.draw(screen)
        
        current_layer_img = FONT.render("couche: " + str(current_layer), True, (0, 100, 100))
        screen.blit(current_layer_img, (SCREEN_WIDTH - 100, 10))
        help_img = FONT.render("aide: h", True, (0, 100, 100))
        screen.blit(help_img, (SCREEN_WIDTH - 100, 42))

        if show_help:
            draw_help(screen)

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


def add_tile_to_map(TILE_MAP, key, coords, zoom_factor=1):
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
    else:
        return VIDE

def draw_help(screen: pygame.Surface):
    screen.blit(HELP_BACKGROUND, (0, 0))
    text = [
        "sauver: q",
        "montrer/cacher l'aide: h",
        "quitter: esc",
        "monter/descendre d'une couche: flèches haut/bas",
        "défaire: ctrl+z",
        "reset zoom: z",
        "remplir rectangle: shift gauche + déplacer souris puis click droit",
        "gomme: e",
        "choisir tuile: click gauche sur la tuile dans la barre de gauche",
        "déplacer: click gauche sur la map + déplacer souris",
        "descendre/monter dans la barre de gauche: molette de la souris",
        "placer tuile: click droit",
        "zoomer/dézoomer: molette de la souris",
        "choisir tuile de la map: click milieu",
    ]
    text_imgs = []
    for line in text:
        text_imgs.append(FONT.render(line, True, (0, 200, 200)))
    for y, img in enumerate(text_imgs):
        screen.blit(img, (20, 20 + y * 40))

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

        self.offset_y = 50
        self.vide_color = (100, 100, 100)
        self.rect = self.menu_image.get_rect()
        self.rect.topleft = (0, self.offset_y)
        self.y_scroll = self.offset_y * 2
        self.scroll_speed = TILE_SIZE
    
    def draw(self, screen: pygame.Surface):
        screen.blit(self.edit_image, (0, 0))
        screen.blit(self.export_image, (70, 0))
        screen.blit(self.zoom_image, (150, 0))

        offset_x = 0
        y = self.y_scroll
        if self.visible:
            screen.blit(self.menu_image, (0, self.offset_y))
            self.collisionRects = []
            for key in self.collisionList:
                img: pygame.Surface = self.collisionList[key]
                pos = (offset_x, self.offset_y + y - img.get_height())
                if self.offset_y < pos[1] < SCREEN_HEIGHT:
                    if key == VIDE:
                        pygame.draw.rect(screen, self.vide_color, pygame.rect.Rect(pos, (TILE_SIZE, TILE_SIZE)))
                    rect = screen.blit(img, pos)
                    self.collisionRects.append({"image": img, "rect": rect, "key": key})
                
                if offset_x + TILE_SIZE < self.menu_image.get_width():
                    offset_x += TILE_SIZE
                else:
                    y += TILE_SIZE
                    offset_x = 0

            if self.dragging != -1:
                if self.dragging == VIDE:
                    pygame.draw.rect(screen, self.vide_color, pygame.rect.Rect(pygame.mouse.get_pos(), (TILE_SIZE, TILE_SIZE)))
                screen.blit(self.collisionList[self.dragging], pygame.mouse.get_pos())
            

def load_map(file_name):
    if os.path.isfile(file_name):
        with open(file_name, "rb") as f:
            TILE_MAP = pickle.load(f)
    else:
        TILE_MAP = [[[VIDE for _ in range(WIDTH_MAP // TILE_SIZE)] for _ in range(HEIGHT_MAP // TILE_SIZE)] for _ in range(NUM_LAYERS)]
    return TILE_MAP

def save_map(file_name, TILE_MAP, gamemap=True):
    tile_map = TILE_MAP
    if gamemap:
        tile_map = [[list(map(appliquer_attributs, row)) for row in layer] for layer in TILE_MAP]
    with open(file_name, "wb") as f:
        pickle.dump(tile_map, f)

def appliquer_attributs(tile_name: str):
    if tile_name in attributs:
        return attributs[tile_name]
    else:
        sep = tile_name.find("::")
        if sep == -1:
            print("Tuile non trouvée: " + tile_name)
            return []
        start = tile_name[:sep]
        if start in tile_maps:
            end = tile_name[sep + 2:]
            sep = end.find("::")
            atlas_num = end[:sep]
            pos = end[sep + 2:]
            sep = pos.find(";")
            return tile_maps[start]["attributs"][int(atlas_num)][int(pos[sep + 1:])][int(pos[:sep])]
        else:
            print("Tuile non trouvée (trouvé ::): " + tile_name)
            return []


def save_map_image(TILE_MAP, images):
    map_surface.fill((255, 255, 255))
    for layer in TILE_MAP:
        for y, row in enumerate(layer):
            for x, tile in enumerate(row):
                map_surface.blit(images[tile], (x * TILE_SIZE, y * TILE_SIZE))

def dialogue_quitter(TILE_MAP, map_sauvegarde, images):
    pygame.quit()
    if not map_sauvegarde:
        print("\n\n")
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