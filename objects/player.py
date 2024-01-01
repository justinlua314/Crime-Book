from copy import deepcopy
from random import sample

from random import randint as rand

from menu import input_buffer
from objects.humans import CrewMember

class Player:
    def __init__(self, world):
        self.crew = {}
        self.weapons = {} # weapon_id : count
        self.money = 100
        self.vests = 0
        self.heat = 0
        self.heat_cap = 500
        self.heat_timer = 0
        self.heat_momentum = 0

    def give_crew_member(self, member): self.crew[id(member)] = member

    def give_random_crew_members(self, world, amount=1):
        for _ in range(amount):
            self.give_crew_member(CrewMember(world))
    
    def give_weapon(self, weapon_id="pistol", amount=1):
        if weapon_id in self.weapons.keys():
            self.weapons[weapon_id] += amount
        else:
            self.weapons[weapon_id] = amount
    
    def take_weapon(self, weapon_id="pistol", amount=1):
        self.weapons[weapon_id] = max(self.weapons[weapon_id] - amount, 0)

        if self.weapons[weapon_id] == 0: self.weapons.pop(weapon_id)

    def loot(self, target):
        self.money += target.money
        if target.weapon != None: self.give_weapon(target.weapon.id)
        if target.armor == 100: self.vests += 1 # Might never happen

    def replace_vests(self, min_quality=0):
        for member in self.crew.values():
            if self.vests == 0: return

            if member.armor <= min_quality:
                self.vests -= 1
                member.armor = 100

    def distribute_vests(self):
        if self.vests == 0:
            print("No armor to distribute!")
            return

        # Replace vests of all crew members starting with the worst ones
        self.replace_vests()
        self.replace_vests(50)
        self.replace_vests(70)
        self.replace_vests(99)
    
    def replace_weapon(self, member, weapon):
        if weapon.id not in self.weapons.keys(): return

        if member.weapon != None: self.give_weapon(member.weapon.id)
        member.weapon = weapon
        self.take_weapon(weapon.id)
    
    def distribute_arms(self, world):
        for _ in range(4): # Done a few times to ensure replaced weapons get checked.
            if len(self.weapons) == 0: break

            weapons = deepcopy(self.weapons)

            for id in weapons:
                weapon = world.weapons.lookup_weapon(id)
                if weapon == None: continue

                for _,member in self.crew.items():
                    if member.weapon == None or member.weapon.power < weapon.power:
                        self.replace_weapon(member, weapon)
    
    def busted(self, world):
        self.heat = 0
        self.heat_timer = 0
        self.heat_momentum = 0
        items_siezed = {}  # item_name : quantity

        wh = world.warehouse
        cooldown = 2

        targets = {} # item_id : [(quality, amount)]

        for id, qualities in wh.items.items():
            for quality, item in qualities.items():
                if rand(1, cooldown) == 1:
                    siezed = rand(1, item.count)

                    if id in targets: targets[id].append((quality, siezed))
                    else: targets[id] = [(quality, siezed)]
                    
                    if item.name in items_siezed: items_siezed[item.name] += siezed
                    else: items_siezed[item.name] = siezed

                    cooldown += 1
                else:
                    cooldown = max(cooldown - 1, 2)
        
        for id, data in targets.items():
            for target in data: wh.remove_item(id, target[0], target[1])

        self.vests //= rand(2, 8)
        for weapon_id in self.weapons: self.weapons[weapon_id] //= rand(2, 8)

        limit = self.money // 8
        money_siezed = rand(limit, max(self.money - (len(self.crew) * 100), limit))

        ply = world.player
        lower = len(ply.crew) // 16
        upper = len(ply.crew) // 4
        crew_siezed = sample(list(ply.crew.keys()), rand(lower, upper))

        for id in crew_siezed: ply.crew.pop(id)

        print("You got busted by the police!\n")
        print("Money Siezed: $", money_siezed, sep='')
        print("Crew Siezed:", len(crew_siezed))

        if len(items_siezed) > 0: print("\nItems Siezed")

        for name, quantity in items_siezed.items():
            print(name, quantity, sep=": ")

        print("\nMake some government trades to keep the cops off your case")

        input_buffer()
        

    def think(self, world, crime_commited):
        if crime_commited:
            self.heat_timer = 0
            self.heat_momentum = 0
        else:
            self.heat = max(self.heat - self.heat_momentum, 0)
            self.heat_timer += 1

            if self.heat_timer == 3:
                self.heat_timer = 0
                self.heat_momentum = min(self.heat_momentum + 1, 5)
            
            if self.heat_momentum == 5:
                self.heat_cap = max(self.heat_cap - 1, 500)
        
        if self.heat >= self.heat_cap: self.busted(world)
