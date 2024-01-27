from math import floor
from copy import deepcopy

from functools import lru_cache

from random import randint as rand

level_costs = []

for level in range(11):
    x = (0 if level < 1 else level_costs[level - 1])
    y = (0 if level < 2 else level_costs[level - 2])
    level_costs.append(8 + (8 * floor((x - y) / 2)))

class Human:
    def __init__(self, world):
        self.type = "Human"
        self.health = 100
        self.armor = 0

        self.stats = {  # stat_name : [level, exp, level_up_cost]
            "accuracy"  : [0, 0, 1],
            "dodging"   : [0, 0, 1],
            "shooting"  : [0, 0, 1],
            "strength"  : [0, 0, 1]
        }

        self.money = 0
        self.weapon = None
    
    def alive(self): return self.health > 0

    def get_recruited(self, world):
        clone = CrewMember(world)
        clone.health = self.health
        clone.armor = self.armor
        clone.money = self.money
        clone.weapon = deepcopy(self.weapon)

        for stat, data in self.stats.items(): clone.stats[stat] = data

        return clone

    def level_up_cost(self, n): return level_costs[max(min(n, 10), 0)]

    def weapon_skill_name(self):
        if self.weapon == None or self.weapon.ranged == False:
            return "strength"
        else: return "shooting"

    def weapon_skill(self): return self.stats[self.weapon_skill_name()]
    
    def inc_stat(self, stat="accuracy"):
        level = self.stats[stat]

        if level[0] < 10:
            level[1] += 1

            if level[1] == level[2]:  # Level up
                level[0] += 1
                level[1] = 0
                level[2] = self.level_up_cost(level[0])
        else: level[1] = min(level[1] + 1, level[2] - 1)
    
    def set_stat(self, stat="accuracy", level=0):
        self.stats[stat][0] = level
        self.stats[stat][1] = 0
        self.stats[stat][2] = self.level_up_cost(level)

    # Returns True if hit
    def hit_roll(self, target):
        x = self.weapon_skill()[0] + 1
        y = target.weapon_skill()[0] + 1

        return rand(1, (x + y)) <= x

    @lru_cache(maxsize=None)
    def power_level(self):
        power = (0 if self.weapon == None else self.weapon.power)
        skill = self.weapon_skill()[0]
        amplitude = 2 # All damage is multiplied by this number
        damage = (max(floor(power * (skill * 0.5)), 1) * amplitude)

        return damage

    def damage(self, amount=0):
        if self.armor >= amount: self.armor -= amount
        else:
            amount -= self.armor
            self.armor = 0
            self.health -= amount
    
    def heal(self, amount=0): self.health = min(self.health + amount, 100)

    def fortify(self, amount=0):
        if amount >= (100 - self.armor):
            amount -= (100 - self.armor)
            self.armor = 100
            self.health += amount

    def give_weapon(self, id, world):
        self.weapon = world.weapons.lookup_weapon(id)

    def use_weapon(self):
        if self.weapon != None: self.weapon.use(self)



class Ped(Human):
    def __init__(self, world, armed=False):
        super().__init__(world)
        self.type = "Pedestrian"
        self.set_stat("accuracy", 0)
        self.set_stat("dodging", rand(0, 2))
        self.set_stat("strength", rand(0, 1))
        self.set_stat("shooting", rand(0, 1))

        if rand(1, 50) == 10: self.money = rand(100, 1000)
        else: self.money = rand(5, 50)

        if armed: self.arm(world)
    
    def arm(self, world):
        pickup = rand(1, 200)

        if pickup > 195: self.give_weapon("pistol", world)
        elif pickup > 190: self.give_weapon("bat", world)



class Cop(Human):
    def __init__(self, world):
        super().__init__(world)
        self.type = "Cop"
        self.set_stat("accuracy", rand(1, 3))
        self.set_stat("dodging", rand(2, 6))
        self.set_stat("strength", rand(1, 4))
        self.set_stat("shooting", rand(2, 5))
        self.money = rand(20, 80)
        self.arm(world)
    
    def arm(self, world):
        pickup = rand(1, 10)

        if pickup > 8: self.give_weapon("shotgun", world)
        elif pickup > 4: self.give_weapon("pistol", world)
        else: self.give_weapon("baton", world)



class Criminal(Human):
    def __init__(self, world, gang):
        super().__init__(world)
        self.type = "Criminal"
        self.gang = gang

        self.set_stat("accuracy", rand(2, 6))
        self.set_stat("dodging", rand(2, 6))
        self.set_stat("strength", rand(2, 6))
        self.set_stat("shooting", rand(2, 6))
    
    def arm(self, world):
        pickup = rand(1, 100)

        if pickup == 1: self.give_weapon("shotgun", world)
        elif pickup < 11: self.give_weapon("pistol", world)
        elif pickup < 51: self.give_weapon("bat", world)



class CrewMember(Human):
    def __init__(self, world):
        super().__init__(world)
        self.type = "Crew Member"

        self.set_stat("accuracy", rand(2, 6))
        self.set_stat("dodging", rand(2, 6))
        self.set_stat("strength", rand(2, 6))
        self.set_stat("shooting", rand(2, 6))
    
    # If player Bool is False, dead crew members won't be deleted automatically
    # Hack to make heists possible
    def fight(self, target, world, log, player=True):
        s_power = self.power_level()
        s_wepskill = self.weapon_skill_name()
        t_power = target.power_level()
        t_wepskill = target.weapon_skill_name()

        while self.alive() and target.alive():
            self.use_weapon()

            if self.hit_roll(target):
                target.damage(s_power)
                self.inc_stat(s_wepskill)
                self.inc_stat("accuracy")
            else: target.inc_stat("dodging")

            if target.health < 1: break
            target.use_weapon()

            # Start skipping turns when they are low hp to balance fighting peds
            if target.health < 20 and target.type == "Pedestrian" and rand(1, 4) == 2:
                continue

            if target.hit_roll(self):
                self.damage(t_power)
                target.inc_stat(t_wepskill)
                target.inc_stat("accuracy")
            else: self.inc_stat("dodging")

        ply = world.player

        if self.alive():
            log.log("money_looted", "Money Looted", target.money)
            ply.money += target.money

            kill_id = (target.type.lower() + "_killed")
            kill_desc = (target.type + "s Killed")
            log.log(kill_id, kill_desc)

            if target.type == "Cop": ply.heat += (2 * rand(0, 1))
            else: ply.heat += (1 if rand(1, 10) == 1 else 0)

            if target.weapon != None:
                s_wep = self.weapon
                s_pow = (0 if s_wep == None else self.weapon.power)
                s_dur = (0 if s_wep == None else self.weapon.durability)
                t_pow = target.weapon.power
                t_dur = target.weapon.durability

                if s_pow < t_pow or (s_pow == t_pow and s_dur < t_dur):
                    self.weapon = deepcopy(target.weapon)
                    loot_id = (self.weapon.id + "_looted")
                    loot_desc = (self.weapon.name + "s picked up by Crew Members")
                    log.log(loot_id, loot_desc)
        elif target.alive():
            kill_id = ("crew_killed_by_" + target.type.lower())
            kill_desc = ("Crew killed by " + target.type)
            log.log(kill_id, kill_desc)
            world.stats.inc_stat("crew_died")
            if player and id(self) in ply.crew: ply.crew.pop(id(self))

    def recruit(self, target, world, log):
        ply = world.player

        if target.type == "Cop":
            log.log("crew_recruited_cop", "Crew members attempted to recruit police")
            self.fight(target, world, log)
        else:
            if rand(1, 15) == 10:
                log.log("crew_fought_ped", "Pedestrians started fight")
                self.fight(target, world, log)
            
            if rand(1, 5) == 5:
                log.log("ped_recruited", "Pedestrians recruited")
                ply.give_crew_member(target.get_recruited(world), world)
    
    def intimidate(self, target, world, log):
        ply = world.player

        if target.type == "Cop":
            if rand(1, 10) > 3: self.fight(target, world, log)
        else:
            t_power = target.power_level()
            s_power = self.power_level()

            if t_power > (s_power * 2):
                log.log("ped_recruited", "Pedestrians recruited")
                ply.give_crew_member(target.get_recruited(world), world)
            elif t_power > s_power:
                log.log("ped_recruited", "Pedestrians recruited")
                ply.give_crew_member(target.get_recruited(world), world)
            else:
                if rand(1, 10) == 8:
                    log.log("ped_recruited", "Pedestrians recruited")
                    ply.give_crew_member(target.get_recruited(world), world)
                elif rand(1, 10) == 5: self.fight(target, world, log)
    
    def bribe(self, target, budget, world, log):
        ply = world.player

        if target.type == "Cop":
            if budget > 100 and rand(1, 100) <= (budget // 100):
                log.log("cop_recruited", "Cops recruited")
                ply.give_crew_member(target.get_recruited(world), world)
                return 0
            else:
                self.fight(target, world, log)

                if self.health == 0: return 0
                else: return budget
        else:
            if rand(1, budget) > (target.money * 2):
                log.log("ped_recruited", "Pedestrians recruited")
                ply.give_crew_member(target.get_recruited(world), world)
                return 0
            else:
                if target.power_level() > self.power_level() and rand(1, 200) == 50:
                    self.fight(target, world, log)

                    if self.health == 0: return 0
                
                return budget         
