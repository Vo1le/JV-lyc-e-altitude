import pygame as py
from inputs import verifierInput, verifierInputList
import math
from maps.attributs import GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT, WIDTH_FACE, HEIGHT_FACE
from Evenements import Evenements
from items import items

RACINEDE2 = math.sqrt(2)


class Joueur(py.sprite.Sprite):
    def __init__(self, x, y, p_items, collectedItems, events=False):
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

        self.talking = False
        self.talkingTo = None
        self.talkingTextIndex = 0.0
        self.talkingSpeed = 7.0
        self.talkRange = 200.0
        self.talkingProgression = 0
        self.talkingFont = py.font.Font(size=32)
        self.talkPossible = False

        self.evenements = events or Evenements()

        self.items = p_items
        self.collectedItems = collectedItems
        self.inMenu = False
        self.menuTabs = {"inventaire": self.drawInventaire} #{"equipment", "inventaire": self.drawInventaire, "stats", "settings", "sauvegardes"}
        self.menuTabsList = ["inventaire"]
        self.menuTab = 0
        self.inventorySurface = py.Surface((GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT), py.SRCALPHA)
        self.inventorySurface.fill((0, 0, 0))
        self.inventorySurface.set_alpha(100)

    def update(self, dt, keys_pressed_once, mapjeu, zoom: float):
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

        self.updateTalk(dt, keys_pressed_once, mapjeu)

        if verifierInputList(keys_pressed_once, "inventaire"):
            self.inMenu = not self.inMenu

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
            item = py.sprite.spritecollideany(self, mapjeu.items)
            if item:
                self.getItem(item, mapjeu)
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
    
    def updateTalk(self, dt, keys_pressed_once, mapjeu):
        if verifierInputList(keys_pressed_once, "interagir"):
            if not self.talking:
                self.talkingTo = py.sprite.spritecollideany(self, mapjeu.objetsDialogue, py.sprite.collide_circle)
                if not self.talkingTo is None:
                    self.talking = True
                    if not self.talkingTo.dialogueKey in self.evenements.dialoguesProgression:
                        self.evenements.dialoguesProgression[self.talkingTo.dialogueKey] = {"index": 0, "skipLastLine": False}
                    if self.evenements.dialoguesProgression[self.talkingTo.dialogueKey]["skipLastLine"] and "restrictions" in self.talkingTo.dialogue and self.evenements.dialoguesProgression[self.talkingTo.dialogueKey]["index"] + 1 in self.talkingTo.dialogue["restrictions"]:
                        attrNames = self.talkingTo.dialogue["restrictions"][self.evenements.dialoguesProgression[self.talkingTo.dialogueKey]["index"] + 1]
                        attr = getattr(self.evenements, attrNames["type"])[attrNames["nom"]]
                        if attrNames["max"] == -1:
                            if attrNames["min"] <= attr["progress"]:
                                self.evenements.dialoguesProgression[self.talkingTo.dialogueKey]["index"] += 1
                                self.evenements.dialoguesProgression[self.talkingTo.dialogueKey]["skipLastLine"] = False
                        else:
                            if attrNames["min"] <= attr["progress"] < attrNames["max"]:
                                self.evenements.dialoguesProgression[self.talkingTo.dialogueKey]["index"] += 1
                                self.evenements.dialoguesProgression[self.talkingTo.dialogueKey]["skipLastLine"] = False
            
            else:
                if self.talkingTextIndex > len(self.talkingTo.dialogue["texte"][self.evenements.dialoguesProgression[self.talkingTo.dialogueKey]["index"]][self.talkingProgression]):
                    self.talkingProgression += 1
                    self.talkingTextIndex = 0.0
                    if self.talkingProgression >= len(self.talkingTo.dialogue["texte"][self.evenements.dialoguesProgression[self.talkingTo.dialogueKey]["index"]]):
                        self.talkingProgression = 0
                        self.talking = False

                        if "evenements" in self.talkingTo.dialogue and self.evenements.dialoguesProgression[self.talkingTo.dialogueKey]["index"] in self.talkingTo.dialogue["evenements"]:
                            attrNames = self.talkingTo.dialogue["evenements"][self.evenements.dialoguesProgression[self.talkingTo.dialogueKey]["index"]]
                            attr = getattr(self.evenements, attrNames["type"])[attrNames["nom"]]
                            if not ("completed" in attrNames and attrNames["completed"]):
                                if attrNames["max"] == -1:
                                    if attrNames["min"] <= attr["progress"]:
                                        self.evenements.progressQuest(attrNames["type"], attrNames["nom"], mapjeu, self)
                                        attrNames["completed"] = True
                                else:
                                    if attrNames["min"] <= attr["progress"] < attrNames["max"]:
                                        self.evenements.progressQuest(attrNames["type"], attrNames["nom"], mapjeu, self)
                                        attrNames["completed"] = True
                        
                        #print(self.evenements.dialoguesProgression[self.talkingTo.dialogueKey]["index"], self.evenements.quests["parlerPotato"]["progress"])
                        if "restrictions" in self.talkingTo.dialogue and self.evenements.dialoguesProgression[self.talkingTo.dialogueKey]["index"] + 1 in self.talkingTo.dialogue["restrictions"]:
                            attrNames = self.talkingTo.dialogue["restrictions"][self.evenements.dialoguesProgression[self.talkingTo.dialogueKey]["index"] + 1]
                            attr = getattr(self.evenements, attrNames["type"])[attrNames["nom"]]
                            if attrNames["min"] <= attr["progress"]:
                                if attrNames["max"] != -1:
                                    if attr["progress"] < attrNames["max"]:
                                        self.evenements.dialoguesProgression[self.talkingTo.dialogueKey]["index"] += 1
                                else:
                                    self.evenements.dialoguesProgression[self.talkingTo.dialogueKey]["index"] += 1
                            else:
                                self.evenements.dialoguesProgression[self.talkingTo.dialogueKey]["skipLastLine"] = True
                        else:
                            self.evenements.dialoguesProgression[self.talkingTo.dialogueKey]["index"] += 1
                        if self.evenements.dialoguesProgression[self.talkingTo.dialogueKey]["index"] >= len(self.talkingTo.dialogue["texte"]):
                            self.evenements.dialoguesProgression[self.talkingTo.dialogueKey]["index"] = len(self.talkingTo.dialogue["texte"]) - 1
                else:
                    self.talkingTextIndex = len(self.talkingTo.dialogue["texte"][self.evenements.dialoguesProgression[self.talkingTo.dialogueKey]["index"]][self.talkingProgression])
        
        if self.talking:
            self.talkingTextIndex += dt * self.talkingSpeed
            if py.Vector2(self.rect.center).distance_to(py.Vector2(self.talkingTo.rect.center)) > self.talkRange:
                self.talking = False
                self.talkingTextIndex = 0.0
                self.talkingProgression = 0
        
        self.talkPossible = not self.talking and not py.sprite.spritecollideany(self, mapjeu.objetsDialogue, py.sprite.collide_circle) is None
    
    def getItem(self, item, mapjeu):
        if item.name in self.evenements.questItems:
            quest = self.evenements.questItems[item.name]
            self.evenements.progressQuest("quests", quest, mapjeu, self)
        if item.name in self.items:
            self.items[item.name].append(item)
            self.collectedItems[item.name].append(item)
        else:
            self.items[item.name] = [item]
            self.collectedItems[item.name] = [item]
        mapjeu.removeTile(item.layerIdx, item.rect.topleft)
        mapjeu.items.remove(item)
    
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
    
    def drawHUD(self, surface: py.Surface):
        if self.talking:
            py.draw.rect(surface, (100, 100, 100), (WIDTH_FACE, GAME_SCREEN_HEIGHT - HEIGHT_FACE - 50.0, GAME_SCREEN_WIDTH / 2, HEIGHT_FACE + 40.0))
            surface.blit(self.talkingTo.face, (0, GAME_SCREEN_HEIGHT - HEIGHT_FACE - 25.0))
            textImg = self.talkingFont.render(self.talkingTo.dialogue["texte"][self.evenements.dialoguesProgression[self.talkingTo.dialogueKey]["index"]][self.talkingProgression][:math.floor(self.talkingTextIndex)], True, (0, 0, 0))
            surface.blit(textImg, (WIDTH_FACE + 25, GAME_SCREEN_HEIGHT - HEIGHT_FACE))
            nameImg = self.talkingFont.render(self.talkingTo.name, True, (0, 255, 255))
            surface.blit(nameImg, (WIDTH_FACE + 5, GAME_SCREEN_HEIGHT - HEIGHT_FACE - 45.0))
        
        if self.talkPossible:
            textImg = self.talkingFont.render("Pour parler: Entrer", True, (255, 0, 100))
            surface.blit(textImg, (GAME_SCREEN_WIDTH - 300, 100))

        if self.inMenu:
            surface.blit(self.inventorySurface, (0, 0))
            self.menuTabs[self.menuTabsList[self.menuTab]](surface)
    
    def drawInventaire(self, surface: py.Surface):
        i = 0
        for item in self.items:
            textImg = self.talkingFont.render(item + ": " + str(len(self.items[item])), True, (255, 100, 100))
            surface.blit(textImg, (25, (i + 1) * 32))
            i += 1

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