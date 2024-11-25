# // librairie ici pygame = py pour gagner du temps//
import pygame as py
from pygame.locals import * 
import sys
from maps.attributs import GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT

# // les init de pygame //
py.init()

# // Set up de l'écran //
ecran = py.display.set_mode(size=(GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT), flags=FULLSCREEN|SCALED)
color = (255,255,255)
ecran.fill(color)


# // Set up du framerate //
FPS = 60
fpsClock = py.time.Clock()

# // imports divers //
from inputs import verifierInputKey

# // Toutes les classes sont si dessous // 
from Joueur import Joueur, get_joueur_position_cell
from Environement import *
from Transition import Transition

def main():
    # // Espace dédié au diverses variables liée au fonctionnement du code //
    continuer = True

    # // ajout des sprites dans le jeu //
    joueur = Joueur(25, 50)

    mapjeu = Map(0, 0)

    transitionEcran = Transition(GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT, end=0.3, transitionType="circle", playType="ping-pong")
    dernierePositionJoueur = joueur.rect.topleft

    zoom = 1
    
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
                zoom = py.math.clamp(zoom, 0.1, 1)
        

        # // mise a niveaux des objets du monde (joueur, pnj, ...)
        dt = fpsClock.get_time() / 1000
        if not transitionEcran.playing:
            joueurCellStart = get_joueur_position_cell(joueur.rect.center)
            positionJoueurStart = joueur.rect.center
            zoom = joueur.update(dt, mapjeu, zoom)
            if joueurCellStart != get_joueur_position_cell(joueur.rect.center):
                transitionEcran.play()
                dernierePositionJoueur = positionJoueurStart
        transitionEcran.update(dt)
        joueurCenter = joueur.rect.center
        if transitionEcran.playing and not transitionEcran.reverse:
            joueurCenter = dernierePositionJoueur
        # // Affichage //
        ecran.fill(color)

        for layer in range(NUM_LAYERS - NUM_LAYERS_ABOVE_PLAYER):
            mapjeu.draw(ecran, joueurCenter, zoom, layer)
        joueur.draw(ecran, zoom, joueurCenter)
        for layer in range(NUM_LAYERS - NUM_LAYERS_ABOVE_PLAYER, NUM_LAYERS):
            mapjeu.draw(ecran, joueurCenter, zoom, layer)

        transitionEcran.draw(ecran)

        py.display.update()

        fpsClock.tick(FPS)

# // fonction diverses //

if __name__ == "__main__":
    main()

