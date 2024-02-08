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
import sys

# // Toutes les classes sont si dessous // 
from Joueur import Joueur
from Environement import*

def main():
    # // Espace dédié au diverses variables liée au fonctionnement du code //
    continuer = True

    # // ajout des sprites dans le jeu //
    joueurdep = py.sprite.Group()
    joueur = Joueur(width//2,height//2)
    joueurdep.add(joueur)

    Environments = py.sprite.Group()
    petitcube = Cube(1000, 1000) 
    Environments.add(petitcube)


    def camera():
        camera_x = width//2 - joueur.rect.centerx
        camera_y = height//2 - joueur.rect.centery
        for object in Environments:
                object.rect.x +=  camera_x
                object.rect.y += camera_y

        joueur.rect.x +=  camera_x
        joueur.rect.y += camera_y
        
    
    # // la boucle pour les evenements et autres //
    while continuer: 

        # // Les évenement (input joueur) sont ici //

        for event in py.event.get():
            if event.type == py.KEYDOWN:
                if verifierInputKey(event.key, "quit"):
                    py.quit()
                    sys.exit()
        
        

        # // mise a niveaux des objets du monde (joueur, pnj, ...)
        dt = fpsClock.get_time() / 1000
        joueurdep.update(dt)
        camera()

        # // Affichage //
        Affichage(joueurdep,Environments)

        fpsClock.tick(FPS)

# // fonction diverses //

def Affichage(joueurdep,Environments):
    ecran.fill(color)
    joueurdep.draw(ecran)
    Environments.draw(ecran)
    
    py.display.flip()
    py.display.update()

if __name__ == "__main__":
    main()

