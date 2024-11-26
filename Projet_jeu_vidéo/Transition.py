import pygame
from typing import Literal

class Transition:
    def __init__(self, GAME_SCREEN_WIDTH: int, GAME_SCREEN_HEIGHT: int, end=0.5, transitionType:Literal["fade", "circle"]="fade", playType:Literal["forward", "reverse", "reverse-ping-pong", "ping-pong"]="forward"):
        """Crée un objet transition

        Args:
            GAME_SCREEN_WIDTH (int): largeur de l'écran
            GAME_SCREEN_HEIGHT (int): hauteur de l'écran
            end (float, optional): durée de la transition. par défaut: 0.5.
            transitionType (str, optional): le type de la transition. par défaut: "fade".
            playType (str, optional): la direction dans laquelle doit jouer l'animation. par défaut: "forward".
        
        Returns:
            Transition: l'objet transition crée
        """
        self.time = 0.0
        self.end = end
        self.playing = False
        self.playType = playType
        self.transitionType = transitionType
        self.reverse = False
        self.gameScreenSize = (GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT)
        self.gameScreenDiag = pygame.Vector2(GAME_SCREEN_WIDTH / 2, GAME_SCREEN_HEIGHT / 2).length() + 10
        self.surface = pygame.Surface(self.gameScreenSize)
        self.surface.fill((0, 0, 0))
    
    def update(self, p_dt):
        if not self.playing: return False
        dt = p_dt if p_dt < 0.2 else 0.2
        if self.reverse:
            self.time -= dt
            if self.time <= 0.0:
                if self.playType == "reverse-ping-pong":
                    self.reverse = False
                    self.time = 0.0
                else:
                    self.stop()
                return True
        else:
            self.time += dt
            if self.time >= self.end:
                if self.playType == "ping-pong":
                    self.reverse = True
                    self.time = self.end
                else:
                    self.stop()
                return True
        return False
    
    def draw(self, screen: pygame.Surface):
        if not self.playing: return
        if self.transitionType == "fade":
            self.surface.set_alpha(pygame.math.lerp(0, 255, self.time / self.end))
            screen.blit(self.surface, (0, 0))
        elif self.transitionType == "circle":
            if not self.reverse:
                radius = pygame.math.lerp(0, self.gameScreenDiag, self.time / self.end) + 10
                pygame.draw.circle(screen, (0, 0, 0), (self.gameScreenSize[0] / 2, self.gameScreenSize[1] / 2), radius)
            else:
                radius = self.gameScreenDiag + 5
                width = int(pygame.math.lerp(0, self.gameScreenDiag, self.time / self.end))
                pygame.draw.circle(screen, (0, 0, 0), (self.gameScreenSize[0] / 2, self.gameScreenSize[1] / 2), radius, width)
    
    def play(self, end=-1, playType=-1):
        self.playing = True
        if playType != -1:
            self.playType = playType
        if end != -1:
            self.end = end
        if "reverse" in self.playType:
            self.time = self.end
            self.reverse = True

    def pause(self):
        self.playing = False

    def stop(self):
        self.playing = False
        self.time = 0.0
        self.reverse = False