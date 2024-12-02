import pygame as py
from inputs import verifierInput
import math
from maps.attributs import GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT

RACINEDE2 = math.sqrt(2)


class Joueur(py.sprite.Sprite):
    def __init__(self, x, y):
        self.rect = py.Rect(0, 0, 50, 100)
        self.rect.center = (x, y)

        py.sprite.Sprite.__init__(self)
        self.image = py.transform.scale(py.image.load("Images/Joueur-idle-1.png").convert_alpha(), (self.rect.width, self.rect.height))
        self.vitesse = py.math.Vector2(0, 0)
        self.vitesseMax = 250.0
        self.acceleration = 1000.0
        self.friction = 2000.0

        self.animations = {
            "idle": {"frames": [py.transform.scale(py.image.load("Images/Joueur-idle-" + str(i) + ".png").convert_alpha(), (self.rect.width, self.rect.height)) for i in range(1, 2)], "max": 1, "speed": 0},
            "marcheBas": {"frames": [py.transform.scale(py.image.load("Images/Joueur-marche-" + str(i) + ".png").convert_alpha(), (self.rect.width, self.rect.height)) for i in range(1, 3)], "max": 2, "speed": 3}
        }
        self.animation = "idle"
        self.frameCourante = 0.0

    def update(self, dt, mapjeu, zoom: float):
        touchesAppuyes = py.key.get_pressed()
        input = py.math.Vector2(verifierInput(touchesAppuyes, "droite") - verifierInput(touchesAppuyes, "gauche"), verifierInput(touchesAppuyes, "bas") - verifierInput(touchesAppuyes, "haut"))
        if input.y:
            if self.vitesse.y != 0.0 and sign(self.vitesse.y) != input.y:
                self.vitesse.y = clamp(self.vitesse.y + self.friction * dt * input.y, 0, self.vitesse.y)
            else:
                self.vitesse.y = py.math.clamp(self.vitesse.y + self.acceleration * dt * input.y, -self.vitesseMax, self.vitesseMax)
        else:
            self.vitesse.move_towards_ip(py.math.Vector2(self.vitesse.x, 0), self.friction * dt)
        
        if input.x:
            if self.vitesse.x != 0.0 and sign(self.vitesse.x) != input.x:
                self.vitesse.x = clamp(self.vitesse.x + self.friction * dt * input.x, 0, self.vitesse.x)
            else:
                self.vitesse.x = py.math.clamp(self.vitesse.x + self.acceleration * dt * input.x, -self.vitesseMax, self.vitesseMax)
        else:
            self.vitesse.move_towards_ip(py.math.Vector2(0, self.vitesse.y), self.friction * dt)
        
        if input.x != 0.0 and input.y != 0.0 and self.vitesse.length() != 0.0:
            self.vitesse.scale_to_length(self.vitesse.length() - self.acceleration * dt / RACINEDE2)
        
        
        location = self.avance(dt, mapjeu)

        self.updateAnimations(dt, input)

        if not input:
            return zoom, location
        return 1.0, location

    def movejoueur(self, x, y):
        self.rect.x = x
        self.rect.y = y
    
    def avance(self, dt, mapjeu):
        if self.vitesse.length() != 0:
            dir = self.vitesse.normalize()
            self.avance_une_direction(dt, mapjeu, py.Vector2(dir.x, 0))
            self.avance_une_direction(dt, mapjeu, py.Vector2(0, dir.y))
            porte = py.sprite.spritecollideany(self, mapjeu.portes)
            if porte:
                return {"destination": porte.destination, "position": porte.position}
        return -1
            
    def avance_une_direction(self, dt, mapjeu, dir):
        rect_avant = self.rect.copy()
        self.rect.move_ip(dir * min(self.vitesse.length(), self.vitesseMax) * dt)
        collision = py.sprite.spritecollideany(self, mapjeu.collisions)
        if collision:
            if dir.x:
                self.vitesse.x = 0.0
            else:
                self.vitesse.y = 0.0
            self.rect = rect_avant.copy()

    def updateAnimations(self, dt, input):
        if input.y > 0:
            self.changeAnimation("marcheBas")
        else:
            self.changeAnimation("idle")
        self.frameCourante += dt * self.animations[self.animation]["speed"]
        if self.frameCourante >= self.animations[self.animation]["max"]:
            self.frameCourante = 0.0
        self.image = self.animations[self.animation]["frames"][math.floor(self.frameCourante)]
    
    def changeAnimation(self, anim: str):
        if anim != self.animation:
            self.animation = anim
            self.frameCourante = 0.0
    
    def draw(self, surface: py.Surface, p_zoom, positionOverride=-1):
        if positionOverride == -1:
            positionOverride = self.rect.center
        zoom = round(p_zoom, 2)
        positionJoueur = get_joueur_position_cell(positionOverride)
        positionJoueur = (positionJoueur[0] + GAME_SCREEN_WIDTH / 2, positionJoueur[1] + GAME_SCREEN_HEIGHT / 2)
        topleft = self.rect.topleft
        if zoom == 1:
            pos = (topleft[0] - positionJoueur[0] + GAME_SCREEN_WIDTH / 2, topleft[1] - positionJoueur[1] + GAME_SCREEN_HEIGHT / 2)
            surface.blit(self.image, pos)
        else:
            pos = (math.floor((topleft[0] - positionJoueur[0]) * zoom + GAME_SCREEN_WIDTH / 2), math.floor((topleft[1] - positionJoueur[1]) * zoom + GAME_SCREEN_HEIGHT / 2))
            surface.blit(py.transform.scale(self.image, (math.ceil(self.rect.width * zoom), math.ceil(self.rect.height * zoom))), pos)
            
    
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

def get_joueur_position_cell(positionJoueurGlobal):
    return (math.floor(positionJoueurGlobal[0] / GAME_SCREEN_WIDTH) * GAME_SCREEN_WIDTH, math.floor(positionJoueurGlobal[1] / GAME_SCREEN_HEIGHT) * GAME_SCREEN_HEIGHT)