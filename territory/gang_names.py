from random import sample

gang_names = [
    "Vipers",
    "Mafia",
    "Dons",
    "Cartel",
    "Assassins",
    "Snakes",
    "Cobras",
    "Hunters",
    "Hitsquad",
    "Dealers",
    "Unholy",
    "Menaces",
    "Nerds",
    "Bangers",
    "Reapers"
]

def random_gang_names(amount=1):
    return [("The " + x) for x in sample(gang_names, amount)]
