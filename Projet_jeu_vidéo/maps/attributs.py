from pygame.math import Vector2

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

    tile_maps["Grass.png"] = {"tile_size": 16, "attributs": [create_tile_atlas(11, 7)]}
    tile_maps["Hills.png"] = {"tile_size": 16, "attributs": [create_tile_atlas(4, 4, [], [MUR], [Vector2(3, i) for i in range(4)], [Vector2(i, 2) for i in range(3)], [Vector2(i, 3) for i in range(3)])]}

# Paramétres de la map:

# nom du répertoire dans lequel se trouve les images
FOLDER_PATH = "collisions"
# nom du répertoire dans lequel se trouve les tilemaps
TILE_MAP_FOLDER_NAME = "tilemaps"
# nom du répertoire dans lequel sauver la map
TILE_MAP_SAVE_FOLDER_NAME = "monde"
# nom du fichier dans lequel sauver la map qui sera utilisée par le jeu
TILE_MAP_FILE_NAME = "map.txt"
# nom du fichier dans lequel sauver la map qui sera utilisée par l'editeur de niveau
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

def create_tile_atlas(size_x: int, size_y: int, default: list = [], fill_with: list = [], *args):
    tile_atlas = [[default.copy() for _ in range(size_x)] for _ in range(size_y)]
    for arg in args:
        if type(arg) is list:
            for v in arg:
                tile_atlas[int(v.y)][int(v.x)] = fill_with.copy()
        else:
            tile_atlas[int(arg.y)][int(arg.x)] = fill_with.copy()
    return tile_atlas

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

main()