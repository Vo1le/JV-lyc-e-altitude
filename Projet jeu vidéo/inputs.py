import pygame
from pygame.locals import K_RIGHT, K_LEFT, K_DOWN, K_UP, K_ESCAPE, K_q, K_d, K_z, K_s

inputs = {
    "bas": [K_DOWN, K_s],
    "haut": [K_UP, K_z],
    "gauche": [K_LEFT, K_q],
    "droite": [K_RIGHT, K_d],
    "quit": [K_ESCAPE],
}