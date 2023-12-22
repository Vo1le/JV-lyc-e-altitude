# // librairie ici pygame = py pour gagner du temps//
import pygame as py
from pygame.locals import * 

# // les init de pygame //
py.init()

# // Set up de l'écran //
ecran = py.display.set_mode(size=(0, 0))
color = (255,255,255)
ecran.fill(color)

# // Espace dédié au diverses variables liée au fonctionnement du code //
continuer = True
noir = (255,255,255)

# // Toutes les classes sont si dessous // 
class joueur(py.sprite.Sprite):
    def __init__(self, x,y):
        py.sprite.Sprite.__init__(self)
        self.image = py.image.load("pouce.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    def movejoueur(self,x,y):
        self.rect.x = x
        self.rect.y = y
    def avancevertical(self, x, y):
        self.rect.move_ip([x,y])
    def avancehorizontal(self, x,y):
        self.rect.move_ip([x,y])
 
# // ajout des sprites dans le jeu //

joueurdep = py.sprite.Group()
joueur_ = joueur(100, 100) 
joueurdep.add(joueur_)

# // fonction deverses //
def controls():
    if py.key.get_pressed()[py.K_z]:
        joueur_.avancevertical(0,-1)
    if py.key.get_pressed()[py.K_s]:
        joueur_.avancevertical(0,1)
    if py.key.get_pressed()[py.K_q]:
        joueur_.avancehorizontal(-1,0)
    if py.key.get_pressed()[py.K_d]:
        joueur_.avancehorizontal(1,0)


# // la boucle pour les evenements et autres //
while continuer: 

    # // Les évenement (input joueur) sont ici //

    for event in py.event.get():
        if event.type == py.KEYDOWN:
            if event.key == py.K_ESCAPE:
                continuer = False

    controls()

    # // Affichage //
    joueurdep.update() 
    joueurdep.draw(ecran)
    py.display.update()


py.quit()

