dialogues = {
    "personne1": {
        "index": 0,
        "skipLastLine": False,
        "evenements": {0: {"type": "quests", "nom": "parlerPotato", "min": 0, "max": 1}},
        "restrictions": {2: {"type": "quests", "nom": "parlerPotato", "min": 2, "max": -1}},
        "texte": [
        ["bla, bla, bla.", "va parler a potato"],
        ["patati patata"],
        ["t'as parlé a potato? Cool!"],
        ["salut!"]
        ]
    },
    "personne2": {
        "index": 0,
        "skipLastLine": False,
        "evenements": {2: {"type": "quests", "nom": "parlerPotato", "min": 1, "max": -1}},
        "restrictions": {2: {"type": "quests", "nom": "parlerPotato", "min": 1, "max": 2}},
        "texte": [
        ["And then Hefest got this run..."],
        ["...", "..........", "..... pyramids"],
        ["Blep t'as demandé de venir me parler!?", "Vas voir Blep."],
        ["POTATO!!!!!"]
        ]
    }
}