dialogues = {
    "blep": {
        "evenements": {
            1: {"type": "quests", "nom": "parlerPotato", "min": 0, "max": 1},
            3: {"type": "quests", "nom": "sauverPoule", "min": 0, "max": -1},
            5: {"type": "quests", "nom": "sauverPoule", "min": 0, "max": -1},
            6: {"type": "quests", "nom": "parlerPotatoEncore", "min": 0, "max": -1},
            7: {"type": "quests", "nom": "parlerPotatoEncore", "min": 0, "max": -1}
        },
        "restrictions": {
            2: {"type": "quests", "nom": "parlerPotato", "min": 2, "max": -1},
            5: {"type": "quests", "nom": "sauverPoule", "min": 5, "max": -1},
            7: {"type": "quests", "nom": "parlerPotatoEncore", "min": 2, "max": -1}
        },
        "texte": [
            ["Bonjour aventurier!"],
            ["Va parler a Potato, il ma chipé mes poules.", "Il est dans la caverne."],
            ["Quoi?! Il a perdu mes poules?!"],
            ["Va sauver mes 4 poules!", "stp"],
            ["Tu peux voir ton inventaire avec TAB"],
            ["T'as sauvé mes poules!!!", "Merci beaucoup!!!"],
            ["Va revoir Potato pour lui dire que tu as retrouvé mes poules."],
            ["Bravo!!! Tu as fini le tutoriel!"],
            ["salut!"]
        ]
    },
    "potato": {
        "evenements": {
            1: {"type": "quests", "nom": "parlerPotato", "min": 1, "max": -1},
            2: {"type": "quests", "nom": "parlerPotatoEncore", "min": 1, "max": -1}
        },
        "restrictions": {
            1: {"type": "quests", "nom": "parlerPotato", "min": 1, "max": 2},
            2: {"type": "quests", "nom": "parlerPotatoEncore", "min": 1, "max": 2},
            3: {"type": "quests", "nom": "parlerPotatoEncore", "min": 3, "max": -1}
        },
        "texte": [
            ["Salut!"],
            ["Blep t'as demandé de venir me parler!?", "Ah, a propos de ses poules.", "En fait, je les ai perdus. Oups!"],
            ["T'as retrouvé les poules, cool!"],
            ["POTATO!!!!"]
        ]
    }
}