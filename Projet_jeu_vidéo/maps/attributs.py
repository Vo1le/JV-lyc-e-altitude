from pygame.math import Vector2
import pygame, os

# Noms des attributs
MUR = 1

def main():
    # Attributs pour chaque type de tuile

    # Pour rajouter un type de tuile:
    # écrire: attributs["nom_du_fichier_dans_/collisions"] = [attribut_1, attribut_2, etc]

    attributs["wall.png"] = [MUR]
    attributs["heart.png"] = []
    attributs["vide.png"] = []

    # Attributs pour chaque tilemap

    # Pour rajouter une tilemap:
    # copier/coller la ligne si dessous:
    #tile_maps["nom"] = {"tile_size": taille, "attributs": [create_tile_atlas(colonnes, rangées)]}
    # enlever le # au debut
    # remplacer nom avec le nom du fichier dans /tilemaps
    # remplacer taille avec la taille d'une tuile dans le fichier tilemap
    # remplacer colonnes avec le nombre de colonnes de tuiles de l'image a prendre
    # remplacer rangées avec le nombre de rangées de tuiles de l'image a prendre. avec colonnes, ceci definit quelles tuiles il faut prendre
    # ceci va définir que chaque tuile est "vide" (n'a pas de collision ni d'attributs particuliers)
    # parametres optionnels pour create_tile_atlas:
    # create_tile_atlas(colonnes, rangées, defaut, remplir_avec, tuile_a_remplir1, tuile_a_remplir2, etc)
    # defaut: les attributs que chaque tuile va avoir. ex: [MUR] ex2: []
    # remplir_avec: les attributs que les tuiles définies avec tuile_a_remplir vont avoir. ex: [MUR]
    # tuile_a_remplir: la position d'une tuile qui va etre remplie avec remplir_avec. ex: Vector2(x, y) ou x et y sont les coordonées de la tuile (en nombre de tuiles, commencant a 0)
    # vous pouvez mettre autant de tuile_a_remplir que vous voulez, mais n'oubliez pas les virgules entre chaque!

    tile_maps["Grass.png"] = {"tile_size": 16, "attributs": [create_tile_atlas(11, 7, [], ["Grass.png"], Vector2(0, 0))]}
    tile_maps["Hills.png"] = {"tile_size": 16, "attributs": [create_tile_atlas(4, 4, [], [MUR], [Vector2(3, i) for i in range(4)], [Vector2(i, 2) for i in range(3)], [Vector2(i, 3) for i in range(3)])]}

    # animations:
    animations["Grass.png"] = {"tile_size": 16, "tiles": create_animation([Vector2(0, i) for i in range(3)])}

# Paramétres de la map:

# nom du répertoire dans lequel se trouve les images
FOLDER_PATH = "collisions"
# nom du répertoire dans lequel se trouve les tilemaps
TILE_MAP_FOLDER_NAME = "tilemaps"
# nom du répertoire dans lequel sauver la map
TILE_MAP_SAVE_FOLDER_NAME = "monde"
# nom du fichier dans lequel sauver la map qui sera utilisée par le jeu
TILE_MAP_FILE_NAME = "map.txt"
# nom du fichier dans lequel sauver la map qui sera utilisée par l'editeur de niveau (et le jeu pour l'affichage)
TILE_MAP_RELOADABLE_FILE_NAME = "map_reload.txt"
# nom du fichier dans lequel sauver l'image de la map qui sera utilisée par le jeu
TILE_MAP_IMAGE_FILE_NAME = "map.png"

# case par defaut
VIDE = "vide.png"

# nombre de couches
NUM_LAYERS = 5
# nombre de couches au dessus du joueur (ces couches seront a la fin des couches. ex: si il y a 5 couches et 2 couches au dessus du joueur, alors les couches 0, 1, 2 seront sous le joueur)
NUM_LAYERS_ABOVE_PLAYER = 2

# taille d'une tuile (en pixels)
TILE_SIZE = 64

# Taille d'un écran (en tuiles)
GAME_SCREEN_WIDTH = 25
GAME_SCREEN_HEIGHT = 14

# Taille de la map (en écrans)
WIDTH_MAP = 3
HEIGHT_MAP = 2

# Ne pas modifier le reste
GAME_SCREEN_WIDTH *= TILE_SIZE
GAME_SCREEN_HEIGHT *= TILE_SIZE
WIDTH_MAP *= GAME_SCREEN_WIDTH
HEIGHT_MAP *= GAME_SCREEN_HEIGHT

attributs = {}
tile_maps = {}
animations = {}

def create_tile_atlas(size_x: int, size_y: int, default: list = [], fill_with: list = [], *args: Vector2 | list[Vector2]):
    tile_atlas = [[default.copy() for _ in range(size_x)] for _ in range(size_y)]
    for arg in args:
        if type(arg) is list:
            for v in arg:
                tile_atlas[int(v.y)][int(v.x)] = fill_with.copy()
        else:
            tile_atlas[int(arg.y)][int(arg.x)] = fill_with.copy()
    return tile_atlas

def create_animation(*args: Vector2 | list[Vector2]):
    anim = []
    for arg in args:
        if type(arg) is list:
            anim.extend(arg)
        else:
            anim.append(arg)
    return anim


class MapSize:
    width = WIDTH_MAP
    height = HEIGHT_MAP
    @classmethod
    def setWidth(cls, val):
        cls.width = val * GAME_SCREEN_WIDTH
    @classmethod
    def setHeight(cls, val):
        cls.height = val * GAME_SCREEN_HEIGHT
    @classmethod
    def getWidth(cls):
        return int(cls.width / GAME_SCREEN_WIDTH)
    @classmethod
    def getHeight(cls):
        return int(cls.height / GAME_SCREEN_HEIGHT)

def setup_images(folder_path, tile_map_folder_name):
    images = {}
    for file in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file)):
            images[file] = pygame.transform.scale(pygame.image.load(os.path.join(folder_path, file)), (TILE_SIZE, TILE_SIZE))
    for file in os.listdir(tile_map_folder_name):
        if os.path.isfile(os.path.join(tile_map_folder_name, file)):
            if file in tile_maps.keys():
                img = pygame.image.load(os.path.join(tile_map_folder_name, file)).convert_alpha()
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
    return images

def draw_tile_map(screen: pygame.Surface, screen_width, screen_height, TILE_MAP, images, zoom_factor=1, offset_x=0, offset_y=0):
    scaled_tile_size = TILE_SIZE * zoom_factor
    scaled_images = {}
    if zoom_factor != 1:
        for img in images:
            scaled_images[img] = pygame.transform.scale(images[img], (scaled_tile_size, scaled_tile_size))
    else:
        scaled_images = images
    for y, row in enumerate(TILE_MAP):
        for x, tile_dict in enumerate(row):
            tile = tile_dict["nom"]
            if not tile in images:
                print("Il manque le fichier image: " + tile)
                continue
            screen_coords = (x * scaled_tile_size + offset_x, y * scaled_tile_size + offset_y)
            if -scaled_tile_size < screen_coords[0] < screen_width and -scaled_tile_size < screen_coords[1] < screen_height:
                tile_img = scaled_images[tile]
                screen.blit(tile_img, screen_coords)

main()