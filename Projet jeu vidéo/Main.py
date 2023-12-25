# // librairie ici pygame = py pour gagner du temps//
import pygame as py
from pygame.locals import * 

# // les init de pygame //
py.init()

# // Set up de l'écran //
ecran = py.display.set_mode(size=(0, 0))
color = (255,255,255)
ecran.fill(color)

# // Set up du framerate //
FPS = 30
fpsClock = py.time.Clock()

# // imports divers //
from inputs import inputs
import sys

# // Toutes les classes sont si dessous // 
from Joueur import Joueur

def main():
    # // Espace dédié au diverses variables liée au fonctionnement du code //
    continuer = True

    # // ajout des sprites dans le jeu //
    joueurdep = py.sprite.Group()
    joueur = Joueur(100, 100) 
    joueurdep.add(joueur)

    # // la boucle pour les evenements et autres //
    while continuer: 

        # // Les évenement (input joueur) sont ici //

        for event in py.event.get():
            if event.type == py.KEYDOWN:
                for key in inputs["quit"]:
                    if event.key == key:
                        py.quit()
                        sys.exit()
        
        # // mise a niveaux des objets du monde (joueur, pnj, ...)
        dt = fpsClock.get_time() / 1000
        joueurdep.update(dt)

        # // Affichage //
        Affichage(joueurdep)

        fpsClock.tick(FPS)

# // fonction diverses //

def Affichage(joueurdep):
    joueurdep.draw(ecran)
    py.display.update()

if __name__ == "__main__":
    main()
