from prettytable import PrettyTable
from os import system
from random import sample

from menu import Menu, Option, input_buffer, valid_numeric_input, coming_soon

def inspect_gear(world):
    ply = world.player

    print("Money: $" + str(ply.money))

    render = PrettyTable()
    render.field_names = ["Resource", "Quantity Available"]
    render.add_row(["Vests", ply.vests], divider=True)

    for id,count in ply.weapons.items():
        weapon_name = world.weapons.lookup_weapon(id).name
        render.add_row([weapon_name, count], divider=True)
    
    print(render)
    input_buffer()

def distribute_armor(world):
    world.player.distribute_vests()
    print("\nArmor Distributed")
    input_buffer()

def distribute_weapons(world):
    world.player.distribute_arms(world)
    print("\nWeapons Distributed")
    input_buffer()

def print_warehouse_crew(world):
    ply = world.player
    wh = world.warehouse

    render = PrettyTable()
    render.field_names = ["Location", "Count"]
    render.add_row(["Active Crew", len(ply.crew)], divider=True)
    render.add_row(["Crew in Warehouse", len(wh.crew)], divider=True)
    print(render, '\n')

'''
def deposit_crew(world):
    ply = world.player
    crew_size = len(ply.crew)

    if crew_size < 2:
        print("\nYou don't have enough crew members to be making deposits!")
        input_buffer(); return

    print_warehouse_crew(world)
    print("How many crew members are we depositing?")
    count = valid_numeric_input("Deposit", 0, crew_size - 1, (crew_size // 2))
    crew = sample(sorted(ply.crew), count)

    for id in crew: world.warehouse.crew[id] = ply.crew.pop(id)

    print("\nDeposited", count, "crew members")
    input_buffer()

def withdraw_crew(world):
    ply = world.player
    wh = world.warehouse
    crew_size = len(wh.crew)

    if crew_size == 0:
        print("\nYou don't have any crew members to withdraw!")
        input_buffer(); return

    print_warehouse_crew(world)
    print("How many crew members are we withdrawing?")
    count = valid_numeric_input("Withdraw", 0, crew_size, (crew_size // 2))
    crew = sample(sorted(wh.crew), count)

    for id in crew: ply.crew[id] = wh.crew.pop(id)

    print("\nWithdrew", count, "crew members")
    input_buffer()

menu_backup = Menu(
    "Backup Crew", "Where are we putting these guys", [
        Option("Deposit Crew Members", '', 'd', deposit_crew),
        Option("Withdraw Crew Members", '', 'w', withdraw_crew)
    ]
)
'''

def inspect_warehouse(world): world.warehouse.inspect_inventory()
def sell_warehouse_items(world): world.warehouse.sell_items(world)

def car_money(world):
    print("Car Shop\n")
    shop = world.car_shop
    print("Cars in car shop: ", shop.car_count(), sep='')
    payment = shop.money

    if payment == 0:
        if len(shop.cars) == 0:
            print("We don't have any cars! Go jack some for us if you want money")
        else:
            print("We haven't sold anything yet! Come back later")
    else:
        shop.money = 0
        world.player.money += payment
        print('$', payment, " paid out by the Car Shop", sep='')

    input_buffer()


menu_warehouse = Menu(
    "Criminal Warehouse", "What would you like to see boss", [
        Option("Inspect Gear", '', 'g', inspect_gear),
        Option("Inspect Warehouse Inventory", '', 'i', inspect_warehouse),
        Option("Sell Warehouse Items", '', 's', sell_warehouse_items),
        Option("Collect Money from Car Shop", '', 'c', car_money),
        Option("Distribute Armor", '', 'a', distribute_armor),
        Option("Distribute Weapons", '', 'w', distribute_weapons),
#        Option("Manage Backup Crew", "menu_backup", 'c')
    ]
)
