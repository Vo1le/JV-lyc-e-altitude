# // librairie ici pygame = py pour gagner du temps//
import pygame as py
from pygame.locals import * 
import sys

# // les init de pygame //
py.init()

# // Set up de l'écran //
ecran = py.display.set_mode(size=(0, 0))
color = (255,255,255)
ecran.fill(color)
width = py.Surface.get_width(ecran)
height = py.Surface.get_height(ecran)


# // Set up du framerate //
FPS = 60
fpsClock = py.time.Clock()

# // imports divers //
from inputs import verifierInputKey

# // Toutes les classes sont si dessous // 
from Joueur import Joueur
from Environement import *

def main():
    # // Espace dédié au diverses variables liée au fonctionnement du code //
    continuer = True

    # // ajout des sprites dans le jeu //
    joueurdep = extendedGroup()
    joueur = Joueur(0, 0)
    joueurdep.add(joueur)

    Environments = extendedGroup()
    mapjeu = Map(0, 0)
    Environments.add(mapjeu)

    zoom = 0.7
    
    # // la boucle pour les evenements et autres //
    while continuer: 

        # // Les évenement (input joueur) sont ici //

        for event in py.event.get():
            if event.type == py.KEYDOWN:
                if verifierInputKey(event.key, "quit"):
                    py.quit()
                    sys.exit()
                elif verifierInputKey(event.key, "zoom"):
                    zoom += 0.2
                elif verifierInputKey(event.key, "dezoom"):
                    zoom -= 0.2
                # un zoom négatif casse tout
                zoom = py.math.clamp(zoom, 0.05, 10)
        

        # // mise a niveaux des objets du monde (joueur, pnj, ...)
        dt = fpsClock.get_time() / 1000
        joueurdep.update(dt, mapjeu)
        # camera()

        # // Affichage //
        Affichage(joueurdep, Environments, joueur.rect.topleft, zoom)

        fpsClock.tick(FPS)

# // fonction diverses //

def Affichage(joueurdep, Environments, positionJoueur, zoom):
    ecran.fill(color)
    
    Environments.draw(ecran, positionJoueur, zoom)
    joueurdep.draw(ecran, positionJoueur, zoom)
    py.display.update()

if __name__ == "__main__":
    main()

