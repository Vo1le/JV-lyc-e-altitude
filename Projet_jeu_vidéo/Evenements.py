class Evenements:
    def __init__(self) -> None:
        self.quests = {
            "parlerPotato": {"progress": 0, "end": 2},
            "sauverPoule": {"progress": 0, "end": 3},
            "parlerPotatoEncore": {"progress": 0, "end": 2}
        }
        self.questItems = {
            "poule": "sauverPoule"
        }

        self.dialoguesProgression = {}
        