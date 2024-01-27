class Achievement:
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description
        self.achieved = False

    # Overwrite returning achieved
    def check(self, world): return False



class AchievementManager:
    def __init__(self):
        self.achievements = {}
    
    def register(self, achievement):
        self.achievements[achievement.id] = achievement



cg_achievements = AchievementManager()


def check(world): return world.player.money >= 1000000000

achievement = Achievement("bezos", "Bezos", "Have a net worth of one billion dollars")
achievement.check = check
cg_achievements.register(achievement)


def check(world):
    ply = world.player

    if len(ply.crew) < 1000: return False

    check = True

    for member in ply.crew.values():
        if member.armor < 100 or member.weapon.id != "rifle":
            check = False
            break
    
    return check

achievement = Achievement("locked", "Locked and Loaded", "Have at least 1,000 Crew Members, all equipped with Rifles and Armor")
achievement.check = check
cg_achievements.register(achievement)
