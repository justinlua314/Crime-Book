from copy import deepcopy
from os import system
from prettytable import PrettyTable

from menu import input_buffer

item_qualities = {
    0 : "Busted",
    1 : "Very Rough",
    2 : "Worn Out",
    3 : "Decent",
    4 : "Fancy",
    5 : "Luxery",
    6 : "Extremely Rare",
    7 : "Legendary",
    8 : "One of a Kind"
}

class Item:
    def __init__(self, id, name, item_type="Generic", value=0, quality=0, count=1):
        self.id = id
        self.name = name
        self.item_type = item_type
        self.value = value
        self.quality = quality
        self.count = count
    
    def get_value(self):
        val = self.value
        quality = self.quality

        if val < 0: return 0
        return int(val * (max(quality - 2, 1) * 0.25 * (quality + 1)))
    
    def get_total_value(self): return (self.get_value() * self.count)

    def quality_name(self):
        if self.quality in item_qualities: return item_qualities[self.quality]
        elif self.quality < 0: return "Actual Garbage"
        else: return "Heavenly"


class Warehouse:
    def __init__(self):
        self.items = {}     # item_id : {item_quality : Item}
        self.crew = {}
        self.item_qualities = item_qualities
    
    def give_item(self, item):
        if item.id in self.items:
            if item.quality in self.items[item.id]:
                self.items[item.id][item.quality].count += item.count
            else:
                self.items[item.id][item.quality] = deepcopy(item)
        else:
            self.items[item.id] = {item.quality : deepcopy(item)}
    
    def remove_item(self, item_id, quality_id, amount):
        self.items[item_id][quality_id].count -= amount

        if self.items[item_id][quality_id].count <= 0:
            self.items[item_id].pop(quality_id)

            if len(self.items[item_id]) == 0: self.items.pop(item_id)

    def get_value(self):
        total = 0

        for qualities in self.items.values():
            for item in qualities.values(): total += item.get_total_value()
        
        return total

    def sell_items(self, world):
        if len(self.items) == 0:
            print("\n\nYour Warehouse has no items in it")
            input_buffer()
            return
        
        system("cls")
        print("Selling the following items\n")
        self.inspect_inventory(False)

        earnings = self.get_value()
        world.player.money += earnings

        self.items.clear()
        print(f"\nYou earned ${earnings} from that sale")
        print("\nYour Warehouse is now empty")
        input_buffer()
    
    def transfer_items(self, target, item_type=None):
        trash = {} # item_id : [quality]

        for id, qualities in self.items.items():
            for quality, item in qualities.items():
                if item_type == None or item.item_type == item_type:
                    target.give_item(item)

                    if id in trash: trash[id].append(quality)
                    else: trash[id] = [quality]
        
        for id, qualities in trash.items():
            for quality in qualities: self.items[id].pop(quality)

    def inspect_inventory(self, buffer=True):
        if len(self.items) == 0:
            print("\n\nYour Warehouse has no items in it")
            input_buffer()
            return

        if buffer: system("cls")

        qualities_owned = []

        for _,item in self.items.items():
            for quality in item:
                if not quality in qualities_owned: qualities_owned.append(quality)
        
        qualities_owned.sort()
        render = PrettyTable()
        headers = ["Item Name"] + [self.item_qualities[n] for n in qualities_owned] + ["Total Quantity", "Total Value"]
        render.field_names = headers
        totals = [0] * len(qualities_owned)
        grand_total = 0
        grand_value = 0

        for item_qualities in self.items.values():
            total = 0
            value = 0
            item = item_qualities[list(item_qualities.keys())[0]]
            row = [item.name]

            for index, quality in enumerate(qualities_owned):
                if quality in item_qualities:
                    item = item_qualities[quality]

                    row.append(item.count)
                    total += item.count
                    totals[index] += item.count
                    value += item.get_total_value()
                else: row.append('')
            
            
            row += [total, '$' + str(value)]
            grand_total += total
            grand_value += value
        
            render.add_row(row, divider=True)

        row = ["Totals"] + totals + [grand_total, '$' + str(grand_value)]
        render.add_row(row, divider=True)

        print(render)
        if buffer: input_buffer()