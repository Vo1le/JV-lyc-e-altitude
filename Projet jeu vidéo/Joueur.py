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
        input = py.math.Vector2(self.verifierInput("droite", touchesAppuyes) - self.verifierInput("gauche", touchesAppuyes), self.verifierInput("bas", touchesAppuyes) - self.verifierInput("haut", touchesAppuyes))
        if input.y:
            if self.vitesse.y != 0 and sign(self.vitesse.y) != input.y:
                self.vitesse.y = clamp(self.vitesse.y + self.friction * dt * input.y, 0, self.vitesse.y)
            else:
                self.vitesse.y = py.math.clamp(self.vitesse.y + self.acceleration * dt * input.y, -self.vitesseMax, self.vitesseMax)
        else:
            self.vitesse.move_towards_ip(py.math.Vector2(self.vitesse.x, 0), self.friction * dt)
        
        if input.x:
            if self.vitesse.x != 0 and sign(self.vitesse.x) != input.x:
                self.vitesse.x = clamp(self.vitesse.x + self.friction * dt * input.x, 0, self.vitesse.x)
            else:
                self.vitesse.x = py.math.clamp(self.vitesse.x + self.acceleration * dt * input.x, -self.vitesseMax, self.vitesseMax)
        else:
            self.vitesse.move_towards_ip(py.math.Vector2(0, self.vitesse.y), self.friction * dt)
        
        if input.x != 0 and input.y != 0:
            self.vitesse.scale_to_length(self.vitesse.length() - self.acceleration * dt / 1.4)
        
        self.avance(self.vitesse, dt)
    
    def movejoueur(self, x, y):
        self.rect.x = x
        self.rect.y = y
    
    def avance(self, direction, dt):
        if direction.length() != 0:
            self.rect.move_ip(direction.normalize() * min(direction.length(), self.vitesseMax) * dt)
    
    def verifierInput(self, action, touchesAppuyes):
        for touche in inputs[action]:
            if touchesAppuyes[touche]:
                return True
        return False

def clamp(n, p_min, p_max):
    if p_max > p_min:
        return min(max(n, p_min), p_max)
    else:
        return min(max(n, p_max), p_min)

def sign(n):
    if n < 0.0:
        return -1
    elif n > 0.0:
        return 1
    return 0