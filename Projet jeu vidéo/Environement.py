import pygame as py

class Cube(py.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = py.Surface((100, 100))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
    def moves(self,camera_x, camera_y):
        self.rect.move(camera_x, camera_y)
