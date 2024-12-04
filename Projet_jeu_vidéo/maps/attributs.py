from pygame.math import Vector2
import pygame, os
from math import floor

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
    # tuile_a_remplir: la position d'une tuile qui va etre remplie avec remplir_avec. ex: Vector2(x, y) où x et y sont les coordonées de la tuile (en nombre de tuiles, commencant a 0)
    # vous pouvez mettre autant de tuile_a_remplir que vous voulez, mais n'oubliez pas les virgules entre chaque!

    tile_maps["Grass.png"] = {"tile_size": 16, "attributs": [create_tile_atlas(0, 0, 11, 7)]}
    tile_maps["Hills.png"] = {"tile_size": 16, "attributs": [create_tile_atlas(0, 0, 4, 4, [], [MUR], [Vector2(3, i) for i in range(4)], [Vector2(i, 2) for i in range(3)], [Vector2(i, 3) for i in range(3)])]}
    tile_maps["Water.png"] = {"tile_size": 16, "attributs": [create_tile_atlas(0, 0, 5, 3, [MUR])]}
    tile_maps["chicken_walk.png"] = {"tile_size": 32, "attributs": [create_tile_atlas(0, 1, 1, 1)]}

    # animations
    # pour rajouter une tuile animée:
    # écrir: animations["nomDuFichierImage"] = {"speed": vitesseAnimation, "tiles": [nomDuFichierImagePourFrame1, nomDuFichierImagePourFrame2, etc]}
    # remplacer nomDuFichierImage par le nom de l'image dans le repertoire tilemaps ou collisions qui sera utilisée comme base et qui sera la tuile a placer dans l'éditeur
    # si le fichier est dans tilemaps, alors ecrire nomDuFichierImage::0::tuileX;tuileY a la place de nomDuFichierImage, où tuileX est la coordonnée sur l'axe des x de la tuile dans la tilemap, et tuileY est la meme chose sur l'axe des y
    # remplacer vitesseAnimation par la vitesse de l'animation (combien de fois l'animation va jouer en 1 seconde)
    # remplacer nomDuFichierImagePourFrameN par le nom du fichier image dans collisions qui sera affichée comme la Nieme frame de l'animation
    # si nomDuFichierImagePourFrameN se trouve dans tilemaps alors écrire:
    # [*create_animation("nomDuFichierImagePourFrames::0", Vector2(frameX, frameY))]
    # a la place de nomDuFichierImagePourFrame1
    # puis remplacer nomDuFichierImagePourFrames par le nom du fichier image dans tilemaps
    # remplacer frameX et frameY par les coordonnées de la tuile dans la tilemap
    animations["Grass.png::0::0;0"] = {"speed": 0.5, "tiles": [*create_animation("Grass.png::0", [Vector2(i, 0) for i in range(3)])]}
    animations["Water.png::0::2;0"] = {"speed": 1, "tiles": [*create_animation("Water.png::0", [Vector2(i, 0) for i in range(2, 5)])]}
    
    groups["Grass.png"] = create_group("Grass.png", 0, 0, 0, 3, 3)

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

WIDTH_FACE = 150.0
HEIGHT_FACE = 150.0

# !!!!! NE PAS MODIFIER LE RESTE !!!!!
# -----------------------------------------------------------------------------------------------------------------------
GAME_SCREEN_WIDTH *= TILE_SIZE
GAME_SCREEN_HEIGHT *= TILE_SIZE
WIDTH_MAP *= GAME_SCREEN_WIDTH
HEIGHT_MAP *= GAME_SCREEN_HEIGHT

attributs = {}
tile_maps = {}
animations = {}
groups = {}

def create_tile_atlas(left: int, top: int, size_x: int, size_y: int, default: list = [], fill_with: list = [], *args: Vector2 | list[Vector2]):
    tile_atlas = [[default.copy() for _ in range(size_x)] for _ in range(size_y)]
    for arg in args:
        if type(arg) is list:
            for v in arg:
                tile_atlas[int(v.y)][int(v.x)] = fill_with.copy()
        else:
            tile_atlas[int(arg.y)][int(arg.x)] = fill_with.copy()
    return tile_atlas

def create_animation(name: str, *args: Vector2 | list[Vector2]):
    anim = []
    for arg in args:
        if type(arg) is list:
            for v in arg:
                anim.append(name + "::" + str(int(v.x)) + ";" + str(int(v.y)))
        else:
            anim.append(name + "::" + str(int(arg.x)) + ";" + str(int(arg.y)))
    return anim

def create_group(name: str, index: int, start_x: int, start_y: int, width: int, height: int):
    start = name + "::" + str(index) + "::"
    return [[start + str(x) + ";" + str(y) for x in range(start_x, width)] for y in range(start_y, height)]

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

def draw_tile_map(dt, screen: pygame.Surface, screen_width, screen_height, TILE_MAP, images, animations, zoom_factor=1, offset_x=0, offset_y=0):
    scaled_tile_size = TILE_SIZE * zoom_factor
    scaled_images = {}
    if zoom_factor != 1:
        scaled_images = {}
    else:
        scaled_images = images
    rangeStartY = max(0, floor((-offset_y - scaled_tile_size) / scaled_tile_size))
    rangeEndY = min(len(TILE_MAP), floor((-offset_y + screen_height + scaled_tile_size) / scaled_tile_size))
    for y, row in enumerate(TILE_MAP[rangeStartY:rangeEndY]):
        rangeStartX = max(0, floor((-offset_x - scaled_tile_size) / scaled_tile_size))
        rangeEndX = min(len(row), floor((-offset_x + screen_width + scaled_tile_size) / scaled_tile_size))
        for x, tile_dict in enumerate(row[rangeStartX:rangeEndX]):
            screen_coords = ((rangeStartX + x) * scaled_tile_size + offset_x, (rangeStartY + y) * scaled_tile_size + offset_y)
            tile = tile_dict["nom"]
            if not tile in images:
                print("Il manque le fichier image: " + tile)
                continue
            if zoom_factor != 1 and not tile in scaled_images:
                scaled_images[tile] = pygame.transform.scale(images[tile], (scaled_tile_size, scaled_tile_size))
            if tile in animations:
                if not "time" in tile_dict["special"]:
                    tile_dict["special"]["time"] = 0.0
                try:
                    tile_dict["special"]["time"] = float(tile_dict["special"]["time"])
                except ValueError:
                    print("Valeur doit etre un nombre!")
                    tile_dict["special"]["time"] = 0.0
                tile_dict["special"]["time"] += dt * animations[tile]["speed"]
                while tile_dict["special"]["time"] > 1.0:
                    tile_dict["special"]["time"] -= 1.0
                anim_tile = animations[tile]["tiles"][min(len(animations[tile]["tiles"]) - 1, floor(pygame.math.lerp(0, len(animations[tile]["tiles"]), tile_dict["special"]["time"])))]
                if zoom_factor != 1 and not anim_tile in scaled_images:
                    scaled_images[anim_tile] = pygame.transform.scale(images[anim_tile], (scaled_tile_size, scaled_tile_size))
                tile_img = scaled_images[anim_tile]
            else:
                tile_img = scaled_images[tile]
            screen.blit(tile_img, screen_coords)

main()