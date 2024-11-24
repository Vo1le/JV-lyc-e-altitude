import pygame

class Transition:
    def __init__(self, GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT, end=0.5):
        self.time = 0.0
        self.end = 0.5
        self.surface = pygame.Surface((GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT))
        self.surface.fill((0, 0, 0))
        self.playing = False
        self.playType = "forward"
        self.reverse = False
    
    def update(self, dt):
        if not self.playing: return
        if self.reverse:
            self.time -= dt
            if self.time <= 0.0:
                self.stop()
        else:
            self.time += dt
            if self.time >= self.end:
                if self.playType == "ping-pong":
                    self.reverse = True
                    self.time = self.end
                else:
                    self.stop()
    
    def draw(self, screen: pygame.Surface):
        if not self.playing: return
        self.surface.set_alpha(pygame.math.lerp(0, 255, self.time / self.end))
        screen.blit(self.surface, (0, 0))
    
    def play(self, end=-1, playType="forward"):
        self.playing = True
        self.playType = playType
        if end != -1:
            self.end = end
        if self.playType == "reverse":
            self.time = self.end
            self.reverse = True

    def pause(self):
        self.playing = False

    def stop(self):
        self.playing = False
        self.time = 0.0
        self.reverse = False