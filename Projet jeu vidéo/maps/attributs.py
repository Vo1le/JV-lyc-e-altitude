# Noms des attributs
MUR = 1

# Attributs pour chaque type de tuile
# Pour rajouter un type de tuile:
# Ajouter une ligne a l'interieur des {}
# écrire: "nom_du_fichier_dans_/collisions": [attribut_1, attribut_2, etc]
attributs = {
    "wall.png": [MUR],
    "heart.png": [],
    "vide.png": [],
}

# Paramétres de la map:

# case par defaut
VIDE = "vide.png"

# taille d'une tuile
TILE_SIZE = 60

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