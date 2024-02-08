import pygame as py
import math

class Cube(py.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = py.Surface((100, 100))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
    def moves(self,camera_x, camera_y):
        self.rect.move(camera_x, camera_y)

# classe qui hérite de py.sprite.Group qui est la classe qui permet l'affichage et l'update d'un groupe de sprites
class extendedGroup(py.sprite.Group):
    # draw est une méthode de py.sprite.Group que je remplace par la mienne
    # elle prend comme argument self, la surface sur laquelle afficher, la position du joueur pour pouvoir décaler les sprites et le zoom a appliquer aux sprites
    def draw(self, surface: py.Surface, positionJoueur, p_zoom):
        # self.sprites est la liste qui contient tout les sprites de ce groupe
        sprites = self.sprites()
        # surface_blit est une réference a la fonction d'affichage, ce qui veut dire que surface_blit() est l'équivalent de surface.blit()
        surface_blit = surface.blit
        windowSize = py.display.get_window_size()
        # je round le zoom pour éviter les erreurs de précision
        zoom = round(p_zoom, 2)
        # je fait ce teste pour ne pas devoir scaler si il n'y en a pas besoin
        if zoom == 1:
            for spr in sprites:
                # spr est une instance d'une classe qui hérite de py.sprite.Sprite qui appartient a ce groupe
                topleft = spr.rect.topleft
                # pos contient la où doit ètre affiché l'objet en prenant le joueur comme centre
                pos = (topleft[0] - positionJoueur[0] + windowSize[0] / 2, topleft[1] - positionJoueur[1] + windowSize[1] / 2)
                # verifier si le sprite est sur l'écran
                if -spr.rect.width < pos[0] < windowSize[0] and -spr.rect.height < pos[1] < windowSize[1]:
                    self.spritedict[spr] = surface_blit(spr.image, pos)
        else:
            for spr in sprites:
                topleft = spr.rect.topleft
                pos = (math.floor((topleft[0] - positionJoueur[0]) * zoom + windowSize[0] / 2), math.floor((topleft[1] - positionJoueur[1]) * zoom + windowSize[1] / 2))
                if -spr.rect.width < pos[0] < windowSize[0] and -spr.rect.height < pos[1] < windowSize[1]:
                    self.spritedict[spr] = surface_blit(py.transform.scale(spr.image, (math.ceil(spr.rect.width * zoom), math.ceil(spr.rect.height * zoom))), pos)
        self.lostsprites = []
