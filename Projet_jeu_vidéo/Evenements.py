class Evenements:
    def __init__(self) -> None:
        self.quests = {
            "parlerPotato": {"progress": 0, "end": 2},
            "sauverPoule": {"progress": 0, "end": 6, "endFunc": self.sauverPouleEnd},
            "parlerPotatoEncore": {"progress": 0, "end": 3}
        }
        self.questItems = {
            "poule": "sauverPoule"
        }

        self.dialoguesProgression = {}
    
    def sauverPouleEnd(self, mapjeu, joueur):
        mapjeu.addItem(2, (200, 100), "coin", "Coin2.png::0::0;0", animated="Coin2.png::0::0;0")
        joueur.items["poule"] = joueur.items["poule"][4:]

    def progressQuest(self, p_type, name, mapjeu, joueur):
        attr = getattr(self, p_type)
        if attr[name]["progress"] < attr[name]["end"]:
            attr[name]["progress"] += 1
            if attr[name]["progress"] == attr[name]["end"] and "endFunc" in attr[name]:
                attr[name]["endFunc"](mapjeu, joueur)