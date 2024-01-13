from prettytable import PrettyTable

from random import randint as rand

from events import EventLog
from menu import input_buffer, valid_numeric_input
from objects.warehouse import Item
from resources.loot_tables import generic_roll

'''
Businesses are generic enough that they do not inherit from any Class
Every Business must have the following methods
    think(self, world)          Returns None
    withdraw(self, world, log)  Returns log
'''

class BusRecruitmentOffice:
    def __init__(self):
        self.name = "Recruitment Office"
        self.count = 1
        self.crew_members = 0
        self.crew_cap = 100
        self.crew_rate = (1, 3)
    
    def think(self, _):
        minimum = self.crew_rate[0] * self.count
        maximum = self.crew_rate[1] * self.count
        self.crew_members = min(
            self.crew_members + (rand(minimum, maximum)),
            (self.crew_cap * self.count)
        )

    def withdraw(self, world, log):
        if self.crew_members == 0: return log
        log.log("crew", "Crew members recruited", self.crew_members)
        world.player.give_random_crew_members(world, self.crew_members)
        self.crew_members = 0
        return log

    def holdings(self): return f"Crew: {self.crew_members}"

class BusGrowFarm:
    def __init__(self):
        self.name = "Grow Farm"
        self.count = 1
        self.packs = 0
        self.pack_cap = 200
        self.pack_time = 20
        self.pack_ticker = 0
        self.min_harvest = 5
        self.max_harvest = 20
    
    def think(self, _):
        self.pack_ticker += 1

        if self.pack_ticker == self.pack_time:
            self.pack_ticker = 0
            self.packs = min(
                self.packs + rand(
                    self.min_harvest * self.count,
                    self.max_harvest * self.count
                ),
                self.pack_cap * self.count
            )
    
    def withdraw(self, world, log):
        if self.packs == 0: return log
        log.log("grow", "Smoke Packs harvested", self.packs)

        qualities = {}
        for i in range(1, 7): qualities[i] = 0

        for _ in range(self.packs):
            qualities[generic_roll([800, 400, 50, 20, 5, 1]) + 1] += 1

        for qual, qty in qualities.items():
            world.warehouse.give_item(Item(
                "smoke_pack", "Smoke Pack", "household", 1000, qual, qty
            ))
        
        self.packs = 0
        return log

    def holdings(self): return f"Smoke Packs: {self.packs}"

class BusYayoFactory(BusGrowFarm):
    def __init__(self):
        super().__init__()
        self.name = "Yayo Factory"
        self.count = 1
        self.pack_cap = 50
        self.pack_time = 10
        self.min_harvest = 1
        self.max_harvest = 3
    
    def withdraw(self, world, log):
        if self.packs == 0: return log
        log.log("yayo", "Yayo Packs cooked", self.packs)

        qualities = {}
        for i in range(2, 8): qualities[i] = 0

        for _ in range(self.packs):
            qualities[generic_roll([50, 100, 200, 20, 10, 5]) + 2] += 1

        for qual, qty in qualities.items():
            world.warehouse.give_item(Item(
                "yayo_pack", "Yayo Pack", "household", 4000, qual, qty
            ))
        
        self.packs = 0
        return log

    def holdings(self): return f"Yayo Packs: {self.packs}"



class BusinessManager:
    def __init__(self):
        self.locations = {} # id : Business
        self.location_limit = 0
        self.sell_rate = 0.6
        self.location_ids = { # id : (Business, price)
            "recruitment"   : (BusRecruitmentOffice, 40000),
            "grow_farm"     : (BusGrowFarm, 75000),
            "yayo_factory"  : (BusYayoFactory, 150000)
        }
    
    def count(self): return sum([b.count for b in self.locations.values()])

    def price(self, id):
        if id in self.location_ids:
            return self.location_ids[id][1]
    
    def sell_value(self, id): return int(self.price(id) * self.sell_rate)

    def new(self, id, count=1):
        if id in self.locations: self.locations[id].count += count
        elif id in self.location_ids:
            new = self.location_ids[id][0]()
            new.id = id
            new.count = count
            self.locations[id] = new

    def increase_limit(self): # Should be called every time a Block is added
        self.location_limit += rand(2, 6)
    
    def think(self, world):
        for business in self.locations.values(): business.think(world)
    
    def withdraw(self, world):
        print("Withdrawing from all Businesses\n")
        log = EventLog()

        for business in self.locations.values():
            log = business.withdraw(world, log)
        
        log.print_events()
        input_buffer()
    
    def inspect(self):
        if self.count() == 0:
            print("You don't own any Businesses")
            input_buffer()
            return

        render = PrettyTable()
        render.field_names = ["Business", "Quantity", "Profit Holding"]

        for busy in self.locations.values():
            render.add_row(
                [busy.name, busy.count, busy.holdings()],
                divider=True
            )
        
        print(render)
        input_buffer()
    
    def purchase(self, world):
        if self.count() == self.location_limit:
            print("You've bought all the prime real estate in every City!")
            print("Consider selling some Businesses or purchasing a new City")
            input_buffer()
            return

        render = PrettyTable()
        render.field_names = ["Key", "Business", "Price"]
        render.add_row([0, "Cancel Selection", 0], divider=True)
        key = 1

        for id, data in self.location_ids.items():
            example = data[0]()
            render.add_row(
                [key, example.name, self.price(id)], divider=True
            )
            key += 1
        
        print(render)

        ply = world.player
        print(f"\nMoney: ${ply.money}")

        choice = valid_numeric_input(
            "\nWhich property would you like to purchase",
            0, len(self.location_ids), 0
        )

        if choice == 0: return

        id = list(self.location_ids.keys())[choice - 1]
        price = self.price(id)

        if ply.money >= price:
            budget = (ply.money // price)
            name = self.location_ids[id][0]().name
            space = self.location_limit - self.count()

            amount = valid_numeric_input(
                f"\nHow many {name}s would you like to purchase?",
                0, min(budget, space), 1
            )

            if amount == 0: return

            price *= amount
            ply.money -= price
            self.new(id, amount)

            print(f"You purchased {amount} {name}s for ${price}")
            input_buffer()
        else:
            print("\nYou can't afford to purchase this business")
            input_buffer()
    
    def sell(self, world):
        if self.count() == 0:
            print("You don't own any Businesses to sell!")
            input_buffer()
            return

        render = PrettyTable()
        render.field_names = [
            "Key", "Business", "Value", "Quantity", "Total Value"
        ]

        render.add_row([0, "Cancel", 0, 0, 0], divider=True)
        key = 1

        for id, busy in self.locations.items():
            value = self.sell_value(id)
            render.add_row([
                key, busy.name, value, busy.count, (value * busy.count)
            ], divider=True)
        
        print(render)

        choice = valid_numeric_input(
            "\nWhich Business would you like to sell?",
            0, len(self.locations), 0
        )

        if choice == 0: return

        id = list(self.locations.keys())[choice - 1]
        busy = self.locations[id]

        amount = valid_numeric_input(
            f"\nHow many {busy.name}s would you like to sell?",
            0, busy.count, 0
        )

        if amount == 0: return

        earnings = (self.sell_value(id) * amount)
        world.player.money += earnings

        busy.count -= amount
        if busy.count == 0: self.locations.pop(busy.id)

        print(f"Earned ${earnings} from selling {amount} {busy.name}s")
        input_buffer()
