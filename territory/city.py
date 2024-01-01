from faker import Faker
from random import sample

from random import randint as rand

from territory.block import Block

fake = Faker()

def generate_city_name():
    name = ' '
    while ' ' in name: name = fake.city()

    return name

class City:
    def __init__(self, world):
        self.name = generate_city_name()
        self.blocks = []
        for _ in range(rand(6, 16)): self.blocks.append(Block(world))
    
    def gang_economy(self): return sum([b.gang_economy() for b in self.blocks])

    def send_crew(self, world, amount):
        allocations = [0] * len(self.blocks)

        while amount > 0:
            allocations[rand(0, len(self.blocks) - 1)] += 1
            amount -= 1
        
        for index, amount in enumerate(allocations):
            conscripts = sample(sorted(world.player.crew), amount)
            self.blocks[index].add_crew_members(world, conscripts)
    
    def evacuate_crew(self, world):
        for block in self.blocks: block.evacuate_crew(world)

    def crew_population(self):
        return sum([b.crew_population() for b in self.blocks])
    
    def top_gang(self):
        gangs = {}

        for block in self.blocks:
            gang = block.controlling_gang().name

            if gang in gangs: gangs[gang] += 1
            else: gangs[gang] = 1
        
        return max(gangs, key=gangs.get)
        

    def think(self, world):
        for block in self.blocks: block.think(world)
