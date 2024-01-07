from random import sample
from random import randint as rand

from objects.humans import Criminal

class Gang:
    def __init__(self, world, name=""):
        self.name = name
        self.money = rand(100, 1000)
        self.crew = {} # Criminal_id : Criminal
        self.crew_cap = 500
        self.turns_until_backup = rand(5, 20)
        self.ai = True

        if name in world.gang_names:
            for _ in range(rand(4, 8)): self.add_criminal(world)
    
    def __repr__(self): 
        first = ("Gang Name: " + self.name + "\tMembers: " + str(len(self.crew)))
        second = ("Health: " + str(self.gang_health()) + "\tArmor: " + str(self.gang_armor()) + "\tPower Level: " + str(self.gang_power()))
        return (first + '\n' + second)

    def __len__(self): return len(self.crew)
    
    def add_criminal(self, world):
        if len(self.crew) == self.crew_cap: return
        new_criminal = Criminal(world, self.name)
        new_criminal.arm(world)
        self.crew[id(new_criminal)] = new_criminal
    
    def crew_population(self): return 0

    def populate(self, world, amount=1):
        for _ in range(amount): self.add_criminal(world)
    
    def gang_power(self):
        count = len(self.crew)
        if count == 0: return 0

        total = sum([member.power_level() for member in self.crew.values()])
        return (total // count)

    def gang_health(self): return sum([member.health for member in self.crew.values()])

    def gang_armor(self): return sum([member.armor for member in self.crew.values()])
    
    def heal_crew(self, amount=10):
        for member in self.crew.values(): member.heal(amount)

    def remove_dead(self):
        dead_members = []

        for id, member in self.crew.items():
            if member.health <= 0: dead_members.append(id)
        
        for id in dead_members: self.crew.pop(id)

    def loot_attempt(self, target_gang):
        if len(target_gang.crew) == 0:
            self.money += target_gang.money
            target_gang.money = 0

    def fight(self, target_gang):
        s_count = len(self.crew)
        t_count = len(target_gang.crew)
        if t_count == 0: return

        # First two checks skip fights where opp has no chance of winning
        if s_count > (t_count * 10):
            target_gang.crew.clear()
            self.loot_attempt(target_gang)
            return

        if t_count > (s_count * 10):
            self.crew.clear()
            target_gang.loot_attempt(self)
            return

        damage = (self.gang_power() // t_count)

        for member in target_gang.crew.values(): member.damage(damage)
        target_gang.remove_dead()

        s_count = len(self.crew)
        if s_count == 0: return

        damage = (target_gang.gang_power() // s_count)

        for member in self.crew.values(): member.damage(damage)
        self.remove_dead()
    
    def go_shopping(self, world):
        for member in self.crew.values():
            if self.money < 99: break

            if member.armor < 50:
                self.money -= 100
                member.armor = 100

        if self.money < 200: return

        for member in self.crew.values():
            if self.money < 200: break
            power = (0 if member.weapon == None else member.weapon.power)

            wep_options = { # wep_id : (power, cost)
                "rifle" : (30, 600),
                "shotgun" : (40, 400),
                "pistol" : (20, 200),
                "bat" : (10, 20)
            }

            for id, data in wep_options.items():
                if power < data[0]:
                    if self.money >= data[1]:
                        self.money -= data[1]
                        member.weapon = world.weapons.lookup_weapon(id)
                        break
                else: break
    
    def think(self, world):
        self.turns_until_backup -= 1

        if self.turns_until_backup == 0:
            self.turns_until_backup = rand(5, 20)
            self.add_criminal(world)

        self.money += (rand(0, 200) * len(self.crew))
        self.go_shopping(world)


class PlayerGang(Gang):
    def __init__(self, world):
        self.name = world.player_gang_name
        self.money = 0
        self.crew = {} # CrewMember_id : CrewMember
        self.crew_cap = 500
        self.ai = False
    
    def add_crew(self, world, amount=1):
        ply = world.player
        amount = min(len(ply.crew), amount)
        targets = sample(sorted(ply.crew), amount)

        for id in targets:
            if len(self.crew) == self.crew_cap: break
            self.crew[id] = ply.crew.pop(id)
    
    def deficit(self, money_cap):
        total = 0

        for crew in self.crew.values():
            power = (0 if crew.weapon == None else crew.weapon.power)
            
            if power < 30: total += 600
            if crew.armor < 50: total += 100

        return total + (money_cap - self.money)
    
    def populate(self, world, amount=1): self.add_crew(world, amount)
    
    def crew_population(self): return len(self.crew)
    
    def think(self, world):
        if len(self.crew) == 0: return
        self.money += world.gang_coffer
        self.go_shopping(world)

        if self.money > world.gang_money_cap:
            world.gang_coffer = (self.money - world.gang_money_cap)
            self.money = world.gang_money_cap
        else: world.gang_coffer = 0
