from copy import deepcopy

class Weapon:
    def __init__(self, id="", name="", ranged=False, power=0, dur=1, price=0):
        self.id = id
        self.name = name
        self.ranged = ranged
        self.power = power
        self.durability = dur
        self.price = price
    
    def use(self, user):
        self.durability -= 1
        if self.durability == 0: user.weapon = None



class WeaponDatabase:
    def __init__(self):
        self.weapons = {} # weapon_name : weapon
    
    def register_weapon(self, weapon):
        self.weapons[weapon.id] = weapon
    
    def lookup_weapon(self, id):
        try: return self.weapons[id]
        except: return None
    
    def give(self, human, weapon_id):
        human.weapon = deepcopy(self.weapons[weapon_id])



crime_weapons = WeaponDatabase()
crime_weapons.register_weapon(Weapon(
    "bat", "Baseball Bat", False, 10, 50, 20
))

crime_weapons.register_weapon(Weapon(
    "baton", "Police Baton", False, 10, 100
))

crime_weapons.register_weapon(Weapon(
    "pistol", "Pistol", True, 20, 48, 200
))

crime_weapons.register_weapon(Weapon(
    "shotgun", "Shotgun", True, 40, 24, 400
))

crime_weapons.register_weapon(Weapon(
    "rifle", "Rifle", True, 30, 120, 600
))
