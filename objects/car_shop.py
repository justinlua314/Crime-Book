from copy import deepcopy

from random import randint as rand

from objects.warehouse import Warehouse
from objects.warehouse import item_qualities as car_qualities

class CarShop(Warehouse):
    def __init__(self):
        self.cars = {} # item_id : {item_quality : Item}
        self.economy = 0
        self.money = 0
    
    def car_count(self):
        total = 0

        for qualities in self.cars.values():
            total += sum([car.count for car in qualities.values()])
        
        return total

    def give_car(self, car):
        if car.id in self.cars:
            if car.quality in self.cars[car.id]:
                self.cars[car.id][car.quality].count += car.count
            else:
                self.cars[car.id][car.quality] = deepcopy(car)
        else:
            self.cars[car.id] = {car.quality : deepcopy(car)}
    
    def remove_car(self, item_id, quality_id, amount):
        self.cars[item_id][quality_id].count -= amount

        if self.cars[item_id][quality_id].count <= 0:
            self.cars[item_id].pop(quality_id)

            if len(self.cars[item_id]) == 0: self.cars.pop(item_id)
    
    def remove_item(self, item_id, quality_id, amount):
        self.remove_car(item_id, quality_id, amount)

    def sell_items(self, world):
        cars_to_sell = rand(0, 4)
        limit = 20

        while cars_to_sell > 0 and self.economy > 0:
            dead_market = True
            trash = {} # item_id : [quality]

            for index, qualities in self.cars.items():
                for quality, car in qualities.items():
                    if car.value <= self.economy:
                        dead_market = False
                        
                        if (rand(1, 10)) == 5:
                            cost = car.get_value()

                            self.economy -= cost
                            self.money += cost
                            cars_to_sell -= 1
                            car.count -= 1
                            world.stats.inc_stat("cars_sold")

                            if car.count == 0:
                                if index in trash: trash[index].append(quality)
                                else: trash[index] = [quality]

            for id, qualities in trash.items():
                for quality in qualities: self.cars[id].pop(quality)

            limit -= 1
            if dead_market or limit == 0: break

    def think(self, world):
        self.economy += rand(100, 2000)
        if rand(1, 3) != 3: self.sell_items(world)
