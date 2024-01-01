from statistics import mean

from random import randint as rand

from territory.gang import Gang, PlayerGang

class Block:
    def __init__(self, world):
        self.gangs = []

        for name in world.gang_names:
            new_gang = Gang(world, name)
            new_gang.populate(world, rand(5, 20))
            self.gangs.append(new_gang)
        
        self.gangs.append(PlayerGang(world))
    
    def add_crew_members(self, world, crew):
        ply = world.player

        for gang in self.gangs:
            if not gang.ai:
                for id in crew: gang.crew[id] = ply.crew.pop(id)
                break
    
    def evacuate_crew(self, world):
        ply = world.player

        for gang in self.gangs:
            if not gang.ai:
                targets = list(gang.crew.keys())
                for id in targets: ply.crew[id] = gang.crew.pop(id)
                break
    
    def crew_population(self):
        for gang in self.gangs:
            if not gang.ai: return gang.crew_population()
    
    def controlling_gang(self):
        top = [self.gangs[0], self.gangs[0].gang_power()]

        for gang in self.gangs:
            power = gang.gang_power()

            if power > top[1]:
                top[0] = gang
                top[1] = power
        
        return top[0]

    def gang_economy(self): return sum([g.money for g in self.gangs])
    def average_crew_size(self): return int(mean([len(g.crew) for g in self.gangs]))

    def gang_war(self):
        for index, first in enumerate(self.gangs[:-1]):
            for second in self.gangs[index+1:]:
                first.fight(second)
    
    def think(self, world):
        for index, attacker in enumerate(self.gangs):
            for target in self.gangs[index:]:
                attacker.fight(target)
        
        top_gang = self.controlling_gang()
        top_gang.heal_crew(10)
        top_gang.money += 25

        for gang in self.gangs:
            if gang != top_gang: gang.heal_crew(25)
            gang.think(world)
