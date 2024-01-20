from random import randint as rand

from territory.gang_names import random_gang_names
from objects.player import Player
from objects.weapons import crime_weapons
from objects.warehouse import Warehouse
from objects.car_shop import CarShop
from objects.lawyers import Lawyers
from objects.bank import Bank
from objects.business import BusinessManager
from objects.stats import StatCounter

from territory.city import City

class World:
    def __init__(self):
        self.stats = StatCounter()

        gangs_per_block = 3
        self.gang_names = random_gang_names(gangs_per_block)

        self.weapons = crime_weapons
        self.player = Player(self)
        self.player_gang_name = "Players Gang"
        self.gang_coffer = 0
        self.gang_money_cap = 5000
        crew_count = 10
        self.player.give_random_crew_members(self, crew_count)

        self.lawyers = Lawyers()

        self.warehouse = Warehouse()
        self.car_shop = CarShop()

        self.bank = Bank()
        self.business = BusinessManager()

        self.cities = {} # city_name : City
        self.city_cost = 500000

        city_count = 8
        for _ in range(city_count): self.add_city()

        self.cheated = False
    

    def add_city(self, name=None):
        new_city = City(self)

        if name == None or name in self.cities:
            while new_city.name in self.cities:
                new_city = City(self)
        
        name = (new_city.name if name == None else name)
        new_city.name = name
        self.cities[name] = new_city

    def gang_deficite(self):
        cap = self.gang_money_cap
        deficit = 0

        for city in self.cities.values():
            for block in city.blocks:
                for gang in block.gangs:
                    if not gang.ai and len(gang) > 0:
                        deficit += gang.deficit(cap)
        
        return max(deficit, 0)


    def send_crew(self, amount):
        allocations = [0] * len(self.cities)

        while amount > 0:
            allocations[rand(0, len(self.cities) - 1)] += 1
            amount -= 1
        
        for index, city_name in enumerate(self.cities.keys()):
            self.cities[city_name].send_crew(self, allocations[index])


    def evacuate_crew(self):
        for city in self.cities.values(): city.evacuate_crew(self)


    def crew_population(self):
        return sum([c.crew_population() for c in self.cities.values()])


    def net_worth(self):
        ply = self.player
        net = ply.money + self.gang_coffer - self.gang_deficite()

        for member in ply.crew.values():
            wep_value = (0 if member.weapon == None else member.weapon.price)
            net += wep_value

        for qualities in self.warehouse.items.values():
            for item in qualities.values():
                net += item.get_total_value()
        
        for qualities in self.car_shop.cars.values():
            for car in qualities.values():
                net += car.get_total_value()
        
        net += self.bank.savings - self.bank.loan

        for loc_id, location in self.business.locations.items():
            value = self.business.location_ids[loc_id][1]
            net += (value * location.count)
        
        return net

    def think(self, crime_commited):
        for city in self.cities.values(): city.think(self)
        self.player.think(self, crime_commited)
        self.car_shop.think(self)
        self.bank.think(self)
        self.business.think(self)
        self.lawyers.think(self)
        self.stats.inc_stat("turns_played")
