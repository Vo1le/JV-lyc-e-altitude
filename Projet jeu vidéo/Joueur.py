import pygame as py
from inputs import inputs

class Joueur(py.sprite.Sprite):
    def __init__(self, x,y):
        py.sprite.Sprite.__init__(self)
        self.image = py.image.load("pouce.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vitesse = py.math.Vector2(0, 0)
        self.vitesseMax = 250.0
        self.acceleration = 500.0
        self.friction = 750.0

    def update(self, dt):
        touchesAppuyes = py.key.get_pressed()
        if self.verifierInput("haut", touchesAppuyes):
            if self.vitesse.y > 0:
                self.vitesse.y = max(self.vitesse.y - self.friction * dt, 0)
            else:
                self.vitesse.y = max(self.vitesse.y - self.acceleration * dt, -self.vitesseMax)
        elif self.verifierInput("bas", touchesAppuyes):
            if self.vitesse.y < 0:
                self.vitesse.y = max(self.vitesse.y + self.friction * dt, 0)
            else:
                self.vitesse.y = min(self.vitesse.y + self.acceleration * dt, self.vitesseMax)
        else:
            self.vitesse.move_towards_ip(py.math.Vector2(self.vitesse.x, 0), self.friction * dt)
        if self.verifierInput("gauche", touchesAppuyes):
            if self.vitesse.x > 0:
                self.vitesse.x = max(self.vitesse.x - self.friction * dt, 0)
            else:
                self.vitesse.x = max(self.vitesse.x - self.acceleration * dt, -self.vitesseMax)
        elif self.verifierInput("droite", touchesAppuyes):
            if self.vitesse.x < 0:
                self.vitesse.x = max(self.vitesse.x - self.friction * dt, 0)
            else:
                self.vitesse.x = min(self.vitesse.x + self.acceleration * dt, self.vitesseMax)
        else:
            self.vitesse.move_towards_ip(py.math.Vector2(0, self.vitesse.y), self.friction * dt)
        
        self.avance(self.vitesse, dt)
    
    def movejoueur(self, x, y):
        self.rect.x = x
        self.rect.y = y
    
    def avance(self, direction, dt):
        if direction.x != 0.0 and direction.y != 0.0:
            longueur = direction.length()
            direction.scale_to_length(min(longueur, self.vitesseMax))
            self.rect.move_ip(direction * dt)
            direction.scale_to_length(longueur)
        else:
            self.rect.move_ip(direction * dt)
        
    def verifierInput(self, action, touchesAppuyes):
        for touche in inputs[action]:
            if touchesAppuyes[touche]:
                return True
        return False