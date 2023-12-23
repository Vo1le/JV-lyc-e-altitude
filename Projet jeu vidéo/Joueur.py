import pygame as py
from inputs import inputs

class Joueur(py.sprite.Sprite):
    def __init__(self, x,y):
        py.sprite.Sprite.__init__(self)
        self.image = py.image.load("pouce.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vitesse = py.math.Vector2(100, 100)

    def update(self, dt):
        touchesAppuyes = py.key.get_pressed()
        if self.verifierInput("haut", touchesAppuyes):
            self.avance(0, -self.vitesse.y * dt)
        if self.verifierInput("bas", touchesAppuyes):
            self.avance(0, self.vitesse.y * dt)
        if self.verifierInput("gauche", touchesAppuyes):
            self.avance(-self.vitesse.x * dt, 0)
        if self.verifierInput("droite", touchesAppuyes):
            self.avance(self.vitesse.x * dt, 0)
    
    def movejoueur(self, x, y):
        self.rect.x = x
        self.rect.y = y
    
    def avance(self, x, y):
        self.rect.move_ip([x,y])
    
    def verifierInput(self, action, touchesAppuyes):
        for touche in inputs[action]:
            if touchesAppuyes[touche]:
                return True
        return False