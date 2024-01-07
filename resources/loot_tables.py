from random import randint as rand

from objects.warehouse import Item

def generic_roll(values):
    roll = rand(1, sum(values))
    sentinal = 0

    for index, pick in enumerate(values):
        sentinal += pick
        if roll <= sentinal: return index
    
    return -1

def roll_car_quality(): return generic_roll([5000, 2500, 1250, 625, 350, 210, 50, 10, 5])

def roll_random_car():
    car_data = { # car_name : base_value
        "Trashed Car"   : 100,
        "Project Car"   : 200,
        "Hooptie"       : 400,
        "Mom Van"       : 500,
        "Economy Car"   : 900,
        "Reliable Car"  : 1000,
        "Motorcylce"    : 1200,
        "Large Van"     : 1500,
        "Sports Car"    : 1600,
        "Electric Car"  : 2000,
        "Vintage Car"   : 5000,
        "Super Car"     : 10000,
        "Futuristic Automobile" : 20000
    }

    car_chances = [30, 60, 90, 150, 350, 1000, 350, 150, 25, 10, 8, 6, 1]

    index = generic_roll(car_chances)

    name = list(car_data.keys())[index]
    id = '_'.join(name.split(' ')).lower()
    value = car_data[name] * 5
    quality = roll_car_quality()

    return Item(id, name, "car", value, quality)

def roll_household_quality():
    return generic_roll([50, 100, 150, 250, 100, 50, 10, 5, 1])

def roll_household_item():
    item_data = {   # item_name : base_value
        "Radio"             : 20,
        "TV"                : 30,
        "Jewelry"           : 80,
        "Designer Clothes"  : 120,
        "Tool Box"          : 140,
        "Collectors Liquor" : 160,
        "Laptop"            : 200,
        "Gaming PC"         : 240,
        "Vase"              : 320,
        "Sound System"      : 400,
        "Smoke Pack"        : 1000,
        "Famous Painting"   : 2000,
        "Yayo Pack"         : 4000,
        "Gold Bars"         : 8000,
        "Precious Diamond"  : 20000
    }

    total = sum(item_data.values())
    item_chances = [int(total * (1/n)) for n in item_data.values()]

    index = generic_roll(item_chances)
    name = list(item_data.keys())[index]
    id = '_'.join(name.split(' ')).lower()
    value = item_data[name]
    quality = roll_household_quality()
    quantity = generic_roll([1000, 200, 20, 1]) + 1

    return Item(id, name, "household", value, quality, quantity)
