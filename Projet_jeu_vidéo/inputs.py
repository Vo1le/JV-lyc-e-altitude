from pygame.locals import *

inputs = {
    "bas": [K_DOWN, K_s],
    "haut": [K_UP, K_z],
    "gauche": [K_LEFT, K_q],
    "droite": [K_RIGHT, K_d],
    "quit": [K_ESCAPE],
    "zoom": [K_x],
    "dezoom": [K_c],
    "interagir": [K_RETURN]
}

def verifierInput(touchesAppuyes, action):
    for touche in inputs[action]:
        if touchesAppuyes[touche]:
            return True
    return False

def verifierInputKey(key, action):
    for touche in inputs[action]:
        if key == touche:
            return True
    return False

def verifierInputList(l: list, action):
    for touche in inputs[action]:
        if touche in l:
            return True
    return False