dialogues = {
    "personne1": {
        "skipLastLine": False,
        "evenements": {
            0: {"type": "quests", "nom": "parlerPotato", "min": 0, "max": 1},
            3: {"type": "quests", "nom": "sauverPoule", "min": 0, "max": -1},
            6: {"type": "quests", "nom": "parlerPotatoEncore", "min": 0, "max": -1}
        },
        "restrictions": {
            2: {"type": "quests", "nom": "parlerPotato", "min": 2, "max": -1},
            5: {"type": "quests", "nom": "sauverPoule", "min": 3, "max": -1},
            8: {"type": "quests", "nom": "parlerPotatoEncore", "min": 2, "max": -1}
        },
        "texte": [
            ["bla, bla, bla.", "va parler a potato"],
            ["patati patata"],
            ["t'as parlé a potato? Cool!"],
            ["Va sauver mes poules!", "stp"],
            ["T'as sauvé mes poules?"],
            ["T'as sauvé mes poules!!!", "Merci beaucoup!!!"],
            ["va parler a potato (encore)"],
            ["plouk"],
            ["Bravo!!!"],
            ["salut!"]
        ]
    },
    "personne2": {
        "skipLastLine": False,
        "evenements": {
            2: {"type": "quests", "nom": "parlerPotato", "min": 1, "max": -1},
            4: {"type": "quests", "nom": "parlerPotatoEncore", "min": 1, "max": -1}
        },
        "restrictions": {
            2: {"type": "quests", "nom": "parlerPotato", "min": 1, "max": 2},
            4: {"type": "quests", "nom": "parlerPotatoEncore", "min": 1, "max": 2}
        },
        "texte": [
            ["And then Hefest got this run..."],
            ["...", "..........", "..... pyramids"],
            ["Blep t'as demandé de venir me parler!?", "Vas voir Blep."],
            ["POTATO!!!!!"],
            ["Blep t'as demandé de venir me parler encore!?", "Vas voir Blep encore."],
            ["PLUS DE POTATO"]
        ]
    }
}